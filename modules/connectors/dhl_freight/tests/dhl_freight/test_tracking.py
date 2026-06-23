"""DHL Freight tracking — DHL Group Unified Tracking API (UTAPI)."""

import unittest
from unittest.mock import patch

import karrio.core.models as models
import karrio.sdk as karrio

from .fixture import gateway


class TestDHLFreightTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(tracking_numbers=["FRT-123456789"])

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        self.assertListEqual(
            request.serialize(),
            [{"trackingNumber": "FRT-123456789", "service": "freight", "language": "en"}],
        )

    def test_get_tracking(self):
        with patch("karrio.mappers.dhl_freight.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            url = mock.call_args[1]["url"]
            headers = mock.call_args[1]["headers"]
            self.assertIn("/track/shipments?", url)
            self.assertIn("trackingNumber=FRT-123456789", url)
            self.assertIn("service=freight", url)
            self.assertEqual(headers["DHL-API-Key"], gateway.settings.client_id)

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.dhl_freight.proxy.lib.request") as mock:
            mock.return_value = TRACKING_RESPONSE
            parsed, messages = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()

            self.assertEqual(messages, [])
            self.assertEqual(len(parsed), 1)
            self.assertEqual(parsed[0].tracking_number, "FRT-123456789")
            self.assertEqual(parsed[0].status, "in_transit")
            self.assertEqual(len(parsed[0].events), 1)
            self.assertEqual(parsed[0].meta["license_plates"], ["00370000000000000001", "00370000000000000002"])

    def test_parse_delivered_response(self):
        with patch("karrio.mappers.dhl_freight.proxy.lib.request") as mock:
            mock.return_value = DELIVERED_RESPONSE
            parsed, _ = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            self.assertEqual(parsed[0].status, "delivered")
            self.assertTrue(parsed[0].delivered)

    def test_parse_error_response(self):
        with patch("karrio.mappers.dhl_freight.proxy.lib.request") as mock:
            mock.return_value = TRACKING_ERROR
            parsed, messages = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            self.assertEqual(parsed, [])
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0].carrier_name, "dhl_freight")


if __name__ == "__main__":
    unittest.main()


TRACKING_RESPONSE = """{
    "shipments": [
        {
            "id": "FRT-123456789",
            "service": "freight",
            "origin": {"address": {"countryCode": "SE", "postalCode": "41758", "addressLocality": "GOTHENBURG"}},
            "destination": {"address": {"countryCode": "DE", "postalCode": "53113", "addressLocality": "BONN"}},
            "status": {"timestamp": "2026-12-31T07:53:47Z", "statusCode": "transit", "status": "IN_TRANSIT", "description": "In transit"},
            "estimatedTimeOfDelivery": "2027-01-03T00:00:00Z",
            "details": {
                "product": {"productName": "DHL Freight Euroconnect"},
                "totalNumberOfPieces": 2,
                "pieceIds": ["00370000000000000001", "00370000000000000002"],
                "weight": {"value": 1100, "unitText": "kg"},
                "references": {"number": "ORDER-9001", "type": "customer-reference"}
            },
            "events": [
                {"timestamp": "2026-12-31T07:53:47", "location": {"address": {"countryCode": "SE", "addressLocality": "GOTHENBURG"}}, "statusCode": "transit", "status": "IN_TRANSIT", "description": "Departed from origin terminal"}
            ]
        }
    ]
}"""

DELIVERED_RESPONSE = """{
    "shipments": [
        {
            "id": "FRT-123456789",
            "service": "freight",
            "status": {"timestamp": "2027-01-03T10:00:00Z", "statusCode": "delivered", "status": "DELIVERED", "description": "Delivered"},
            "events": [
                {"timestamp": "2027-01-03T10:00:00", "statusCode": "delivered", "status": "DELIVERED", "description": "Delivered to consignee"}
            ]
        }
    ]
}"""

TRACKING_ERROR = """{
    "title": "No result found",
    "detail": "No shipment with given tracking number found.",
    "status": 404,
    "instance": "/shipments/FRT-123456789"
}"""
