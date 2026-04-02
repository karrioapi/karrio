"""SmartKargo carrier tracking tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class TestSmartKargoTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        self.assertEqual(lib.to_dict(request.serialize()), TrackingRequestData)

    def test_get_tracking(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = "[]"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)
            self.assertIn(
                "tracking?packageReference=yogi045",
                mock.call_args[1]["url"],
            )

    def test_get_tracking_by_airwaybill(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = "[]"
            tracking_request = models.TrackingRequest(
                tracking_numbers=["XIA00291643"]
            )
            karrio.Tracking.fetch(tracking_request).from_(gateway)
            self.assertIn(
                "tracking?",
                mock.call_args[1]["url"],
            )
            self.assertIn("prefix=XIA", mock.call_args[1]["url"])
            self.assertIn("Airwaybill=00291643", mock.call_args[1]["url"])

    def test_get_tracking_from_shipment_meta(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = "[]"
            tracking_request = models.TrackingRequest(
                tracking_numbers=["XIA00291643"],
                options={
                    "XIA00291643": {
                        "smartkargo_prefix": "XIA",
                        "smartkargo_air_waybill": "00291643",
                    }
                },
            )
            karrio.Tracking.fetch(tracking_request).from_(gateway)
            self.assertIn("prefix=XIA", mock.call_args[1]["url"])
            self.assertIn("Airwaybill=00291643", mock.call_args[1]["url"])

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response),
                ParsedTrackingResponse,
            )

    def test_parse_partner_tracking_response(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = PartnerTrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response),
                ParsedPartnerTrackingResponse,
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response),
                ParsedTrackingErrorResponse,
            )


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["yogi045"],
}

TrackingRequestData = [
    {
        "tracking_number": "yogi045",
        "query_params": {"packageReference": "yogi045"},
    }
]

TrackingResponse = """[
  {
    "prefix": "AXB",
    "airWaybill": "00006510",
    "headerReference": "yogi045",
    "packageReference": "yogi045",
    "pieceReference": "yogi045-001",
    "eventType": "BKD",
    "eventDate": "2021-01-25T13:03:17",
    "flightNumber": "AC123",
    "flightDate": "2021-01-26T13:30:00",
    "eventLocation": "BOS",
    "flightSegmentOrigin": null,
    "flightSegmentDestination": "LAX",
    "pieces": 1.00,
    "weight": 2.8400,
    "description": "Electronic information submitted by shipper Boston Logan.",
    "referenceAirWaybill": null,
    "estimatedDeliveryDate": "2021-01-28T23:59:00",
    "bagNumber": null,
    "subEventType": null
  },
  {
    "prefix": "AXB",
    "airWaybill": "00006510",
    "headerReference": "yogi045",
    "packageReference": "yogi045",
    "pieceReference": "yogi045-002",
    "eventType": "DDL",
    "eventDate": "2021-01-26T14:30:00",
    "flightNumber": "AC123",
    "flightDate": "2021-01-26T13:30:00",
    "eventLocation": "LAX",
    "flightSegmentOrigin": "BOS",
    "flightSegmentDestination": "LAX",
    "pieces": 1.00,
    "weight": 2.8400,
    "description": "Package has been successfully delivered to the consignee.",
    "referenceAirWaybill": null,
    "estimatedDeliveryDate": "2021-01-28T23:59:00",
    "bagNumber": "T0101",
    "subEventType": null
  }
]"""

PartnerTrackingResponse = """[
  {
    "headerReference": "TEST-REF-001",
    "packageReference": "TEST-PKG-001",
    "pieceReference": "TEST-PCE-001",
    "eventDate": "2024-03-15T10:30:00",
    "flightNumber": "AB1234",
    "flightDate": "2024-03-15T08:00:00",
    "eventLocation": "JFK",
    "flightSegmentOrigin": "JFK",
    "flightSegmentDestination": "LAX",
    "pieces": 2.0,
    "weight": 5.50,
    "description": "Shipment has departed from origin facility.",
    "prefix": "ABC",
    "airWaybill": "12345678",
    "eventType": "DEP",
    "location": {
      "eventLocation": "JFK",
      "street": "123 Main St",
      "city": "New York",
      "state": "NY",
      "zip": "10001",
      "latitude": "40.7128",
      "longitude": "-74.0060",
      "timezone": "America/New_York",
      "countryId": "US"
    },
    "estimatedDeliveryDate": "2024-03-17T23:59:00"
  },
  {
    "headerReference": "TEST-REF-001",
    "packageReference": "TEST-PKG-001",
    "pieceReference": "TEST-PCE-001",
    "eventDate": "2024-03-14T08:00:00",
    "flightNumber": "AB1234",
    "flightDate": "2024-03-14T06:00:00",
    "eventLocation": "BOS",
    "flightSegmentOrigin": null,
    "flightSegmentDestination": "JFK",
    "pieces": 2.0,
    "weight": 5.50,
    "description": "Shipment received at origin facility.",
    "prefix": "ABC",
    "airWaybill": "12345678",
    "eventType": "RCS",
    "location": {
      "eventLocation": "BOS",
      "street": "456 Oak Ave",
      "city": "Boston",
      "state": "MA",
      "zip": "02101",
      "latitude": "42.3601",
      "longitude": "-71.0589",
      "timezone": "America/New_York",
      "countryId": "US"
    },
    "estimatedDeliveryDate": "2024-03-17T23:59:00"
  }
]"""

ErrorResponse = """{
  "error": {
    "code": "NOT_FOUND",
    "message": "Tracking information not found"
  }
}"""

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "smartkargo",
            "carrier_name": "smartkargo",
            "delivered": True,
            "estimated_delivery": "2021-01-28",
            "events": [
                {
                    "code": "DDL",
                    "date": "2021-01-26",
                    "description": "Package has been successfully delivered to the consignee.",
                    "location": "LAX",
                    "status": "delivered",
                    "time": "14:30",
                    "timestamp": "2021-01-26T14:30:00.000Z",
                },
                {
                    "code": "BKD",
                    "date": "2021-01-25",
                    "description": "Electronic information submitted by shipper Boston Logan.",
                    "location": "BOS",
                    "status": "pending",
                    "time": "13:03",
                    "timestamp": "2021-01-25T13:03:17.000Z",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://www.deliverdirect.com/tracking?ref=yogi045",
                "package_weight": 2.84,
                "package_weight_unit": "KG",
                "shipment_package_count": 1,
            },
            "meta": {
                "smartkargo_air_waybill": "00006510",
                "smartkargo_flight_number": "AC123",
                "smartkargo_header_reference": "yogi045",
                "smartkargo_package_reference": "yogi045",
                "smartkargo_piece_reference": "yogi045-002",
                "smartkargo_prefix": "AXB",
            },
            "status": "delivered",
            "tracking_number": "yogi045",
        },
    ],
    [],
]

ParsedPartnerTrackingResponse = [
    [
        {
            "carrier_id": "smartkargo",
            "carrier_name": "smartkargo",
            "delivered": False,
            "estimated_delivery": "2024-03-17",
            "events": [
                {
                    "code": "DEP",
                    "date": "2024-03-15",
                    "description": "Shipment has departed from origin facility.",
                    "latitude": 40.7128,
                    "location": "New York, NY",
                    "longitude": -74.006,
                    "status": "in_transit",
                    "time": "10:30",
                    "timestamp": "2024-03-15T10:30:00.000Z",
                },
                {
                    "code": "RCS",
                    "date": "2024-03-14",
                    "description": "Shipment received at origin facility.",
                    "latitude": 42.3601,
                    "location": "Boston, MA",
                    "longitude": -71.0589,
                    "status": "picked_up",
                    "time": "08:00",
                    "timestamp": "2024-03-14T08:00:00.000Z",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://www.deliverdirect.com/tracking?ref=yogi045",
                "package_weight": 5.5,
                "package_weight_unit": "KG",
                "shipment_package_count": 2,
            },
            "meta": {
                "smartkargo_air_waybill": "12345678",
                "smartkargo_flight_number": "AB1234",
                "smartkargo_header_reference": "TEST-REF-001",
                "smartkargo_package_reference": "TEST-PKG-001",
                "smartkargo_piece_reference": "TEST-PCE-001",
                "smartkargo_prefix": "ABC",
            },
            "status": "in_transit",
            "tracking_number": "yogi045",
        },
    ],
    [],
]

ParsedTrackingErrorResponse = [
    [],
    [
        {
            "carrier_id": "smartkargo",
            "carrier_name": "smartkargo",
            "code": "NOT_FOUND",
            "details": {
                "tracking_number": "yogi045",
            },
            "message": "Tracking information not found",
        },
    ],
]
