import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestSEKOLogisticsManifest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ManifestRequest = models.ManifestRequest(**ManifestPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_manifest_request(self.ManifestRequest)

        self.assertEqual(request.serialize(), ManifestRequest)

    def test_create_manifest(self):
        with patch("karrio.mappers.seko.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Manifest.create(self.ManifestRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_manifest_response(self):
        with patch("karrio.mappers.seko.proxy.lib.request") as mock:
            mock.return_value = ManifestResponse
            parsed_response = (
                karrio.Manifest.create(self.ManifestRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedManifestResponse)


if __name__ == "__main__":
    unittest.main()


ManifestPayload = {
    "shipment_identifiers": ["794947717776"],
    "address": {
        "city": "Los Angeles",
        "state_code": "CA",
        "postal_code": "90001",
        "country_code": "US",
    },
    "options": {},
}

ParsedManifestResponse = [
    {
        "carrier_id": "seko",
        "carrier_name": "seko",
        "doc": {"manifest": ANY},
        "meta": {},
    },
    [],
]


ManifestRequest = ["6994008906", "6994008907"]

ManifestResponse = """{
  "OutboundManifest": [
    {
      "ManifestNumber": "OHG00288",
      "ManifestedConnotes": ["01593505840002135181", "01593505840002135198"],
      "ManifestContent": "JVBERi0xLjcgCiXi48/TIAoxIDAgb2JqIAo8PCAKL1R5cGUgL0NhdGFsb2cgCi9QYWdlcyAyIDAgUiAKL1BhZ2VNb2RlIC9Vc2VOb25lIAovVmlld2VyUH...."
    }
  ],
  "InboundManifest": [],
  "Error": [],
  "StatusCode": 200,
  "UnManifestedConnotes": []
}
"""
