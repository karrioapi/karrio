import json
from unittest.mock import patch, ANY
from django.urls import reverse
from rest_framework import status
from karrio.core.models import ManifestDetails as ManifestDetailsModel
from karrio.server.manager.tests.test_shipments import (
    TestShipmentFixture,
    RETURNED_RATES_VALUE,
    CREATED_SHIPMENT_RESPONSE,
    SINGLE_CALL_LABEL_DATA,
)


class TestManifestDocumentDownload(TestShipmentFixture):
    """Test manifest document download POST API."""

    def create_manifest(self):
        """Create a manifest via API with a purchased shipment."""
        # First create and purchase a shipment
        shipment_url = reverse("karrio.server.manager:shipment-list")

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.side_effect = [RETURNED_RATES_VALUE, CREATED_SHIPMENT_RESPONSE]
            response = self.client.post(shipment_url, SINGLE_CALL_LABEL_DATA)
            shipment = json.loads(response.content)

        # Create manifest via API
        manifest_url = reverse("karrio.server.manager:manifest-list")
        manifest_data = {
            "carrier_name": "canadapost",
            "shipment_ids": [shipment["id"]],
            "address": {
                "address_line1": "125 Church St",
                "city": "Moncton",
                "country_code": "CA",
                "postal_code": "E1C4Z8",
                "state_code": "NB",
            },
        }

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = MANIFEST_RESPONSE
            response = self.client.post(manifest_url, manifest_data)
            return json.loads(response.content)

    def test_download_manifest_document(self):
        manifest = self.create_manifest()

        url = reverse(
            "karrio.server.manager:manifest-document-download",
            kwargs=dict(pk=manifest["id"]),
        )
        response = self.client.post(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, MANIFEST_DOCUMENT_RESPONSE)

    def test_download_manifest_not_found(self):
        url = reverse(
            "karrio.server.manager:manifest-document-download",
            kwargs=dict(pk="manf_non_existent_id"),
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


MANIFEST_RESPONSE = (
    ManifestDetailsModel(
        carrier_id="canadapost",
        carrier_name="canadapost",
        doc=dict(manifest="JVBERi0xLjQK"),
    ),
    [],
)

MANIFEST_DOCUMENT_RESPONSE = {
    "category": "manifest",
    "format": "PDF",
    "base64": "JVBERi0xLjQK",
    "url": ANY,
}
