"""MyDHL carrier document upload tests."""

import unittest
from unittest.mock import patch
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models
from .fixture import gateway


class TestMyDHLDocument(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.DocumentUploadRequest = models.DocumentUploadRequest(
            **DocumentUploadPayload
        )

    def test_create_document_request(self):
        request = gateway.mapper.create_document_upload_request(
            self.DocumentUploadRequest
        )

        self.assertEqual(request.serialize(), DocumentUploadRequest)

    def test_upload_document(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Document.upload(self.DocumentUploadRequest).from_(gateway)

            url = mock.call_args[1]["url"]
            self.assertEqual(
                url,
                f"{gateway.settings.server_url}/shipments/1234567890/upload-image",
            )

    def test_document_response_parsing(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = DocumentUploadResponse
            parsed_response = (
                karrio.Document.upload(self.DocumentUploadRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedDocumentUploadResponse
            )

    def test_document_error_response_parsing(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = DocumentUploadErrorResponse
            parsed_response = (
                karrio.Document.upload(self.DocumentUploadRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedDocumentUploadErrorResponse
            )


if __name__ == "__main__":
    unittest.main()


DocumentUploadPayload = {
    "tracking_number": "1234567890",
    "shipment_date": "2024-01-15",
    "document_files": [
        {
            "doc_format": "pdf",
            "doc_name": "invoice.pdf",
            "doc_type": "commercial_invoice",
            "doc_file": "JVBERi0xLjQK",
        }
    ],
    "options": {
        "mydhl_product_code": "P",
    },
}

DocumentUploadRequest = {
    "originalPlannedShippingDate": "2024-01-15",
    "accounts": [{"typeCode": "shipper", "number": "123456789"}],
    "productCode": "P",
    "documentImages": [
        {
            "typeCode": "CIN",
            "imageFormat": "PDF",
            "content": "JVBERi0xLjQK",
        }
    ],
    "shipmentTrackingNumber": "1234567890",
}

DocumentUploadResponse = "{}"

DocumentUploadErrorResponse = """{
  "status": 400,
  "title": "Bad Request",
  "detail": "7096: The provided Shipment Identification Number is invalid. Please check the request message and retry.",
  "instance": "/expressapi/shipments/1234567890/upload-image"
}"""

ParsedDocumentUploadResponse = [
    {
        "carrier_id": "mydhl",
        "carrier_name": "mydhl",
        "documents": [
            {
                "doc_id": "1234567890",
                "file_name": "invoice.pdf",
            }
        ],
        "meta": {"tracking_number": "1234567890"},
    },
    [],
]

ParsedDocumentUploadErrorResponse = [
    None,
    [
        {
            "carrier_id": "mydhl",
            "carrier_name": "mydhl",
            "code": "400",
            "message": "7096: The provided Shipment Identification Number is invalid. Please check the request message and retry.",
            "details": {
                "instance": "/expressapi/shipments/1234567890/upload-image",
                "title": "Bad Request",
            },
        }
    ],
]
