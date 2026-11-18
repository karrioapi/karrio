import json
import types
import base64
import io
import html
import tempfile
import threading
import http.server
import urllib.request
import weasyprint.urls
from unittest.mock import patch
from django.test import override_settings
import unittest
import jinja2.exceptions
from unittest.mock import ANY
from django.urls import reverse
from rest_framework import status
from karrio.server.core.tests import APITestCase
from karrio.server.core.utils import ResourceAccessToken
from karrio.server.documents.models import DocumentTemplate
import karrio.server.manager.models as manager_models
import karrio.server.orders.models as order_models
import karrio.server.documents.utils as documents_utils
import karrio.server.documents.generator as generator
import datetime
from decimal import Decimal
from django.contrib.auth import get_user_model
from karrio.server.serializers.abstract import get_object_context


class TestDocumentGenerator(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.template = DocumentTemplate.objects.create(
            **{
                "name": "Test Generator Template",
                "slug": "test_generator",
                "template": SIMPLE_HTML_TEMPLATE,
                "description": "A test template for generation",
                "related_object": "shipment",
                "metadata": {"doc_type": "invoice"},
                "options": {"page_size": "A4"},
                "created_by": self.user,
            }
        )

    def test_generate_document_with_template_id(self):
        """Test document generation using template_id"""
        url = reverse("karrio.server.documents:document-generator")
        data = {
            "template_id": self.template.id,
            "data": {
                "title": "Test Invoice",
                "shipment": {
                    "tracking_number": "TEST123456",
                    "service": "Standard",
                    "status": "delivered",
                },
            },
            "doc_name": "test_invoice.pdf",
            "doc_format": "PDF",
        }

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("doc_file", response_data)
        self.assertEqual(response_data["doc_name"], "test_invoice.pdf")
        self.assertEqual(response_data["doc_format"], "PDF")

        # Verify the doc_file is a valid base64 string
        try:
            decoded_pdf = base64.b64decode(response_data["doc_file"])
            self.assertGreater(len(decoded_pdf), 0)
            # Basic PDF header check
            self.assertTrue(decoded_pdf.startswith(b"%PDF"))
        except Exception as e:
            self.fail(f"Invalid base64 PDF content: {e}")

    def test_generate_document_with_inline_template(self):
        """Test document generation using inline template"""
        url = reverse("karrio.server.documents:document-generator")
        data = {
            "template": SIMPLE_HTML_TEMPLATE,
            "data": {
                "title": "Inline Template Test",
                "order": {
                    "order_id": "ORD-001",
                    "order_date": "2023-12-01",
                },
            },
            "doc_name": "inline_test.pdf",
        }

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("doc_file", response_data)
        self.assertEqual(response_data["doc_name"], "inline_test.pdf")

        # Verify the doc_file is a valid base64 string and PDF
        try:
            decoded_pdf = base64.b64decode(response_data["doc_file"])
            self.assertGreater(len(decoded_pdf), 0)
            # Basic PDF header check
            self.assertTrue(decoded_pdf.startswith(b"%PDF"))
        except Exception as e:
            self.fail(f"Invalid base64 PDF content: {e}")

    def test_generate_document_missing_template(self):
        """Test error when neither template nor template_id is provided"""
        url = reverse("karrio.server.documents:document-generator")
        data = {
            "data": {"title": "No Template Test"},
            "doc_name": "no_template.pdf",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("template or template_id is required", str(response.content))

    def test_generate_document_with_metadata_and_options(self):
        """Test document generation with metadata and options"""
        url = reverse("karrio.server.documents:document-generator")
        data = {
            "template_id": self.template.id,
            "data": {
                "title": "Metadata Test",
                "shipment": {"tracking_number": "META123"},
            },
            "options": {
                "prefetch": {
                    "current_date": "{{ utils.datetime.now().strftime('%Y-%m-%d') }}",
                    "tracking_url": "https://track.example.com/{{ shipment.tracking_number }}",
                }
            },
        }

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("doc_file", response_data)

        # Verify the doc_file is a valid base64 string and PDF
        try:
            decoded_pdf = base64.b64decode(response_data["doc_file"])
            self.assertGreater(len(decoded_pdf), 0)
            # Basic PDF header check
            self.assertTrue(decoded_pdf.startswith(b"%PDF"))
        except Exception as e:
            self.fail(f"Invalid base64 PDF content: {e}")


class TestDocumentPrinters(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.template = DocumentTemplate.objects.create(
            **{
                "name": "Printer Test Template",
                "slug": "printer_test",
                "template": SIMPLE_HTML_TEMPLATE,
                "description": "A test template for printing",
                "related_object": "shipment",
                "created_by": self.user,
            }
        )

    def test_template_docs_printer(self):
        """Test template document printing endpoint"""
        token = str(
            ResourceAccessToken.for_resource(
                user=self.user,
                resource_type="template",
                resource_ids=[self.template.id],
                access=["render"],
            )
        )
        url = f"/documents/templates/{self.template.id}.{self.template.slug}"
        response = self.client.get(url, {"title": "Printed Document", "token": token})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response["Content-Type"].startswith("application/pdf"))

        # Verify we got a valid PDF - handle streaming content
        if hasattr(response, "streaming_content"):
            content = b"".join(response.streaming_content)
        else:
            content = response.content
        self.assertGreater(len(content), 0)
        self.assertTrue(content.startswith(b"%PDF"))

    def test_template_docs_printer_with_download(self):
        """Test template document printing with download flag"""
        token = str(
            ResourceAccessToken.for_resource(
                user=self.user,
                resource_type="template",
                resource_ids=[self.template.id],
                access=["render"],
            )
        )
        url = f"/documents/templates/{self.template.id}.{self.template.slug}"
        response = self.client.get(
            url, {"download": "true", "title": "Download Test", "token": token}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("attachment", response.get("Content-Disposition", ""))

        # Verify we got a valid PDF - handle streaming content
        if hasattr(response, "streaming_content"):
            content = b"".join(response.streaming_content)
        else:
            content = response.content
        self.assertGreater(len(content), 0)
        self.assertTrue(content.startswith(b"%PDF"))


class TestDocumentGeneratorIntegration(APITestCase):
    """Integration tests for the document generator with real data"""

    def setUp(self) -> None:
        super().setUp()
        self.invoice_template = DocumentTemplate.objects.create(
            **{
                "name": "Invoice Template",
                "slug": "invoice",
                "template": INVOICE_HTML_TEMPLATE,
                "description": "Invoice template for testing",
                "related_object": "shipment",
                "metadata": {"doc_type": "commercial_invoice"},
                "created_by": self.user,
            }
        )

    def test_shipment_context_generation(self):
        """Test document generation with shipment context"""
        # Create address instances
        recipient = manager_models.Address.objects.create(
            person_name="John Doe",
            address_line1="123 Main St",
            city="Test City",
            country_code="CA",
            postal_code="12345",
            created_by=self.user,
        )

        # Create recipient and shipper as dict data for JSON fields
        recipient_data = {
            "id": "adr_recipient123",
            "person_name": "Test Customer",
            "address_line1": "123 Test Street",
            "city": "Test City",
            "country_code": "US",
            "postal_code": "12345",
        }

        shipper_data = {
            "id": "adr_shipper456",
            "person_name": "Shipper Inc",
            "address_line1": "456 Business Ave",
            "city": "Ship City",
            "country_code": "CA",
            "postal_code": "67890",
        }

        # Create parcel as dict data for JSON field
        parcel_data = {
            "id": "pcl_parcel789",
            "weight": 2.5,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "width": 20,
            "height": 15,
            "length": 30,
        }

        # Create a test shipment with JSON field data
        shipment = manager_models.Shipment.objects.create(
            recipient=recipient_data,
            shipper=shipper_data,
            parcels=[parcel_data],
            test_mode=True,
            status="shipped",
            tracking_number="TRACK123456",
            selected_rate={
                "service": "express",
                "carrier_id": "test_carrier",
                "carrier_name": "Test Carrier",
                "currency": "USD",
                "total_charge": 10.00,
                "test_mode": True,
            },
            created_by=self.user,
        )

        url = reverse("karrio.server.documents:document-generator")
        data = {
            "template_id": self.invoice_template.id,
            "data": {"shipments": str(shipment.id)},
            "doc_name": "shipment_invoice.pdf",
        }

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("doc_file", response_data)
        self.assertEqual(response_data["doc_name"], "shipment_invoice.pdf")

        # Verify the doc_file is a valid base64 string and PDF
        try:
            decoded_pdf = base64.b64decode(response_data["doc_file"])
            self.assertGreater(len(decoded_pdf), 0)
            # Basic PDF header check
            self.assertTrue(decoded_pdf.startswith(b"%PDF"))
        except Exception as e:
            self.fail(f"Invalid base64 PDF content: {e}")


class TestTemplateContextsArePlainData(APITestCase):
    """A template author must reach plain values only. The contexts used to be
    DRF ReturnDicts, which carry ``.serializer.instance`` (the live model), and
    ``lib.failsafe`` called whatever it was handed outside the sandbox, so a
    template could read and delete rows of any tenant through the ORM."""

    def setUp(self) -> None:
        super().setUp()
        self.shipment = self._shipment(self.user, "TRACK-OWN")
        self.other_user = get_user_model().objects.create_user(
            "other@example.com", "other-password"
        )
        self.other_shipment = self._shipment(self.other_user, "TRACK-OTHER")
        # The author's own request context (ignored where the generator does not scope).
        self.context = get_object_context(self.shipment)
        self.order = order_models.Order.objects.create(
            order_id="ORD-1",
            shipping_to=SHIPMENT_ADDRESS,
            line_items=[documents_utils.ORDER_SAMPLE["order"]["line_items"][0]],
            test_mode=True,
            created_by=self.user,
        )

    def _shipment(self, user, tracking_number):
        return manager_models.Shipment.objects.create(
            recipient=SHIPMENT_ADDRESS,
            shipper=SHIPMENT_ADDRESS,
            parcels=[dict(id="pcl_1", weight=1.0, weight_unit="KG")],
            test_mode=True,
            status="purchased",
            tracking_number=tracking_number,
            created_by=user,
        )

    def _render(self, body: str) -> str:
        """Render `body` through the generator's render step, against the context
        it builds for a shipment (serializer output)."""
        import karrio.server.manager.serializers as manager_serializers

        context = dict(shipment=manager_serializers.Shipment(self.shipment).data)
        try:
            return generator._render(
                generator.SANDBOXED_ENV.from_string(body),
                generator._render_data(context, {}, generator._shared_render_data()),
            )
        except jinja2.exceptions.TemplateError as error:
            return f"refused: {type(error).__name__}"

    def _generate(self, body: str):
        try:
            generator.Documents.generate(
                body,
                data=dict(shipments=self.shipment.id),
                related_object="shipment",
                context=self.context,
            )
        except generator.TemplateRenderingError:
            pass

    def test_the_probes_render_against_the_shipment(self):
        """Guards the delete probes below against passing vacuously."""
        from unittest.mock import patch

        with patch.object(generator, "_render", wraps=generator._render) as render:
            self._generate("{{ shipment.tracking_number }}")

        self.assertEqual(render.call_args.args[1]["shipment"]["tracking_number"], "TRACK-OWN")

    def test_failsafe_cannot_delete_the_shipment(self):
        self._generate("{{ lib.failsafe(shipment.serializer.instance.delete) }}")

        self.assertTrue(manager_models.Shipment.objects.filter(id=self.shipment.id).exists())

    def test_failsafe_cannot_delete_another_tenants_shipments(self):
        self._generate(
            "{{ lib.failsafe(shipment.serializer.instance.created_by"
            ".shipment_set.model.objects.all().delete) }}"
        )

        self.assertTrue(
            manager_models.Shipment.objects.filter(id=self.other_shipment.id).exists()
        )

    def test_template_cannot_count_or_read_other_rows(self):
        probes = {
            "cross-tenant count": "{{ shipment.serializer.instance.created_by"
            ".shipment_set.model.objects.count() }}",
            "password hash": "{{ shipment.serializer.instance.created_by.password|length }}",
            "serializer": "{{ shipment.serializer is defined }}",
        }
        rendered = {label: self._render(body) for label, body in probes.items()}

        self.assertTrue(rendered["cross-tenant count"].startswith("refused"), rendered)
        self.assertTrue(rendered["password hash"].startswith("refused"), rendered)
        self.assertEqual(rendered["serializer"], "False")

    def test_failsafe_returns_plain_values_and_never_calls_a_python_callable(self):
        self.assertEqual(self._render("{{ lib.failsafe(shipment.tracking_number) }}"), "TRACK-OWN")
        self.assertEqual(
            self._render("{% macro m() %}from macro{% endmacro %}{{ lib.failsafe(m) }}"),
            "from macro",
        )
        self.assertNotIn("{", self._render("{{ lib.failsafe(lib.to_dict) }}"))

    def test_a_template_cannot_change_what_the_next_document_sees(self):
        """One process renders every tenant's templates; changes a template makes
        to the shared data stay in its own document."""
        import copy

        saved = copy.deepcopy((documents_utils.ORDER_SAMPLE, generator.UNITS))
        self.addCleanup(lambda: documents_utils.ORDER_SAMPLE.update(saved[0]))
        self.addCleanup(lambda: generator.UNITS.update(saved[1]))
        self._render(
            "{{ utils.ORDER_SAMPLE.update({'order': None}) }}"
            "{{ units.CountryISO.clear() }}{{ units.update({'PAGE_SEPARATOR': 'x'}) }}"
        )

        self.assertEqual(
            self._render("{{ utils.ORDER_SAMPLE.order is none }}|{{ units.CountryISO|length > 0 }}"),
            "False|True",
        )
        self.assertEqual((documents_utils.ORDER_SAMPLE, generator.UNITS), saved)

    def test_template_local_lists_and_dicts_can_be_changed(self):
        body = (
            "{% set l = [3, 1] %}{% set _ = l.append(2) %}{% set _ = l.sort() %}"
            "{% set d = {} %}{% set _ = d.update({'a': 1}) %}{% set _ = d.setdefault('b', 2) %}"
            "{% set _ = l.pop() %}{{ l }}|{{ d['a'] + d['b'] }}"
        )

        self.assertEqual(self._render(body), "[1, 2]|3")

    def test_plain_data_keeps_numbers_dates_and_keys(self):
        import enum
        from django.utils.safestring import mark_safe

        class Level(enum.IntEnum):
            HIGH = 2

        data = generator.to_plain(
            dict(
                amount=Decimal("1.50"),
                when=datetime.datetime(2026, 11, 16, 7, 0),
                day=datetime.date(2026, 11, 16),
                pair=(1, 2),
                tags={"x"},
                safe=mark_safe("<b>x</b>"),
                level=Level.HIGH,
                by_code={1: "one"},
            )
        )
        rendered = generator.SANDBOXED_ENV.from_string(
            "{{ data.amount * 2 }}|{{ data.when.year }}|{{ data.day.isoformat() }}|"
            "{{ data.pair[1] }}|{{ data.by_code[1] }}|{{ data.level + 1 }}"
        ).render(data=data)

        self.assertEqual(rendered, "3.00|2026|2026-11-16|2|one|3")
        self.assertIs(type(data["safe"]), str)
        self.assertEqual((data["pair"], data["tags"]), ([1, 2], ["x"]))

    def test_failsafe_accepts_the_callable_keyword(self):
        self.assertEqual(
            self._render("{% macro m() %}ok{% endmacro %}{{ lib.failsafe(callable=m) }}"),
            "ok",
        )

    def test_every_render_path_hands_jinja_plain_data_only(self):
        """Structural: whatever reaches Jinja is plain data on every path that
        builds a context, so a future context cannot bring an object back."""
        from unittest.mock import patch

        self.order.shipments.add(self.shipment)
        DocumentTemplate.objects.create(
            name="Invoice", slug="plain_invoice", template="x",
            related_object="shipment", created_by=self.user,
        )
        prefetch = {"prefetch": {"tn": "{{ shipment.tracking_number if shipment is defined else '' }}"}}
        paths = {
            "shipment ids": lambda: generator.Documents.generate(
                "x",
                data=dict(shipments=self.shipment.id),
                related_object="shipment",
                options=prefetch,
                context=self.context,
            ),
            "order ids": lambda: generator.Documents.generate(
                "x",
                data=dict(orders=self.order.id),
                related_object="order",
                options=prefetch,
                context=self.context,
            ),
            "samples": lambda: generator.Documents.generate(
                "x", data=dict(shipments="sample", orders="sample"), related_object="shipment"
            ),
            "invoice at purchase": lambda: generator.Documents.generate_shipment_document(
                "plain_invoice", self.shipment
            ),
            "generic data with non-JSON values": lambda: generator.Documents.generate(
                "x",
                data=dict(when=datetime.datetime(2026, 11, 16, 7, 0), amount=Decimal("1.50")),
                metadata=dict(doc_type="x", at=datetime.date(2026, 11, 16)),
                options=prefetch,
            ),
        }
        calls = []
        real_render = jinja2.environment.Template.render

        def spy(template, *args, **kwargs):
            calls.append(kwargs)
            return real_render(template, *args, **kwargs)

        offenders = []
        for label, drive in paths.items():
            calls.clear()
            with patch.object(jinja2.environment.Template, "render", spy):
                drive()
            self.assertTrue(calls, label)
            for kwargs in calls:
                data = {k: v for k, v in kwargs.items() if k not in ("lib", "utils")}
                offenders += [f"{label}: {p}" for p in _non_plain(data)]

        self.assertEqual(offenders, [])

    def test_fixture_templates_render_identically_from_plain_contexts(self):
        """Plain contexts change nothing a real template can see."""
        import jinja2.sandbox
        import karrio.server.manager.serializers as manager_serializers

        context = dict(shipment=manager_serializers.Shipment(self.shipment).data)
        metadata = dict(doc_type="commercial_invoice")
        # The helpers as they were before: the real lib.to_dict / lib.to_json.
        import karrio.lib as lib

        legacy_lib = generator._TemplateNamespace(
            "lib",
            **{**generator.TEMPLATE_LIB._members, "to_dict": lib.to_dict, "to_json": lib.to_json},
        )
        globals_ = dict(
            lib=legacy_lib,
            utils=generator.TEMPLATE_UTILS,
            units=generator.UNITS,
            metadata=metadata,
        )
        templates = dict(
            invoice=INVOICE_HTML_TEMPLATE,
            simple=SIMPLE_HTML_TEMPLATE,
            helpers=HELPERS_TEMPLATE,
        )

        for name, body in templates.items():
            body = body.replace("utils.datetime.now().strftime('%Y-%m-%d %H:%M:%S')", "'now'")
            with self.subTest(name):
                legacy = jinja2.sandbox.SandboxedEnvironment().from_string(body)
                rendered = generator._render(
                    generator.SANDBOXED_ENV.from_string(body),
                    generator._render_data(context, metadata, generator._shared_render_data()),
                )
                # Autoescape writes the JSON helpers' quotes as entities; the
                # document text is the same.
                self.assertEqual(
                    html.unescape(rendered) if name == "helpers" else rendered,
                    legacy.render(**{**context, **globals_}),
                )

    def test_data_is_printed_as_text_not_markup(self):
        context = dict(shipment=dict(recipient=dict(company_name='A & B <b>x</b> "q"')))
        rendered = generator._render(
            generator.SANDBOXED_ENV.from_string(
                "<p>{{ shipment.recipient.company_name }}</p>{{ units.PAGE_SEPARATOR }}"
            ),
            generator._render_data(context, {}, generator._shared_render_data()),
        )

        self.assertEqual(
            rendered,
            "<p>A &amp; B &lt;b&gt;x&lt;/b&gt; &#34;q&#34;</p>" + generator.PAGE_SEPARATOR,
        )

    def test_a_prefetch_snippet_keeps_its_markup_and_escapes_its_data(self):
        from unittest.mock import patch

        rendered = []
        with patch.object(generator, "render_pdf", side_effect=lambda c: rendered.append(c) or io.BytesIO()):
            generator.Documents.generate(
                "<div>{{ prefetch.name }}</div>",
                data=dict(name="<i>&</i>"),
                options=dict(prefetch=dict(name="<b>{{ data.name }}</b>")),
            )

        self.assertEqual(rendered, ["<div><b>&lt;i&gt;&amp;&lt;/i&gt;</b></div>"])



class TestDocumentAssetsAreNotFetchedFromAnywhere(APITestCase):
    """Rendered documents go to WeasyPrint, whose default fetcher reads file://
    paths into the PDF and requests any http(s) URL from the server. The HTML
    comes from user templates and user data, so it chooses those URLs."""

    def setUp(self) -> None:
        super().setUp()
        secret = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False)
        secret.write("CANARY-not-for-documents")
        secret.close()
        self.secret_url = f"file://{secret.name}"
        self.hits = []
        hits = self.hits

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                hits.append(self.path)
                self.send_response(200)
                self.send_header("Content-Type", "text/css")
                self.end_headers()
                self.wfile.write(b"p { color: red }")

            def log_message(self, *args):
                pass

        self.server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.shutdown)
        self.loopback = f"http://127.0.0.1:{self.server.server_port}"

    def _pdf(self, template: str, **kwargs) -> bytes:
        return generator.Documents.generate(template, **kwargs).getvalue()

    def test_a_template_cannot_attach_a_server_file(self):
        pdf = self._pdf(f'<link rel="attachment" href="{self.secret_url}"><p>x</p>')

        self.assertFalse(_pdf_contains(pdf, b"CANARY-not-for-documents"))

    def test_shipment_data_cannot_attach_a_server_file(self):
        """No template access needed: the tag sits in an address field and an
        ordinary invoice template prints it."""
        shipment = manager_models.Shipment.objects.create(
            recipient=dict(
                SHIPMENT_ADDRESS,
                address_line1=f'<link rel="attachment" href="{self.secret_url}">',
            ),
            shipper=SHIPMENT_ADDRESS,
            parcels=[dict(id="pcl_1", weight=1.0, weight_unit="KG")],
            test_mode=True,
            created_by=self.user,
        )
        pdf = self._pdf(
            INVOICE_HTML_TEMPLATE,
            data=dict(shipments=shipment.id),
            related_object="shipment",
            context=get_object_context(shipment),
        )

        self.assertFalse(_pdf_contains(pdf, b"CANARY-not-for-documents"))

    def test_a_template_cannot_make_the_server_request_internal_urls(self):
        self._pdf(
            f'<link rel="stylesheet" href="{self.loopback}/link.css">'
            f'<style>@import url("{self.loopback}/import.css");'
            f' p {{ background: url("{self.loopback}/bg.png") }}</style>'
            f'<img src="{self.loopback}/img.png"><p>x</p>'
        )

        self.assertEqual(self.hits, [])

    def test_a_refused_asset_logs_scheme_and_host_only(self):
        with patch.object(generator.logger, "warning") as warning:
            self._pdf(f'<img src="{self.loopback}/img.png?token=secret"><p>x</p>')

        warning.assert_called_with("Document asset refused", scheme="http", host="127.0.0.1")

    def test_the_fetcher_rules(self):
        fetcher = generator.asset_fetcher()
        refused = [
            self.secret_url,
            f"{self.loopback}/x.css",
            "https://evil.example/x.css",
            "https://cdn.jsdelivr.net/npm/other-package@1.0.0/x.css",
            "https://cdn.jsdelivr.net/gh/someone/repo/x.css",
            "https://cdn.jsdelivr.net.evil.example/x.css",
            "https://user@cdn.jsdelivr.net/x.css",
            "https://cdn.jsdelivr.net:8443/x.css",
            "ftp://cdn.jsdelivr.net/x.css",
        ]
        for url in refused:
            with self.subTest(url), self.assertRaises(ValueError):
                fetcher.fetch(url)

        self.assertEqual(fetcher.fetch("data:text/plain,hello").read(), b"hello")
        self.assertEqual(generator.allowed_asset_origins(), set())
        self.assertFalse(
            any(isinstance(h, urllib.request.HTTPRedirectHandler) for h in fetcher.handlers),
            "redirects must not be followed",
        )

    def test_an_allowed_origin_is_fetched_with_a_size_cap(self):
        def respond(body):
            return lambda self, url, headers=None: weasyprint.urls.URLFetcherResponse(
                url, body, {"Content-Type": "text/css"}
            )

        fetcher = generator.asset_fetcher()
        allowed = generator.REMOTE_STYLESHEET_URL
        with patch.object(weasyprint.urls.URLFetcher, "fetch", respond(b"p{}")):
            self.assertEqual(fetcher.fetch(allowed).read(), b"p{}")
        with patch.object(
            weasyprint.urls.URLFetcher, "fetch", respond(b"x" * (generator.ASSET_MAX_BYTES + 1))
        ), self.assertRaises(ValueError):
            fetcher.fetch(allowed)

    @override_settings(DOCUMENT_ASSET_ALLOWED_ORIGINS=["https://assets.example.com"])
    def test_the_operator_can_allow_another_origin(self):
        self.assertIn("https://assets.example.com", generator.allowed_asset_origins())


def _pdf_contains(pdf: bytes, needle: bytes) -> bool:
    """Look inside every (decompressed) stream of the PDF."""
    import PyPDF2

    reader = PyPDF2.PdfReader(io.BytesIO(pdf))
    for numbers in reader.xref.values():
        for number in numbers:
            obj = reader.get_object(PyPDF2.generic.IndirectObject(number, 0, reader))
            if hasattr(obj, "get_data") and needle in obj.get_data():
                return True
    return False

PLAIN_TYPES = (
    str, int, float, bool, type(None), Decimal, datetime.datetime, datetime.date, datetime.time
)

# Formatting a stored template typically does with the helpers and filters.
HELPERS_TEMPLATE = (
    "{{ lib.to_money(shipment.parcels[0].weight) }}|"
    "{{ lib.format_decimal(shipment.parcels[0].weight, 3) }}|"
    "{{ '%.2f'|format(shipment.parcels[0].weight) }}|"
    "{{ lib.fdate(shipment.created_at[:10], '%Y-%m-%d') }}|"
    "{{ lib.to_date(shipment.created_at[:10]).year }}|"
    "{{ lib.text(shipment.recipient.person_name, shipment.recipient.city) }}|"
    "{{ lib.to_country_name(shipment.recipient.country_code) }}|"
    "{{ lib.to_json(shipment.recipient) }}|"
    "{{ lib.to_dict(shipment.recipient) }}|"
    "{{ shipment.tracking_number|upper }}|{{ shipment.parcels|length }}|"
    "{{ shipment.meta|default({}) }}|{{ shipment.missing|default('n/a') }}"
)


def _non_plain(value, path="$"):
    if isinstance(value, PLAIN_TYPES):
        return []
    if type(value) is dict:
        return [p for k, v in value.items() for p in _non_plain(v, f"{path}.{k}")]
    if type(value) is list:
        return [p for i, v in enumerate(value) for p in _non_plain(v, f"{path}[{i}]")]
    return [f"{path}: {type(value).__name__}"]


SHIPMENT_ADDRESS = dict(
    person_name="Jane Doe",
    address_line1="1 Main St",
    city="Montreal",
    country_code="CA",
    postal_code="H1H1H1",
)

# Test Data and Fixtures
SIMPLE_HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title | default('Simple Test Document') }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; }
        .content { margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ title | default('Simple Test Document') }}</h1>
    </div>

    <div class="content">
        {% if shipment %}
        <p><strong>Tracking Number:</strong> {{ shipment.tracking_number }}</p>
        <p><strong>Service:</strong> {{ shipment.service }}</p>
        <p><strong>Status:</strong> {{ shipment.status }}</p>
        {% endif %}

        {% if order %}
        <p><strong>Order ID:</strong> {{ order.order_id }}</p>
        <p><strong>Order Date:</strong> {{ order.order_date }}</p>
        {% endif %}

        <p>Generated at: {{ utils.datetime.now().strftime('%Y-%m-%d %H:%M:%S') }}</p>
    </div>
</body>
</html>
"""

INVOICE_HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Commercial Invoice</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .header { text-align: center; margin-bottom: 30px; }
        .addresses { display: table; width: 100%; margin-bottom: 30px; }
        .address { display: table-cell; width: 50%; vertical-align: top; padding: 10px; }
        .invoice-details { margin-bottom: 30px; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .total { text-align: right; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>COMMERCIAL INVOICE</h1>
        {% if metadata and metadata.doc_type %}
        <p>Document Type: {{ metadata.doc_type }}</p>
        {% endif %}
    </div>

    <div class="addresses">
        {% if shipment %}
        <div class="address">
            <h3>Ship From:</h3>
            <p>{{ shipment.shipper.person_name or shipment.shipper.company_name }}</p>
            <p>{{ shipment.shipper.address_line1 }}</p>
            {% if shipment.shipper.address_line2 %}
            <p>{{ shipment.shipper.address_line2 }}</p>
            {% endif %}
            <p>{{ shipment.shipper.city }}, {{ shipment.shipper.state_code }} {{ shipment.shipper.postal_code }}</p>
            <p>{{ shipment.shipper.country_code }}</p>
        </div>

        <div class="address">
            <h3>Ship To:</h3>
            <p>{{ shipment.recipient.person_name or shipment.recipient.company_name }}</p>
            <p>{{ shipment.recipient.address_line1 }}</p>
            {% if shipment.recipient.address_line2 %}
            <p>{{ shipment.recipient.address_line2 }}</p>
            {% endif %}
            <p>{{ shipment.recipient.city }}, {{ shipment.recipient.state_code }} {{ shipment.recipient.postal_code }}</p>
            <p>{{ shipment.recipient.country_code }}</p>
        </div>
        {% endif %}
    </div>

    {% if shipment %}
    <div class="invoice-details">
        <table>
            <tr>
                <th>Tracking Number</th>
                <td>{{ shipment.tracking_number }}</td>
                <th>Service</th>
                <td>{{ shipment.service }}</td>
            </tr>
            <tr>
                <th>Status</th>
                <td>{{ shipment.status }}</td>
                <th>Created Date</th>
                <td>{{ shipment.created_at }}</td>
            </tr>
        </table>
    </div>
    {% endif %}

    {% if line_items %}
    <h3>Items</h3>
    <table>
        <thead>
            <tr>
                <th>SKU</th>
                <th>Description</th>
                <th>Quantity</th>
                <th>Unit Price</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
            {% for item in line_items %}
            <tr>
                <td>{{ item.sku }}</td>
                <td>{{ item.title }}</td>
                <td>{{ item.quantity }}</td>
                <td>${{ "%.2f"|format(item.unit_price|float) }}</td>
                <td>${{ "%.2f"|format((item.unit_price|float) * (item.quantity|int)) }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% endif %}

    <p style="text-align: center; margin-top: 40px;">
        Generated by Karrio on {{ utils.datetime.now().strftime('%Y-%m-%d') }}
    </p>
</body>
</html>
"""

# Sample base64 encoded PDF (minimal valid PDF)
SAMPLE_PDF_BASE64 = "JVBERi0xLjQKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMiAwIFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1R5cGUgL1BhZ2VzCi9LaWRzIFszIDAgUl0KL0NvdW50IDEKPD4KZW5kb2JqCjMgMCBvYmoKPDwKL1R5cGUgL1BhZ2UKL1BhcmVudCAyIDAgUgovTWVkaWFCb3ggWzAgMCA2MTIgNzkyXQo+PgplbmRvYmoKeHJlZgowIDQKMDAwMDAwMDAwMCA2NTUzNSBmCjAwMDAwMDAwMDkgMDAwMDAgbgowMDAwMDAwMDU4IDAwMDAwIG4KMDAwMDAwMDExNSAwMDAwMCBuCnRyYWlsZXIKPDwKL1NpemUgNAovUm9vdCAxIDAgUgo+PgpzdGFydHhyZWYKMTc4CiUlRU9G"

# Sample base64 encoded ZIP file (for testing multi-document bundling)
SAMPLE_ZIP_BASE64 = """UEsDBBQAAAAIAKOOdU8e6yR4HQAAAB8AAAANAAAAdGVzdC1kb2MxLnBkZitIQ1BQ0KdJI5tT37IM5rK/ZIHYsyeCOYhNnwKNOkKjDqN9rCE9C/qzlvggwAEw2TnZ+UpJOZn5eUrJOcY5QCOjkWRzQpOy"""


class TestTemplateHelpersAreAllowlisted(APITestCase):
    """Document templates are written by users and rendered on the server, so
    what the render globals expose is the security boundary, not the sandbox.

    Jinja2's sandbox blocks attribute walks such as ``"".__class__``, but any
    callable placed in the globals is callable. Passing ``karrio.lib`` whole
    gave every template author ``lib.load_file_content`` (any readable path)
    and ``lib.request`` (any URL), reachable through /v1/documents/generate
    with an inline template.
    """

    def setUp(self) -> None:
        super().setUp()
        self.url = reverse("karrio.server.documents:document-generator")
        self.secret_file = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False)
        self.secret_file.write("not-for-templates")
        self.secret_file.close()

    def _generate(self, template: str):
        return self.client.post(
            self.url,
            {"template": template, "data": {"title": "x"}, "doc_name": "probe.pdf"},
        )

    def test_inline_template_cannot_read_a_server_file(self):
        withheld = {
            "lib file read": "{{ lib.load_file_content('%s') }}",
            "lib via utils": "{{ utils.lib.load_file_content('%s') }}",
        }
        for label, body in withheld.items():
            with self.subTest(label):
                response = self._generate(body % self.secret_file.name)

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn("not available in document templates", str(response.content))

    def test_inline_template_cannot_reach_the_http_client(self):
        response = self._generate("{{ lib.request(url='http://127.0.0.1:1/') }}")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("not available in document templates", str(response.content))

    def test_inline_template_with_allowed_helpers_still_renders(self):
        response = self._generate(
            "<p>{{ lib.to_money(12.5) }} {{ lib.fdate('2026-09-30', '%Y-%m-%d') }} "
            "{{ utils.datetime.now().year }} {{ units.CountryISO.US }}</p>"
        )
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(base64.b64decode(response_data["doc_file"]).startswith(b"%PDF"))


class TestTemplateGlobalsAreNarrowed(unittest.TestCase):
    def _render(self, body: str) -> str:
        return generator.SANDBOXED_ENV.from_string(body).render(
            lib=generator.TEMPLATE_LIB,
            utils=generator.TEMPLATE_UTILS,
            units={},
            metadata={},
        )

    def test_the_sandbox_itself_still_blocks_attribute_escape(self):
        with self.assertRaises(jinja2.exceptions.SecurityError):
            self._render('{{ "".__class__.__mro__ }}')

    def test_nothing_that_opens_a_socket_or_reads_a_path_is_reachable(self):
        withheld = {
            "http client": '{{ lib.request(url="http://169.254.169.254/") }}',
            "local file read": '{{ lib.load_file_content("/etc/passwd") }}',
            "stdlib by name": '{{ lib.urllib.parse.quote("a b") }}',
            "units module": "{{ lib.units.pathlib }}",
            "lib via utils": '{{ utils.lib.load_file_content("/etc/passwd") }}',
            "io via utils": "{{ utils.io.open }}",
            "base64 via utils": '{{ utils.base64.b64decode("x") }}',
        }
        for label, body in withheld.items():
            with self.subTest(label), self.assertRaises(jinja2.exceptions.SecurityError):
                self._render(body)

    def test_the_helpers_a_document_needs_still_work(self):
        self.assertEqual(self._render("{{ lib.to_money(12.5) }}"), "12.5")
        self.assertEqual(self._render('{{ lib.fdate("2026-09-30", "%Y-%m-%d") }}'), "2026-09-30")
        self.assertEqual(
            self._render("{{ utils.datetime.now().year }}"),
            str(documents_utils.datetime.now().year),
        )
        self.assertIn("create_barcode", generator.TEMPLATE_UTILS)
        self.assertIn("generate_code", generator.TEMPLATE_UTILS)

    def test_no_module_is_reachable_from_the_exposed_helpers(self):
        """The invariant rather than a list of known escapes: nothing exposed is
        a module, and nothing exposed re-exports one a level down."""
        offenders = set()
        for label, namespace in (("lib", generator.TEMPLATE_LIB), ("utils", generator.TEMPLATE_UTILS)):
            for name, value in namespace._members.items():
                if isinstance(value, types.ModuleType):
                    offenders.add(f"{label}.{name}")
                for attr in dir(value):
                    if not attr.startswith("_") and isinstance(getattr(value, attr, None), types.ModuleType):
                        offenders.add(f"{label}.{name}.{attr}")

        self.assertEqual(offenders, set())
