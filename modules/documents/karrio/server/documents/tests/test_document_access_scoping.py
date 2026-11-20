import io
import json
import base64
from unittest import mock

from django.contrib.auth import get_user_model
from rest_framework import status
from PyPDF2 import PdfReader, PdfWriter

import karrio.server.manager.models as manager_models
import karrio.server.documents.generator as generator
from karrio.server.user.models import Token
from karrio.server.orders.models import Order
from karrio.server.core.middleware import CreatorAccess
from karrio.server.core.tests import APITestCase
from karrio.server.core.utils import ResourceAccessToken
from karrio.server.documents.models import DocumentTemplate


def _pdf_b64(width: int = 200) -> str:
    writer = PdfWriter()
    writer.add_blank_page(width=width, height=100)
    buffer = io.BytesIO()
    writer.write(buffer)
    return base64.b64encode(buffer.getvalue()).decode("ascii")


PDF_B64 = _pdf_b64()
MANIFEST_ADDRESS = {"postal_code": "10115", "city": "Berlin", "country_code": "DE", "address_line1": "Sample Str. 1"}
SHIPMENT_TEMPLATE = "{% for s in shipments %}{{ s.shipment.tracking_number }};{% endfor %}"


class DocumentAccessScopingTestCase(APITestCase):
    """Document downloads serve only the caller's rows.

    `validate_resource_token` lets every signed-in caller through, so each download
    view scopes its own lookup. The test default access filter (`WideAccess`) filters
    nothing, so a per-owner filter is patched in: the boundary a multi-tenant build has.
    Batch tests print one of the caller's documents and one of another tenant's; the
    page count of the bundle shows which were served.
    """

    def setUp(self) -> None:
        super().setUp()
        self.rendered = []
        self.victim = get_user_model().objects.create_user("victim@example.com", "test")
        self.intruder = get_user_model().objects.create_user("intruder@example.com", "test")

        patches = [
            mock.patch("karrio.server.core.models.base.get_access_filter", CreatorAccess()),
            mock.patch("karrio.server.documents.generator.Documents.generate", side_effect=self._capture),
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)

    def _capture(self, template, data=None, related_object=None, **kwargs):
        # Records what a template render would read, without rendering a PDF.
        self.rendered.append(
            [
                ctx["shipment"]["tracking_number"]
                for ctx in generator.get_shipments_context(data.get("shipments", ""), kwargs.get("context"))
            ]
            if related_object == "shipment" and "shipments" in (data or {})
            else []
        )
        return io.BytesIO(base64.b64decode(PDF_B64))

    def _as(self, user) -> None:
        token = Token.objects.create(user=user, test_mode=True)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    @staticmethod
    def _shipment(user, tracking_number: str) -> manager_models.Shipment:
        return manager_models.Shipment.objects.create(
            created_by=user,
            test_mode=True,
            tracking_number=tracking_number,
            # Distinct bytes per shipment: the order printer de-duplicates documents.
            label=_pdf_b64(200 + len(tracking_number)),
            invoice=_pdf_b64(300 + len(tracking_number)),
            label_type="PDF",
        )

    def _order(self, user) -> Order:
        order = Order.objects.create(order_id=f"ORD-{user.pk}", test_mode=True, created_by=user)
        order.shipments.set([self._shipment(user, f"TRK-ORD-{user.email}")])
        return order

    @staticmethod
    def _manifest(user) -> manager_models.Manifest:
        return manager_models.Manifest.objects.create(
            created_by=user, test_mode=True, address=MANIFEST_ADDRESS, manifest=PDF_B64
        )

    @staticmethod
    def _template(user, slug: str) -> DocumentTemplate:
        return DocumentTemplate.objects.create(
            name=slug, slug=slug, template=SHIPMENT_TEMPLATE, related_object="shipment", created_by=user
        )

    @staticmethod
    def _pages(response) -> int:
        body = b"".join(response.streaming_content) if hasattr(response, "streaming_content") else response.content
        return len(PdfReader(io.BytesIO(body)).pages)


class TestBatchPrinterScoping(DocumentAccessScopingTestCase):
    def _batch(self, path: str, param: str, own, foreign):
        self._as(self.intruder)
        intruder = self.client.get(path, {param: f"{own.id},{foreign.id}"})
        self._as(self.victim)
        owner = self.client.get(path, {param: foreign.id})
        return (intruder.status_code, self._pages(intruder), owner.status_code, self._pages(owner))

    def test_shipment_labels_of_another_tenant_are_not_served(self):
        result = self._batch(
            "/documents/shipments/label.pdf",
            "shipments",
            self._shipment(self.intruder, "TRK-OWN"),
            self._shipment(self.victim, "TRK-VICTIM"),
        )
        self.assertEqual(result, (status.HTTP_200_OK, 1, status.HTTP_200_OK, 1))

    def test_shipment_invoices_of_another_tenant_are_not_served(self):
        result = self._batch(
            "/documents/shipments/invoice.pdf",
            "shipments",
            self._shipment(self.intruder, "TRK-OWN"),
            self._shipment(self.victim, "TRK-VICTIM"),
        )
        self.assertEqual(result, (status.HTTP_200_OK, 1, status.HTTP_200_OK, 1))

    def test_order_labels_of_another_tenant_are_not_served(self):
        result = self._batch(
            "/documents/orders/label.pdf", "orders", self._order(self.intruder), self._order(self.victim)
        )
        self.assertEqual(result, (status.HTTP_200_OK, 1, status.HTTP_200_OK, 1))

    def test_order_invoices_of_another_tenant_are_not_served(self):
        result = self._batch(
            "/documents/orders/invoice.pdf", "orders", self._order(self.intruder), self._order(self.victim)
        )
        self.assertEqual(result, (status.HTTP_200_OK, 1, status.HTTP_200_OK, 1))

    def test_manifests_of_another_tenant_are_not_served(self):
        result = self._batch(
            "/documents/manifests/manifest.pdf",
            "manifests",
            self._manifest(self.intruder),
            self._manifest(self.victim),
        )
        self.assertEqual(result, (status.HTTP_200_OK, 1, status.HTTP_200_OK, 1))

    def test_a_share_link_still_prints_what_it_was_minted_for(self):
        foreign = self._shipment(self.victim, "TRK-VICTIM")
        token = ResourceAccessToken.for_resource(
            user=self.victim, resource_type="document", resource_ids=[foreign.id], access=["batch_labels"]
        )

        self.client.credentials()
        response = self.client.get("/documents/shipments/label.pdf", {"shipments": foreign.id, "token": str(token)})

        self.assertEqual((response.status_code, self._pages(response)), (status.HTTP_200_OK, 1))


class TestSingleDocumentScoping(DocumentAccessScopingTestCase):
    def _single(self, path: str):
        self._as(self.intruder)
        intruder = self.client.get(path)
        self._as(self.victim)
        owner = self.client.get(path)
        return (intruder.status_code, owner.status_code)

    def test_a_shipment_label_of_another_tenant_is_not_served(self):
        shipment = self._shipment(self.victim, "TRK-VICTIM")
        result = self._single(f"/v1/shipments/{shipment.id}/label.pdf")
        self.assertEqual(result, (status.HTTP_404_NOT_FOUND, status.HTTP_200_OK))

    def test_a_shipment_invoice_of_another_tenant_is_not_served(self):
        shipment = self._shipment(self.victim, "TRK-VICTIM")
        result = self._single(f"/v1/shipments/{shipment.id}/invoice.pdf")
        self.assertEqual(result, (status.HTTP_404_NOT_FOUND, status.HTTP_200_OK))

    def test_a_manifest_of_another_tenant_is_not_served(self):
        manifest = self._manifest(self.victim)
        result = self._single(f"/v1/manifests/{manifest.id}/manifest.pdf")
        self.assertEqual(result, (status.HTTP_404_NOT_FOUND, status.HTTP_200_OK))


class TestTemplateScoping(DocumentAccessScopingTestCase):
    def test_another_tenants_template_is_not_printed(self):
        template = self._template(self.victim, "victim_tpl")
        path = f"/documents/templates/{template.id}.{template.slug}"

        self._as(self.intruder)
        intruder = self.client.get(path)
        self._as(self.victim)
        owner = self.client.get(path)

        self.assertEqual((intruder.status_code, owner.status_code), (status.HTTP_404_NOT_FOUND, status.HTTP_200_OK))

    def test_an_own_template_does_not_render_another_tenants_shipment(self):
        own = self._shipment(self.intruder, "TRK-OWN")
        foreign = self._shipment(self.victim, "TRK-VICTIM")
        template = self._template(self.intruder, "own_tpl")

        self._as(self.intruder)
        response = self.client.get(
            f"/documents/templates/{template.id}.{template.slug}", {"shipments": f"{own.id},{foreign.id}"}
        )

        self.assertEqual((response.status_code, self.rendered), (status.HTTP_200_OK, [["TRK-OWN"]]))

    def test_a_token_link_renders_only_what_its_minter_can_see(self):
        own = self._shipment(self.intruder, "TRK-OWN")
        foreign = self._shipment(self.victim, "TRK-VICTIM")
        template = self._template(self.intruder, "own_tpl")
        token = ResourceAccessToken.for_resource(
            user=self.intruder, resource_type="template", resource_ids=[template.id], access=["render"]
        )

        self.client.credentials()
        response = self.client.get(
            f"/documents/templates/{template.id}.{template.slug}",
            {"shipments": f"{own.id},{foreign.id}", "token": str(token)},
        )

        self.assertEqual((response.status_code, self.rendered), (status.HTTP_200_OK, [["TRK-OWN"]]))

    def test_generate_refuses_another_tenants_template(self):
        template = self._template(self.victim, "victim_tpl")
        payload = json.dumps({"template_id": template.id, "data": {}})

        self._as(self.intruder)
        intruder = self.client.post("/v1/documents/generate", payload, content_type="application/json")
        self._as(self.victim)
        owner = self.client.post("/v1/documents/generate", payload, content_type="application/json")

        self.assertEqual((intruder.status_code, owner.status_code), (status.HTTP_404_NOT_FOUND, status.HTTP_201_CREATED))

    def test_generate_does_not_render_another_tenants_shipment(self):
        own = self._shipment(self.intruder, "TRK-OWN")
        foreign = self._shipment(self.victim, "TRK-VICTIM")
        template = self._template(self.intruder, "own_tpl")

        self._as(self.intruder)
        response = self.client.post(
            "/v1/documents/generate",
            json.dumps({"template_id": template.id, "data": {"shipments": f"{own.id},{foreign.id}"}}),
            content_type="application/json",
        )

        self.assertEqual((response.status_code, self.rendered), (status.HTTP_201_CREATED, [["TRK-OWN"]]))
