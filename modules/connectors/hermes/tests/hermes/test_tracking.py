"""Hermes carrier tracking tests."""

import unittest
from unittest.mock import patch, PropertyMock
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class TestHermesTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        serialized = request.serialize()
        print(f"Tracking request: {serialized}")
        self.assertEqual(serialized, TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.providers.hermes.utils.Settings.access_token", new_callable=PropertyMock) as mock_token:
            mock_token.return_value = {"access_token": "test_token"}
            with patch("karrio.mappers.hermes.proxy.lib.request") as mock:
                mock.return_value = "{}"
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)
                call_url = mock.call_args[1]["url"]
                print(f"Tracking URL: {call_url}")
                self.assertIn("/shipmentinfo?", call_url)
                self.assertIn("shipmentID=H1234567890123456789", call_url)

    def test_parse_tracking_response(self):
        with patch("karrio.providers.hermes.utils.Settings.access_token", new_callable=PropertyMock) as mock_token:
            mock_token.return_value = {"access_token": "test_token"}
            with patch("karrio.mappers.hermes.proxy.lib.request") as mock:
                mock.return_value = TrackingResponse
                parsed_response = (
                    karrio.Tracking.fetch(self.TrackingRequest)
                    .from_(gateway)
                    .parse()
                )
                print(f"Parsed tracking response: {parsed_response}")
                self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_tracking_error_response(self):
        with patch("karrio.providers.hermes.utils.Settings.access_token", new_callable=PropertyMock) as mock_token:
            mock_token.return_value = {"access_token": "test_token"}
            with patch("karrio.mappers.hermes.proxy.lib.request") as mock:
                mock.return_value = TrackingErrorResponse
                parsed_response = (
                    karrio.Tracking.fetch(self.TrackingRequest)
                    .from_(gateway)
                    .parse()
                )
                print(f"Parsed tracking error response: {parsed_response}")
                self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["H1234567890123456789"],
}

TrackingRequest = ["H1234567890123456789"]

TrackingResponse = """{
    "shipmentinfo": [
        {
            "shipmentID": "H1234567890123456789",
            "clientReference": "ORDER-12345",
            "trackingLink": "https://www.myhermes.de/tracking/H1234567890123456789",
            "receiverAddress": {
                "city": "Hamburg",
                "zipCode": "22419",
                "countryCode": "DEU"
            },
            "deliveryForecast": {
                "fixed": false,
                "date": "2024-01-20",
                "timeSlot": {
                    "from": "10:00",
                    "to": "18:00"
                }
            },
            "status": [
                {
                    "timestamp": "2024-01-18T08:30:00+01:00",
                    "code": "0000",
                    "description": "The shipment has been notified to Hermes electronically.",
                    "scanningUnit": {
                        "name": "Hermes Germany",
                        "city": "Berlin",
                        "countryCode": "DEU"
                    }
                },
                {
                    "timestamp": "2024-01-19T10:15:00+01:00",
                    "code": "2000",
                    "description": "The shipment has arrived at the Hermes distribution center.",
                    "scanningUnit": {
                        "name": "Hermes Germany",
                        "city": "Hamburg",
                        "countryCode": "DEU"
                    }
                },
                {
                    "timestamp": "2024-01-20T07:00:00+01:00",
                    "code": "3000",
                    "description": "The shipment has gone out on a delivery route. Delivery is expected today.",
                    "scanningUnit": {
                        "name": "Hermes Germany",
                        "city": "Hamburg",
                        "countryCode": "DEU"
                    }
                },
                {
                    "timestamp": "2024-01-20T14:30:00+01:00",
                    "code": "3500",
                    "description": "The shipment has been delivered.",
                    "scanningUnit": {
                        "name": "Hermes Germany",
                        "city": "Hamburg",
                        "countryCode": "DEU"
                    }
                }
            ]
        }
    ]
}"""

TrackingErrorResponse = """{
    "shipmentinfo": [
        {
            "shipmentID": "H1234567890123456789",
            "result": {
                "code": "e001",
                "message": "There is no information for the entered value."
            }
        }
    ]
}"""

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "hermes",
            "carrier_name": "hermes",
            "tracking_number": "H1234567890123456789",
            "events": [
                {
                    "date": "2024-01-20",
                    "time": "14:30 PM",
                    "description": "The shipment has been delivered.",
                    "code": "3500",
                    "location": "Hamburg, DEU",
                    "timestamp": "2024-01-20T14:30:00+01:00",
                    "status": "delivered"
                },
                {
                    "date": "2024-01-20",
                    "time": "07:00 AM",
                    "description": "The shipment has gone out on a delivery route. Delivery is expected today.",
                    "code": "3000",
                    "location": "Hamburg, DEU",
                    "timestamp": "2024-01-20T07:00:00+01:00",
                    "status": "out_for_delivery"
                },
                {
                    "date": "2024-01-19",
                    "time": "10:15 AM",
                    "description": "The shipment has arrived at the Hermes distribution center.",
                    "code": "2000",
                    "location": "Hamburg, DEU",
                    "timestamp": "2024-01-19T10:15:00+01:00",
                    "status": "in_transit"
                },
                {
                    "date": "2024-01-18",
                    "time": "08:30 AM",
                    "description": "The shipment has been notified to Hermes electronically.",
                    "code": "0000",
                    "location": "Berlin, DEU",
                    "timestamp": "2024-01-18T08:30:00+01:00",
                    "status": "pending"
                }
            ],
            "delivered": True,
            "status": "delivered",
            "estimated_delivery": "2024-01-20",
            "info": {
                "carrier_tracking_link": "https://www.myhermes.de/tracking/H1234567890123456789",
                "shipment_destination_country": "DEU",
                "shipment_destination_postal_code": "22419"
            },
            "meta": {
                "client_reference": "ORDER-12345"
            }
        }
    ],
    []
]

ParsedTrackingErrorResponse = [
    [],
    [
        {
            "carrier_id": "hermes",
            "carrier_name": "hermes",
            "code": "e001",
            "message": "There is no information for the entered value.",
            "details": {
                "shipment_id": "H1234567890123456789"
            }
        }
    ]
]
