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
        self.ManifestRequest = models.ManifestRequest(
            shipments=["SHIP123456", "SHIP789012"]
        )

    def test_create_manifest_request(self):
        request = gateway.mapper.create_manifest_request(self.ManifestRequest)
        self.assertEqual(request.serialize(), ManifestRequest)

    def test_create_manifest(self):
        with patch("karrio.mappers.asendia.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Manifest.create(self.ManifestRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/manifests"
            )

    def test_parse_manifest_response(self):
        with patch("karrio.mappers.asendia.proxy.lib.request") as mock:
            mock.return_value = ManifestResponse
            parsed_response = (
                karrio.Manifest.create(self.ManifestRequest)
                .from_(gateway)
                .parse()
            )
            self.assertIsNotNone(parsed_response[0])
            self.assertEqual(len(parsed_response[1]), 0)
            self.assertEqual(parsed_response[0].carrier_name, "asendia")

    def test_parse_error_response(self):
        with patch("karrio.mappers.asendia.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Manifest.create(self.ManifestRequest)
                .from_(gateway)
                .parse()
            )
            self.assertIsNone(parsed_response[0])
            self.assertEqual(len(parsed_response[1]), 1)
            self.assertEqual(parsed_response[1][0].code, "manifest_error")


if __name__ == "__main__":
    unittest.main()


ManifestResponse = """{
  "carrier_id": "asendia",
  "carrier_name": "asendia",
  "manifest": "JVBERi0xLjcKCjEgMCBvYmogICUgZW50cnkgcG9pbnQKPDwKICAvVHlwZSAvQ2F0YWxvZwogIC9QYWdlcyAyIDAgUgo+PgplbmRvYmoKCjIgMCBvYmoKPDwKICAvVHlwZSAvUGFnZXMKICAvTWVkaWFCb3ggWyAwIDAgMjAwIDIwMCBdCiAgL0NvdW50IDEKICAvS2lkcyBbIDMgMCBSIF0KPj4KZW5kb2JqCgozIDAgb2JqCjw8CiAgL1R5cGUgL1BhZ2UKICAvUGFyZW50IDIgMCBSCiAgL1Jlc291cmNlcyA8PAogICAgL0ZvbnQgPDwKICAgICAgL0YxIDQgMCBSIAogICAgPj4KICA+PgogIC9Db250ZW50cyA1IDAgUgo+PgplbmRvYmoKCjQgMCBvYmoKPDwKICAvVHlwZSAvRm9udAogIC9TdWJ0eXBlIC9UeXBlMQogIC9CYXNlRm9udCAvVGltZXMtUm9tYW4KPj4KZW5kb2JqCgo1IDAgb2JqICAlIHBhZ2UgY29udGVudAo8PAogIC9MZW5ndGggNDQKPj4Kc3RyZWFtCkJUCjcwIDUwIFRECi9GMSAxMiBUZgooSGVsbG8sIHdvcmxkISkgVGoKRVQKZW5kc3RyZWFtCmVuZG9iagoKeHJlZgowIDYKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDEwIDAwMDAwIG4gCjAwMDAwMDAwNzkgMDAwMDAgbiAKMDAwMDAwMDE3MyAwMDAwMCBuIAowMDAwMDAwMzAxIDAwMDAwIG4gCjAwMDAwMDAzODAgMDAwMDAgbiAKdHJhaWxlcgo8PAogIC9TaXplIDYKICAvUm9vdCAxIDAgUgo+PgpzdGFydHhyZWYKNDkyCiUlRU9G"
}"""

ManifestRequest = """{
  "shipmentIdentifiers": [
    "SHIP123456",
    "SHIP789012"
  ],
  "address": {
    "addressLine1": "123 Main Street",
    "city": "Los Angeles",
    "postalCode": "90001",
    "countryCode": "US",
    "stateCode": "CA",
    "personName": "John Doe",
    "companyName": "Test Company",
    "phoneNumber": "555-123-4567",
    "email": "john.doe@example.com"
  },
  "reference": "REF123",
  "options": {
    "close_date": "2023-07-01"
  }
}"""

ErrorResponse = """{
  "error": {
    "code": "manifest_error",
    "message": "Unable to create manifest",
    "details": "Invalid shipment identifiers provided"
  }
}"""