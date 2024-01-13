import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestFedExTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.DocumentUploadRequest = models.DocumentUploadRequest(
            **DocumentUploadPayload
        )

    def test_create_tracking_request(self):
        request = gateway.mapper.create_document_upload_request(
            self.DocumentUploadRequest
        )

        self.assertEqual(request.serialize(), DocumentUploadRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Document.fetch(self.create_document_upload_request).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_document_upload_response(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = DocumentUploadResponse
            parsed_response = (
                karrio.Document.fetch(self.DocumentUploadRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedDocumentUploadResponse
            )


if __name__ == "__main__":
    unittest.main()


DocumentUploadPayload = {
    "document_files": [
        {
            "doc_format": "txt",
            "doc_name": "file.txt",
            "doc_type": "other",
            "doc_file": "R0lGODdhIAOwBPAAAA==",
        }
    ],
}

ParsedDocumentUploadResponse = [
    {
        "carrier_id": "carrier_id",
        "carrier_name": "carrier_id",
        "documents": [
            {
                "document_id": "090493e181586308",
                "file_name": "file.txt",
            }
        ],
        "meta": {},
    },
    [],
]


DocumentUploadRequest = [
    {
        "document": {
            "workflowName": "ETDPostshipment",
            "carrierCode": "FDXE",
            "name": "file.txt",
            "contentType": "text/plain",
            "meta": {
                "shipDocumentType": "COMMERCIAL_INVOICE",
                "formCode": "USMCA",
                "trackingNumber": "794791292805",
                "shipmentDate": "2021-02-17T00:00:00",
                "originLocationCode": "GVTKK",
                "originCountryCode": "US",
                "destinationLocationCode": "JNUA",
                "destinationCountryCode": "IN",
            },
        },
        "attachment": "file.txt",
    }
]

DocumentUploadResponse = """{
  "output": {
    "meta": {
      "documentType": "CO",
      "docId": "090493e181586308",
      "folderId": [
        "0b0493e1812f8921"
      ]
    }
  },
  "customerTransactionId": "XXXX_XXX123XXXXX"
}
"""
