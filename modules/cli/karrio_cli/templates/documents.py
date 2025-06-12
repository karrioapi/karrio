from jinja2 import Template

PROVIDER_DOCUMENT_UPLOAD_TEMPLATE = Template(
    '''"""Karrio {{name}} document upload API implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract document details from the response

import typing
import base64
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils
import karrio.providers.{{id}}.units as provider_units


def parse_document_upload_response(
    _response: lib.Deserializable[{% if is_xml_api %}lib.Element{% else %}dict{% endif %}],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.DocumentUploadDetails, typing.List[models.Message]]:
    """
    Parse document upload response from carrier API

    _response: The carrier response to deserialize
    settings: The carrier connection settings

    Returns a tuple with (DocumentUploadDetails, List[Message])
    """
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    details = _extract_details(response, settings)

    return details, messages


def _extract_details(
    data: {% if is_xml_api %}lib.Element{% else %}dict{% endif %},
    settings: provider_utils.Settings,
) -> models.DocumentUploadDetails:
    """
    Extract document upload details from carrier response data

    data: The carrier-specific document upload response data
    settings: The carrier connection settings

    Returns a DocumentUploadDetails object with the uploaded document information
    """
    {% if is_xml_api %}
    # Example implementation for XML response:
    # Extract document IDs and file names from the response
    # documents = []
    # doc_elements = lib.find_element("document", data)
    # for doc_element in doc_elements:
    #     doc_id = lib.find_element("id", doc_element, first=True).text
    #     file_name = lib.find_element("file-name", doc_element, first=True).text
    #     documents.append({"document_id": doc_id, "file_name": file_name})

    # For development, return sample data
    documents = [{"document_id": "doc_123456", "file_name": "invoice.pdf"}]
    {% else %}
    # Example implementation for JSON response:
    # documents = []
    # doc_data = data.get("documents", [])
    # for doc in doc_data:
    #     documents.append({
    #         "document_id": doc.get("id"),
    #         "file_name": doc.get("fileName")
    #     })

    # For development, return sample data
    documents = [{"document_id": "doc_123456", "file_name": "invoice.pdf"}]
    {% endif %}

    return models.DocumentUploadDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        documents=[
            models.DocumentDetails(
                document_id=doc["document_id"],
                file_name=doc["file_name"],
            )
            for doc in documents
        ],
        meta=dict(
            # Additional carrier-specific metadata
            upload_timestamp="2023-07-01T12:00:00Z"
        ),
    )


def document_upload_request(
    payload: models.DocumentUploadRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a document upload request for the carrier API

    payload: The standardized DocumentUploadRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    # Extract document files from the payload
    documents = payload.document_files

    {% if is_xml_api %}
    # Example implementation for XML document upload request:
    # import karrio.schemas.{{id}}.document_upload_request as {{id}}_req
    #
    # doc_list = []
    # for doc in documents:
    #     doc_list.append({{id}}_req.Document(
    #         file_name=doc.get("doc_name", ""),
    #         file_format=doc.get("doc_format", "PDF"),
    #         document_type=doc.get("doc_type", "invoice"),
    #         file_content=doc.get("doc_file", "")
    #     ))
    #
    # request = {{id}}_req.DocumentUploadRequest(
    #     account_number=settings.account_number,
    #     documents=doc_list
    # )
    #
    # return lib.Serializable(
    #     request,
    #     lambda _: lib.to_xml(
    #         _,
    #         name_="DocumentUploadRequest",
    #         namespacedef_='xmlns="http://{{id}}.com/schema/document/upload"'
    #     )
    # )

    # For development, return a simple XML request
    document_content = next((doc.get("doc_file", "") for doc in documents), "")
    document_name = next((doc.get("doc_name", "document.pdf") for doc in documents), "")
    document_type = next((doc.get("doc_type", "invoice") for doc in documents), "")
    document_format = next((doc.get("doc_format", "PDF") for doc in documents), "")

    request = f"""<?xml version="1.0"?>
<document-upload-request>
  <account-number>{settings.account_number}</account-number>
  <document>
    <file-name>{document_name}</file-name>
    <file-format>{document_format}</file-format>
    <document-type>{document_type}</document-type>
    <file-content>{document_content}</file-content>
  </document>
</document-upload-request>"""

    return lib.Serializable(request, lambda r: r)
    {% else %}
    # Example implementation for JSON document upload request:
    # import karrio.schemas.{{id}}.document_upload_request as {{id}}_req
    #
    # doc_list = []
    # for doc in documents:
    #     doc_list.append({
    #         "fileName": doc.get("doc_name", ""),
    #         "fileFormat": doc.get("doc_format", "PDF"),
    #         "documentType": doc.get("doc_type", "invoice"),
    #         "fileContent": doc.get("doc_file", "")
    #     })
    #
    # request = {{id}}_req.DocumentUploadRequestType(
    #     accountNumber=settings.account_number,
    #     documents=doc_list
    # )
    #
    # return lib.Serializable(request, lib.to_dict)

    # For development, return a simple JSON request
    doc_list = []
    for doc in documents:
        doc_list.append({
            "fileName": doc.get("doc_name", ""),
            "fileFormat": doc.get("doc_format", "PDF"),
            "documentType": doc.get("doc_type", "invoice"),
            "fileContent": doc.get("doc_file", "")
        })

    request = {
        "accountNumber": settings.account_number,
        "documents": doc_list
    }

    return lib.Serializable(request, lib.to_dict)
    {% endif %}
'''
)

# Provider document upload template
PROVIDER_DOCUMENT_UPLOAD_TEMPLATE = Template(
    '''"""Karrio {{name}} document upload API implementation."""
import attr
from typing import List, Dict, Any, Optional
from base64 import b64encode
from karrio.core.models import (
    Message,
    CheckoutResponse,
    DocumentModels,
)
from karrio.core.errors import UploadDocumentError
from karrio.providers.{{id}}.utils import Settings
from karrio.providers.{{id}}.error import parse_error_response


def upload_document(
    documents: List[DocumentModels.Document],
    settings: Settings,
) -> CheckoutResponse:
    """Upload documents to carrier's API
    Parameters:
        documents: List of document to upload
        settings: carrier connection settings

    Returns:
        upload document checkout response
    """
    response = CheckoutResponse(messages=[], documents=[])

    try:
        # Implement carrier-specific document upload logic here
        # For example:
        # client = create_client(settings)
        # for document in documents:
        #     result = client.upload_document(document)
        #     if result.successful:
        #         response.documents.append(
        #             DocumentModels.Document(
        #                 id=result.id,
        #                 type=document.type,
        #                 name=document.name,
        #             )
        #         )
        #     else:
        #         response.messages.append(Message(code="error", message=result.error))

        # Placeholder implementation
        for document in documents:
            reference_id = f"DOC-{document.name[:8]}-{document.type[:3]}"
            response.documents.append(
                DocumentModels.Document(
                    id=reference_id,
                    type=document.type,
                    name=document.name,
                )
            )
            response.messages.append(
                Message(
                    code="success",
                    message=f"Document {document.name} uploaded successfully",
                    details=f"Document ID: {reference_id}",
                )
            )

    except Exception as e:
        error_response = parse_error_response(response, e)
        response.messages.append(
            Message(
                code="upload_document_error",
                message=str(error_response),
                carrier_name="{{id}}",
                carrier_id="{{id}}",
            )
        )

    return response
'''
)

# Test document upload template
TEST_DOCUMENT_UPLOAD_TEMPLATE = Template(
    '''import unittest
from unittest.mock import patch, ANY
import karrio.core
from karrio.core.models import DocumentModels, CheckoutResponse
from .fixture import gateway
import logging

logger = logging.getLogger(__name__)

class TestDocumentUpload(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.settings = gateway.settings

        # Test document
        self.document = DocumentModels.Document(
            type="COMMERCIAL_INVOICE",
            name="invoice.pdf",
            content="SGVsbG8gV29ybGQh",
            format="PDF",
        )

    def test_document_upload(self):
        with patch('karrio.providers.{{id}}.document.upload_document') as mock:
            mock.return_value = CheckoutResponse(
                messages=[],
                documents=[DocumentModels.Document(
                    id="DOC123456",
                    type="COMMERCIAL_INVOICE",
                    name="invoice.pdf",
                )]
            )

            # Check the function is called with expected parameters
            response = karrio.core.checkout.upload_document(
                documents=[self.document],
                settings=self.settings
            )

            mock.assert_called_once_with([self.document], self.settings)
            self.assertEqual(len(response.documents), 1)
'''
)


XML_SCHEMA_DOCUMENT_UPLOAD_REQUEST_TEMPLATE = Template("""<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/document-upload-request" xmlns="http://{{id}}.com/ws/document-upload-request" elementFormDefault="qualified">
    <xsd:element name="document-upload-request">
        <xsd:complexType>
            <xsd:all>
                <xsd:element name="account-number" type="xsd:string" minOccurs="0" />
                <xsd:element name="documents">
                    <xsd:complexType>
                        <xsd:sequence>
                            <xsd:element name="document" maxOccurs="unbounded">
                                <xsd:complexType>
                                    <xsd:all>
                                        <xsd:element name="document-type" type="xsd:string" />
                                        <xsd:element name="document-name" type="xsd:string" />
                                        <xsd:element name="document-format" type="xsd:string" />
                                        <xsd:element name="document-content" type="xsd:base64Binary" />
                                        <xsd:element name="reference" type="xsd:string" minOccurs="0" />
                                    </xsd:all>
                                </xsd:complexType>
                            </xsd:element>
                        </xsd:sequence>
                    </xsd:complexType>
                </xsd:element>
            </xsd:all>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
"""
)

XML_SCHEMA_DOCUMENT_UPLOAD_RESPONSE_TEMPLATE = Template("""<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/document-upload-response" xmlns="http://{{id}}.com/ws/document-upload-response" elementFormDefault="qualified">
    <xsd:element name="document-upload-response">
        <xsd:complexType>
            <xsd:all>
                <xsd:element name="status" type="xsd:string" />
                <xsd:element name="documents" minOccurs="0">
                    <xsd:complexType>
                        <xsd:sequence>
                            <xsd:element name="document" maxOccurs="unbounded">
                                <xsd:complexType>
                                    <xsd:all>
                                        <xsd:element name="document-id" type="xsd:string" />
                                        <xsd:element name="document-name" type="xsd:string" minOccurs="0" />
                                        <xsd:element name="status" type="xsd:string" minOccurs="0" />
                                        <xsd:element name="reference" type="xsd:string" minOccurs="0" />
                                    </xsd:all>
                                </xsd:complexType>
                            </xsd:element>
                        </xsd:sequence>
                    </xsd:complexType>
                </xsd:element>
            </xsd:all>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
"""
)

# JSON schema templates for document upload operations
JSON_SCHEMA_DOCUMENT_UPLOAD_REQUEST_TEMPLATE = Template(
    """{
  "documentUploadRequest": {
    "accountNumber": "123456",
    "documents": [
      {
        "documentType": "INVOICE",
        "documentName": "invoice.pdf",
        "documentFormat": "PDF",
        "documentContent": "base64_encoded_document_data",
        "reference": "REF123456"
      },
      {
        "documentType": "COMMERCIAL_INVOICE",
        "documentName": "commercial_invoice.pdf",
        "documentFormat": "PDF",
        "documentContent": "base64_encoded_document_data",
        "reference": "REF789012"
      }
    ]
  }
}
"""
)

JSON_SCHEMA_DOCUMENT_UPLOAD_RESPONSE_TEMPLATE = Template(
    """{
  "documentUploadResponse": {
    "status": "completed",
    "documents": [
      {
        "documentId": "DOC123456",
        "documentName": "invoice.pdf",
        "status": "uploaded",
        "reference": "REF123456"
      },
      {
        "documentId": "DOC789012",
        "documentName": "commercial_invoice.pdf",
        "status": "uploaded",
        "reference": "REF789012"
      }
    ]
  }
}
"""
)
