"""Asendia carrier manifest tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class TestAsendiaManifest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ManifestRequest = models.ManifestRequest(**ManifestPayload)

    def test_create_manifest_request(self):
        request = gateway.mapper.create_manifest_request(self.ManifestRequest)
        print(lib.to_dict(request.serialize()))
        self.assertEqual(lib.to_dict(request.serialize()), ManifestRequest)

    def test_create_manifest(self):
        with patch("karrio.mappers.asendia.proxy.lib.request") as mock:
            with patch("karrio.providers.asendia.utils.Settings.access_token", new_callable=lambda: property(lambda self: "test_token")):
                mock.return_value = "{}"
                karrio.Manifest.create(self.ManifestRequest).from_(gateway)
                print(mock.call_args[1]["url"])
                self.assertEqual(
                    mock.call_args[1]["url"],
                    f"{gateway.settings.server_url}/api/manifests"
                )

    def test_parse_manifest_response(self):
        with patch("karrio.mappers.asendia.proxy.lib.request") as mock:
            with patch("karrio.providers.asendia.utils.Settings.access_token", new_callable=lambda: property(lambda self: "test_token")):
                mock.return_value = ManifestResponse
                parsed_response = (
                    karrio.Manifest.create(self.ManifestRequest)
                    .from_(gateway)
                    .parse()
                )
                print(lib.to_dict(parsed_response))
                self.assertListEqual(lib.to_dict(parsed_response), ParsedManifestResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.asendia.proxy.lib.request") as mock:
            with patch("karrio.providers.asendia.utils.Settings.access_token", new_callable=lambda: property(lambda self: "test_token")):
                mock.return_value = ErrorResponse
                parsed_response = (
                    karrio.Manifest.create(self.ManifestRequest)
                    .from_(gateway)
                    .parse()
                )
                print(lib.to_dict(parsed_response))
                self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


ManifestPayload = {
    "shipment_identifiers": [
        "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "4fa85f64-5717-4562-b3fc-2c963f66afa7",
    ],
    "address": {
        "city": "Bern",
        "country_code": "CH",
    },
}

ManifestRequest = {
    "parcelIds": [
        "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "4fa85f64-5717-4562-b3fc-2c963f66afa7",
    ],
}

ManifestResponse = """{
  "id": "manifest-123",
  "createdAt": "2024-04-15T10:00:00Z",
  "errorMessage": null,
  "errorParcelIds": [],
  "status": "CREATED",
  "manifestDocumentLocation": "/manifests/manifest-123/document",
  "parcelsLocation": "/manifests/manifest-123/parcels",
  "manifestLocation": "/manifests/manifest-123"
}"""

ParsedManifestResponse = [
    {
        "carrier_id": "asendia",
        "carrier_name": "asendia",
        "id": "manifest-123",
        "meta": {
            "status": "CREATED",
            "created_at": "2024-04-15T10:00:00Z",
            "manifest_document_location": "/manifests/manifest-123/document",
            "parcels_location": "/manifests/manifest-123/parcels",
            "manifest_location": "/manifests/manifest-123",
        },
    },
    []
]

ErrorResponse = """{
  "type": "https://www.asendia-sync.com/problem/constraint-violation",
  "title": "Bad Request",
  "status": 400,
  "detail": "Invalid parcel IDs",
  "path": "/api/manifests",
  "message": "error.manifest.invalid_parcels",
  "errorMessage": "One or more parcel IDs are invalid",
  "errorParcelIds": ["invalid-parcel-id"]
}"""

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "asendia",
            "carrier_name": "asendia",
            "code": "400",
            "details": {"path": "/api/manifests", "type": "https://www.asendia-sync.com/problem/constraint-violation"},
            "message": "Invalid parcel IDs",
        },
        {
            "carrier_id": "asendia",
            "carrier_name": "asendia",
            "code": "MANIFEST_ERROR",
            "message": "One or more parcel IDs are invalid",
        },
        {
            "carrier_id": "asendia",
            "carrier_name": "asendia",
            "code": "PARCEL_ERROR",
            "message": "Failed to include parcel: invalid-parcel-id",
        },
    ],
]
