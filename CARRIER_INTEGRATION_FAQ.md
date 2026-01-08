# Carrier Integration FAQ

This document complements the [CARRIER_INTEGRATION_GUIDE.md](./CARRIER_INTEGRATION_GUIDE.md) with frequently asked questions and common patterns learned from carrier implementations.

---

## Table of Contents

1. [Settings vs ConnectionConfig](#settings-vs-connectionconfig)
2. [Enums and Units](#enums-and-units)
3. [lib Utilities](#lib-utilities)
4. [Test Writing Patterns](#test-writing-patterns)
5. [Common Pitfalls](#common-pitfalls)
   - [Wrong Attribute for Service Name](#1-wrong-attribute-for-service-name)
   - [Missing Context in Deserializable](#2-missing-context-in-deserializable)
   - [Boolean Options Always True](#3-boolean-options-always-true)
   - [Not Filtering None in Test Assertions](#4-not-filtering-none-in-test-assertions)
   - [Redundant None Checks on Package Dimensions](#5-redundant-none-checks-on-package-dimensions)
   - [Defensive Empty String Fallbacks](#6-defensive-empty-string-fallbacks-in-response-parsing)
   - [Using Helper Functions Instead of Single Tree](#7-using-_build_-helper-functions-instead-of-single-tree-instantiation)
   - [Services and Options Declaration Patterns](#8-services-and-options-declaration-patterns)
6. [SOAP/WCF Integration Patterns](#soapwcf-integration-patterns)
7. [Error Handling](#error-handling)
8. [Service and Option Mappings](#service-and-option-mappings)
9. [JSON Schema Files](#json-schema-files)
10. [Multi-Piece/Multi-Package Shipments](#multi-piecemulti-package-shipments)

---

## Settings vs ConnectionConfig

### What should go in Settings vs ConnectionConfig?

**Settings (utils.py)** should ONLY contain:
- Required credentials (username, password, client_id, etc.)
- Standard karrio settings (id, test_mode, carrier_id, metadata, config)
- Computed properties that derive from credentials (server_url, carrier_name)

**ConnectionConfig (units.py)** should contain:
- Optional configuration options (label_format, label_size, profile, etc.)
- Per-connection customizations
- Enum-based options using `lib.units.create_enum()`

### Settings Pattern (CORRECT)

```python
# utils.py
import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """Carrier connection settings."""

    # Only required credentials here
    username: str
    password: str
    client_id: str

    account_country_code: str = "AT"

    @property
    def carrier_name(self):
        return "carrier_name"

    @property
    def server_url(self):
        return (
            "https://api-sandbox.example.com"
            if self.test_mode
            else "https://api.example.com"
        )

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.carrier.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )
```

### ConnectionConfig Pattern (units.py)

```python
import karrio.lib as lib


class LabelFormat(lib.StrEnum):
    PDF = "PDF"
    ZPL2 = "ZPL2"


class LabelSize(lib.StrEnum):
    SIZE_100x150 = "100x150"
    SIZE_100x200 = "100x200"


class ConnectionConfig(lib.Enum):
    """Connection configuration options."""

    server_url = lib.OptionEnum("server_url", str)
    label_format = lib.OptionEnum(
        "label_format",
        lib.units.create_enum("LabelFormat", [_.name for _ in LabelFormat]),
    )
    label_size = lib.OptionEnum(
        "label_size",
        lib.units.create_enum("LabelSize", [_.name for _ in LabelSize]),
    )
    shipping_services = lib.OptionEnum("shipping_services", list)
    shipping_options = lib.OptionEnum("shipping_options", list)
```

### Accessing ConnectionConfig Values

Always use `.state` to access the current value:

```python
# In shipment/create.py
def shipment_request(payload, settings):
    label_format = settings.connection_config.label_format.state  # Returns value or None
    label_size = settings.connection_config.label_size.state

    # Use in request
    request = SomeRequestType(
        LabelFormat=label_format,
        LabelSize=label_size,
    )
```

### Test Fixture Configuration

Put optional config in the `config` dict:

```python
# fixture.py
gateway = karrio.gateway["carrier"].create(
    dict(
        carrier_id="carrier",
        test_mode=True,
        # Required credentials
        username="test_user",
        password="test_pass",
        client_id="test_client",
        # Optional config - goes in config dict
        config=dict(
            label_format="PDF",
            label_size="SIZE_100x200",
        ),
    )
)
```

### WRONG: Adding optional settings to Settings class

```python
# WRONG - DO NOT DO THIS!
class Settings(core.Settings):
    username: str
    password: str

    # These should be in ConnectionConfig, not here!
    label_format: str = "PDF"  # WRONG
    label_size: str = None     # WRONG
    paper_layout: str = None   # WRONG
```

---

## Enums and Units

### How do I define shipping services for a carrier?

Use `lib.StrEnum` for service codes that map carrier-specific values:

```python
class ShippingService(lib.StrEnum):
    """Carrier + Product combinations.

    Format: carrier_service_name
    The service code maps to internal values.
    """
    carrier_standard = "STANDARD"
    carrier_express = "EXPRESS"
    carrier_international = "INTERNATIONAL"
```

### How do I parse service codes with multiple parts?

Create a helper function to split composite service codes:

```python
def parse_service_code(service_code: str) -> tuple:
    """Parse a service code to extract parts.

    Args:
        service_code: Service code in format "PART1_PART2"

    Returns:
        Tuple of (part1, part2)
    """
    if "_" in service_code:
        parts = service_code.split("_", 1)
        return parts[0], parts[1] if len(parts) > 1 else ""
    return service_code, ""
```

### How do I access a service's name vs its value?

When iterating through services using `lib.to_services()`:

```python
# CORRECT - use .name for the service name
services = lib.to_services(payload.services, initializer=shipping_services_initializer)
for service in services:
    service_name = service.name        # e.g., "carrier_standard"
    service_value = service.value      # e.g., "STANDARD"

# WRONG - .name_or_key is for EnumWrapper, not enum members
# service.name_or_key  # AttributeError!
```

### How do I define shipping options?

Use `lib.OptionEnum` for carrier-specific options:

```python
class ShippingOption(lib.Enum):
    """Carrier specific options."""

    # Carrier-specific options with their API identifiers
    carrier_cod = lib.OptionEnum("COD", float)           # Cash on delivery
    carrier_insurance = lib.OptionEnum("INS", float)     # Insurance
    carrier_signature = lib.OptionEnum("SIG", bool)      # Signature required
    carrier_saturday = lib.OptionEnum("SAT", bool)       # Saturday delivery
    carrier_email_notify = lib.OptionEnum("MAIL", str)   # Email notification

    # Unified option mappings to karrio standard options
    cash_on_delivery = carrier_cod
    insurance = carrier_insurance
    signature_required = carrier_signature
    saturday_delivery = carrier_saturday
```

### How do I define tracking status mappings?

Map carrier status codes to karrio unified statuses:

```python
class TrackingStatus(lib.Enum):
    """Carrier tracking status mapping."""

    pending = [
        "CREATED",
        "REGISTERED",
        "DATA_RECEIVED",
    ]
    delivered = [
        "DELIVERED",
        "POD",
    ]
    in_transit = [
        "IN_TRANSIT",
        "DEPARTED",
        "ARRIVED",
    ]
    out_for_delivery = [
        "OUT_FOR_DELIVERY",
    ]
    delivery_failed = [
        "FAILED",
        "EXCEPTION",
    ]
```

---

## lib Utilities

### Core Serialization/Deserialization

#### `lib.Serializable`
Wraps a request object for serialization:

```python
return lib.Serializable(
    request_object,
    lambda req: serialize_to_string(req, settings),
)
```

#### `lib.Deserializable`
Wraps a response for deserialization with optional context:

```python
return lib.Deserializable(
    response_text,
    lib.to_element,
    request.ctx,  # Pass context for tracking requests
)
```

### Address and Package Utilities

#### `lib.to_address`
Converts payload address to a standardized Address object:

```python
shipper = lib.to_address(payload.shipper)
recipient = lib.to_address(payload.recipient)

# Access properties
shipper.company_name
shipper.person_name
shipper.street           # Combined street with number
shipper.street_number    # Parsed street number
shipper.postal_code
shipper.city
shipper.country_code
shipper.state_code
shipper.email
shipper.phone_number
```

#### `lib.to_packages`
Converts parcels with validation:

```python
packages = lib.to_packages(
    payload.parcels,
    required=["weight"],  # Required fields
)

for index, pkg in enumerate(packages, 1):
    pkg.weight.KG        # Weight in KG
    pkg.weight.LB        # Weight in LB
    pkg.length.CM        # Dimensions in CM
    pkg.width.CM
    pkg.height.CM
    pkg.parcel.id        # Original parcel ID
```

### Options and Services

#### `lib.to_shipping_options`
Parses shipping options with initializer:

```python
options = lib.to_shipping_options(
    payload.options,
    package_options=packages.options,
    initializer=shipping_options_initializer,
)

# Access options with .state
if options.cash_on_delivery.state:
    cod_amount = options.cash_on_delivery.state

if options.insurance.state:
    insurance_amount = options.insurance.state

# Check string options (returns actual value or None)
email = options.carrier_email_notify.state
if email and isinstance(email, str):
    # Use email value
    pass
```

#### `lib.to_services`
Creates a services collection:

```python
services = lib.to_services(
    payload.services,
    initializer=shipping_services_initializer,
)

for service in services:
    print(service.name)   # Service enum name
    print(service.value)  # Service enum value
```

### XML Utilities

#### `lib.to_xml`
Serializes an object to XML:

```python
xml_str = lib.to_xml(
    request_object,
    name_="RootElement",
    namespacedef_='xmlns:ns="http://example.com"',
)
```

#### `lib.to_element`
Parses XML string to Element:

```python
element = lib.to_element(xml_string)
```

#### `lib.find_element`
Finds and deserializes XML elements:

```python
results: typing.List[ResultType] = lib.find_element(
    "ElementName",
    response_element,
    ResultType,
)
```

### Value Conversions

#### `lib.to_money`
Converts to decimal money value:

```python
amount = lib.to_money(value_string)  # Returns float/Decimal
```

#### `lib.to_dict`
Converts objects to dictionary (filters None values):

```python
result_dict = lib.to_dict(shipment_details)
# Note: None values are automatically filtered out
```

#### `lib.to_date` and `lib.to_time`
Parse date/time strings:

```python
date = lib.to_date("2024-01-15")           # Returns "2024-01-15"
time = lib.to_time("14:30:00")             # Returns "14:30:00"

# From datetime string
date = lib.to_date("2024-01-15T14:30:00")  # Extracts date part
time = lib.to_time("2024-01-15T14:30:00")  # Extracts time part
```

---

## Test Writing Patterns

### Standard Test Structure

Follow the 4-test pattern for each feature (rate, shipment, tracking, etc.):

```python
class TestCarrierFeature(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.Request = models.RequestType(**Payload)

    def test_create_request(self):
        """Test request serialization."""
        request = gateway.mapper.create_feature_request(self.Request)
        self.assertEqual(request.serialize(), ExpectedRequest)

    def test_feature_call(self):
        """Test API call is made correctly."""
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = "<response/>"
            karrio.Feature.method(self.Request).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/endpoint",
            )

    def test_parse_response(self):
        """Test response parsing."""
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = SuccessResponse
            parsed_response = (
                karrio.Feature.method(self.Request).from_(gateway).parse()
            )
            print(parsed_response)  # ALWAYS add for debugging
            self.assertListEqual(lib.to_dict(parsed_response), ExpectedParsedResponse)

    def test_parse_error_response(self):
        """Test error parsing."""
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Feature.method(self.Request).from_(gateway).parse()
            )
            print(parsed_response)  # ALWAYS add for debugging
            self.assertListEqual(lib.to_dict(parsed_response), ExpectedErrorResponse)
```

### Fixture File Structure

Create a `fixture.py` in the test directory:

```python
import karrio
import karrio.lib as lib

gateway = karrio.gateway["carrier"].create(
    dict(
        username="test_user",
        password="test_password",
        # Add carrier-specific settings
        mandator_id="TEST_MANDATOR",
        consigner_id="TEST_CONSIGNER",
        carrier_id="carrier",
    )
)
```

### Expected Response Format

Remember that `lib.to_dict()` filters out None values:

```python
# WRONG - includes None values
ParsedResponse = [
    {
        "carrier_id": "carrier",
        "label_url": None,  # This will be filtered!
    },
    [],
]

# CORRECT - omit None values
ParsedResponse = [
    {
        "carrier_id": "carrier",
        # label_url omitted since it's None
    },
    [],
]
```

---

## Common Pitfalls

### 1. Wrong Attribute for Service Name

```python
# WRONG - EnumWrapper pattern (not for iteration)
for service in services:
    name = service.name_or_key  # AttributeError!

# CORRECT - Enum member pattern
for service in services:
    name = service.name
```

### 2. Missing Context in Deserializable

For tracking requests that need to match responses to tracking numbers:

```python
# WRONG - no context passed
return lib.Deserializable(response, lib.to_element)

# CORRECT - pass context for tracking number matching
return lib.Deserializable(response, lib.to_element, request.ctx)
```

### 3. Boolean Options Always True

```python
# WRONG - .state returns truthy value for any option
if options.email_notification.state:  # True even if empty string!

# CORRECT - check for meaningful value
email_value = options.carrier_email_notify.state
if email_value and isinstance(email_value, str):
    # Use email_value
```

### 4. Not Filtering None in Test Assertions

```python
# Test fails because lib.to_dict filters None
self.assertListEqual(
    lib.to_dict(parsed_response),
    [{"field": "value", "optional_field": None}]  # None will be filtered!
)

# Correct expectation
self.assertListEqual(
    lib.to_dict(parsed_response),
    [{"field": "value"}]  # Omit None fields
)
```

### 5. Redundant None Checks on Package Dimensions

The `Package` wrapper's dimension properties (`length`, `width`, `height`) return a `Dimension` object that already handles None values. The `Dimension.CM`, `Dimension.IN` etc. properties return `None` when the underlying value is None.

```python
# WRONG - Redundant conditional check
parcelat.ColloRowType(
    Weight=package.weight.KG,
    Length=package.length.CM if package.length else None,  # WRONG!
    Width=package.width.CM if package.width else None,     # WRONG!
    Height=package.height.CM if package.height else None,  # WRONG!
)

# CORRECT - Dimension.CM already returns None when value is None
parcelat.ColloRowType(
    Weight=package.weight.KG,
    Length=package.length.CM,
    Width=package.width.CM,
    Height=package.height.CM,
)
```

**Why?** Looking at `karrio/core/units.py`:
```python
class Dimension:
    @property
    def CM(self):
        if self._unit is None or self._value is None:
            return None  # Already handles None!
        # ... conversion logic
```

The Package wrapper always returns a Dimension object, and that object's properties handle None values internally. No need for defensive checks.

### 6. Defensive Empty String Fallbacks in Response Parsing

When parsing responses, don't use defensive fallbacks like `else ""` for required data. If you've already validated the response has data, trust it.

```python
# WRONG - Defensive fallback suggests data might not exist
tracking_number = tracking_numbers[0] if tracking_numbers else ""

# CORRECT - We only call _extract_details when we know data exists
tracking_number = tracking_numbers[0]
```

The validation should happen in `parse_*_response()` before calling `_extract_details()`:
```python
def parse_shipment_response(_response, settings):
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    result = lib.find_element("Result", response, first=True)

    # Only extract if we have valid data
    shipment = (
        _extract_details(response, settings)
        if result is not None and not any(messages)
        else None
    )
    return shipment, messages
```

### 7. Using `_build_*` Helper Functions Instead of Single Tree Instantiation

**Never create helper functions** like `_build_services()`, `_build_customs_data()`, `_build_address()` to construct parts of a request. Always use **single tree instantiation** where the entire request object is built in one expression.

```python
# WRONG - DO NOT DO THIS!
def _build_services(options):
    """Build services list from options."""
    services = []
    if options.cash_on_delivery.state:
        services.append(ServiceType(ServiceID="COD", Value=options.cash_on_delivery.state))
    if options.insurance.state:
        services.append(ServiceType(ServiceID="INS", Value=options.insurance.state))
    return services

def _build_customs_data(customs):
    """Build customs data."""
    return CustomsType(
        InvoiceNo=customs.invoice,
        Items=[ItemType(...) for item in customs.commodities],
    )

def shipment_request(payload, settings):
    # ... setup code ...
    services = _build_services(options)  # WRONG!
    customs_data = _build_customs_data(customs)  # WRONG!

    request = ShipmentType(
        Services=services,
        Customs=customs_data,
    )
```

```python
# CORRECT - Single tree instantiation with everything inline
def shipment_request(payload, settings):
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels, required=["weight"])
    options = lib.to_shipping_options(payload.options, ...)
    customs = payload.customs

    request = ShipmentType(
        ShipToData=AddressType(
            Name1=recipient.company_name or recipient.person_name,
            Street=recipient.street,
            City=recipient.city,
            Country=recipient.country_code,
        ),
        ShipFromData=AddressType(
            Name1=shipper.company_name or shipper.person_name,
            Street=shipper.street,
            City=shipper.city,
            Country=shipper.country_code,
        ),
        Packages=[
            PackageType(
                Weight=pkg.weight.KG,
                Length=pkg.length.CM,
                Width=pkg.width.CM,
                Height=pkg.height.CM,
                # Customs data inline per package
                CustomsData=(
                    CustomsType(
                        InvoiceNo=customs.invoice,
                        Items=[
                            ItemType(
                                Description=item.description,
                                Quantity=item.quantity,
                                Value=item.value_amount,
                            )
                            for item in (customs.commodities or [])
                        ] if customs.commodities else None,
                    )
                    if customs
                    else None
                ),
            )
            for index, pkg in enumerate(packages, 1)
        ],
        # Services inline - see pattern below
        Services=[
            *(
                [ServiceType(ServiceID="COD", Value=str(options.cash_on_delivery.state))]
                if options.cash_on_delivery.state
                else []
            ),
            *(
                [ServiceType(ServiceID="INS", Value=str(options.insurance.state))]
                if options.insurance.state
                else []
            ),
            *([ServiceType(ServiceID="SIG")] if options.signature_required.state else []),
        ],
    )

    return lib.Serializable(request, lib.to_dict)
```

**Why single tree instantiation?**
- Easier to read and understand the complete request structure
- No jumping between functions to understand what's being built
- Consistent with karrio codebase patterns (see DHL Express, Canada Post, UPS)
- Makes it obvious what data goes where

### 8. Services and Options Declaration Patterns

When declaring services or options inline, follow these patterns based on the complexity:

#### Pattern A: Uniform Structure (Canada Post, DHL Express)

When all options have the **same structure**, use a filtered list comprehension:

```python
# From canadapost/shipment/create.py - all options have same structure
options=(
    canadapost.optionsType(
        option=[
            canadapost.OptionType(
                option_code=option.code,
                option_amount=lib.to_money(option.state),
            )
            for _, option in package.options.items()
            if option.state is not False
        ]
    )
    if any([option for _, option in package.options.items() if option.state is not False])
    else None
),
```

```python
# From dhl_express/shipment.py - filter options first, then map
option_items = [
    option for _, option in options.items() if option.state is not False
]

# Then in the request tree:
SpecialService=[
    dhl.SpecialService(
        SpecialServiceType=svc.code,
        ChargeValue=lib.to_money(svc.state),
        CurrencyCode=(currency if lib.to_money(svc.state) is not None else None),
    )
    for svc in option_items
],
```

#### Pattern B: Different Structures (Spread Syntax)

When services have **different structures** (some need values, some don't), use spread syntax with conditionals:

```python
# Each service type has different requirements
Services=[
    # COD needs Value with amount and currency
    *(
        [
            ServiceType(
                ServiceID="COD",
                Value=AmountType(
                    Value=str(options.cash_on_delivery.state),
                    Currency=options.carrier_cod_currency.state or "EUR",
                ),
            )
        ]
        if options.cash_on_delivery.state
        else []
    ),
    # Insurance also needs Value
    *(
        [
            ServiceType(
                ServiceID="INS",
                Value=AmountType(
                    Value=str(options.insurance.state),
                    Currency=options.carrier_insurance_currency.state or "EUR",
                ),
            )
        ]
        if options.insurance.state
        else []
    ),
    # Signature just needs ServiceID (no Value)
    *([ServiceType(ServiceID="SIG")] if options.signature_required.state else []),
    # Saturday delivery just needs ServiceID
    *([ServiceType(ServiceID="SDO")] if options.saturday_delivery.state else []),
    # Email notification needs Parameters (not Value)
    *(
        [
            ServiceType(
                ServiceID="MAIL",
                Parameters=options.carrier_notification_email.state,
            )
        ]
        if options.carrier_notification_email.state
        else []
    ),
],
```

#### Important: Empty Lists vs None for jstruct

When using jstruct JList fields, pass an **empty list `[]`** instead of `None` to avoid `[None]` serialization:

```python
# WRONG - jstruct converts None to [None]
Services=services if services else None,  # Results in {"Services": [None]}

# CORRECT - empty list gets stripped by lib.to_dict()
Services=services,  # Empty [] gets stripped, non-empty list is kept
```

**Reference implementations:**
- `modules/connectors/dhl_express/karrio/providers/dhl_express/shipment.py`
- `modules/connectors/canadapost/karrio/providers/canadapost/shipment/create.py`
- `modules/connectors/ups/karrio/providers/ups/shipment/create.py`

---

## SOAP/WCF Integration Patterns

### CRITICAL: Use Generated Schema Types, Not Hardcoded XML Strings

**NEVER** create SOAP envelopes using f-strings or manual XML construction. Instead, use:
- `lib.Envelope` and `lib.Body` for the SOAP envelope structure
- Generated schema types from XSD/WSDL for the request body
- `lib.envelope_serializer` for serialization

### Correct Pattern: Using lib.Envelope with Generated Types

```python
import karrio.schemas.carrier.types as carrier_schema
import karrio.lib as lib

def shipment_request(
    payload: models.ShipmentRequest,
    settings: Settings,
) -> lib.Serializable:
    """Create a shipment request using generated schema types."""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)

    # Use generated schema types directly - NOT f-strings!
    request = lib.Envelope(
        Body=lib.Body(
            carrier_schema.CreateShipmentType(
                ClientID=settings.client_id,
                SenderAddress=carrier_schema.AddressType(
                    Name1=shipper.company_name or shipper.person_name,
                    AddressLine1=shipper.street,
                    PostalCode=shipper.postal_code,
                    City=shipper.city,
                    CountryID=shipper.country_code,
                ),
                RecipientAddress=carrier_schema.AddressType(
                    Name1=recipient.company_name or recipient.person_name,
                    AddressLine1=recipient.street,
                    PostalCode=recipient.postal_code,
                    City=recipient.city,
                    CountryID=recipient.country_code,
                ),
                Packages=carrier_schema.PackageListType(
                    Package=[
                        carrier_schema.PackageType(
                            Weight=package.weight.KG,
                            Length=package.length.CM,
                            Width=package.width.CM,
                            Height=package.height.CM,
                        )
                        for package in packages
                    ]
                ),
            )
        )
    )

    # Use lib.envelope_serializer - NOT custom f-string serializers!
    return lib.Serializable(request, lib.envelope_serializer)
```

### WRONG: Hardcoded XML Strings (DO NOT USE)

```python
# WRONG - DO NOT DO THIS!
def shipment_request_wrong(payload, settings) -> lib.Serializable:
    xml = f'''<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <CreateShipment>
                <ClientID>{settings.client_id}</ClientID>
                <SenderAddress>
                    <Name1>{shipper.company_name}</Name1>
                    ...
                </SenderAddress>
            </CreateShipment>
        </soap:Body>
    </soap:Envelope>'''
    return lib.Serializable(xml, lambda x: x)  # WRONG!
```

This approach is:
- Error-prone (missing escaping, typos in XML tags)
- Hard to maintain
- Defeats the purpose of generated schema types
- Inconsistent with karrio patterns

### Generating Schema Types from XSD

Create a `generate` script in your connector directory:

```bash
#!/bin/bash
SCHEMAS=./schemas
LIB_MODULES=./karrio/schemas/carrier_name

# Clean and regenerate
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \;
touch "${LIB_MODULES}/__init__.py"

# Generate Python types from XSD
generateDS --no-namespace-defs -o "${LIB_MODULES}/types.py" $SCHEMAS/carrier.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/void_types.py" $SCHEMAS/carrier_void.xsd
```

Then run: `./bin/run-generate-on carrier_name`

### Proxy Configuration for SOAP

```python
class Proxy(karrio.Proxy):
    settings: provider_utils.Settings

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=self.settings.server_url,
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": "http://carrier.namespace/IService/CreateShipment",
            },
        )
        return lib.Deserializable(response, lib.to_element)
```

### WS-Security Headers (When Required)

If the carrier requires WS-Security, use the `lib.Header` component:

```python
request = lib.Envelope(
    Header=lib.Header(
        # WS-Security elements if needed
    ),
    Body=lib.Body(
        carrier_schema.RequestType(...)
    )
)
```

### Legacy Pattern (Avoid Unless Absolutely Necessary)

The f-string pattern below should only be used if the carrier API requires non-standard SOAP formatting that cannot be achieved with `lib.Envelope`:

```python
# LEGACY - Only use if lib.Envelope cannot handle the format
def create_envelope(body: str, settings: Settings) -> str:
    """Create SOAP envelope with WS-Security header."""
    return f'''<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Header>
        <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
            <wsse:UsernameToken>
                <wsse:Username>{settings.username}</wsse:Username>
                <wsse:Password>{settings.password}</wsse:Password>
            </wsse:UsernameToken>
        </wsse:Security>
    </soapenv:Header>
    <soapenv:Body>
        {body}
    </soapenv:Body>
</soapenv:Envelope>'''
```

### Parsing SOAP Responses

```python
def parse_response(
    _response: lib.Deserializable[lib.Element],
    settings: Settings,
) -> typing.Tuple[ResultType, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Find typed elements
    results: typing.List[schema.ResultElement] = lib.find_element(
        "ResultElement",
        response,
        schema.ResultElement,
    )

    result = None
    if any(results):
        data = results[0]
        if data.Success == 1:
            result = extract_result(data, settings)

    return result, messages
```

---

## Error Handling

### Standard Error Parser

```python
def parse_error_response(
    response: lib.Element,
    settings: Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse error messages from response."""
    errors: typing.List[schema.Error] = lib.find_element(
        "Error",
        response,
        schema.Error,
    )

    # Also check for top-level failures
    results: typing.List[schema.ActionResult] = lib.find_element(
        "ActionResult",
        response,
        schema.ActionResult,
    )

    messages = []

    # Collect errors from Error elements
    for error in errors:
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=error.ErrorNo,
                message=error.Message,
                details={},
            )
        )

    # Check ActionResult for failures
    for result in results:
        if result.Success == 0 and result.Errors:
            for err in result.Errors.Error:
                messages.append(
                    models.Message(
                        carrier_id=settings.carrier_id,
                        carrier_name=settings.carrier_name,
                        code=err.ErrorNo,
                        message=err.Message,
                        details={},
                    )
                )

    return messages
```

---

## Service and Option Mappings

### Services Initializer

```python
def shipping_services_initializer(
    services: typing.List[str],
    **kwargs,
) -> units.Services:
    """Apply default service codes to the list of services."""
    _services = list(set(services or []))

    if not _services:
        return units.Services([], ShippingService)

    return units.Services(_services, ShippingService)
```

### Options Initializer

```python
def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """Apply default values to the given options."""
    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)
```

### Default Services List

Define default services for carrier configuration:

```python
DEFAULT_SERVICES = [
    {
        "service_code": "carrier_standard",
        "service_name": "Standard Delivery",
        "currency": "EUR",
    },
    {
        "service_code": "carrier_express",
        "service_name": "Express Delivery",
        "currency": "EUR",
    },
]
```

---

## Quick Reference

| Task | Pattern | Example |
|------|---------|---------|
| Define service | `lib.StrEnum` | `class ShippingService(lib.StrEnum)` |
| Define option | `lib.OptionEnum` | `option = lib.OptionEnum("CODE", type)` |
| Parse address | `lib.to_address()` | `shipper = lib.to_address(payload.shipper)` |
| Parse packages | `lib.to_packages()` | `packages = lib.to_packages(payload.parcels)` |
| Parse options | `lib.to_shipping_options()` | `options = lib.to_shipping_options(...)` |
| Serialize | `lib.Serializable()` | `return lib.Serializable(req, serializer)` |
| Deserialize | `lib.Deserializable()` | `return lib.Deserializable(resp, parser, ctx)` |
| Find XML elements | `lib.find_element()` | `results = lib.find_element("Name", el, Type)` |
| Convert to XML | `lib.to_xml()` | `xml = lib.to_xml(obj, name_="Root")` |
| Convert to dict | `lib.to_dict()` | `d = lib.to_dict(obj)` (filters None) |

---

## JSON Schema Files

### What are JSON schema files in karrio?

JSON schema files in karrio are **sample data files** (not JSON Schema definitions). They represent the actual request/response structures of carrier APIs with all fields populated with sample values.

Location: `modules/connectors/{carrier}/schemas/`

### Required Files

For a complete carrier integration, create these JSON sample files:

```
schemas/
├── shipping_request.json    # Create shipment request
├── shipping_response.json   # Create shipment response
├── tracking_request.json    # Tracking request (if applicable)
├── tracking_response.json   # Tracking response
├── void_request.json        # Cancel/void shipment request
├── void_response.json       # Cancel/void response
├── rating_request.json      # Rate request (if applicable)
├── rating_response.json     # Rate response
└── error_response.json      # Error response format
```

### How to Create Accurate JSON Samples

1. **Start from vendor documentation** - Always base schemas on official API docs, WSDL/XSD files, or sample requests/responses
2. **Include ALL fields** - Populate every field the API supports, even optional ones
3. **Use realistic sample values** - Use plausible test data, not placeholders like "?"
4. **Match exact field names** - Field names must match the API exactly (case-sensitive)
5. **Verify against vendor samples** - Cross-reference with actual vendor request/response examples

Example shipping request structure:

```json
{
  "ShipperAddress": {
    "Name1": "Sender Company GmbH",
    "AddressLine1": "Hauptstrasse",
    "HouseNumber": "123",
    "PostalCode": "1010",
    "City": "Wien",
    "CountryID": "AT",
    "Tel1": "+43 1 234567",
    "Email": "sender@example.com"
  },
  "RecipientAddress": {
    "Name1": "Recipient Company",
    "AddressLine1": "Empfangerweg",
    "HouseNumber": "456",
    "PostalCode": "8010",
    "City": "Graz",
    "CountryID": "AT"
  },
  "Packages": [
    {
      "Weight": 5.5,
      "Length": 30.0,
      "Width": 20.0,
      "Height": 15.0
    }
  ]
}
```

### Generating Python Dataclasses

JSON samples are used to generate Python dataclasses:

```bash
# Generate schemas for a carrier
./bin/run-generate-on {carrier_name}

# This creates Python modules in:
# karrio/schemas/{carrier_name}/
```

### Verification Checklist

Before committing schema files, verify:

- [ ] All fields from vendor documentation are included
- [ ] Field names match exactly (case-sensitive)
- [ ] Data types are correct (string, number, boolean, array, object)
- [ ] Nested structures match the API hierarchy
- [ ] Sample values are realistic and valid
- [ ] Error response format matches actual API errors

### Common Mistakes

1. **Using JSON Schema format** - karrio uses sample data, not JSON Schema definitions
2. **Missing fields** - Include all fields, even optional ones with sample values
3. **Wrong field names** - Copy exact names from vendor docs
4. **Inventing fields** - Only include fields documented by the carrier
5. **Generic placeholders** - Use realistic test data, not "sample" or "?"

---

## Multi-Piece/Multi-Package Shipments

### How does karrio handle multi-package shipments?

Karrio supports two distinct patterns for multi-package shipments, depending on how the carrier API is designed:

1. **Bundled Request Pattern** - All packages in a single API request
2. **Per-Package Request Pattern** - Separate API request for each package

### Pattern 1: Bundled Request (FedEx, UPS, DHL Express, Purolator)

These carriers accept all packages in a **single request** and return a **master tracking number** with individual package results.

#### Request Structure
```python
# All packages in one request
request = ShipmentRequestType(
    packages=[
        PackageType(weight=pkg1.weight, dimensions=pkg1.dims),
        PackageType(weight=pkg2.weight, dimensions=pkg2.dims),
        # ... more packages
    ]
)
return lib.Serializable(request, lib.to_dict)
```

#### Response Parsing
```python
def parse_shipment_response(_response, settings):
    response = _response.deserialize()

    # Extract master tracking number
    tracking_number = response.masterTrackingNumber  # or ShipmentIdentificationNumber

    # Extract individual package tracking numbers
    packages = lib.failsafe(lambda: response.PackageResults) or []
    tracking_ids = [pkg.TrackingID for pkg in packages if pkg.TrackingID]

    # Bundle all labels into single document
    labels = [pkg.Label for pkg in packages if pkg.Label]
    label = lib.bundle_base64(labels, "PDF") if len(labels) > 1 else next(iter(labels), None)

    return models.ShipmentDetails(
        tracking_number=tracking_number,
        shipment_identifier=response.ShipmentID,
        docs=models.Documents(label=label),
        meta=dict(
            tracking_numbers=tracking_ids,  # All package tracking numbers
        ),
    ), messages
```

### Pattern 2: Per-Package Request (Canada Post, USPS, Teleship)

These carriers require **separate API requests** for each package. Karrio aggregates the responses using `lib.to_multi_piece_shipment()`.

#### Request Structure
```python
def shipment_request(payload, settings):
    packages = lib.to_packages(payload.parcels)

    # Create list of requests, one per package
    request = [
        ShipmentType(
            # ... common shipment data
            parcel_characteristics=ParcelCharacteristicsType(
                weight=pkg.weight.KG,
                dimensions=DimensionsType(length=pkg.length.CM, ...),
            ),
        )
        for pkg in packages  # One request per package
    ]

    return lib.Serializable(request, serializer)
```

#### Response Parsing with `lib.to_multi_piece_shipment()`
```python
def parse_shipment_response(_response, settings):
    responses = _response.deserialize()  # List of responses
    messages = error.parse_error_response(responses, settings)

    # Extract details from each package response
    shipment_details = [
        (f"{idx}", _extract_shipment(response, settings))
        for idx, response in enumerate(responses, start=1)
        if _is_valid_response(response)
    ]

    # Combine into single ShipmentDetails
    shipment = lib.to_multi_piece_shipment(shipment_details)
    return shipment, messages
```

### What does `lib.to_multi_piece_shipment()` do?

This utility function combines multiple individual shipment responses into a single master shipment:

**Input:** `List[Tuple[str, ShipmentDetails]]` - List of (package_id, shipment_details) tuples

**Output:** Single `ShipmentDetails` with:
- `tracking_number`: from first package (master)
- `shipment_identifier`: from first package (master)
- `docs.label`: bundled labels from all packages via `lib.bundle_base64()`
- `meta['tracking_numbers']`: list of all tracking numbers
- `meta['shipment_identifiers']`: list of all shipment IDs

### What is `lib.bundle_base64()`?

This function combines multiple base64-encoded labels (typically PDFs) into a single document:

```python
# Bundle multiple labels into one PDF
labels = [pkg.Label for pkg in packages if pkg.Label]
combined_label = lib.bundle_base64(labels, "PDF")
```

### How do I determine which pattern to use?

Check the carrier API documentation:

| API Behavior | Pattern to Use |
|-------------|----------------|
| Single endpoint accepts array of packages | **Bundled Pattern** |
| Response includes `PackageResults` or `pieceResponses` | **Bundled Pattern** |
| Response has `masterTrackingNumber` | **Bundled Pattern** |
| Must call endpoint once per package | **Per-Package Pattern** |
| Each package gets separate label/tracking | **Per-Package Pattern** |

### Standard Meta Fields for Multi-Piece

Always populate these meta fields for multi-package shipments:

```python
meta=dict(
    tracking_numbers=["TRK001", "TRK002", "TRK003"],  # All package tracking
    shipment_identifiers=["SHIP001", "SHIP002"],      # All shipment IDs (if different)
    carrier_tracking_link="https://...",              # Link for master tracking
)
```

### Comparison Table

| Carrier | Request Type | Master Tracking | Label Handling | Aggregation Method |
|---------|-------------|-----------------|----------------|-------------------|
| **FedEx** | Single bundled | `masterTrackingNumber` | `pieceDocuments` bundled | Built-in response |
| **UPS** | Single bundled | `ShipmentIdentificationNumber` | `PackageResults` bundled | Built-in response |
| **DHL Express** | Single bundled | `AirwayBillNumber` | `MultiLabel` structure | Built-in response |
| **Canada Post** | Multiple separate | First package | Per-package combined | `lib.to_multi_piece_shipment()` |
| **USPS** | Multiple separate | First package | Per-package combined | `lib.to_multi_piece_shipment()` |

---

## See Also

- [CARRIER_INTEGRATION_GUIDE.md](./CARRIER_INTEGRATION_GUIDE.md) - Complete integration guide
- [AGENTS.md](./AGENTS.md) - Project conventions and guidelines
