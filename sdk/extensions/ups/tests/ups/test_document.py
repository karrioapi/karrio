import unittest
from unittest.mock import patch
import karrio
import karrio.lib as lib
import karrio.core.models as models
from .fixture import gateway


class TestUPSDocument(unittest.TestCase):
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
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Document.upload(self.DocumentUploadRequest).from_(gateway)

            url = mock.call_args[1]["url"]
            self.assertEqual(
                url,
                "https://onlinetools.ups.com/api/paperlessdocuments/v1/upload",
            )

    def test_document_response_parsing(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
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
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
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
    "document_files": [
        {
            "doc_format": "txt",
            "doc_name": "TestFile.txt",
            "doc_type": "ups_declaration",
            "doc_file": "R0lGODdhIAOwBPAAAA==",
        }
    ],
}

ParsedDocumentUploadResponse = [
    {
        "carrier_id": "ups",
        "carrier_name": "ups",
        "documents": [
            {
                "doc_id": "2016-01-18-11.01.07.589501",
                "file_name": "2016-01-18-11.01.07.589501",
            }
        ],
        "meta": {},
    },
    [],
]

ParsedDocumentUploadErrorResponse = [
    None,
    [
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "code": "9590018",
            "message": "Your UPS Account number is not authorized for user generated forms functionality.",
        }
    ],
]


DocumentUploadRequest = {
    "UploadRequest": {
        "Request": {"TransactionReference": "document upload"},
        "ShipperNumber": "Your Account Number",
        "UserCreatedForm": [
            {
                "UserCreatedFormDocumentType": "013",
                "UserCreatedFormFile": "R0lGODdhIAOwBPAAAA==",
                "UserCreatedFormFileFormat": "txt",
                "UserCreatedFormFileName": "TestFile.txt",
            }
        ],
    }
}


DocumentUploadResponse = """{
  "UploadResponse": {
    "Response": {
      "ResponseStatus": {
        "Code": "1",
        "Description": "Success"
      },
      "TransactionReference": {}
    },
    "FormsHistoryDocumentID": {
      "DocumentID": "2016-01-18-11.01.07.589501"
    }
  }
}
"""

DocumentUploadErrorResponse = """{
  "response": {
    "errors": [
      {
        "code": "9590018",
        "message": "Your UPS Account number is not authorized for user generated forms functionality."
      }
    ]
  }
}
"""
