import unittest
from unittest.mock import patch
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestFedexRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.DocumentUploadRequest = models.DocumentUploadRequest(
            **DocumentUploadPayload
        )

    def test_create_document_upload_request(self):
        request = gateway.mapper.create_document_upload_request(
            self.DocumentUploadRequest
        )

        self.assertEqual(request.serialize(), DocumentUploadRequest)

    def test_upload_document(self):
        with patch("karrio.mappers.fedex_ws.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Document.upload(self.DocumentUploadRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/uploaddocument",
            )

    def test_parse_document_upload_response(self):
        with patch("karrio.mappers.fedex_ws.proxy.lib.request") as mock:
            mock.return_value = DocumentUploadResponse
            parsed_response = (
                karrio.Document.upload(self.DocumentUploadRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedDocumentUploadResponse
            )


if __name__ == "__main__":
    unittest.main()


DocumentUploadPayload = {
    "reference": "By-Vikas",
    "tracking_number": "794604790138",
    "document_files": [
        {
            "doc_format": "txt",
            "doc_name": "vikas_coo.txt",
            "doc_type": "fedex_certificate_of_origin",
            "doc_file": "R0lGODdhIAOwBPAAAA==",
        }
    ],
    "options": {
        "destination_country_code": "US",
        "destination_postal_code": "US",
        "fedex_document_producer": "CUSTOMER",
    },
}

ParsedDocumentUploadResponse = [
    {
        "carrier_id": "carrier_id",
        "carrier_name": "carrier_id",
        "documents": [
            {
                "doc_id": "090493e1815c194e",
                "file_name": "vikas_coo.txt",
            }
        ],
        "meta": {},
    },
    [],
]


DocumentUploadRequest = """<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v19="http://fedex.com/ws/uploaddocument/v19">
    <tns:Body>
        <v19:UploadDocumentsRequest>
            <v19:WebAuthenticationDetail>
                <v19:UserCredential>
                    <v19:Key>user_key</v19:Key>
                    <v19:Password>password</v19:Password>
                </v19:UserCredential>
            </v19:WebAuthenticationDetail>
            <v19:ClientDetail>
                <v19:AccountNumber>2349857</v19:AccountNumber>
                <v19:MeterNumber>1293587</v19:MeterNumber>
            </v19:ClientDetail>
            <v19:TransactionDetail>
                <v19:CustomerTransactionId>Upload Documents</v19:CustomerTransactionId>
            </v19:TransactionDetail>
            <v19:Version>
                <v19:ServiceId>cdus</v19:ServiceId>
                <v19:Major>19</v19:Major>
                <v19:Intermediate>0</v19:Intermediate>
                <v19:Minor>0</v19:Minor>
            </v19:Version>
            <v19:ProcessingOptions>
                <v19:PostShipmentUploadDetail>
                    <v19:TrackingNumber>794604790138</v19:TrackingNumber>
                </v19:PostShipmentUploadDetail>
            </v19:ProcessingOptions>
            <v19:DestinationCountryCode>US</v19:DestinationCountryCode>
            <v19:DestinationPostalCode>US</v19:DestinationPostalCode>
            <v19:Documents>
                <v19:LineNumber>1</v19:LineNumber>
                <v19:CustomerReference>By-Vikas</v19:CustomerReference>
                <v19:DocumentProducer>CUSTOMER</v19:DocumentProducer>
                <v19:DocumentType>CERTIFICATE_OF_ORIGIN</v19:DocumentType>
                <v19:FileName>vikas_coo.txt</v19:FileName>
                <v19:DocumentContent>R0lGODdhIAOwBPAAAA==</v19:DocumentContent>
            </v19:Documents>
        </v19:UploadDocumentsRequest>
    </tns:Body>
</tns:Envelope>
"""

DocumentUploadResponse = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Header />
    <SOAP-ENV:Body>
        <UploadDocumentsReply xmlns="http://fedex.com/ws/uploaddocument/v19">
            <HighestSeverity>SUCCESS</HighestSeverity>
            <Notifications>
                <Severity>SUCCESS</Severity>
                <Source>cdus</Source>
                <Code>0</Code>
                <Message>Success.</Message>
                <LocalizedMessage>Success.</LocalizedMessage>
            </Notifications>
            <TransactionDetail>
                <CustomerTransactionId>Upload Documents</CustomerTransactionId>
            </TransactionDetail>
            <Version>
                <ServiceId>cdus</ServiceId>
                <Major>19</Major>
                <Intermediate>0</Intermediate>
                <Minor>0</Minor>
            </Version>
            <DocumentStatuses>
                <LineNumber>2</LineNumber>
                <CustomerReference>By-Vikas</CustomerReference>
                <DocumentProducer>CUSTOMER</DocumentProducer>
                <DocumentType>CERTIFICATE_OF_ORIGIN</DocumentType>
                <FileName>vikas_coo.txt</FileName>
                <Status>SUCCESS</Status>
                <Message>SUCCESS</Message>
                <DocumentId>090493e1815c194e</DocumentId>
            </DocumentStatuses>
        </UploadDocumentsReply>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""
