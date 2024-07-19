import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestZoom2uTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.zoom2u.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/v1/delivery/status/89108749065090",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.zoom2u.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.zoom2u.proxy.lib.request") as mock:
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

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "zoom2u",
            "carrier_name": "zoom2u",
            "delivered": True,
            "events": [
                {
                    "code": "Dropped Off",
                    "date": "2018-11-12",
                    "description": "Dropped Off",
                    "time": "10:29 AM",
                }
            ],
            "info": {
                "carrier_tracking_link": "https://deliveries.zoom2u.com/EMPQ28I5J"
            },
            "meta": {},
            "tracking_number": "Z20190101123456",
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "zoom2u",
            "carrier_name": "zoom2u",
            "code": "403",
            "details": {"tracking_number": "89108749065090"},
            "message": "Forbidden",
        }
    ],
]


TrackingRequest = ["89108749065090"]

TrackingResponse = """{
  "reference": "Z20190101123456",
  "status": "Dropped Off",
  "statusChangeDateTime": "2018-11-12T10:29:16.867Z",
  "purchaseOrderNumber": "",
  "tracking-link": "https://deliveries.zoom2u.com/EMPQ28I5J",
  "proofOfDeliveryPhotoUrl": null,
  "signatureUrl": null,
  "courier": {
    "id": "1234",
    "name": "Test Courier",
    "phone": "02 1234 5678"
  }
}
"""

ErrorResponse = """{
    "error-code": "403",
    "message": "Forbidden"
}
"""
