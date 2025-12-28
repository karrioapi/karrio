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

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        self.assertEqual(lib.to_dict(request.serialize()), ShipmentRequest)

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
                self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


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

ShipmentRequest = {
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
        "addressAddition": "Test Company"
    },
    "parcel": {
        "parcelHeight": 200,
        "parcelWidth": 300,
        "parcelDepth": 400,
        "parcelWeight": 5000,
        "productType": "PARCEL"
    }
}

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
        "label_type": "application/pdf",
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
