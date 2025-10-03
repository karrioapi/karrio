"""DTDC carrier shipment tests."""

import unittest
from unittest.mock import patch
from .fixture import gateway
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestDTDCShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.MultiPieceShipmentRequest = models.ShipmentRequest(
            **MultiPieceShipmentPayload
        )
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **ShipmentCancelPayload
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(lib.to_dict(request.serialize()), ExpectedShipmentRequest)

    def test_create_multi_piece_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.MultiPieceShipmentRequest)

        self.assertEqual(
            lib.to_dict(request.serialize()), ExpectedMultiPieceShipmentRequest
        )

    def test_create_shipment_cancel_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )
        self.assertEqual(
            lib.to_dict(request.serialize()), ExpectedShipmentCancelRequest
        )

    def test_create_shipment(self):
        with patch("karrio.mappers.dtdc.proxy.lib.request") as mock:
            mock.side_effect = [ShipmentResponse, LabelResponse]
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args_list[0][1]["url"],
                f"{gateway.settings.server_url}/api/customer/integration/consignment/softdata",
            )
            self.assertEqual(
                mock.call_args_list[1][1]["url"],
                f"{gateway.settings.label_server_url}/api/customer/integration/consignment/shippinglabel/stream?reference_number=100008518801&label_format=base64&label_code=SHIP_LABEL_4X6",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.dtdc.proxy.lib.request") as mock:
            mock.side_effect = [ShipmentCancelResponse]
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)
            self.assertEqual(
                mock.call_args_list[0][1]["url"],
                f"{gateway.settings.server_url}/api/customer/integration/consignment/cancel",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.dtdc.proxy.lib.request") as mock:
            mock.side_effect = [ShipmentResponse, LabelResponse]
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_shipment_cancel_response(self):
        with patch("karrio.mappers.dtdc.proxy.lib.request") as mock:
            mock.side_effect = [ShipmentCancelResponse]
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedShipmentCancelResponse
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.dtdc.proxy.lib.request") as mock:
            mock.side_effect = [ErrorResponse]
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "shipper": {
        "address_line1": "123 Test Street",
        "city": "Mumbai",
        "postal_code": "400001",
        "country_code": "IN",
        "state_code": "MH",
        "person_name": "Test Person",
        "company_name": "Test Company",
        "phone_number": "9876543210",
        "email": "test@example.com",
    },
    "recipient": {
        "address_line1": "456 Test Avenue",
        "city": "Delhi",
        "postal_code": "110001",
        "country_code": "IN",
        "state_code": "DL",
        "person_name": "Recipient Person",
        "company_name": "Recipient Company",
        "phone_number": "9876543211",
        "email": "recipient@example.com",
    },
    "parcels": [
        {
            "weight": 2.0,
            "width": 15.0,
            "height": 10.0,
            "length": 20.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "packaging_type": "your_packaging",
        }
    ],
    "service": "dtdc_b2c_priority",
    "options": {
        "dtdc_invoice_date": "2025-08-09",
    },
}

MultiPieceShipmentPayload = {
    **ShipmentPayload,
    "parcels": [
        {
            "weight": 2.0,
            "width": 15.0,
            "height": 10.0,
            "length": 20.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "packaging_type": "your_packaging",
        },
        {
            "weight": 3.0,
            "width": 16.0,
            "height": 11.0,
            "length": 21.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "packaging_type": "your_packaging",
        },
    ],
    "options": {
        "shipping_date": "2025-08-09T10:00",
    },
}


ShipmentCancelPayload = {"shipment_identifier": "DT123456789"}

ExpectedShipmentRequest = {
    "consignments": [
        {
            "customer_code": "TESTCUST001",
            "declared_value": "1",
            "destination_details": {
                "address_line_1": "456 Test Avenue",
                "city": "Delhi",
                "email": "recipient@example.com",
                "name": "Recipient Person",
                "phone": "9876543211",
                "pincode": 110001,
                "state": "DL",
            },
            "dimension_unit": "cm",
            "height": "10.0",
            "invoice_date": "09 Aug 2025",
            "length": "20.0",
            "load_type": "NON-DOCUMENT",
            "num_pieces": 1,
            "origin_details": {
                "address_line_1": "123 Test Street",
                "alternate_phone": "9876543210",
                "city": "Mumbai",
                "email": "test@example.com",
                "name": "Test Person",
                "phone": "9876543210",
                "pincode": 400001,
                "state": "MH",
            },
            "return_details": {
                "address_line_1": "123 Test Street",
                "city": "Mumbai",
                "email": "test@example.com",
                "name": "Test Person",
                "phone": "9876543210",
                "pincode": 400001,
            },
            "service_type_id": "B2C PRIORITY",
            "weight": "2.0",
            "weight_unit": "kg",
            "width": "15.0",
        }
    ]
}

ExpectedMultiPieceShipmentRequest = {
    "consignments": [
        {
            "customer_code": "TESTCUST001",
            "declared_value": "1",
            "destination_details": {
                "address_line_1": "456 Test Avenue",
                "city": "Delhi",
                "email": "recipient@example.com",
                "name": "Recipient Person",
                "phone": "9876543211",
                "pincode": 110001,
                "state": "DL",
            },
            "dimension_unit": "cm",
            "height": "10.0",
            "invoice_date": "09 Aug 2025",
            "length": "20.0",
            "load_type": "NON-DOCUMENT",
            "num_pieces": 2,
            "origin_details": {
                "address_line_1": "123 Test Street",
                "alternate_phone": "9876543210",
                "city": "Mumbai",
                "email": "test@example.com",
                "name": "Test Person",
                "phone": "9876543210",
                "pincode": 400001,
                "state": "MH",
            },
            "pieces_detail": [
                {"height": 10.0, "length": 20.0, "weight": 2.0, "width": 15.0},
                {"height": 11.0, "length": 21.0, "weight": 3.0, "width": 16.0},
            ],
            "return_details": {
                "address_line_1": "123 Test Street",
                "city": "Mumbai",
                "email": "test@example.com",
                "name": "Test Person",
                "phone": "9876543210",
                "pincode": 400001,
            },
            "service_type_id": "B2C PRIORITY",
            "weight": "2.0",
            "weight_unit": "kg",
            "width": "15.0",
        }
    ]
}

ExpectedShipmentCancelRequest = {
    "AWBNo": ["DT123456789"],
    "customerCode": "TESTCUST001",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "dtdc",
        "carrier_name": "dtdc",
        "docs": {"label": "base64_encoded_label_data"},
        "label_type": "PDF",
        "meta": {
            "carrier_tracking_link": "https://www.dtdc.com/tracking?trackid=100008518801",
            "dtdc_chargeable_weight": 0.025,
            "dtdc_customer_reference_number": "#100001",
            "dtdc_self_pickup_enabled": True,
            "service_name": "B2C PRIORITY",
            "tracking_numbers": ["100008518801001"],
        },
        "shipment_identifier": "100008518801",
        "tracking_number": "100008518801",
    },
    [],
]

ParsedShipmentCancelResponse = [
    {
        "carrier_id": "dtdc",
        "carrier_name": "dtdc",
        "success": True,
        "operation": "Cancel Shipment",
    },
    [],
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "dtdc",
            "carrier_name": "dtdc",
            "code": "WRONG_INPUT",
            "details": {},
            "message": "Consignment Series with service B2C PRIORITY does not Belong to "
            "Client",
        }
    ],
]

LabelResponse = """{
	"referenceNumber": "7X9150223",
    "label": "base64_encoded_label_data"
}"""

ShipmentResponse = """{
  "status": "OK",
  "data": [
    {
      "success": true,
      "reference_number": "100008518801",
      "courier_partner": null,
      "courier_account": "",
      "courier_partner_reference_number": null,
      "chargeable_weight": 0.025,
      "self_pickup_enabled": true,
      "customer_reference_number": "#100001",
      "pieces": [
        {
          "reference_number": "100008518801001",
          "product_code": ""
        }
      ],
      "barCodeData": ""
    }
  ]
}
"""

MultipleShipmentResponse = """{
  "status": "OK",
  "data": [
    {
      "success": true,
      "reference_number": "7X9150226",
      "courier_partner": null,
      "courier_account": "",
      "courier_partner_reference_number": null,
      "chargeable_weight": 14,
      "self_pickup_enabled": true,
      "customer_reference_number": "TEST-MPS-002",
      "pieces": [
        {
          "reference_number": "7X9150226001",
          "product_code": ""
        },
        {
          "reference_number": "7X9150226002",
          "product_code": ""
        },
        {
          "reference_number": "7X9150226003",
          "product_code": ""
        }
      ],
      "barCodeData": ""
    }
  ]
}
"""

ShipmentCancelResponse = """{
  "success": true,
  "status": "OK",
  "successConsignments": [
    {
      "reference_number": "DT123456789",
      "success": true
    }
  ]
}"""

ErrorResponse = """{
	"status": "OK",
	"data": [
		{
			"reason": "WRONG_INPUT",
			"success": false,
			"message": "Consignment Series with service B2C PRIORITY does not Belong to Client",
			"reference_number": "karrio12345",
			"customer_reference_number": "TEST-MPS-001"
		}
	]
}
"""
