"""Spring carrier tracking tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class TestSpringTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(lib.to_dict(request.serialize()), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.spring.proxy.lib.run_asynchronously") as mock_async:
            mock_async.return_value = [("LXAB00000000NL", "{}")]
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertTrue(mock_async.called)

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.spring.proxy.lib.run_asynchronously") as mock_async:
            mock_async.return_value = [("LXAB00000000NL", TrackingResponse)]
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.spring.proxy.lib.run_asynchronously") as mock_async:
            mock_async.return_value = [("LXAB00000000NL", TrackingErrorResponse)]
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedTrackingErrorResponse
            )


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["LXAB00000000NL"],
}

TrackingRequest = [
    {
        "Apikey": "TEST_API_KEY",
        "Command": "TrackShipment",
        "Shipment": {
            "TrackingNumber": "LXAB00000000NL",
        },
    }
]

TrackingResponse = """{
    "ErrorLevel": 0,
    "Error": "",
    "Shipment": {
        "TrackingNumber": "LXAB00000000NL",
        "ShipperReference": "ORDER-12345",
        "Service": "PPTT",
        "Carrier": "PostNL",
        "CarrierTrackingNumber": "3STEST1234567890",
        "CarrierLocalTrackingNumber": "LOCAL123",
        "CarrierTrackingUrl": "https://tracking.postnl.nl/track/3STEST1234567890",
        "DisplayId": "LXAB00000000NL",
        "Weight": "2.5",
        "WeightUnit": "kg",
        "Events": [
            {
                "Timestamp": 1704110400,
                "DateTime": "2024-01-01 12:00:00",
                "Country": "NL",
                "City": "Amsterdam",
                "State": "",
                "Zip": "1012AB",
                "Code": 20,
                "Description": "Shipment accepted at origin facility"
            },
            {
                "Timestamp": 1704196800,
                "DateTime": "2024-01-02 12:00:00",
                "Country": "DE",
                "City": "Berlin",
                "State": "",
                "Zip": "10115",
                "Code": 100,
                "Description": "Delivered"
            }
        ]
    }
}"""

TrackingErrorResponse = """{
    "ErrorLevel": 10,
    "Error": "Tracking number not found"
}"""

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "spring",
            "carrier_name": "spring",
            "tracking_number": "LXAB00000000NL",
            "delivered": True,
            "status": "delivered",
            "events": [
                {
                    "date": "2024-01-02",
                    "description": "Delivered",
                    "code": "100",
                    "time": "12:00 PM",
                    "location": "Berlin, DE",
                    "timestamp": "2024-01-02T12:00:00.000Z",
                    "status": "delivered",
                },
                {
                    "date": "2024-01-01",
                    "description": "Shipment accepted at origin facility",
                    "code": "20",
                    "time": "12:00 PM",
                    "location": "Amsterdam, NL",
                    "timestamp": "2024-01-01T12:00:00.000Z",
                    "status": "in_transit",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://tracking.postnl.nl/track/3STEST1234567890",
                "package_weight": "2.5",
                "package_weight_unit": "kg",
            },
            "meta": {
                "service": "PPTT",
                "carrier": "PostNL",
                "display_id": "LXAB00000000NL",
                "shipper_reference": "ORDER-12345",
                "carrier_tracking_number": "3STEST1234567890",
                "carrier_local_tracking_number": "LOCAL123",
            },
        }
    ],
    [],
]

ParsedTrackingErrorResponse = [
    [],
    [
        {
            "carrier_id": "spring",
            "carrier_name": "spring",
            "code": "10",
            "message": "Tracking number not found",
            "details": {
                "tracking_number": "LXAB00000000NL",
            },
        }
    ],
]
