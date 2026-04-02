"""SmartKargo carrier shipment tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class TestSmartKargoShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **ShipmentCancelPayload
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        self.assertEqual(lib.to_dict(request.serialize()), ShipmentRequestData)

    def test_create_shipment(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.side_effect = [ShipmentResponse, LabelResponse]
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)
            self.assertEqual(
                mock.call_args_list[0][1]["url"],
                f"{gateway.settings.server_url}/exchange/single?version=2.0",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.side_effect = [ShipmentResponse, LabelResponse]
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response),
                ParsedShipmentResponse,
            )

    def test_create_shipment_cancel_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )
        self.assertEqual(lib.to_dict(request.serialize()), ShipmentCancelRequestData)

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
            self.assertListEqual(
                lib.to_dict(parsed_response),
                ParsedCancelShipmentResponse,
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response),
                ParsedErrorResponse,
            )

    def test_parse_rejected_shipment_response(self):
        with patch("karrio.mappers.smartkargo.proxy.lib.request") as mock:
            mock.return_value = RejectedShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response),
                ParsedRejectedShipmentResponse,
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
        "email": "test@test.com",
        "federal_tax_id": "US123456789",
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
        "email": "test2@test.com",
        "federal_tax_id": "US987654321",
    },
    "parcels": [
        {
            "weight": 10.0,
            "width": 20.0,
            "height": 20.0,
            "length": 20.0,
            "weight_unit": "LB",
            "dimension_unit": "IN",
            "description": "Test Products",
            "reference_number": "PKG-TEST-001",
        }
    ],
    "service": "smartkargo_standard",
    "reference": "SHIP-REQ-001",
    "options": {
        "insurance": 150.0,
        "smartkargo_commodity_type": "GEN-6501",
    },
}

ShipmentCancelPayload = {
    "shipment_identifier": "PKG-REF-001",
    "options": {
        "tracking_numbers": ["AXB01234567"],
        "prefix": "AXB",
        "air_waybill": "01234567",
    },
}

ShipmentRequestData = [
    {
        "issueDate": ANY,
        "packages": [
            {
                "channel": "Direct",
                "commodityType": "GEN-6501",
                "insuranceAmmount": 150.0,
                "deliveryType": "DoorToDoor",
                "dimensions": [
                    {
                        "grossWeight": 10.0,
                        "height": 20.0,
                        "length": 20.0,
                        "pieces": 1,
                        "width": 20.0,
                    }
                ],
                "grossVolumeUnityMeasure": "CFT",
                "grossWeightUnityMeasure": "LBR",
                "hasInsurance": True,
                "packageDescription": "Test Products",
                "participants": [
                    {
                        "account": "TEST_ACCOUNT",
                        "additionalId": "TEST_ID",
                        "city": "Boston",
                        "countryId": "US",
                        "email": "test@test.com",
                        "name": "Test Company",
                        "phoneNumber": "19999999999",
                        "postCode": "02142",
                        "primaryId": "TEST_ID",
                        "state": "MA",
                        "street": "1 Broadway",
                        "taxId": "US123456789",
                        "type": "Shipper",
                    },
                    {
                        "city": "Los Angeles",
                        "countryId": "US",
                        "email": "test2@test.com",
                        "name": "Tester Tester",
                        "phoneNumber": "8888347867",
                        "postCode": "98148",
                        "state": "CA",
                        "street": "124 Main St",
                        "street2": "Unit 4",
                        "taxId": "US987654321",
                        "type": "Consignee",
                    },
                ],
                "paymentMode": "PX",
                "reference": "PKG-TEST-001",
                "serviceType": "EST",
                "totalGrossWeight": 10.0,
                "totalPackages": 1,
                "totalPieces": 1,
            }
        ],
        "reference": "SHIP-REQ-001",
    }
]

ShipmentCancelRequestData = [
    {
        "airWaybill": "01234567",
        "prefix": "AXB",
    }
]

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
      "barCode": "LASTMILE123456",
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
        "selected_rate": {
            "carrier_id": "smartkargo",
            "carrier_name": "smartkargo",
            "currency": "USD",
            "extra_charges": [
                {"amount": 8.5, "currency": "USD", "name": "Shipping Fee"},
                {"amount": 2.0, "currency": "USD", "name": "Insurance"},
                {"amount": 1.05, "currency": "USD", "name": "Tax"},
            ],
            "service": "smartkargo_standard",
            "total_charge": 10.5,
        },
        "meta": {
            "carrier_tracking_link": "https://www.deliverdirect.com/tracking?ref=AXB01234567",
            "estimated_delivery": "2021-07-05T21:00:00",
            "last_mile_tracking_number": "LASTMILE123456",
            "service_name": "smartkargo_standard",
            "smartkargo_air_waybill": "01234567",
            "smartkargo_header_reference": "ReferencesToBeSet",
            "smartkargo_label_url": "https://api.smartkargo.com/label?prefix=AXB&airWaybill=01234567",
            "smartkargo_origin": "YUL99",
            "smartkargo_package_reference": "2021-06-03-1",
            "smartkargo_prefix": "AXB",
            "smartkargo_service_type": "EST",
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

RejectedShipmentResponse = """[{
  "exchangeId": "test-aaaa-bbbb-cccc-dddddddddddd",
  "fileIdentifier": null,
  "siteId": "TEST",
  "inputType": "StandardJson",
  "status": "Rejected",
  "valid": "No",
  "createdOn": "2025-01-15T10:30:00.0000000",
  "shipments": [
    {
      "issueDate": "2025-01-15T10:30:00",
      "siteId": "TEST",
      "headerReference": "#ORDER-TEST-001",
      "packageReference": "TEST-PKG-001",
      "status": "Rejected",
      "validations": [
        {
          "message": "171 The requested destination ZIP code is currently not serviceable"
        }
      ]
    }
  ],
  "validations": []
}]"""

ParsedRejectedShipmentResponse = [
    None,
    [
        {
            "carrier_id": "smartkargo",
            "carrier_name": "smartkargo",
            "code": "VALIDATION_ERROR",
            "details": {
                "header_reference": "#ORDER-TEST-001",
                "package_reference": "TEST-PKG-001",
                "shipment_status": "REJECTED",
            },
            "message": "171 The requested destination ZIP code is currently not serviceable",
        },
        {
            "carrier_id": "smartkargo",
            "carrier_name": "smartkargo",
            "code": "ERROR",
            "details": {},
            "message": "An unknown error occurred",
        },
    ],
]
