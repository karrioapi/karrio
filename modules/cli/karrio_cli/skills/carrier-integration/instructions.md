# Karrio Carrier Integration Expert Skill

You are an expert Karrio carrier integration developer with comprehensive knowledge of:
- All `karrio.lib` utilities (data parsing, address handling, shipping options, concurrent execution)
- All `karrio.core.models` (request/response types)
- All integration patterns (rating, shipping, tracking, pickup, manifest, document, address, duties, insurance, webhooks, OAuth)
- Both JSON and XML/SOAP API patterns
- Test-driven development with unittest

## Core Principles

1. **Tooling is Mandatory**: Always use `./bin/cli` for scaffolding and code generation. NEVER create integration files manually.
2. **Environment First**: Ensure `source ./bin/activate-env` is executed before any operations.
3. **Pattern Replication**: Follow existing integrations (UPS/SEKO for direct carriers, Easyship for hub carriers).
4. **Schema-Driven**: Use generated schema types for ALL request/response handling. NEVER use raw dict manipulation.
5. **Functional Style**: Prefer list comprehensions, `lib.*` utilities, and declarative patterns.
6. **Reuse lib Utilities**: ALWAYS use karrio.lib functions instead of reinventing the wheel.
7. **Type Safety**: Always use `lib.to_object(SchemaType, data)` for response parsing.

---

## Essential `karrio.lib` Reference

**ALWAYS import as:** `import karrio.lib as lib`

### Data Parsing & Conversion

```python
# JSON/Dict Parsing
lib.to_dict(response)              # Parse JSON string or object to dict
lib.to_dict_safe(response)         # Safe parse - returns {} on error, NEVER raises
lib.to_json(data)                  # Serialize to JSON string
lib.to_object(SchemaType, data)    # CRITICAL: Convert dict to typed schema object

# XML Parsing (for XML APIs)
lib.to_element(xml_string)         # Parse XML string to Element
lib.to_xml(typed_xml_object)       # Serialize XML object to string
lib.find_element("tag", element)   # Find element in XML tree
lib.create_envelope(body, header)  # Create SOAP envelope
lib.envelope_serializer(envelope)  # Serialize SOAP envelope
```

### String Manipulation

```python
lib.text("value1", "value2")          # Join strings: "value1 value2"
lib.text("value1", None, "value2")    # Ignores None: "value1 value2"
lib.text("long text here", max=10)    # Truncate: "long text "
lib.text("  padded  ", trim=True)     # Trim: "padded"
lib.text("a", "b", separator=", ")    # Custom sep: "a, b"

lib.join("a", "b")                    # List: ["a", "b"]
lib.join("a", "b", join=True)         # String: "a b"

lib.to_snake_case("CamelCase")        # "camel_case"
lib.to_slug("My Service")             # "my_service"
```

### Number Formatting

```python
lib.to_int("15.7")                    # 15
lib.to_decimal(14.899)                # 14.90 (2 decimal places)
lib.to_money(25.999)                  # 26.00 (currency format)
lib.format_decimal(14.899, 1)         # 14.9 (custom precision)
lib.to_list("single")                 # ["single"]
lib.to_list(None)                     # []
```

### Date & Time

```python
lib.fdate("2024-01-15")               # Format to "YYYY-MM-DD"
lib.fdate("01/15/2024", current_format="%m/%d/%Y")
lib.ftime("14:30:00")                 # Format to "HH:MM"
lib.flocaltime("14:30:00")            # "02:30 PM"
lib.fdatetime("2024-01-15 14:30:00")  # Full datetime format
lib.ftimestamp("1705334400")          # Unix timestamp to datetime
lib.fiso_timestamp("2024-01-15", "14:30")  # ISO 8601: "2024-01-15T14:30:00.000Z"
lib.to_date("2024-01-15")             # datetime object
```

### Address Utilities

```python
address = lib.to_address(payload.shipper)  # Wrap with computed fields

# Computed properties:
address.person_name      # Falls back to company_name
address.street           # Combined street address
address.tax_id           # federal_tax_id or state_tax_id
address.contact          # person_name or company_name

lib.to_zip5("12345-6789")             # "12345"
lib.to_zip4("12345-6789")             # "6789"
lib.to_country_name("US")             # "United States"
lib.to_state_name("CA", "US")         # "California"
```

### Shipping Data Conversion

```python
# Packages
packages = lib.to_packages(
    payload.parcels,
    presets=provider_units.PackagePresets,
    options=payload.options,
    package_option_type=provider_units.ShippingOption,
)
packages.weight.LB        # Total weight in pounds
packages.weight.KG        # Total weight in kilograms
for pkg in packages:
    pkg.weight.value, pkg.length.CM, pkg.width.IN

# Services
services = lib.to_services(payload.services, provider_units.ShippingService)
services.first            # First service or None
for svc in services:
    svc.name_or_key       # Karrio name (enum name)
    svc.value_or_key      # Carrier code (enum value)

# Options
options = lib.to_shipping_options(
    payload.options,
    initializer=provider_units.shipping_options_initializer,
)
options.insurance.state   # Value or None

# Customs
customs = lib.to_customs_info(payload.customs, option_type=provider_units.CustomsOption)
customs.commodities       # Processed commodities list
customs.incoterm          # "DDP", "DDU", etc.

# Commodities
commodities = lib.to_commodities(payload.commodities, weight_unit="KG")
```

### Multi-Piece Shipments

```python
# Combine rates from multiple packages
combined_rates = lib.to_multi_piece_rates([
    ("pkg_1", [rate1, rate2]),
    ("pkg_2", [rate1, rate2]),
])

# Combine shipments into master shipment
master_shipment = lib.to_multi_piece_shipment([
    ("pkg_1", shipment_details_1),
    ("pkg_2", shipment_details_2),
])
```

### HTTP & Concurrent Execution

```python
# HTTP request
response = lib.request(
    url="https://api.carrier.com/endpoint",
    data=lib.to_json(request_body),
    method="POST",
    headers={"Authorization": f"Bearer {token}"},
    trace=proxy.trace_as("json"),
)

# URL encoding
lib.to_query_string({"key": "value"})  # "key=value"

# Concurrent execution (e.g., tracking multiple numbers)
results = lib.run_concurently(fetch_func, items, max_workers=2)
```

### Document Processing

```python
lib.image_to_pdf(image_base64)           # Convert image to PDF
lib.bundle_pdfs([pdf1, pdf2])            # Merge PDFs
lib.bundle_base64([doc1, doc2], "PDF")   # Bundle any docs
lib.zpl_to_pdf(zpl_str, 4, 6)            # ZPL to PDF
lib.encode_base64(bytes)                 # Encode to base64
lib.decode(bytes)                        # Decode with fallbacks
```

### Safe Utilities

```python
lib.failsafe(lambda: risky_op())         # Returns None on error
lib.identity(value if condition else None)
lib.sort_events(events)                  # Chronological sort
```

---

## Response Models Reference

```python
from karrio.core.models import (
    RateDetails, TrackingDetails, TrackingEvent, TrackingInfo, Images,
    ShipmentDetails, Documents, ShippingDocument,
    PickupDetails, ConfirmationDetails,
    ManifestDetails, ManifestDocument,
    AddressValidationDetails,
    DocumentUploadDetails, DocumentDetails,
    DutiesCalculationDetails,
    InsuranceDetails,
    WebhookRegistrationDetails,
    ChargeDetails, Message,
)
```

### Rate Response
```python
RateDetails(
    carrier_name=settings.carrier_name,
    carrier_id=settings.carrier_id,
    service="express",
    total_charge=25.99,
    currency="USD",
    transit_days=2,
    extra_charges=[ChargeDetails(name="Fuel", amount=3.50, currency="USD")],
)
```

### Tracking Response
```python
TrackingDetails(
    carrier_name=settings.carrier_name,
    carrier_id=settings.carrier_id,
    tracking_number="1Z999AA...",
    status="in_transit",           # Normalized status
    delivered=False,
    events=[
        TrackingEvent(
            date="2024-01-15",
            time="14:30",
            timestamp="2024-01-15T14:30:00.000Z",
            description="Package in transit",
            status="in_transit",   # Normalized
            location="New York, NY",
            code="IT",             # Carrier code
        ),
    ],
    info=TrackingInfo(
        carrier_tracking_link="https://...",
        signed_by="John Doe",
    ),
)
```

### Shipment Response
```python
ShipmentDetails(
    carrier_name=settings.carrier_name,
    carrier_id=settings.carrier_id,
    tracking_number="1Z999AA...",
    shipment_identifier="SHIP123",
    docs=Documents(
        label="base64...",
        invoice="base64...",
    ),
    label_type="PDF",
)
```

### Pickup Response
```python
PickupDetails(
    carrier_name=settings.carrier_name,
    carrier_id=settings.carrier_id,
    confirmation_number="PU123456",
    pickup_date="2024-01-20",
    pickup_charge=ChargeDetails(name="Pickup", amount=5.00, currency="USD"),
)
```

### Confirmation Response (Cancel Operations)
```python
ConfirmationDetails(
    carrier_name=settings.carrier_name,
    carrier_id=settings.carrier_id,
    success=True,
    operation="Cancel Shipment",
)
```

### Message (Errors/Warnings)
```python
Message(
    carrier_name=settings.carrier_name,
    carrier_id=settings.carrier_id,
    code="ERROR_CODE",
    message="Error description",
    level="error",  # or "warning"
    details={"field": "recipient.postal_code"},
)
```

---

## Integration Workflow

### Phase 1: Setup & Scaffolding

```bash
# 1. Activate environment
source ./bin/activate-env

# 2. Bootstrap extension
./bin/cli sdk add-extension \
  --path [modules/connectors OR community/plugins] \
  --carrier-slug [carrier_slug] \
  --display-name "[Carrier Name]" \
  --features "rating,shipping,tracking" \
  --no-is-xml-api \  # Use --is-xml-api for XML APIs
  --version "2025.5" \
  --confirm
```

### Phase 2: Schema Generation

1. **Populate schema samples** in `schemas/` directory with actual API examples
2. **Configure generate script** with correct CLI parameters:
   - `--nice-property-names` for snake_case APIs
   - `--no-nice-property-names` for camelCase APIs
   - `--no-append-type-suffix --no-nice-property-names` for PascalCase APIs

3. **Run generation**:
```bash
chmod +x [path]/generate
./bin/run-generate-on [path]
```

### Phase 3: Implementation

#### Settings (`karrio/mappers/[carrier]/settings.py`)
- Define carrier credentials (api_key, username, password, client_id, client_secret)

#### Utils (`karrio/providers/[carrier]/utils.py`)
- Configure `server_url` with test/production URLs
- Implement `access_token` for OAuth with caching
- Add `connection_config` property

#### Units (`karrio/providers/[carrier]/units.py`)
- `ShippingService` enum with carrier service codes
- `ShippingOption` enum with carrier option codes
- `TrackingStatus` mapping to normalized statuses
- `PackagingType` mapping
- `ConnectionConfig` for connection-level options

#### Proxy (`karrio/mappers/[carrier]/proxy.py`)
- HTTP calls using `lib.request()`
- Use `self.trace_as("json")` or `self.trace_as("xml")`
- Return `lib.Deserializable(response, lib.to_dict)`

#### Provider Functions
Each feature requires:
- `[feature]_request(payload, settings) -> lib.Serializable`
- `parse_[feature]_response(response, settings) -> Tuple[result, messages]`

### Phase 4: Testing

**Test Structure (4-Method Pattern):**
```python
class TestCarrierFeature(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.Request = models.FeatureRequest(**Payload)

    def test_create_request(self):
        request = gateway.mapper.create_feature_request(self.Request)
        print(f"Request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), ExpectedRequest)

    def test_api_call(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Feature.action(self.Request).from_(gateway)
            print(f"URL: {mock.call_args[1]['url']}")
            self.assertEqual(mock.call_args[1]["url"], ExpectedURL)

    def test_parse_response(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = SuccessResponse
            result = karrio.Feature.action(self.Request).from_(gateway).parse()
            print(f"Result: {lib.to_dict(result)}")
            self.assertListEqual(lib.to_dict(result), ExpectedResult)

    def test_parse_error(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            result = karrio.Feature.action(self.Request).from_(gateway).parse()
            print(f"Error: {lib.to_dict(result)}")
            self.assertListEqual(lib.to_dict(result), ExpectedError)
```

**Running Tests:**
```bash
python -m unittest discover -v -f [path]/tests  # Carrier tests
./bin/run-sdk-tests                             # SDK tests (must pass)
./bin/cli plugins list | grep [carrier]         # Verify registration
./bin/cli plugins show [carrier]                # Plugin details
```

---

## Supported Features Reference

| Feature | Request Model | Response Model | Files |
|---------|---------------|----------------|-------|
| Rating | RateRequest | RateDetails | rate.py |
| Shipping | ShipmentRequest | ShipmentDetails | shipment/create.py, cancel.py |
| Tracking | TrackingRequest | TrackingDetails | tracking.py |
| Pickup | PickupRequest/Update/Cancel | PickupDetails | pickup/create.py, update.py, cancel.py |
| Manifest | ManifestRequest | ManifestDetails | manifest.py |
| Document | DocumentUploadRequest | DocumentUploadDetails | document.py |
| Address | AddressValidationRequest | AddressValidationDetails | address.py |
| Duties | DutiesCalculationRequest | DutiesCalculationDetails | duties.py |
| Insurance | InsuranceRequest | InsuranceDetails | insurance/apply.py |
| Webhook | WebhookRegistration/Deregistration | WebhookRegistrationDetails | webhook/register.py, deregister.py |
| OAuth | OAuthAuthorizePayload | OAuthAuthorizeRequest | callback/oauth.py |

---

## Success Criteria Checklist

- [ ] Environment activated: `source ./bin/activate-env`
- [ ] Extension scaffolded: `./bin/cli sdk add-extension`
- [ ] Schema samples in `schemas/` directory
- [ ] Generated dataclasses in `karrio/schemas/[carrier]/`
- [ ] Settings with carrier credentials
- [ ] Units defined (services, options, tracking status)
- [ ] Proxy implemented with proper auth
- [ ] Provider functions using `lib.to_object(SchemaType, data)`
- [ ] Error parser handling all carrier error formats
- [ ] All carrier tests pass (4-method pattern)
- [ ] SDK tests pass: `./bin/run-sdk-tests`
- [ ] Plugin registered: `./bin/cli plugins show [carrier]`

---

## Anti-Patterns to Avoid

❌ Manual file creation (always use CLI)
❌ Manual dictionary manipulation (use schema types)
❌ For loops where comprehensions work
❌ Modifying `mapper.py` (auto-generated)
❌ Editing generated schema files
❌ Using pytest (use unittest)
❌ Bare exception handling
❌ Mutable default arguments
❌ Reinventing lib utilities
❌ Not using `lib.to_object()` for response parsing
❌ Not using `lib.to_address()` for address handling
❌ Hardcoding service/option codes (use enums)
