"""SmartKargo carrier shipment tests."""

import unittest
from unittest.mock import patch
from .fixture import gateway
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestSmartKargoShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(**ShipmentCancelPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        serialized = request.serialize()
        # Per-package pattern: serialize returns a list of requests
        self.assertIsInstance(serialized, list)
        self.assertEqual(len(serialized), 1)
        self.assertIn("reference", serialized[0])
        self.assertIn("packages", serialized[0])
        self.assertEqual(len(serialized[0]["packages"]), 1)
        self.assertEqual(serialized[0]["packages"][0]["serviceType"], "EST")

    def test_create_shipment(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            # First call returns booking response, second call returns label
            mock.side_effect = [ShipmentResponse, LabelResponse]
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)
            # First call: booking, second call: label fetch
            first_call_url = mock.call_args_list[0][1]["url"]
            self.assertEqual(
                first_call_url,
                f"{gateway.settings.server_url}/exchange/single?version=2.0"
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.side_effect = [ShipmentResponse, LabelResponse]
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest)
                .from_(gateway)
                .parse()
            )
            print(parsed_response)
            self.assertListEqual(
                lib.to_dict(parsed_response),
                ParsedShipmentResponse,
            )

    def test_create_shipment_cancel_request(self):
        request = gateway.mapper.create_cancel_shipment_request(self.ShipmentCancelRequest)
        serialized = request.serialize()
        # Per-package pattern: serialize returns a list of cancel requests
        self.assertIsInstance(serialized, list)
        self.assertEqual(len(serialized), 1)
        self.assertEqual(serialized[0]["prefix"], "AXB")
        self.assertEqual(serialized[0]["airWaybill"], "01234567")

    def test_create_shipment_cancel_request_single_piece_fallback(self):
        """Test cancel request for single-piece shipment (no tracking_numbers in meta)."""
        cancel_request = models.ShipmentCancelRequest(
            shipment_identifier="PKG-REF-001",
            options={"prefix": "AXB", "air_waybill": "01234567"},
        )
        request = gateway.mapper.create_cancel_shipment_request(cancel_request)
        serialized = request.serialize()
        self.assertIsInstance(serialized, list)
        self.assertEqual(len(serialized), 1)
        self.assertEqual(serialized[0]["prefix"], "AXB")
        self.assertEqual(serialized[0]["airWaybill"], "01234567")

    def test_cancel_shipment(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)
            call_url = mock.call_args[1]["url"]
            self.assertIn("shipment/void?", call_url)
            self.assertIn("prefix=AXB", call_url)
            self.assertIn("airWaybill=01234567", call_url)

    def test_parse_shipment_cancel_response(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )
            print(parsed_response)
            self.assertListEqual(
                lib.to_dict(parsed_response),
                ParsedCancelShipmentResponse,
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            # Error response has no labelUrl/Booked status, so only 1 call (booking)
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest)
                .from_(gateway)
                .parse()
            )
            print(parsed_response)
            self.assertListEqual(
                lib.to_dict(parsed_response),
                ParsedErrorResponse,
            )


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "shipper": {
        "address_line1": "1 Broadway",
        "city": "Boston",
        "postal_code": "02142",
        "country_code": "US",
        "state_code": "MA",
        "person_name": "TESTER TEST",
        "company_name": "Test Company",
        "phone_number": "19999999999",
        "email": "test@test.com"
    },
    "recipient": {
        "address_line1": "124 Main St",
        "address_line2": "Unit 4",
        "city": "Los Angeles",
        "postal_code": "98148",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Tester Tester",
        "phone_number": "8888347867",
        "email": "test2@test.com"
    },
    "parcels": [{
        "weight": 10.0,
        "width": 20.0,
        "height": 20.0,
        "length": 20.0,
        "weight_unit": "LB",
        "dimension_unit": "IN",
        "description": "Test Products",
        "reference_number": "PKG-TEST-001",
    }],
    "service": "smartkargo_standard",
    "reference": "SHIP-REQ-001",
    "options": {
        "insurance": 150.0,
        "smartkargo_commodity_type": "GEN-6501",
    }
}

ShipmentCancelPayload = {
    "shipment_identifier": "PKG-REF-001",
    "options": {
        "tracking_numbers": ["AXB01234567"],
        "prefix": "AXB",
        "air_waybill": "01234567",
    }
}

ShipmentResponse = """[{
  "exchangeId": "test-17f7-test-2382-test",
  "fileIdentifier": null,
  "siteId": "TEST",
  "inputType": "StandardJson",
  "status": "Processed",
  "valid": "Yes",
  "createdOn": "2021-06-28T03:08:30.1127523",
  "shipments": [
    {
      "issueDate": "2021-06-29T20:00:00",
      "siteId": "TEST",
      "headerReference": "ReferencesToBeSet",
      "packageReference": "2021-06-03-1",
      "prefix": "AXB",
      "airWaybill": "01234567",
      "estimatedDeliveryDate": "2021-07-05T21:00:00",
      "commodityType": "GEN-6501",
      "serviceType": "EST",
      "origin": "YUL99",
      "destination": null,
      "packageDescription": "Test Products",
      "totalGrossWeight": 10.00,
      "totalPackages": 1.00,
      "totalPieces": 1.00,
      "currency": "USD",
      "insuranceRequired": true,
      "declaredValue": 150.00,
      "specialHandlingType": "INS",
      "deliveryRequestTime": "2021-06-28T03:08:30.1011107",
      "pickupRequestTime": "2021-06-28T03:08:30.1011081",
      "expectedSLAInHours": null,
      "paymentMode": "PX",
      "grossVolumeUnitMeasure": "CFT",
      "grossWeightUnitMeasure": "KG",
      "status": "Booked",
      "createdOn": "2021-06-28T03:08:30.1127526",
      "labelUrl": "https://api.smartkargo.com/label?prefix=AXB&airWaybill=01234567",
      "shippingFee": 8.50,
      "insurance": 2.00,
      "totalCharges": 0.00,
      "total": 10.50,
      "totalTax": 1.05
    }
  ],
  "validations": []
}]"""

ShipmentCancelResponse = """{
  "result": {
    "cancelled": true,
    "messages": null
  }
}"""

ErrorResponse = """{
  "status": "Failed",
  "valid": "No",
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid shipment request"
  },
  "validations": [
    {
      "code": "VAL001",
      "message": "Missing required field: weight"
    }
  ]
}"""

LabelResponse = """{
  "base64Content": "data:application/pdf;base64,JVBERi0xLjQKJeLjz9M="
}"""

ParsedShipmentResponse = [
    {
        "carrier_id": "smartkargo",
        "carrier_name": "smartkargo",
        "docs": {
            "label": "JVBERi0xLjQKJeLjz9M=",
        },
        "label_type": "PDF",
        "meta": {
            "air_waybill": "01234567",
            "carrier_tracking_link": "https://www.deliverdirect.com/tracking?ref=AXB01234567",
            "currency": "USD",
            "estimated_delivery": "2021-07-05T21:00:00",
            "header_reference": "ReferencesToBeSet",
            "label_url": "https://api.smartkargo.com/label?prefix=AXB&airWaybill=01234567",
            "origin": "YUL99",
            "package_reference": "2021-06-03-1",
            "prefix": "AXB",
            "service_name": "smartkargo_standard",
            "service_type": "EST",
            "total_charge": 10.5,
        },
        "shipment_identifier": "2021-06-03-1",
        "tracking_number": "AXB01234567",
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "smartkargo",
        "carrier_name": "smartkargo",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "smartkargo",
            "carrier_name": "smartkargo",
            "code": "INVALID_REQUEST",
            "details": {},
            "message": "Invalid shipment request",
        },
    ],
]
