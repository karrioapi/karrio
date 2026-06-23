"""GLS Customs Document Management (paperless trade) tests."""

import unittest
from unittest.mock import patch

import karrio.core.models as models
import karrio.sdk as karrio

from .fixture import gateway


class TestGLSGroupDocumentUpload(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.DocumentUploadRequest = models.DocumentUploadRequest(**DocumentUploadPayload)

    def test_create_document_upload_request(self):
        request = gateway.mapper.create_document_upload_request(self.DocumentUploadRequest)
        self.assertListEqual(request.serialize(), DocumentUploadRequest)
        # The binary payload rides on ctx for the proxy to PUT to the
        # pre-signed URL returned by prepare-upload.
        self.assertEqual(len(request.ctx["files"]), 2)
        self.assertEqual(request.ctx["files"][0]["doc_file"], "JVBERi0xLjQK")

    def test_upload_document_fires_two_legs_per_file(self):
        """End-to-end: each document is a prepare-upload POST followed by
        a PUT to the returned upload URL. Two files → four wire calls in
        order (prepare, PUT, prepare, PUT)."""
        with patch("karrio.mappers.gls.proxy.lib.request") as mock:
            mock.side_effect = [
                PrepareUploadResponseA,
                "",  # PUT returns empty
                PrepareUploadResponseB,
                "",
            ]
            details, _ = karrio.Document.upload(self.DocumentUploadRequest).from_(gateway).parse()

            self.assertEqual(mock.call_count, 4)
            self.assertEqual(
                mock.call_args_list[0][1]["url"],
                f"{gateway.settings.document_management_url}/documents/customs/prepare-upload",
            )
            self.assertEqual(mock.call_args_list[1][1]["method"], "PUT")
            self.assertEqual(
                mock.call_args_list[1][1]["url"],
                "https://upload.gls/abc",
            )
            self.assertEqual(mock.call_args_list[2][1]["method"], "POST")
            self.assertEqual(
                mock.call_args_list[3][1]["url"],
                "https://upload.gls/def",
            )

            # Parsed result surfaces documentIds for downstream linkedDocuments.
            self.assertListEqual(
                [d.doc_id for d in details.documents],
                ["doc-uuid-A", "doc-uuid-B"],
            )


if __name__ == "__main__":
    unittest.main()


DocumentUploadPayload = {
    "tracking_number": "601079500843",
    "shipment_date": "2026-05-27",
    "document_files": [
        {
            "doc_file": "JVBERi0xLjQK",
            "doc_name": "commercial-invoice.pdf",
            "doc_type": "commercial_invoice",
            "doc_format": "PDF",
        },
        {
            "doc_file": "JVBERi0xLjQK",
            "doc_name": "packing-list.pdf",
            "doc_type": "packing_list",
            "doc_format": "PDF",
        },
    ],
}

DocumentUploadRequest = [
    {
        "attributes": {
            "documentType": "COMMERCIAL_INVOICE",
            "documentFormat": "pdf",
            "displayFileName": "commercial-invoice.pdf",
        }
    },
    {
        "attributes": {
            "documentType": "PACKING_LIST",
            "documentFormat": "pdf",
            "displayFileName": "packing-list.pdf",
        }
    },
]

PrepareUploadResponseA = (
    '{"documentId":"doc-uuid-A","uploadURL":"https://upload.gls/abc","downloadURL":"https://download.gls/abc"}'
)
PrepareUploadResponseB = (
    '{"documentId":"doc-uuid-B","uploadURL":"https://upload.gls/def","downloadURL":"https://download.gls/def"}'
)
