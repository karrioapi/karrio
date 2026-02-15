"""SmartKargo carrier shipment tests."""

import unittest
from unittest.mock import patch, ANY
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
        # Check key fields are present
        self.assertIn("reference", serialized)
        self.assertIn("packages", serialized)
        self.assertEqual(len(serialized["packages"]), 1)
        self.assertEqual(serialized["packages"][0]["serviceType"], "EST")

    def test_create_shipment(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)
            # The first call should be to exchange/single, subsequent calls are for label fetching
            first_call_url = mock.call_args_list[0][1]["url"]
            self.assertEqual(
                first_call_url,
                f"{gateway.settings.server_url}/exchange/single?version=2.0"
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest)
                .from_(gateway)
                .parse()
            )
            print(parsed_response)
            self.assertIsNotNone(parsed_response[0])
            self.assertEqual(parsed_response[0].tracking_number, "AXB01234567")

    def test_create_shipment_cancel_request(self):
        request = gateway.mapper.create_cancel_shipment_request(self.ShipmentCancelRequest)
        serialized = request.serialize()
        self.assertEqual(serialized["prefix"], "AXB")
        self.assertEqual(serialized["airWaybill"], "01234567")

    def test_cancel_shipment(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)
            self.assertIn(
                "shipment/void?prefix=AXB&airWaybill=01234567",
                mock.call_args[1]["url"]
            )

    def test_parse_shipment_cancel_response(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )
            print(parsed_response)
            self.assertIsNotNone(parsed_response[0])
            self.assertTrue(parsed_response[0].success)

    def test_parse_error_response(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest)
                .from_(gateway)
                .parse()
            )
            print(parsed_response)
            self.assertIsNone(parsed_response[0])
            self.assertTrue(len(parsed_response[1]) > 0)


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
    "shipment_identifier": "AXB01234567"
}

ShipmentResponse = """{
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
}"""

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
