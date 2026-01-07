"""Asendia carrier shipment tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class TestAsendiaShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(**ShipmentCancelPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        # Request is now a list (one per package) for Pattern B
        self.assertEqual(lib.to_dict(request.serialize()), ShipmentRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.asendia.proxy.lib.run_asynchronously") as mock_async:
            with patch("karrio.providers.asendia.utils.Settings.access_token", new_callable=lambda: property(lambda self: "test_token")):
                mock_async.return_value = [ShipmentResponse]
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway)
                # Verify the async function was called with a list of requests
                self.assertTrue(mock_async.called)

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.asendia.proxy.lib.run_asynchronously") as mock_async:
            with patch("karrio.providers.asendia.utils.Settings.access_token", new_callable=lambda: property(lambda self: "test_token")):
                mock_async.return_value = [ShipmentResponse]
                parsed_response = (
                    karrio.Shipment.create(self.ShipmentRequest)
                    .from_(gateway)
                    .parse()
                )
                self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_create_cancel_request(self):
        request = gateway.mapper.create_cancel_shipment_request(self.ShipmentCancelRequest)
        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_cancel_shipment(self):
        with patch("karrio.mappers.asendia.proxy.lib.request") as mock:
            with patch("karrio.providers.asendia.utils.Settings.access_token", new_callable=lambda: property(lambda self: "test_token")):
                mock.return_value = "{}"
                karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)
                self.assertEqual(
                    mock.call_args[1]["url"],
                    f"{gateway.settings.server_url}/api/parcels/3fa85f64-5717-4562-b3fc-2c963f66afa6"
                )

    def test_parse_cancel_response(self):
        with patch("karrio.mappers.asendia.proxy.lib.request") as mock:
            with patch("karrio.providers.asendia.utils.Settings.access_token", new_callable=lambda: property(lambda self: "test_token")):
                mock.return_value = "{}"
                parsed_response = (
                    karrio.Shipment.cancel(self.ShipmentCancelRequest)
                    .from_(gateway)
                    .parse()
                )
                self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentCancelResponse)


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "shipper": {
        "address_line1": "Musterstrasse 10",
        "city": "Bern",
        "postal_code": "3030",
        "country_code": "CH",
        "person_name": "John Sender",
        "company_name": "Sender Company",
        "phone_number": "+41791234567",
        "email": "sender@example.com"
    },
    "recipient": {
        "address_line1": "123 Main Street",
        "city": "New York",
        "postal_code": "10001",
        "country_code": "US",
        "state_code": "NY",
        "person_name": "Jane Receiver",
        "company_name": "Receiver Inc",
        "phone_number": "+12125551234",
        "email": "receiver@example.com"
    },
    "parcels": [{
        "weight": 1.5,
        "weight_unit": "KG",
    }],
    "service": "asendia_epaq_standard",
    "reference": "REF-123456",
}

ShipmentCancelPayload = {
    "shipment_identifier": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}

# Request is now a list (one per package) for Pattern B: Per-Package Request
ShipmentRequest = [
    {
        "addresses": {
            "receiver": {
                "address1": "123 Main Street",
                "city": "New York",
                "company": "Receiver Inc",
                "country": "US",
                "email": "receiver@example.com",
                "name": "Jane Receiver",
                "phone": "+12125551234",
                "postalCode": "10001",
                "province": "NY",
            },
            "sender": {
                "address1": "Musterstrasse 10",
                "city": "Bern",
                "company": "Sender Company",
                "country": "CH",
                "email": "sender@example.com",
                "name": "John Sender",
                "phone": "+41791234567",
                "postalCode": "3030",
            },
        },
        "asendiaService": {
            "format": "B",
            "product": "EPAQSTD",
        },
        "customerId": "CUST123",
        "labelType": "PDF",
        "referencenumber": "REF-123456",
        "weight": 1.5,
    }
]

ShipmentCancelRequest = "3fa85f64-5717-4562-b3fc-2c963f66afa6"

ShipmentResponse = """{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "trackingNumber": "ASENDIA123456789",
  "returnTrackingNumber": null,
  "errorMessages": [],
  "labelLocation": "/parcels/3fa85f64-5717-4562-b3fc-2c963f66afa6/label",
  "returnLabelLocation": null,
  "customsDocumentLocation": "/parcels/3fa85f64-5717-4562-b3fc-2c963f66afa6/customs-document",
  "manifestLocation": null,
  "commercialInvoiceLocation": null
}"""

ParsedShipmentResponse = [
    {
        "carrier_id": "asendia",
        "carrier_name": "asendia",
        "label_type": "PDF",
        "meta": {
            "customs_document_location": "/parcels/3fa85f64-5717-4562-b3fc-2c963f66afa6/customs-document",
            "label_location": "/parcels/3fa85f64-5717-4562-b3fc-2c963f66afa6/label",
        },
        "shipment_identifier": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "tracking_number": "ASENDIA123456789",
    },
    []
]

ParsedShipmentCancelResponse = [
    {
        "carrier_id": "asendia",
        "carrier_name": "asendia",
        "success": True,
        "operation": "Cancel Shipment"
    },
    []
]
