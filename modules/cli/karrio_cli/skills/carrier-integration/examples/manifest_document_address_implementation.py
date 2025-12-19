"""Example: Manifest, Document Upload & Address Validation Patterns

This example demonstrates implementation patterns for:
1. Manifest (end-of-day close out)
2. Document Upload (paperless trade)
3. Address Validation
"""

# =============================================================================
# MANIFEST IMPLEMENTATION
# =============================================================================

# === FILE: karrio/providers/[carrier]/manifest.py ===

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.[carrier].error as error
import karrio.providers.[carrier].utils as provider_utils
import karrio.schemas.[carrier].manifest_request as carrier_req
import karrio.schemas.[carrier].manifest_response as carrier_res


def parse_manifest_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ManifestDetails, typing.List[models.Message]]:
    """Parse manifest response."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    manifest = (
        _extract_details(response, settings)
        if not any(messages)
        else None
    )
    
    return manifest, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ManifestDetails:
    """Extract manifest details from carrier response."""
    manifest = lib.to_object(carrier_res.ManifestResponseType, data)
    
    # Get manifest document (base64 encoded PDF typically)
    manifest_doc = lib.identity(
        manifest.manifestData if hasattr(manifest, 'manifestData') else None
    )
    
    # Some carriers return URL instead of data
    if hasattr(manifest, 'manifestUrl') and manifest.manifestUrl and not manifest_doc:
        manifest_doc = lib.request(url=manifest.manifestUrl, decoder=lib.encode_base64)
    
    return models.ManifestDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        doc=models.ManifestDocument(
            manifest=manifest_doc,
        ) if manifest_doc else None,
        meta=dict(
            manifest_id=manifest.manifestId if hasattr(manifest, 'manifestId') else None,
            shipment_count=manifest.shipmentCount if hasattr(manifest, 'shipmentCount') else None,
            status=manifest.status if hasattr(manifest, 'status') else None,
        ),
    )


def manifest_request(
    payload: models.ManifestRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create manifest request."""
    address = lib.to_address(payload.address)
    
    request = carrier_req.ManifestRequestType(
        # Shipments to include in manifest
        shipmentIds=payload.shipment_identifiers,
        # Origin/pickup address
        pickupAddress=carrier_req.AddressType(
            name=address.person_name,
            company=address.company_name,
            addressLine1=address.address_line1,
            city=address.city,
            stateCode=address.state_code,
            postalCode=address.postal_code,
            countryCode=address.country_code,
        ),
        # Manifest date (usually today)
        manifestDate=lib.fdate(payload.options.get("manifest_date")) or lib.fdate(
            str(__import__("datetime").date.today())
        ),
        # Account
        accountNumber=settings.account_number,
        # Reference
        reference=payload.reference,
    )
    
    return lib.Serializable(request, lib.to_dict)


# === Proxy method ===
"""
def create_manifest(self, request: lib.Serializable) -> lib.Deserializable[str]:
    response = lib.request(
        url=f"{self.settings.server_url}/manifests",
        data=lib.to_json(request.serialize()),
        trace=self.trace_as("json"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.settings.api_key}",
        },
    )
    return lib.Deserializable(response, lib.to_dict)
"""


# =============================================================================
# DOCUMENT UPLOAD IMPLEMENTATION
# =============================================================================

# === FILE: karrio/providers/[carrier]/document.py ===

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.[carrier].error as error
import karrio.providers.[carrier].utils as provider_utils
import karrio.providers.[carrier].units as provider_units
import karrio.schemas.[carrier].document_upload_request as carrier_req
import karrio.schemas.[carrier].document_upload_response as carrier_res


def parse_document_upload_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.DocumentUploadDetails, typing.List[models.Message]]:
    """Parse document upload response."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    details = (
        _extract_details(response, settings)
        if not any(messages)
        else None
    )
    
    return details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.DocumentUploadDetails:
    """Extract document upload details."""
    result = lib.to_object(carrier_res.DocumentUploadResponseType, data)
    
    # Extract uploaded document references
    documents = [
        models.DocumentDetails(
            doc_id=doc.documentId if hasattr(doc, 'documentId') else doc.id,
            file_name=doc.fileName if hasattr(doc, 'fileName') else doc.name,
        )
        for doc in (result.documents or [])
    ] if hasattr(result, 'documents') else []
    
    return models.DocumentUploadDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        documents=documents,
        meta=dict(
            shipment_id=result.shipmentId if hasattr(result, 'shipmentId') else None,
        ),
    )


def document_upload_request(
    payload: models.DocumentUploadRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create document upload request."""
    # Convert document files to processed format
    document_files = lib.to_document_files(payload.document_files)
    
    # Get upload options
    options = lib.to_upload_options(
        payload.options,
        option_type=provider_units.UploadOption if hasattr(provider_units, 'UploadOption') else None,
    )
    
    request = carrier_req.DocumentUploadRequestType(
        # Associated shipment/tracking
        trackingNumber=payload.tracking_number,
        shipmentDate=lib.fdate(payload.shipment_date) if payload.shipment_date else None,
        # Documents to upload
        documents=[
            carrier_req.DocumentType(
                fileName=doc.doc_name,
                fileContent=doc.doc_file,  # Base64 encoded
                documentType=doc.doc_type or "OTHER",
                fileFormat=doc.doc_format or "PDF",
            )
            for doc in document_files
        ],
        # Reference
        reference=payload.reference,
    )
    
    return lib.Serializable(request, lib.to_dict)


# === Proxy method ===
"""
def upload_document(self, request: lib.Serializable) -> lib.Deserializable[str]:
    response = lib.request(
        url=f"{self.settings.server_url}/documents",
        data=lib.to_json(request.serialize()),
        trace=self.trace_as("json"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.settings.api_key}",
        },
    )
    return lib.Deserializable(response, lib.to_dict)
"""


# =============================================================================
# ADDRESS VALIDATION IMPLEMENTATION
# =============================================================================

# === FILE: karrio/providers/[carrier]/address.py ===

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.[carrier].error as error
import karrio.providers.[carrier].utils as provider_utils
import karrio.schemas.[carrier].address_validation_request as carrier_req
import karrio.schemas.[carrier].address_validation_response as carrier_res


def parse_address_validation_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.AddressValidationDetails], typing.List[models.Message]]:
    """Parse address validation response."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    # Some carriers return multiple address suggestions
    validations = _extract_details(response, settings) if not any(messages) else []
    
    return validations, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> typing.List[models.AddressValidationDetails]:
    """Extract address validation details."""
    result = lib.to_object(carrier_res.AddressValidationResponseType, data)
    
    # Check if validation was successful
    is_valid = result.valid if hasattr(result, 'valid') else False
    
    # Get corrected/suggested addresses
    addresses = result.suggestedAddresses if hasattr(result, 'suggestedAddresses') else []
    if not addresses and hasattr(result, 'correctedAddress'):
        addresses = [result.correctedAddress]
    
    if not addresses:
        # No suggestions, return validation status only
        return [
            models.AddressValidationDetails(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                success=is_valid,
                complete_address=None,
            )
        ]
    
    # Return all suggested addresses
    return [
        models.AddressValidationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=is_valid,
            complete_address=models.Address(
                address_line1=addr.addressLine1 if hasattr(addr, 'addressLine1') else addr.line1,
                address_line2=addr.addressLine2 if hasattr(addr, 'addressLine2') else None,
                city=addr.city,
                state_code=addr.stateCode if hasattr(addr, 'stateCode') else addr.state,
                postal_code=addr.postalCode if hasattr(addr, 'postalCode') else addr.zip,
                country_code=addr.countryCode if hasattr(addr, 'countryCode') else addr.country,
            ),
        )
        for addr in addresses
    ]


def address_validation_request(
    payload: models.AddressValidationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create address validation request."""
    address = lib.to_address(payload.address)
    
    request = carrier_req.AddressValidationRequestType(
        address=carrier_req.AddressType(
            addressLine1=address.address_line1,
            addressLine2=address.address_line2,
            city=address.city,
            stateCode=address.state_code,
            postalCode=address.postal_code,
            countryCode=address.country_code,
            # Some carriers need residential indicator
            residential=address.residential,
        ),
    )
    
    return lib.Serializable(request, lib.to_dict)


# === Proxy method ===
"""
def validate_address(self, request: lib.Serializable) -> lib.Deserializable[str]:
    response = lib.request(
        url=f"{self.settings.server_url}/address/validate",
        data=lib.to_json(request.serialize()),
        trace=self.trace_as("json"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.settings.api_key}",
        },
    )
    return lib.Deserializable(response, lib.to_dict)
"""


# =============================================================================
# TEST PATTERNS
# =============================================================================

"""
# === Manifest Test ===
class TestCarrierManifest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ManifestRequest = models.ManifestRequest(**ManifestPayload)

    def test_create_manifest_request(self):
        request = gateway.mapper.create_manifest_request(self.ManifestRequest)
        print(f"Generated request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), ManifestRequest)

    def test_create_manifest(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Manifest.create(self.ManifestRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/manifests"
            )

    def test_parse_manifest_response(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = ManifestResponse
            parsed_response = (
                karrio.Manifest.create(self.ManifestRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Parsed response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedManifestResponse)

ManifestPayload = {
    "shipment_identifiers": ["SHIP123", "SHIP456"],
    "address": {
        "company_name": "Test Company",
        "address_line1": "123 Main St",
        "city": "New York",
        "postal_code": "10001",
        "country_code": "US",
        "state_code": "NY",
    },
}


# === Document Upload Test ===
class TestCarrierDocument(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.DocumentUploadRequest = models.DocumentUploadRequest(**DocumentPayload)

    def test_create_document_upload_request(self):
        request = gateway.mapper.create_document_upload_request(self.DocumentUploadRequest)
        print(f"Generated request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), DocumentUploadRequest)

DocumentPayload = {
    "tracking_number": "1Z999AA10123456784",
    "document_files": [
        {
            "doc_file": "JVBERi0xLjQK...",  # Base64 PDF
            "doc_name": "commercial_invoice.pdf",
            "doc_type": "commercial_invoice",
            "doc_format": "PDF",
        }
    ],
}


# === Address Validation Test ===
class TestCarrierAddress(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.AddressValidationRequest = models.AddressValidationRequest(**AddressPayload)

    def test_create_address_validation_request(self):
        request = gateway.mapper.create_address_validation_request(self.AddressValidationRequest)
        print(f"Generated request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), AddressValidationRequest)

AddressPayload = {
    "address": {
        "address_line1": "123 Main Street",
        "city": "New York",
        "postal_code": "10001",
        "country_code": "US",
        "state_code": "NY",
    },
}
"""
