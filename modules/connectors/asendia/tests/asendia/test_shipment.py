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
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **ShipmentCancelPayload
        )
        self.MultiPieceShipmentRequest = models.ShipmentRequest(
            **MultiPieceShipmentPayload
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        # Request is now a list (one per package) for Pattern B
        self.assertEqual(lib.to_dict(request.serialize()), ShipmentRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.asendia.proxy.lib.run_asynchronously") as mock_async:
            with patch(
                "karrio.providers.asendia.utils.Settings.access_token",
                new_callable=lambda: property(lambda self: "test_token"),
            ):
                # Mock both async calls: 1) create parcels, 2) fetch labels
                mock_async.side_effect = [
                    [ShipmentResponse],  # First call: create parcel
                    [
                        {
                            "parcel": lib.to_dict(ShipmentResponse),
                            "label": MockLabelBase64,
                        }
                    ],  # Second call: fetch label
                ]
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway)
                # Verify the async function was called twice (create + fetch labels)
                self.assertEqual(mock_async.call_count, 2)

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.asendia.proxy.lib.run_asynchronously") as mock_async:
            with patch(
                "karrio.providers.asendia.utils.Settings.access_token",
                new_callable=lambda: property(lambda self: "test_token"),
            ):
                # Mock both async calls: 1) create parcels, 2) fetch labels
                mock_async.side_effect = [
                    [ShipmentResponse],  # First call: create parcel
                    [
                        {
                            "parcel": lib.to_dict(ShipmentResponse),
                            "label": MockLabelBase64,
                        }
                    ],  # Second call: fetch label
                ]
                parsed_response = (
                    karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
                )
                self.assertListEqual(
                    lib.to_dict(parsed_response), ParsedShipmentResponse
                )

    def test_create_cancel_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )
        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_cancel_shipment(self):
        with patch("karrio.mappers.asendia.proxy.lib.request") as mock:
            with patch(
                "karrio.providers.asendia.utils.Settings.access_token",
                new_callable=lambda: property(lambda self: "test_token"),
            ):
                mock.return_value = "{}"
                karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)
                self.assertEqual(
                    mock.call_args[1]["url"],
                    f"{gateway.settings.server_url}/api/parcels/3fa85f64-5717-4562-b3fc-2c963f66afa6",
                )

    def test_parse_cancel_response(self):
        with patch("karrio.mappers.asendia.proxy.lib.request") as mock:
            with patch(
                "karrio.providers.asendia.utils.Settings.access_token",
                new_callable=lambda: property(lambda self: "test_token"),
            ):
                mock.return_value = "{}"
                parsed_response = (
                    karrio.Shipment.cancel(self.ShipmentCancelRequest)
                    .from_(gateway)
                    .parse()
                )
                self.assertListEqual(
                    lib.to_dict(parsed_response), ParsedShipmentCancelResponse
                )

    def test_create_multi_piece_shipment_request(self):
        """Test that multi-piece shipments create one request per package."""
        request = gateway.mapper.create_shipment_request(self.MultiPieceShipmentRequest)
        serialized = lib.to_dict(request.serialize())
        # Verify we get a list with 2 requests (one per package)
        self.assertEqual(len(serialized), 2)
        self.assertEqual(serialized, MultiPieceShipmentRequest)

    def test_parse_multi_piece_shipment_response(self):
        """Test that multi-piece responses are aggregated correctly using lib.to_multi_piece_shipment()."""
        with patch("karrio.mappers.asendia.proxy.lib.run_asynchronously") as mock_async:
            with patch(
                "karrio.providers.asendia.utils.Settings.access_token",
                new_callable=lambda: property(lambda self: "test_token"),
            ):
                with patch(
                    "karrio.core.utils.transformer.utils.bundle_base64"
                ) as mock_bundle:
                    # Mock bundle_base64 to return the first label (skip actual PDF merging)
                    mock_bundle.return_value = MockLabelBase64
                    # Mock both async calls: 1) create parcels, 2) fetch labels
                    mock_async.side_effect = [
                        [
                            MultiPieceShipmentResponse1,
                            MultiPieceShipmentResponse2,
                        ],  # First call: create parcels
                        [
                            {
                                "parcel": lib.to_dict(MultiPieceShipmentResponse1),
                                "label": MockLabelBase64,
                            },
                            {
                                "parcel": lib.to_dict(MultiPieceShipmentResponse2),
                                "label": MockLabelBase64,
                            },
                        ],  # Second call: fetch labels
                    ]
                    parsed_response = (
                        karrio.Shipment.create(self.MultiPieceShipmentRequest)
                        .from_(gateway)
                        .parse()
                    )
                    result = lib.to_dict(parsed_response)
                    # Sort the lists in meta for comparison since lib.to_multi_piece_shipment() uses sets
                    result[0]["meta"]["shipment_identifiers"] = sorted(
                        result[0]["meta"]["shipment_identifiers"]
                    )
                    result[0]["meta"]["tracking_numbers"] = sorted(
                        result[0]["meta"]["tracking_numbers"]
                    )
                    self.assertListEqual(result, ParsedMultiPieceShipmentResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.asendia.proxy.lib.run_asynchronously") as mock_async:
            with patch(
                "karrio.providers.asendia.utils.Settings.access_token",
                new_callable=lambda: property(lambda self: "test_token"),
            ):
                # Mock error response from create parcel
                error_dict = lib.to_dict(ErrorResponse)
                mock_async.side_effect = [
                    [ErrorResponse],  # First call: create parcel returns error
                    [
                        {"parcel": error_dict, "label": None}
                    ],  # Second call: return error with no label
                ]
                parsed_response = (
                    karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
                )
                self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


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
        "email": "sender@example.com",
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
        "email": "receiver@example.com",
    },
    "parcels": [
        {
            "weight": 1.5,
            "weight_unit": "KG",
        }
    ],
    "service": "asendia_epaq_standard",
    "reference": "REF-123456",
}

ShipmentCancelPayload = {"shipment_identifier": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}

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

# Mock base64-encoded label (simple PDF header for testing)
MockLabelBase64 = (
    "JVBERi0xLjQKJeLjz9MKMSAwIG9iago8PC9UeXBlL0NhdGFsb2cvUGFnZXMgMiAwIFI+PgplbmRvYmoK"
)

ParsedShipmentResponse = [
    {
        "carrier_id": "asendia",
        "carrier_name": "asendia",
        "docs": {"label": MockLabelBase64},
        "label_type": "PDF",
        "meta": {
            "carrier_tracking_link": "https://tracking.asendia.com/tracking/ASENDIA123456789",
            "customs_document_location": "/parcels/3fa85f64-5717-4562-b3fc-2c963f66afa6/customs-document",
            "label_location": "/parcels/3fa85f64-5717-4562-b3fc-2c963f66afa6/label",
        },
        "shipment_identifier": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "tracking_number": "ASENDIA123456789",
    },
    [],
]

ParsedShipmentCancelResponse = [
    {
        "carrier_id": "asendia",
        "carrier_name": "asendia",
        "success": True,
        "operation": "Cancel Shipment",
    },
    [],
]

# Multi-piece shipment test data
MultiPieceShipmentPayload = {
    "shipper": {
        "address_line1": "Musterstrasse 10",
        "city": "Bern",
        "postal_code": "3030",
        "country_code": "CH",
        "person_name": "John Sender",
        "company_name": "Sender Company",
        "phone_number": "+41791234567",
        "email": "sender@example.com",
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
        "email": "receiver@example.com",
    },
    "parcels": [
        {"weight": 1.5, "weight_unit": "KG"},
        {"weight": 2.0, "weight_unit": "KG"},
    ],
    "service": "asendia_epaq_standard",
    "reference": "REF-MULTI-001",
}

MultiPieceShipmentRequest = [
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
        "asendiaService": {"format": "B", "product": "EPAQSTD"},
        "customerId": "CUST123",
        "labelType": "PDF",
        "referencenumber": "REF-MULTI-001",
        "weight": 1.5,
    },
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
        "asendiaService": {"format": "B", "product": "EPAQSTD"},
        "customerId": "CUST123",
        "labelType": "PDF",
        "referencenumber": "REF-MULTI-001",
        "weight": 2.0,
    },
]

MultiPieceShipmentResponse1 = """{
  "id": "pkg-001-uuid",
  "trackingNumber": "ASENDIA111111111",
  "returnTrackingNumber": null,
  "errorMessages": [],
  "labelLocation": "/parcels/pkg-001-uuid/label",
  "returnLabelLocation": null,
  "customsDocumentLocation": null,
  "manifestLocation": null,
  "commercialInvoiceLocation": null
}"""

MultiPieceShipmentResponse2 = """{
  "id": "pkg-002-uuid",
  "trackingNumber": "ASENDIA222222222",
  "returnTrackingNumber": null,
  "errorMessages": [],
  "labelLocation": "/parcels/pkg-002-uuid/label",
  "returnLabelLocation": null,
  "customsDocumentLocation": null,
  "manifestLocation": null,
  "commercialInvoiceLocation": null
}"""

ParsedMultiPieceShipmentResponse = [
    {
        "carrier_id": "asendia",
        "carrier_name": "asendia",
        "docs": {
            "label": MockLabelBase64
        },  # lib.to_multi_piece_shipment() bundles labels
        "label_type": "PDF",
        "meta": {
            "carrier_tracking_link": "https://tracking.asendia.com/tracking/ASENDIA111111111",
            "label_location": "/parcels/pkg-001-uuid/label",
            # Sorted for comparison since lib.to_multi_piece_shipment() uses sets
            "shipment_identifiers": ["pkg-001-uuid", "pkg-002-uuid"],
            "tracking_numbers": ["ASENDIA111111111", "ASENDIA222222222"],
        },
        "shipment_identifier": "pkg-001-uuid",
        "tracking_number": "ASENDIA111111111",
    },
    [],
]

ErrorResponse = """{
  "type": "https://www.asendia-sync.com/problem/constraint-violation",
  "title": "Bad Request",
  "status": 400,
  "detail": "Validation failed",
  "path": "/api/parcels",
  "message": "error.validation",
  "fieldErrors": [
    {
      "objectName": "parcel",
      "field": "weight",
      "message": "Weight must be greater than 0"
    }
  ]
}"""

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "asendia",
            "carrier_name": "asendia",
            "code": "400",
            "details": {"field": "weight", "objectName": "parcel"},
            "message": "weight: Weight must be greater than 0",
        }
    ],
]
