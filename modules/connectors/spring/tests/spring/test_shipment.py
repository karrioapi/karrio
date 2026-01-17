"""Spring carrier shipment tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class TestSpringShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(**ShipmentCancelPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        print(f"Generated request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), ShipmentRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.spring.proxy.lib.run_asynchronously") as mock_async:
            mock_async.return_value = ["{}"]
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)
            print(f"run_asynchronously called: {mock_async.called}")
            self.assertTrue(mock_async.called)

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.spring.proxy.lib.run_asynchronously") as mock_async:
            mock_async.return_value = [ShipmentResponse]
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Parsed response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(self.ShipmentCancelRequest)
        print(f"Generated cancel request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), ShipmentCancelRequest)

    def test_cancel_shipment(self):
        with patch("karrio.mappers.spring.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.spring.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Parsed cancel response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentCancelResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.spring.proxy.lib.run_asynchronously") as mock_async:
            mock_async.return_value = [ErrorResponse]
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Error response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


class TestSpringMultiPieceShipment(unittest.TestCase):
    """Test multi-piece shipment handling for Spring."""

    def setUp(self):
        self.maxDiff = None
        self.MultiPieceShipmentRequest = models.ShipmentRequest(**MultiPieceShipmentPayload)

    def test_create_multi_piece_shipment_request(self):
        """Verify that multi-piece shipments create one request per package."""
        request = gateway.mapper.create_shipment_request(self.MultiPieceShipmentRequest)
        serialized = lib.to_dict(request.serialize())
        print(f"Multi-piece request: {serialized}")
        # Should have 2 requests (one per package)
        self.assertEqual(len(serialized), 2)
        # References should include package index
        self.assertIn("-1", serialized[0]["Shipment"]["ShipperReference"])
        self.assertIn("-2", serialized[1]["Shipment"]["ShipperReference"])
        # Each package should have its own weight
        self.assertEqual(serialized[0]["Shipment"]["Weight"], "2.5")
        self.assertEqual(serialized[1]["Shipment"]["Weight"], "1.5")

    def test_parse_multi_piece_shipment_response(self):
        """Verify that multi-piece responses are aggregated correctly."""
        with patch("karrio.mappers.spring.proxy.lib.run_asynchronously") as mock_async:
            mock_async.return_value = [MultiPieceShipmentResponse1, MultiPieceShipmentResponse2]
            parsed_response = (
                karrio.Shipment.create(self.MultiPieceShipmentRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Multi-piece parsed response: {lib.to_dict(parsed_response)}")
            result = lib.to_dict(parsed_response)
            # Should have shipment details
            self.assertIsNotNone(result[0])
            # Master tracking number should be from first package
            self.assertEqual(result[0]["tracking_number"], "LXAB00000001NL")
            # Should have multiple tracking numbers in meta (order may vary)
            self.assertIn("tracking_numbers", result[0]["meta"])
            self.assertEqual(
                set(result[0]["meta"]["tracking_numbers"]),
                {"LXAB00000001NL", "LXAB00000002NL"}
            )
            # Should have multiple shipment identifiers in meta (tracking numbers for cancellation)
            self.assertIn("shipment_identifiers", result[0]["meta"])
            self.assertEqual(
                set(result[0]["meta"]["shipment_identifiers"]),
                {"LXAB00000001NL", "LXAB00000002NL"}
            )


if __name__ == "__main__":
    unittest.main()


MultiPieceShipmentPayload = {
    "shipper": {
        "address_line1": "Sender Street 123",
        "city": "Amsterdam",
        "postal_code": "1012AB",
        "country_code": "NL",
        "person_name": "John Sender",
        "company_name": "Sender Company",
        "phone_number": "+31201234567",
        "email": "sender@example.com",
    },
    "recipient": {
        "address_line1": "Recipient Ave 456",
        "city": "Berlin",
        "postal_code": "10115",
        "country_code": "DE",
        "person_name": "Jane Recipient",
        "company_name": "Recipient GmbH",
        "phone_number": "+49301234567",
        "email": "recipient@example.com",
    },
    "parcels": [
        {
            "weight": 2.5,
            "width": 20.0,
            "height": 15.0,
            "length": 30.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        },
        {
            "weight": 1.5,
            "width": 15.0,
            "height": 10.0,
            "length": 25.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        }
    ],
    "service": "PPTT",
    "reference": "ORDER-MULTI",
}

MultiPieceShipmentResponse1 = """{
    "ErrorLevel": 0,
    "Error": "",
    "Shipment": {
        "TrackingNumber": "LXAB00000001NL",
        "ShipperReference": "ORDER-MULTI-1",
        "LabelImage": "XlhBXkNJMTNeTFQwXkxIMCwwXk1URAo=",
        "LabelFormat": "ZPL",
        "Service": "PPTT",
        "Carrier": "PostNL",
        "CarrierTrackingNumber": "3STEST0000000001",
        "CarrierTrackingUrl": "https://tracking.postnl.nl/track/3STEST0000000001",
        "DisplayId": "LXAB00000001NL",
        "LabelType": "ZPL"
    }
}"""

MultiPieceShipmentResponse2 = """{
    "ErrorLevel": 0,
    "Error": "",
    "Shipment": {
        "TrackingNumber": "LXAB00000002NL",
        "ShipperReference": "ORDER-MULTI-2",
        "LabelImage": "XlhBXkNJMTNeTFQwXkxIMCwwXk1URAo=",
        "LabelFormat": "ZPL",
        "Service": "PPTT",
        "Carrier": "PostNL",
        "CarrierTrackingNumber": "3STEST0000000002",
        "CarrierTrackingUrl": "https://tracking.postnl.nl/track/3STEST0000000002",
        "DisplayId": "LXAB00000002NL",
        "LabelType": "ZPL"
    }
}"""

ShipmentPayload = {
    "shipper": {
        "address_line1": "Sender Street 123",
        "city": "Amsterdam",
        "postal_code": "1012AB",
        "country_code": "NL",
        "person_name": "John Sender",
        "company_name": "Sender Company",
        "phone_number": "+31201234567",
        "email": "sender@example.com",
    },
    "recipient": {
        "address_line1": "Recipient Ave 456",
        "city": "Berlin",
        "postal_code": "10115",
        "country_code": "DE",
        "person_name": "Jane Recipient",
        "company_name": "Recipient GmbH",
        "phone_number": "+49301234567",
        "email": "recipient@example.com",
    },
    "parcels": [
        {
            "weight": 2.5,
            "width": 20.0,
            "height": 15.0,
            "length": 30.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        }
    ],
    "service": "PPTT",
    "reference": "ORDER-12345",
}

ShipmentCancelPayload = {
    "shipment_identifier": "LXAB00000000NL",
}

ShipmentRequest = [
    {
        "Apikey": "TEST_API_KEY",
        "Command": "OrderShipment",
        "Shipment": {
            "LabelFormat": "PDF",
            "ShipperReference": "ORDER-12345",
            "Service": "PPTT",
            "Weight": "2.5",
            "WeightUnit": "kg",
            "Length": "30.0",
            "Width": "20.0",
            "Height": "15.0",
            "DimUnit": "cm",
            "CustomsDuty": "DDU",
            "DangerousGoods": "N",
            "ConsignorAddress": {
                "Name": "John Sender",
                "Company": "Sender Company",
                "AddressLine1": "Sender Street 123",
                "City": "Amsterdam",
                "Zip": "1012AB",
                "Country": "NL",
                "Phone": "+31201234567",
                "Email": "sender@example.com",
            },
            "ConsigneeAddress": {
                "Name": "Jane Recipient",
                "Company": "Recipient GmbH",
                "AddressLine1": "Recipient Ave 456",
                "City": "Berlin",
                "Zip": "10115",
                "Country": "DE",
                "Phone": "+49301234567",
                "Email": "recipient@example.com",
            },
        },
    }
]

ShipmentCancelRequest = {
    "Apikey": "TEST_API_KEY",
    "Command": "VoidShipment",
    "Shipment": {
        "TrackingNumber": "LXAB00000000NL",
    },
}

ShipmentResponse = """{
    "ErrorLevel": 0,
    "Error": "",
    "Shipment": {
        "TrackingNumber": "LXAB00000000NL",
        "ShipperReference": "ORDER-12345",
        "LabelImage": "JVBERi0xLjQKJeLjz9MKMyAwIG9iago=",
        "LabelFormat": "PDF",
        "Service": "PPTT",
        "Carrier": "PostNL",
        "CarrierTrackingNumber": "3STEST1234567890",
        "CarrierTrackingUrl": "https://tracking.postnl.nl/track/3STEST1234567890",
        "DisplayId": "LXAB00000000NL",
        "LabelType": "PDF"
    }
}"""

ShipmentCancelResponse = """{
    "ErrorLevel": 0,
    "Error": "",
    "Shipment": {
        "TrackingNumber": "LXAB00000000NL",
        "ShipperReference": "ORDER-12345"
    }
}"""

ErrorResponse = """{
    "ErrorLevel": 10,
    "Error": "Invalid API key provided"
}"""

ParsedShipmentResponse = [
    {
        "carrier_id": "spring",
        "carrier_name": "spring",
        "tracking_number": "LXAB00000000NL",
        "shipment_identifier": "LXAB00000000NL",
        "label_type": "PDF",
        "docs": {
            "label": "JVBERi0xLjQKJeLjz9MKMyAwIG9iago=",
        },
        "meta": {
            "service": "PPTT",
            "carrier": "PostNL",
            "shipper_reference": "ORDER-12345",
            "carrier_tracking_number": "3STEST1234567890",
            "carrier_tracking_url": "https://tracking.postnl.nl/track/3STEST1234567890",
            "display_id": "LXAB00000000NL",
            "label_type": "PDF",
        },
    },
    [],
]

ParsedShipmentCancelResponse = [
    {
        "carrier_id": "spring",
        "carrier_name": "spring",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "spring",
            "carrier_name": "spring",
            "code": "10",
            "message": "Invalid API key provided",
            "details": {},
        }
    ],
]
