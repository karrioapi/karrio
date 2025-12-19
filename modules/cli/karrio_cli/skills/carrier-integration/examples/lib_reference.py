"""Comprehensive karrio.lib Reference

This file documents ALL utilities available in karrio.lib that MUST be used
instead of reinventing the wheel. Always import as: `import karrio.lib as lib`
"""

import typing
import karrio.lib as lib

# =============================================================================
# DATA PARSING & CONVERSION
# =============================================================================

# --- JSON/Dict Parsing ---

# Parse JSON string or XML to dict
response_dict = lib.to_dict('{"key": "value"}')

# Safe parse - returns {} on error instead of raising
safe_dict = lib.to_dict_safe(response)  # Never raises, returns {} on failure

# Serialize object to JSON string
json_str = lib.to_json({"key": "value"})

# Convert dict to typed object (dataclass instantiation)
# CRITICAL: Use this for all response parsing with generated schema types
typed_obj = lib.to_object(SchemaType, data_dict)


# --- XML Parsing (for XML APIs) ---

# Parse XML string to Element
xml_element = lib.to_element('<root><item>value</item></root>')

# Serialize typed XML object to string
xml_str = lib.to_xml(typed_xml_object)

# Find element in XML tree
found = lib.find_element("tagname", xml_element, ElementType)

# Create SOAP envelope
envelope = lib.create_envelope(
    body_content=body_object,
    header_content=header_object,  # Optional
    envelope_prefix="soap",
)

# Serialize SOAP envelope
soap_xml = lib.envelope_serializer(
    envelope,
    namespace='xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"',
    prefixes={"Request": "ns1"},
)


# =============================================================================
# STRING MANIPULATION
# =============================================================================

# Join strings safely (ignores None values)
result = lib.text("value1", "value2")  # "value1 value2"
result = lib.text("value1", None, "value2")  # "value1 value2"
result = lib.text("long text here", max=10)  # "long text "
result = lib.text("  padded  ", trim=True)  # "padded"
result = lib.text("a", "b", separator=", ")  # "a, b"

# Join to list or string
result = lib.join("a", "b")  # ["a", "b"]
result = lib.join("a", "b", join=True)  # "a b"
result = lib.join("a", "b", join=True, separator="-")  # "a-b"

# Convert to snake_case
slug = lib.to_snake_case("CamelCase")  # "camel_case"
slug = lib.to_slug("MyService Name")  # "my_service_name"


# =============================================================================
# NUMBER FORMATTING
# =============================================================================

# Parse to integer
num = lib.to_int("15.7")  # 15
num = lib.to_int(15.7)  # 15
num = lib.to_int(None)  # None

# Parse to decimal (2 decimal places by default)
dec = lib.to_decimal(14.899)  # 14.90
dec = lib.to_decimal("14.899")  # 14.90

# Format decimal with custom precision
dec = lib.format_decimal(14.899, decimal_places=1)  # 14.9
dec = lib.format_decimal(14.899, decimal_places=3)  # 14.899

# Parse to money (alias for to_decimal, handles edge cases)
money = lib.to_money(25.999)  # 26.00
money = lib.to_money("25.50")  # 25.50
money = lib.to_money(None)  # None

# Ensure value is a list
items = lib.to_list("single")  # ["single"]
items = lib.to_list(["already", "list"])  # ["already", "list"]
items = lib.to_list(None)  # []


# =============================================================================
# DATE & TIME PARSING
# =============================================================================

# Format date string to standard format
date = lib.fdate("2024-01-15")  # "2024-01-15"
date = lib.fdate("01/15/2024", current_format="%m/%d/%Y")  # "2024-01-15"
date = lib.fdate("20240115", try_formats=["%Y%m%d"])  # "2024-01-15"

# Format time string
time = lib.ftime("14:30:00")  # "14:30"
time = lib.ftime("143000", current_format="%H%M%S")  # "14:30"

# Format to local time with AM/PM
time = lib.flocaltime("14:30:00")  # "02:30 PM"

# Format datetime
dt = lib.fdatetime("2024-01-15 14:30:00")  # "2024-01-15 14:30:00"
dt = lib.fdatetime(
    "2024-01-15T14:30:00Z",
    current_format="%Y-%m-%dT%H:%M:%SZ",
    output_format="%Y-%m-%d %H:%M"
)  # "2024-01-15 14:30"

# Parse Unix timestamp
dt = lib.ftimestamp("1705334400")  # "2024-01-15 14:00:00"

# Convert to ISO 8601 timestamp
iso = lib.fiso_timestamp("2024-01-15", "14:30:00")  # "2024-01-15T14:30:00.000Z"

# Parse to datetime object
dt_obj = lib.to_date("2024-01-15")  # datetime.datetime object

# Get next business datetime
next_biz = lib.to_next_business_datetime("2024-01-13")  # Skips weekends


# =============================================================================
# ADDRESS UTILITIES
# =============================================================================

# Wrap address with computed fields and None handling
address = lib.to_address(payload.shipper)

# Access computed properties:
address.person_name  # Falls back to company_name if None
address.company_name  # Original value or ""
address.address_line1  # Original value or ""
address.address_line2  # Original value or None
address.street  # Combined street address
address.city  # Original value
address.state_code  # Original value
address.postal_code  # Original value
address.country_code  # Original value
address.phone_number  # Formatted phone number
address.email  # Original value
address.tax_id  # federal_tax_id or state_tax_id
address.contact  # person_name or company_name

# Postal code utilities
zip5 = lib.to_zip5("12345-6789")  # "12345"
zip4 = lib.to_zip4("12345-6789")  # "6789"

# Country/State name lookup
country = lib.to_country_name("US")  # "United States"
state = lib.to_state_name("CA", "US")  # "California"


# =============================================================================
# SHIPPING DATA CONVERSION
# =============================================================================

# Convert parcels to Packages helper
packages = lib.to_packages(
    payload.parcels,
    presets=provider_units.PackagePresets,  # Optional preset enum
    options=payload.options,  # Shipping options dict
    package_option_type=provider_units.ShippingOption,  # Option enum
    shipping_options_initializer=provider_units.shipping_options_initializer,
)

# Packages provides:
packages.weight  # Total Weight object
packages.weight.LB  # Total in pounds
packages.weight.KG  # Total in kilograms
packages.options  # Merged ShippingOptions
packages.items  # List of commodities from all packages

# Iterate over individual Package objects:
for package in packages:
    package.weight.value  # Weight value
    package.weight.unit  # Weight unit
    package.weight.LB  # Weight in LB
    package.weight.KG  # Weight in KG
    package.length.value  # Length value
    package.length.CM  # Length in CM
    package.length.IN  # Length in IN
    package.width.CM  # Width in CM
    package.height.CM  # Height in CM
    package.dimension_unit  # Dimension unit string
    package.packaging_type  # Packaging type string
    package.description  # Package description
    package.options  # Package-level options


# Convert services list to Services helper
services = lib.to_services(
    payload.services,  # List of service codes
    service_type=provider_units.ShippingService,  # Service enum
)

# Services provides:
services.first  # First service or None
for service in services:
    service.name_or_key  # Karrio service name (enum name)
    service.value_or_key  # Carrier API code (enum value)


# Convert options dict to ShippingOptions helper
options = lib.to_shipping_options(
    payload.options,
    package_options=packages.options,  # Merge with package options
    initializer=provider_units.shipping_options_initializer,
)

# Access options by name:
options.insurance.state  # Value or None
options.signature_required.state  # Value or None
options.saturday_delivery.state  # Value or None


# Convert customs info
customs = lib.to_customs_info(
    payload.customs,
    option_type=provider_units.CustomsOption,  # Optional customs options enum
    weight_unit="KG",  # Default weight unit
    shipper=payload.shipper,  # For tax ID extraction
    recipient=payload.recipient,  # For tax ID extraction
)

# CustomsInfo provides:
customs.commodities  # List of processed commodities
customs.duty  # Duty info
customs.incoterm  # Incoterm code
customs.content_type  # Content type
customs.invoice  # Invoice number
customs.options  # Customs options


# Convert commodities list
commodities = lib.to_commodities(
    payload.commodities,
    weight_unit="KG",
)

# Iterate commodities:
for item in commodities:
    item.title
    item.description
    item.quantity
    item.weight
    item.value_amount
    item.hs_code
    item.origin_country


# =============================================================================
# MULTI-PIECE SHIPMENT UTILITIES
# =============================================================================

# Combine rates from multiple packages into unified rates
combined_rates = lib.to_multi_piece_rates([
    ("pkg_1", [rate1, rate2]),  # Rates for package 1
    ("pkg_2", [rate1, rate2]),  # Rates for package 2
])
# Result: Rates with same service are combined (totals summed)


# Combine shipments from multiple packages into master shipment
master_shipment = lib.to_multi_piece_shipment([
    ("pkg_1", shipment_details_1),
    ("pkg_2", shipment_details_2),
])
# Result: Single shipment with combined labels, tracking numbers in meta


# =============================================================================
# HTTP REQUESTS
# =============================================================================

# Make HTTP request
response = lib.request(
    url="https://api.carrier.com/endpoint",
    data=lib.to_json(request_body),  # Request body
    method="POST",  # HTTP method
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    },
    trace=proxy.trace_as("json"),  # For tracing/logging
    timeout=30,  # Timeout in seconds
    decoder=lib.to_dict,  # Response decoder (default: decode bytes)
)

# URL encoding
query_string = lib.to_query_string({"param1": "value1", "param2": "value2"})
# Result: "param1=value1&param2=value2"


# =============================================================================
# CONCURRENT EXECUTION
# =============================================================================

# Run function concurrently for multiple items (e.g., tracking multiple numbers)
def fetch_tracking(tracking_number: str):
    return tracking_number, lib.request(url=f".../{tracking_number}")

results = lib.run_concurently(
    fetch_tracking,
    ["TRACK1", "TRACK2", "TRACK3"],
    max_workers=2,
)
# Results: List of (tracking_number, response) tuples


# Run asynchronously
results = lib.run_asynchronously(fetch_tracking, items)


# =============================================================================
# DOCUMENT PROCESSING
# =============================================================================

# Convert image to PDF (for carriers returning image labels)
pdf_base64 = lib.image_to_pdf(image_base64_string)
pdf_base64 = lib.image_to_pdf(image_base64, rotate=90, resize={"width": 400})

# Bundle multiple PDFs into one
merged_pdf = lib.bundle_pdfs([pdf1_base64, pdf2_base64])

# Bundle multiple images into one
bundled_image = lib.bundle_imgs([img1_base64, img2_base64])

# Bundle ZPL labels
bundled_zpl = lib.bundle_zpls([zpl1_base64, zpl2_base64])

# Bundle any format (auto-detects)
bundled = lib.bundle_base64([doc1, doc2], format="PDF")

# Convert ZPL to PDF
pdf_base64 = lib.zpl_to_pdf(zpl_string, width=4, height=6, dpmm=12)

# Decode/Encode base64
buffer = lib.to_buffer(base64_string)  # Decode to bytes
encoded = lib.encode_base64(byte_data)  # Encode to base64 string

# Decode bytes with fallback encodings
decoded_str = lib.decode(byte_data)  # Tries utf-8, then ISO-8859-1

# Convert binary string to base64
base64_str = lib.binary_to_base64(binary_string)


# =============================================================================
# FILE LOADING
# =============================================================================

# Load and parse JSON file
data = lib.load_json("/path/to/file.json")

# Load file content as string
content = lib.load_file_content("/path/to/file.txt")


# =============================================================================
# SAFE EXECUTION
# =============================================================================

# Execute potentially failing code safely (returns None on error)
result = lib.failsafe(lambda: risky_operation())
result = lib.failsafe(lambda: int("not_a_number"), warning="Could not parse")

# Identity function - returns value or None
# Useful for conditional field assignment
value = lib.identity(some_value if condition else None)

# Sort tracking events chronologically
sorted_events = lib.sort_events(events)  # Most recent first


# =============================================================================
# CORE CLASSES & TYPES
# =============================================================================

# Serializable - Wrap request for pipeline
request = lib.Serializable(request_object, serializer=lib.to_dict)
# Usage: request.serialize() returns dict

# Deserializable - Wrap response for parsing
response = lib.Deserializable(response_str, deserializer=lib.to_dict)
# Usage: response.deserialize() returns dict

# Pipeline - Chain multiple operations (for multi-step APIs)
pipeline = lib.Pipeline(
    lib.Job(fn=step1_function, fallback=default_value),
    lib.Job(fn=step2_function),
)
result = pipeline.apply(initial_data)

# Enum classes for carrier units
class MyService(lib.StrEnum):
    service_a = "API_CODE_A"
    service_b = "API_CODE_B"

class MyOption(lib.Enum):
    option_a = lib.OptionEnum("CARRIER_CODE", bool)
    option_b = lib.OptionEnum("OTHER_CODE", float)

# Element type (XML element)
element: lib.Element = lib.to_element(xml_string)

# Cache for connection data (used in Settings)
cache = lib.Cache()


# =============================================================================
# CONNECTION CONFIG
# =============================================================================

# Parse connection config options
config = lib.to_connection_config(
    settings.config or {},
    option_type=provider_units.ConnectionConfig,
)

# Access config values:
config.currency.state  # "USD" or None
config.label_type.state  # "PDF" or None


# =============================================================================
# DOCUMENT UPLOAD
# =============================================================================

# Convert document files
doc_files = lib.to_document_files(payload.document_files)

for doc in doc_files:
    doc.doc_file  # Base64 content
    doc.doc_name  # File name
    doc.doc_type  # Document type
    doc.doc_format  # File format (PDF, PNG, etc.)

# Parse upload options
upload_options = lib.to_upload_options(
    payload.options,
    option_type=provider_units.UploadOption,
)
