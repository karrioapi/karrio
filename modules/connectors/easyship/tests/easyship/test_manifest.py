import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestEasyshipManifest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ManifestRequest = models.ManifestRequest(**ManifestPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_manifest_request(self.ManifestRequest)

        self.assertEqual(request.serialize(), ManifestRequest)

    def test_create_manifest(self):
        with patch("karrio.mappers.easyship.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Manifest.create(self.ManifestRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/2023-01/manifests",
            )

    def test_parse_manifest_response(self):
        with patch("karrio.mappers.easyship.proxy.lib.request") as mock:
            mock.side_effect = [ManifestResponse, "base64_encoded_file"]
            parsed_response = (
                karrio.Manifest.create(self.ManifestRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedManifestResponse)


if __name__ == "__main__":
    unittest.main()


ManifestPayload = {
    "shipment_identifiers": ["ESSG10006001"],
    "address": {
        "city": "Los Angeles",
        "state_code": "CA",
        "postal_code": "90001",
        "country_code": "US",
    },
    "options": {
        "easyship_courier_account_id": "01563646-58c1-4607-8fe0-cae3e33c0001",
    },
}

ParsedManifestResponse = [
    {
        "carrier_id": "easyship",
        "carrier_name": "easyship",
        "doc": {"manifest": ANY},
        "meta": {
            "courier_account_id": "01563646-58c1-4607-8fe0-cae3e33c0001",
            "courier_umbrella_name": "USPS",
            "manifest_id": "01563646-58c1-4607-8fe0-cae3e33c0001",
            "manifest_url": "http://document.url",
            "reference": "ABC123",
        },
    },
    [],
]


ManifestRequest = {
    "courier_account_id": "01563646-58c1-4607-8fe0-cae3e33c0001",
    "shipment_ids": ["ESSG10006001"],
}


ManifestResponse = """{
  "manifest": {
    "courier_account_id": "01563646-58c1-4607-8fe0-cae3e33c0001",
    "courier_umbrella_name": "USPS",
    "created_at": "2022-02-22T12:21:00Z",
    "document": {
      "format": "url",
      "url": "http://document.url"
    },
    "id": "01563646-58c1-4607-8fe0-cae3e33c0001",
    "ref_number": "ABC123",
    "shipments_count": 1
  },
  "meta": {
    "request_id": "01563646-58c1-4607-8fe0-cae3e92c4477"
  }
}
"""
