"""Comprehensive karrio.core.models Reference

This file documents ALL request and response models used in Karrio integrations.
Import as: `import karrio.core.models as models`
"""

import karrio.core.models as models

# =============================================================================
# REQUEST MODELS (Inputs to your provider functions)
# =============================================================================

# --- Rate Request ---
# Used in: rate_request(payload: models.RateRequest, settings)
"""
models.RateRequest:
    shipper: models.Address (REQUIRED)
    recipient: models.Address (REQUIRED)
    parcels: List[models.Parcel] (REQUIRED)
    services: List[str] = []          # Requested service codes
    options: Dict = {}                # Shipping options
    payment: models.Payment = None
    customs: models.Customs = None
    return_address: models.Address = None
    billing_address: models.Address = None
    reference: str = ""
"""

# --- Shipment Request ---
# Used in: shipment_request(payload: models.ShipmentRequest, settings)
"""
models.ShipmentRequest:
    service: str (REQUIRED)            # Selected service code
    shipper: models.Address (REQUIRED)
    recipient: models.Address (REQUIRED)
    parcels: List[models.Parcel] (REQUIRED)
    payment: models.Payment = None
    customs: models.Customs = None
    return_address: models.Address = None
    billing_address: models.Address = None
    options: Dict = {}
    reference: str = ""
    label_type: str = None            # PDF, ZPL, PNG
    metadata: Dict = {}
"""

# --- Shipment Cancel Request ---
# Used in: shipment_cancel_request(payload: models.ShipmentCancelRequest, settings)
"""
models.ShipmentCancelRequest:
    shipment_identifier: str (REQUIRED)  # Carrier's shipment ID
    service: str = None
    options: Dict = {}
"""

# --- Tracking Request ---
# Used in: tracking_request(payload: models.TrackingRequest, settings)
"""
models.TrackingRequest:
    tracking_numbers: List[str] (REQUIRED)
    account_number: str = None
    reference: str = None
    options: Dict = {}
"""

# --- Pickup Request ---
# Used in: pickup_request(payload: models.PickupRequest, settings)
"""
models.PickupRequest:
    pickup_date: str (REQUIRED)        # YYYY-MM-DD
    ready_time: str (REQUIRED)         # HH:MM
    closing_time: str (REQUIRED)       # HH:MM
    address: models.Address (REQUIRED)
    parcels: List[models.Parcel] = []
    shipment_identifiers: List[str] = []
    package_location: str = None
    instruction: str = None
    options: Dict = {}
    metadata: Dict = {}
"""

# --- Pickup Update Request ---
# Used in: pickup_update_request(payload: models.PickupUpdateRequest, settings)
"""
models.PickupUpdateRequest:
    confirmation_number: str (REQUIRED)
    pickup_date: str (REQUIRED)
    ready_time: str (REQUIRED)
    closing_time: str (REQUIRED)
    address: models.Address (REQUIRED)
    parcels: List[models.Parcel] = []
    shipment_identifiers: List[str] = []
    package_location: str = None
    instruction: str = None
    options: Dict = {}
"""

# --- Pickup Cancel Request ---
# Used in: pickup_cancel_request(payload: models.PickupCancelRequest, settings)
"""
models.PickupCancelRequest:
    confirmation_number: str (REQUIRED)
    address: models.Address = None
    pickup_date: str = None
    reason: str = None
    options: Dict = {}
"""

# --- Address Validation Request ---
# Used in: address_validation_request(payload: models.AddressValidationRequest, settings)
"""
models.AddressValidationRequest:
    address: models.Address (REQUIRED)
    options: Dict = {}
"""

# --- Manifest Request ---
# Used in: manifest_request(payload: models.ManifestRequest, settings)
"""
models.ManifestRequest:
    shipment_identifiers: List[str] (REQUIRED)  # List of shipment IDs to manifest
    address: models.Address (REQUIRED)          # Pickup/origin address
    reference: str = None
    metadata: Dict = {}
    options: Dict = {}
"""

# --- Document Upload Request ---
# Used in: document_upload_request(payload: models.DocumentUploadRequest, settings)
"""
models.DocumentUploadRequest:
    document_files: List[models.DocumentFile] (REQUIRED)
    tracking_number: str = None        # Associated tracking number
    shipment_date: str = None
    reference: str = None
    options: Dict = {}

models.DocumentFile:
    doc_file: str (REQUIRED)           # Base64 encoded content
    doc_name: str (REQUIRED)           # File name
    doc_type: str = None               # Document type
    doc_format: str = None             # File format (PDF, PNG, etc.)
"""

# --- Duties Calculation Request ---
# Used in: duties_calculation_request(payload: models.DutiesCalculationRequest, settings)
"""
models.DutiesCalculationRequest:
    shipment_identifier: str (REQUIRED)
    shipper: models.Address (REQUIRED)
    recipient: models.Address (REQUIRED)
    customs: models.Customs (REQUIRED)
    shipping_charge: models.ChargeDetails = None
    insurance_charge: models.ChargeDetails = None
    reference: str = None
    metadata: Dict = {}
    options: Dict = {}
"""

# --- Insurance Request ---
# Used in: insurance_request(payload: models.InsuranceRequest, settings)
"""
models.InsuranceRequest:
    shipment_identifier: str (REQUIRED)
    amount: float (REQUIRED)           # Coverage amount
    currency: str (REQUIRED)
    shipper: models.Address (REQUIRED)
    recipient: models.Address (REQUIRED)
    parcel: models.Parcel (REQUIRED)
    provider: str = None               # Insurance provider name
    reference: str = None
    metadata: Dict = {}
    options: Dict = {}
"""

# --- Webhook Registration Request ---
# Used in: webhook_registration_request(payload: models.WebhookRegistrationRequest, settings)
"""
models.WebhookRegistrationRequest:
    url: str (REQUIRED)                # Webhook endpoint URL
    description: str = None
    enabled_events: List[str] = []     # Events to subscribe to
    options: Dict = {}
    metadata: Dict = {}
"""

# --- Webhook Deregistration Request ---
# Used in: webhook_deregistration_request(payload: models.WebhookDeregistrationRequest, settings)
"""
models.WebhookDeregistrationRequest:
    webhook_id: str (REQUIRED)
    options: Dict = {}
"""


# =============================================================================
# SUPPORTING DATA TYPES
# =============================================================================

"""
models.Address:
    id: str = None
    postal_code: str = None
    city: str = None
    person_name: str = None
    company_name: str = None
    country_code: str = None
    email: str = None
    phone_number: str = None
    state_code: str = None
    residential: bool = False
    address_line1: str = ""
    address_line2: str = None
    street_number: str = None
    suite: str = None
    federal_tax_id: str = None
    state_tax_id: str = None
"""

"""
models.Parcel:
    id: str = None
    weight: float = None
    width: float = None
    height: float = None
    length: float = None
    weight_unit: str = None            # KG, LB, OZ, G
    dimension_unit: str = None         # CM, IN
    packaging_type: str = None
    package_preset: str = None
    is_document: bool = False
    description: str = None
    content: str = None
    items: List[models.Commodity] = []
    reference_number: str = None
    freight_class: str = None
    options: Dict = {}
"""

"""
models.Commodity:
    id: str = None
    sku: str = None
    title: str = None
    quantity: int = 1
    hs_code: str = None
    weight: float = None
    weight_unit: str = None
    description: str = None
    value_amount: float = None
    value_currency: str = None
    origin_country: str = None
    category: str = None
    product_url: str = None
    image_url: str = None
    metadata: Dict = {}
"""

"""
models.Customs:
    commodities: List[models.Commodity] (REQUIRED)
    certify: bool = None
    signer: str = None
    content_type: str = None           # DOCUMENTS, GIFT, SAMPLE, MERCHANDISE, etc.
    content_description: str = None
    incoterm: str = None               # DDP, DDU, DAP, etc.
    invoice: str = None
    invoice_date: str = None
    duty: models.Duty = None
    duty_billing_address: models.Address = None
    commercial_invoice: bool = False
    options: Dict = {}
"""

"""
models.Payment:
    paid_by: str = "sender"            # sender, recipient, third_party
    currency: str = None
    account_number: str = None
"""

"""
models.Duty:
    paid_by: str = "sender"
    currency: str = None
    account_number: str = None
    declared_value: float = None
"""


# =============================================================================
# RESPONSE MODELS (Outputs from your parse functions)
# =============================================================================

# --- Rate Details ---
# Returned from: parse_rate_response() -> Tuple[List[RateDetails], List[Message]]
"""
models.RateDetails(
    carrier_name="carrier",            # REQUIRED: Use settings.carrier_name
    carrier_id="carrier",              # REQUIRED: Use settings.carrier_id
    service="express",                 # REQUIRED: Service code
    currency="USD",
    total_charge=25.99,
    extra_charges=[                    # Itemized charges
        models.ChargeDetails(
            name="Fuel Surcharge",
            amount=3.50,
            currency="USD",
        ),
    ],
    estimated_delivery="2024-01-20",
    transit_days=2,
    meta=dict(
        service_name="Express Service",
        quote_id="abc123",
    ),
)
"""

# --- Tracking Details ---
# Returned from: parse_tracking_response() -> Tuple[List[TrackingDetails], List[Message]]
"""
models.TrackingDetails(
    carrier_name="carrier",            # REQUIRED
    carrier_id="carrier",              # REQUIRED
    tracking_number="1Z999AA...",      # REQUIRED
    events=[                           # REQUIRED: List of events
        models.TrackingEvent(
            date="2024-01-15",         # REQUIRED: YYYY-MM-DD
            description="Delivered",   # REQUIRED
            code="DL",                 # Carrier event code
            time="14:30",              # HH:MM
            timestamp="2024-01-15T14:30:00.000Z",  # ISO 8601
            status="delivered",        # Normalized status
            location="New York, NY",
            latitude=40.7128,
            longitude=-74.0060,
        ),
    ],
    estimated_delivery="2024-01-20",
    delivered=True,
    status="delivered",                # Normalized status string
    info=models.TrackingInfo(
        carrier_tracking_link="https://...",
        signed_by="John Doe",
        shipping_date="2024-01-10",
        expected_delivery="2024-01-15",
    ),
    images=models.Images(
        delivery_image="base64...",
        signature_image="base64...",
    ),
    meta=dict(
        carrier_status="DELIVERED",
    ),
)
"""

# --- Shipment Details ---
# Returned from: parse_shipment_response() -> Tuple[ShipmentDetails, List[Message]]
"""
models.ShipmentDetails(
    carrier_name="carrier",            # REQUIRED
    carrier_id="carrier",              # REQUIRED
    tracking_number="1Z999AA...",      # REQUIRED
    shipment_identifier="SHIP123",     # REQUIRED: Carrier's internal ID
    docs=models.Documents(             # REQUIRED
        label="base64...",             # Base64 encoded label
        invoice="base64...",           # Base64 encoded invoice
        zpl_label="^XA...",            # ZPL format label
        extra_documents=[
            models.ShippingDocument(
                category="customs",
                format="PDF",
                base64="...",
            ),
        ],
    ),
    selected_rate=models.RateDetails(...),  # If rate returned with shipment
    label_type="PDF",
    meta=dict(
        carrier_tracking_link="https://...",
        service_name="Express",
    ),
)
"""

# --- Pickup Details ---
# Returned from: parse_pickup_response() -> Tuple[PickupDetails, List[Message]]
"""
models.PickupDetails(
    carrier_name="carrier",            # REQUIRED
    carrier_id="carrier",              # REQUIRED
    confirmation_number="PU123456",    # REQUIRED
    pickup_date="2024-01-20",
    pickup_charge=models.ChargeDetails(
        name="Pickup Fee",
        amount=5.00,
        currency="USD",
    ),
    ready_time="09:00",
    closing_time="17:00",
    meta=dict(
        location_id="LOC123",
    ),
)
"""

# --- Confirmation Details ---
# Returned from: cancel operations -> Tuple[ConfirmationDetails, List[Message]]
"""
models.ConfirmationDetails(
    carrier_name="carrier",            # REQUIRED
    carrier_id="carrier",              # REQUIRED
    success=True,                      # REQUIRED
    operation="Cancel Shipment",       # REQUIRED: Operation name
)
"""

# --- Address Validation Details ---
# Returned from: parse_address_validation_response() -> Tuple[List[AddressValidationDetails], List[Message]]
"""
models.AddressValidationDetails(
    carrier_name="carrier",            # REQUIRED
    carrier_id="carrier",              # REQUIRED
    success=True,                      # REQUIRED
    complete_address=models.Address(   # Corrected/validated address
        address_line1="123 MAIN ST",
        city="NEW YORK",
        postal_code="10001",
        country_code="US",
        state_code="NY",
    ),
)
"""

# --- Manifest Details ---
# Returned from: parse_manifest_response() -> Tuple[ManifestDetails, List[Message]]
"""
models.ManifestDetails(
    carrier_name="carrier",            # REQUIRED
    carrier_id="carrier",              # REQUIRED
    doc=models.ManifestDocument(
        manifest="base64...",          # Base64 encoded manifest document
    ),
    meta=dict(
        manifest_id="MAN123",
        shipment_count=5,
    ),
)
"""

# --- Document Upload Details ---
# Returned from: parse_document_upload_response() -> Tuple[DocumentUploadDetails, List[Message]]
"""
models.DocumentUploadDetails(
    carrier_name="carrier",            # REQUIRED
    carrier_id="carrier",              # REQUIRED
    documents=[
        models.DocumentDetails(
            doc_id="DOC123",
            file_name="invoice.pdf",
        ),
    ],
    meta=dict(),
)
"""

# --- Duties Calculation Details ---
# Returned from: parse_duties_calculation_response() -> Tuple[DutiesCalculationDetails, List[Message]]
"""
models.DutiesCalculationDetails(
    carrier_name="carrier",            # REQUIRED
    carrier_id="carrier",              # REQUIRED
    total_charge=150.00,               # REQUIRED
    currency="USD",                    # REQUIRED
    charges=[
        models.ChargeDetails(
            name="Import Duty",
            amount=100.00,
            currency="USD",
        ),
        models.ChargeDetails(
            name="VAT",
            amount=50.00,
            currency="USD",
        ),
    ],
    meta=dict(),
)
"""

# --- Insurance Details ---
# Returned from: parse_insurance_response() -> Tuple[InsuranceDetails, List[Message]]
"""
models.InsuranceDetails(
    carrier_name="carrier",            # REQUIRED
    carrier_id="carrier",              # REQUIRED
    fees=[
        models.ChargeDetails(
            name="Insurance Premium",
            amount=12.50,
            currency="USD",
        ),
    ],
    meta=dict(
        policy_number="POL123456",
        coverage_amount=1000.00,
    ),
)
"""

# --- Webhook Registration Details ---
# Returned from: parse_webhook_registration_response()
"""
models.WebhookRegistrationDetails(
    carrier_name="carrier",            # REQUIRED
    carrier_id="carrier",              # REQUIRED
    secret="webhook_secret_123",       # REQUIRED: For signature validation
    webhook_identifier="WH123",
    meta=dict(
        status="active",
    ),
)
"""

# --- Message (Error/Warning) ---
# Always included in response tuples for errors
"""
models.Message(
    carrier_name="carrier",            # REQUIRED
    carrier_id="carrier",              # REQUIRED
    code="ERROR_CODE",                 # Error/warning code
    message="Error description",       # Human-readable message
    level="error",                     # error, warning, info
    details=dict(                      # Additional context
        field="recipient.postal_code",
    ),
)
"""

# --- Charge Details ---
"""
models.ChargeDetails(
    name="Fuel Surcharge",
    amount=5.00,
    currency="USD",
)
"""


# =============================================================================
# RESPONSE TUPLE PATTERNS
# =============================================================================

# All parse functions return a tuple: (result, messages)

# Rate Response:
# Tuple[List[RateDetails], List[Message]]

# Tracking Response:
# Tuple[List[TrackingDetails], List[Message]]

# Shipment Response:
# Tuple[ShipmentDetails, List[Message]]  # Single shipment, not list

# Cancel Response:
# Tuple[ConfirmationDetails, List[Message]]

# Pickup Response:
# Tuple[PickupDetails, List[Message]]

# Address Validation Response:
# Tuple[List[AddressValidationDetails], List[Message]]

# Manifest Response:
# Tuple[ManifestDetails, List[Message]]

# Document Upload Response:
# Tuple[DocumentUploadDetails, List[Message]]

# Duties Response:
# Tuple[DutiesCalculationDetails, List[Message]]

# Insurance Response:
# Tuple[InsuranceDetails, List[Message]]

# Webhook Response:
# Tuple[WebhookRegistrationDetails, List[Message]]
