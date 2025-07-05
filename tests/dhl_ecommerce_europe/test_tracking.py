import unittest
from unittest.mock import patch, ANY
from .fixture import gateway, TrackingPayload, TrackingResponse

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestDHLEcommerceEuropeTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        # Check if the request structure is correct
        self.assertIn("trackingNumbers", request.serialize())
        self.assertEqual(request.serialize()["trackingNumbers"], ["00340434292135100186"])

    def test_get_tracking(self):
        with patch("karrio.mappers.dhl_ecommerce_europe.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            # Check if the correct URL is being called
            self.assertIn("api", mock.call_args[1]["url"])

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.dhl_ecommerce_europe.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)


if __name__ == "__main__":
    unittest.main()


ParsedTrackingResponse = [
    [
        {
            "carrier_id": "dhl_ecommerce_europe",
            "carrier_name": "dhl_ecommerce_europe",
            "delivered": True,
            "estimated_delivery": "2025-01-22",
            "events": [
                {
                    "code": "PU",
                    "date": "2025-01-20",
                    "description": "Shipment picked up",
                    "location": "Hamburg, 20095, DE",
                    "time": "09:15:00",
                },
                {
                    "code": "OK",
                    "date": "2025-01-22",
                    "description": "Delivered",
                    "location": "Berlin, 10115, DE",
                    "time": "14:30:00",
                },
            ],
            "meta": {
                "shipment_status": {
                    "description": "Delivered",
                    "location": {
                        "address": {
                            "addressLocality": "Berlin",
                            "countryCode": "DE",
                            "postalCode": "10115",
                        }
                    },
                    "status": "delivered",
                    "statusCode": "delivered",
                    "timestamp": "2025-01-22T14:30:00",
                }
            },
            "status": "delivered",
            "tracking_number": "00340434292135100186",
        }
    ],
    [],
] 