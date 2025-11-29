"""Teleship carrier manifest tests."""

import unittest
from unittest.mock import patch
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestTeleshipManifest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ManifestRequest = models.ManifestRequest(**ManifestPayload)

    def test_create_manifest_request(self):
        request = gateway.mapper.create_manifest_request(self.ManifestRequest)

        self.assertEqual(lib.to_dict(request.serialize()), ManifestRequest)

    def test_create_manifest(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Manifest.create(self.ManifestRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/manifests",
            )

    def test_parse_manifest_response(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = ManifestResponse
            parsed_response = (
                karrio.Manifest.create(self.ManifestRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedManifestResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Manifest.create(self.ManifestRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


ManifestPayload = {
    "shipment_identifiers": ["SHP-UK-US-98765", "SHP-UK-US-98766", "SHP-UK-US-98767"],
    "reference": "MANIFEST-2025-001",
    "address": {
        "address_line1": "123 Business Park",
        "city": "London",
        "postal_code": "SW1A 1AA",
        "country_code": "GB",
        "state_code": "LDN",
        "person_name": "John Smith",
        "company_name": "UK Exports Ltd",
        "phone_number": "+442071234567",
        "email": "shipping@ukexports.co.uk",
    },
}

ManifestRequest = {
    "address": {
        "address": {
            "city": "London",
            "country": "GB",
            "line1": "123 Business Park",
            "postcode": "SW1A 1AA",
            "state": "LDN",
        },
        "company": "UK Exports Ltd",
        "email": "shipping@ukexports.co.uk",
        "name": "John Smith",
        "phone": "+442071234567",
    },
    "reference": "MANIFEST-2025-001",
    "shipmentIds": ["SHP-UK-US-98765", "SHP-UK-US-98766", "SHP-UK-US-98767"],
}

ManifestResponse = """{
    "id": "MNF-2025-001",
    "status": "created",
    "reference": "MANIFEST-2025-001",
    "createdAt": "2025-01-15T10:30:00.000Z"
}"""

ErrorResponse = """{
    "messages": [
        {
            "code": 400,
            "timestamp": "2025-01-15T10:30:45Z",
            "message": "Invalid manifest request",
            "details": [
                "Shipment SHP-UK-US-98765 has already been manifested",
                "Shipment SHP-UK-US-98768 not found"
            ]
        }
    ]
}"""

ParsedManifestResponse = [
    {
        "carrier_id": "teleship",
        "carrier_name": "teleship",
        "id": "MNF-2025-001",
        "meta": {
            "createdAt": "2025-01-15T10:30:00.000Z",
            "reference": "MANIFEST-2025-001",
            "status": "created",
        },
    },
    [],
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "teleship",
            "carrier_name": "teleship",
            "code": "400",
            "message": "Invalid manifest request",
            "details": {
                "timestamp": "2025-01-15T10:30:45Z",
                "details": [
                    "Shipment SHP-UK-US-98765 has already been manifested",
                    "Shipment SHP-UK-US-98768 not found",
                ],
            },
        }
    ],
]
