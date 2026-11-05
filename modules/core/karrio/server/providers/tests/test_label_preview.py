"""Tests for the generic carrier label template preview endpoint."""

from django.urls import reverse
from rest_framework import status
from karrio.server.core.tests import APITestCase
import karrio.server.providers.models as providers


class TestCarrierLabelPreview(APITestCase):
    """Tests for GET /v1/carriers/{pk}/label.{format}."""

    def setUp(self):
        super().setUp()
        self.generic_carrier = providers.CarrierConnection.objects.create(
            carrier_code="generic",
            carrier_id="custom_carrier",
            test_mode=True,
            created_by=self.user,
            credentials=dict(
                custom_carrier_name="Custom Carrier",
                display_name="Custom Carrier Display",
                label_template=LABEL_TEMPLATE,
            ),
            capabilities=["rating", "shipping"],
        )

    def test_label_preview(self):
        """A generic connection with a persisted label_template renders it."""
        url = reverse(
            "karrio.server.providers:carrier-label",
            kwargs=dict(pk=self.generic_carrier.id, format="svg"),
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, EXPECTED_LABEL)

    def test_label_preview_without_template(self):
        """A generic connection without a label_template falls back to the
        default sample shipment and template."""
        carrier = providers.CarrierConnection.objects.create(
            carrier_code="generic",
            carrier_id="custom_carrier_default",
            test_mode=True,
            created_by=self.user,
            credentials=dict(
                custom_carrier_name="Custom Carrier",
                display_name="Custom Carrier Display",
            ),
            capabilities=["rating", "shipping"],
        )
        url = reverse(
            "karrio.server.providers:carrier-label",
            kwargs=dict(pk=carrier.id, format="svg"),
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


LABEL_TEMPLATE = {
    "slug": "ucc_128",
    "width": 4,
    "height": 6,
    "template_type": "SVG",
    # Renders the sample shipment shipper company name from
    # karrio.providers.generic.units.SAMPLE_SHIPMENT_REQUEST.
    "template": (
        "<svg xmlns='http://www.w3.org/2000/svg' width='4in' height='6in'>"
        "{{ shipment.shipper.get('company_name', '').upper() }}</svg>"
    ),
    "shipment_sample": {},
}

EXPECTED_LABEL = (
    "<svg xmlns='http://www.w3.org/2000/svg' width='4in' height='6in'>CGI</svg>"
).encode("utf-8")
