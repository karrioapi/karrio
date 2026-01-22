"""Hermes carrier shipment tests."""

import unittest
from unittest.mock import patch, PropertyMock
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class TestHermesShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.MultiPieceShipmentRequest = models.ShipmentRequest(**MultiPieceShipmentPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        # Request now returns a list (even for single package)
        serialized = request.serialize()
        self.assertEqual(serialized, ShipmentRequest)

    def test_create_multi_piece_shipment_request(self):
        """Test multi-piece shipment request generation."""
        request = gateway.mapper.create_shipment_request(self.MultiPieceShipmentRequest)
        serialized = request.serialize()
        print(f"Multi-piece request: {serialized}")
        # Should be a list of 3 requests
        self.assertEqual(len(serialized), 3)
        # First package should have partNumber=1, no parentShipmentOrderID (omitted when None)
        self.assertEqual(serialized[0]["service"]["multipartService"]["partNumber"], 1)
        self.assertEqual(serialized[0]["service"]["multipartService"]["numberOfParts"], 3)
        # parentShipmentOrderID is not present (lib.to_dict removes None values)
        self.assertNotIn("parentShipmentOrderID", serialized[0]["service"]["multipartService"])
        # Second package should have partNumber=2
        self.assertEqual(serialized[1]["service"]["multipartService"]["partNumber"], 2)
        self.assertEqual(serialized[1]["service"]["multipartService"]["numberOfParts"], 3)
        # Third package should have partNumber=3
        self.assertEqual(serialized[2]["service"]["multipartService"]["partNumber"], 3)
        self.assertEqual(serialized[2]["service"]["multipartService"]["numberOfParts"], 3)

    def test_create_shipment(self):
        with patch("karrio.providers.hermes.utils.Settings.access_token", new_callable=PropertyMock) as mock_token:
            mock_token.return_value = {"access_token": "test_token"}
            with patch("karrio.mappers.hermes.proxy.lib.request") as mock:
                mock.return_value = "{}"
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway)
                self.assertEqual(
                    mock.call_args[1]["url"],
                    f"{gateway.settings.server_url}/shipmentorders/labels"
                )

    def test_parse_shipment_response(self):
        with patch("karrio.providers.hermes.utils.Settings.access_token", new_callable=PropertyMock) as mock_token:
            mock_token.return_value = {"access_token": "test_token"}
            with patch("karrio.mappers.hermes.proxy.lib.request") as mock:
                mock.return_value = ShipmentResponse
                parsed_response = (
                    karrio.Shipment.create(self.ShipmentRequest)
                    .from_(gateway)
                    .parse()
                )
                print(f"Parsed response: {parsed_response}")
                self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_error_response(self):
        with patch("karrio.providers.hermes.utils.Settings.access_token", new_callable=PropertyMock) as mock_token:
            mock_token.return_value = {"access_token": "test_token"}
            with patch("karrio.mappers.hermes.proxy.lib.request") as mock:
                mock.return_value = ErrorResponse
                parsed_response = (
                    karrio.Shipment.create(self.ShipmentRequest)
                    .from_(gateway)
                    .parse()
                )
                print(f"Error response: {parsed_response}")
                self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)

    def test_create_multi_piece_shipment(self):
        """Test multi-piece shipment creation with sequential API calls."""
        with patch("karrio.providers.hermes.utils.Settings.access_token", new_callable=PropertyMock) as mock_token:
            mock_token.return_value = {"access_token": "test_token"}
            with patch("karrio.mappers.hermes.proxy.lib.request") as mock:
                # Return different responses for each package
                mock.side_effect = [
                    MultiPieceShipmentResponse1,
                    MultiPieceShipmentResponse2,
                    MultiPieceShipmentResponse3,
                ]
                parsed_response = (
                    karrio.Shipment.create(self.MultiPieceShipmentRequest)
                    .from_(gateway)
                    .parse()
                )
                print(f"Multi-piece parsed response: {parsed_response}")
                # Should have 3 API calls
                self.assertEqual(mock.call_count, 3)
                # Second and third calls should have parentShipmentOrderID injected
                second_call_data = lib.to_dict(mock.call_args_list[1][1]["data"])
                self.assertEqual(
                    second_call_data["service"]["multipartService"]["parentShipmentOrderID"],
                    "11111111111"
                )
                third_call_data = lib.to_dict(mock.call_args_list[2][1]["data"])
                self.assertEqual(
                    third_call_data["service"]["multipartService"]["parentShipmentOrderID"],
                    "11111111111"
                )
                # Check the response structure (not exact label value due to bundling)
                shipment, messages = parsed_response
                self.assertIsNotNone(shipment)
                self.assertEqual(shipment.tracking_number, "H1111111111111111111")
                self.assertEqual(shipment.shipment_identifier, "11111111111")
                # Check meta contains all tracking numbers (order may vary due to lib.to_multi_piece_shipment)
                tracking_numbers = set(shipment.meta.get("tracking_numbers", []))
                self.assertEqual(
                    tracking_numbers,
                    {"H1111111111111111111", "H2222222222222222222", "H3333333333333333333"}
                )
                self.assertEqual(messages, [])


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "shipper": {
        "address_line1": "Essener Bogen 1",
        "city": "Hamburg",
        "postal_code": "22419",
        "country_code": "DE",
        "person_name": "Max Mustermann",
        "company_name": "Test Company",
        "phone_number": "+49401234567",
        "email": "sender@example.com"
    },
    "recipient": {
        "address_line1": "Essener Bogen 1",
        "city": "Hamburg",
        "postal_code": "22419",
        "country_code": "DE",
        "person_name": "Max Mustermann",
        "phone_number": "+49401234567",
        "email": "receiver@example.com"
    },
    "parcels": [{
        "weight": 5.0,
        "width": 30.0,
        "height": 20.0,
        "length": 40.0,
        "weight_unit": "KG",
        "dimension_unit": "CM",
    }],
    "service": "hermes_standard",
    "reference": "ORDER-12345"
}

MultiPieceShipmentPayload = {
    "shipper": {
        "address_line1": "Essener Bogen 1",
        "city": "Hamburg",
        "postal_code": "22419",
        "country_code": "DE",
        "person_name": "Max Mustermann",
        "company_name": "Test Company",
        "phone_number": "+49401234567",
        "email": "sender@example.com"
    },
    "recipient": {
        "address_line1": "Essener Bogen 1",
        "city": "Hamburg",
        "postal_code": "22419",
        "country_code": "DE",
        "person_name": "Max Mustermann",
        "phone_number": "+49401234567",
        "email": "receiver@example.com"
    },
    "parcels": [
        {
            "weight": 5.0,
            "width": 30.0,
            "height": 20.0,
            "length": 40.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        },
        {
            "weight": 3.0,
            "width": 25.0,
            "height": 15.0,
            "length": 35.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        },
        {
            "weight": 2.0,
            "width": 20.0,
            "height": 10.0,
            "length": 30.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        },
    ],
    "service": "hermes_standard",
    "reference": "ORDER-MULTI"
}

# Single package request - now returns a list with one item
ShipmentRequest = [{
    "clientReference": "ORDER-12345",
    "receiverName": {
        "firstname": "Max",
        "lastname": "Mustermann"
    },
    "receiverAddress": {
        "street": "Essener Bogen",
        "houseNumber": "1",
        "zipCode": "22419",
        "town": "Hamburg",
        "countryCode": "DE"
    },
    "receiverContact": {
        "phone": "+49401234567",
        "mail": "receiver@example.com"
    },
    "senderName": {
        "firstname": "Max",
        "lastname": "Mustermann"
    },
    "senderAddress": {
        "street": "Essener Bogen",
        "houseNumber": "1",
        "zipCode": "22419",
        "town": "Hamburg",
        "countryCode": "DE",
        "addressAddition3": "Test Company"
    },
    "parcel": {
        "parcelHeight": 200,
        "parcelWidth": 300,
        "parcelDepth": 400,
        "parcelWeight": 5000,
        "productType": "PARCEL"
    }
}]

ShipmentResponse = """{
    "listOfResultCodes": [],
    "shipmentID": "H1234567890123456789",
    "shipmentOrderID": "12345678901",
    "labelImage": "JVBERi0xLjQKMSAwIG9iago8PAovVHlwZS...",
    "commInvoiceImage": null,
    "labelMediatype": "application/pdf"
}"""

ErrorResponse = """{
    "listOfResultCodes": [
        {
            "code": "e010",
            "message": "Error while creating shipment order – Parcel class does not match the dimensions."
        }
    ]
}"""

ParsedShipmentResponse = [
    {
        "carrier_id": "hermes",
        "carrier_name": "hermes",
        "tracking_number": "H1234567890123456789",
        "shipment_identifier": "12345678901",
        "label_type": "PDF",
        "docs": {
            "label": "JVBERi0xLjQKMSAwIG9iago8PAovVHlwZS..."
        },
        "meta": {
            "shipment_id": "H1234567890123456789",
            "shipment_order_id": "12345678901"
        }
    },
    []
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "hermes",
            "carrier_name": "hermes",
            "code": "e010",
            "message": "Error while creating shipment order – Parcel class does not match the dimensions.",
            "details": {}
        }
    ]
]

# Multi-piece shipment responses (one per package)
# Using a valid minimal 1x1 red PNG as base64 for testing
# This is a real PNG image that bundle_base64 can process
VALID_PNG_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="

MultiPieceShipmentResponse1 = f"""{{
    "listOfResultCodes": [],
    "shipmentID": "H1111111111111111111",
    "shipmentOrderID": "11111111111",
    "labelImage": "{VALID_PNG_BASE64}",
    "commInvoiceImage": null,
    "labelMediatype": "image/png"
}}"""

MultiPieceShipmentResponse2 = f"""{{
    "listOfResultCodes": [],
    "shipmentID": "H2222222222222222222",
    "shipmentOrderID": "22222222222",
    "labelImage": "{VALID_PNG_BASE64}",
    "commInvoiceImage": null,
    "labelMediatype": "image/png"
}}"""

MultiPieceShipmentResponse3 = f"""{{
    "listOfResultCodes": [],
    "shipmentID": "H3333333333333333333",
    "shipmentOrderID": "33333333333",
    "labelImage": "{VALID_PNG_BASE64}",
    "commInvoiceImage": null,
    "labelMediatype": "image/png"
}}"""

# Expected parsed response for multi-piece shipment (aggregated)
# Note: The bundled label is created by lib.to_multi_piece_shipment using bundle_base64
# which concatenates the PDF labels. We just check the structure here.
ParsedMultiPieceShipmentResponse = [
    {
        "carrier_id": "hermes",
        "carrier_name": "hermes",
        "tracking_number": "H1111111111111111111",
        "shipment_identifier": "11111111111",
        "label_type": "PNG",
        "docs": {
            # The bundled label value will be dynamically generated
            "label": None  # Will be checked separately
        },
        "meta": {
            "shipment_ids": [
                "H1111111111111111111",
                "H2222222222222222222",
                "H3333333333333333333"
            ],
            "tracking_numbers": [
                "H1111111111111111111",
                "H2222222222222222222",
                "H3333333333333333333"
            ]
        }
    },
    []
]
