import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestEasyshipTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.easyship.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.easyship.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.easyship.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["89108749065090"],
}

ParsedTrackingResponse = []

ParsedErrorResponse = []


TrackingRequest = {}

TrackingResponse = """{
  "meta": {
    "request_id": "01563646-58c1-4607-8fe0-cae3e92c4477"
  },
  "tracking": {
    "courier": {
      "id": "01563646-58c1-4607-8fe0-cae3e33c0001",
      "umbrella_name": "DHL"
    },
    "destination_country_alpha2": "SG",
    "easyship_shipment_id": "ESSG10006002",
    "eta_date": "string",
    "id": "01563646-58c1-4607-8fe0-cae3e33c0001",
    "origin_country_alpha2": "HK",
    "platform_order_number": "string",
    "source": "external",
    "status": "string",
    "tracking_number": "Z5400000001",
    "tracking_status": "created",
    "tracking_page_url": "http://localhost:9003/shipment-tracking/ESSG10006002",
    "checkpoints": [
      {
        "checkpoint_time": "2024-05-01T00:00:00Z",
        "city": "City",
        "country_iso3": "string",
        "country_name": "string",
        "handler": "string",
        "location": "string",
        "message": "string",
        "order_number": "string",
        "postal_code": "string",
        "country_alpha2": "SG",
        "description": "Description",
        "primary_status": "string",
        "state": "State"
      }
    ]
  }
}
"""

ErrorResponse = """{
  "error": {
    "code": "over_limit",
    "details": [
      "We were unable to generate a label as your maximum balance limit has been reached. Please contact your account manager."
    ],
    "message": "You have reached your plan limit. Please upgrade your subscription plan.",
    "request_id": "01563646-58c1-4607-8fe0-cae3e92c4477",
    "type": "invalid_request_error"
  }
}
"""
