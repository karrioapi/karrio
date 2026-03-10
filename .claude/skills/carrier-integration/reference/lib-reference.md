# karrio.lib Utilities Reference

Complete reference for `karrio.lib` — always import as `import karrio.lib as lib`.

## Data Parsing & Conversion

```python
# JSON/Dict
lib.to_dict(response)              # Parse JSON string or object to dict
lib.to_dict_safe(response)         # Safe parse - returns {} on error, NEVER raises
lib.to_json(data)                  # Serialize to JSON string
lib.to_object(SchemaType, data)    # CRITICAL: Convert dict to typed schema object

# XML (for XML/SOAP APIs)
lib.to_element(xml_string)         # Parse XML string to Element
lib.to_xml(typed_xml_object)       # Serialize XML object to string
lib.find_element("tag", element)   # Find element in XML tree
lib.create_envelope(body, header)  # Create SOAP envelope
lib.envelope_serializer(envelope)  # Serialize SOAP envelope
```

## String Manipulation

```python
lib.text("value1", "value2")          # "value1 value2" (joins, ignores None)
lib.text("a", "b", separator=", ")    # "a, b"
lib.text("long text", max=10)         # Truncate to max length
lib.text("  padded  ", trim=True)     # "padded"

lib.join("a", "b")                    # ["a", "b"] (list)
lib.join("a", "b", join=True)         # "a b" (string)

lib.to_snake_case("CamelCase")        # "camel_case"
lib.to_slug("My Service")             # "my_service"
```

## Number Formatting

```python
lib.to_int("15.7")                    # 15
lib.to_decimal(14.899)                # 14.90
lib.to_money(25.999)                  # 26.00
lib.format_decimal(14.899, 1)         # 14.9
lib.to_list("single")                 # ["single"]
lib.to_list(None)                     # []
```

## Date & Time

```python
lib.fdate("2024-01-15")                              # "YYYY-MM-DD"
lib.fdate("01/15/2024", current_format="%m/%d/%Y")   # Parse custom format
lib.ftime("14:30:00")                                # "HH:MM"
lib.flocaltime("14:30:00")                           # "02:30 PM"
lib.fdatetime("2024-01-15 14:30:00")                 # Full datetime
lib.ftimestamp("1705334400")                         # Unix to datetime
lib.fiso_timestamp("2024-01-15", "14:30")            # ISO 8601
lib.to_date("2024-01-15")                            # datetime object
```

## Address Utilities

```python
address = lib.to_address(payload.shipper)  # Wraps with computed fields

# Computed properties available after wrapping:
address.person_name      # Falls back to company_name
address.street           # Combined street address
address.tax_id           # federal_tax_id or state_tax_id
address.contact          # person_name or company_name

lib.to_zip5("12345-6789")             # "12345"
lib.to_zip4("12345-6789")             # "6789"
lib.to_country_name("US")             # "United States"
lib.to_state_name("CA", "US")         # "California"
```

## Shipping Data Conversion

```python
# Packages (with presets and options)
packages = lib.to_packages(
    payload.parcels,
    presets=provider_units.PackagePresets,
    options=payload.options,
    package_option_type=provider_units.ShippingOption,
)
packages.weight.LB        # Total weight in pounds
packages.weight.KG        # Total weight in kilograms

# Services
services = lib.to_services(payload.services, provider_units.ShippingService)
services.first            # First service or None
# Each service has: svc.name_or_key (karrio name), svc.value_or_key (carrier code)

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

## Multi-Piece Shipments

```python
# Combine rates from per-package requests
combined_rates = lib.to_multi_piece_rates([
    ("pkg_1", [rate1, rate2]),
    ("pkg_2", [rate1, rate2]),
])

# Combine shipment details into master shipment
master_shipment = lib.to_multi_piece_shipment([
    ("pkg_1", shipment_details_1),
    ("pkg_2", shipment_details_2),
])
```

## HTTP & Concurrent Execution

```python
# HTTP request (used in Proxy classes)
response = lib.request(
    url="https://api.carrier.com/endpoint",
    data=lib.to_json(request_body),
    method="POST",
    headers={"Authorization": f"Bearer {token}"},
    trace=proxy.trace_as("json"),  # or "xml"
)

# URL encoding
lib.to_query_string({"key": "value"})  # "key=value"

# Concurrent execution (e.g., multi-tracking)
results = lib.run_concurently(fetch_func, items, max_workers=2)

# Async execution
results = lib.run_asynchronously(async_func, items)
```

## Document Processing

```python
lib.image_to_pdf(image_base64)           # Convert image to PDF
lib.bundle_pdfs([pdf1, pdf2])            # Merge multiple PDFs
lib.bundle_base64([doc1, doc2], "PDF")   # Bundle any docs as base64
lib.zpl_to_pdf(zpl_str, 4, 6)           # ZPL label to PDF
lib.encode_base64(bytes_data)            # Encode to base64
lib.decode(bytes_data)                   # Decode with fallbacks
```

## Safe Utilities

```python
lib.failsafe(lambda: risky_op())         # Returns None on exception
lib.identity(value if condition else None)  # Conditional value passing
lib.sort_events(events)                  # Sort tracking events chronologically
lib.to_buffer(content)                   # Convert to BytesIO buffer
```

## Serializable / Deserializable Pattern

```python
# Request wrapping (provider → proxy)
request = lib.Serializable(
    data=carrier_request_obj,
    serialize=lambda obj: lib.to_dict(obj, serialize=True),
    ctx={"shipment_date": "2024-02-15"},  # Metadata for response parsing
)

# Response wrapping (proxy → provider)
response = lib.Deserializable(
    data=carrier_api_response,
    deserialize=lib.to_dict,
    ctx=request.ctx,  # Inherit request context
)
```
