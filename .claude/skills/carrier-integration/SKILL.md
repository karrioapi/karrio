---
name: carrier-integration
description: Builds Karrio shipping carrier integrations from scratch. Covers scaffolding, schema generation, provider implementation (rating, shipping, tracking, pickup, manifest, document upload, address validation), and testing. Triggers on requests to add a new carrier, implement shipping features, build carrier connectors, or integrate carrier APIs with Karrio.
disable-model-invocation: true
---

# Karrio Carrier Integration

Expert guidance for building Karrio shipping carrier integrations. Covers all features, API patterns (JSON/XML/SOAP), and the complete development lifecycle.

## Before You Start

1. Read [CARRIER_INTEGRATION_GUIDE.md](../../CARRIER_INTEGRATION_GUIDE.md) for the comprehensive step-by-step guide
2. Read [CARRIER_INTEGRATION_FAQ.md](../../CARRIER_INTEGRATION_FAQ.md) for common pitfalls and patterns
3. Read [AGENTS.md](../../AGENTS.md) for project conventions and coding style

## Core Principles

1. **CLI Tooling is Mandatory**: Always use `./bin/cli sdk add-extension` for scaffolding. NEVER create files manually.
2. **Environment First**: Run `source ./bin/activate-env` before any operation.
3. **Schema-Driven**: Use generated schema types for ALL request/response handling. NEVER use raw dict manipulation.
4. **Functional Style**: Use list comprehensions, `lib.*` utilities, and declarative patterns. No imperative loops.
5. **Pattern Replication**: Study existing integrations before implementing.
6. **Type Safety**: Always use `lib.to_object(SchemaType, data)` for response parsing.

## Reference Carriers

| Pattern | Carrier | Path |
|---------|---------|------|
| JSON API (direct) | SEKO | `modules/connectors/seko` |
| JSON API (full) | UPS | `modules/connectors/ups` |
| XML API | Canada Post | `modules/connectors/canadapost` |
| Hub carrier | Easyship | `community/plugins/easyship` |
| OAuth flow | FedEx | `modules/connectors/fedex` |

## Integration Workflow

### Phase 1: Setup & Scaffolding

```bash
# 1. Activate environment (ALWAYS FIRST)
source ./bin/activate-env

# 2. Bootstrap extension
./bin/cli sdk add-extension \
  --path [modules/connectors OR community/plugins] \
  --carrier-slug [carrier_slug] \
  --display-name "[Carrier Name]" \
  --features "rating,shipping,tracking" \
  --no-is-xml-api \
  --version "2025.5" \
  --confirm
```

### Phase 2: Schema Generation

1. Add API request/response JSON samples to `schemas/` directory
2. Configure `generate` script with correct CLI flags:
   - `--nice-property-names` for snake_case APIs
   - `--no-nice-property-names` for camelCase APIs
   - `--no-append-type-suffix --no-nice-property-names` for PascalCase APIs
3. Run: `chmod +x [path]/generate && ./bin/run-generate-on [path]`
4. Verify: `python -c "import karrio.schemas.[carrier] as s; print(dir(s))"`

### Phase 3: Implementation

Implement files in this order:

1. **Settings** (`karrio/providers/[carrier]/utils.py`): Carrier credentials, server URLs, OAuth
2. **Units** (`karrio/providers/[carrier]/units.py`): Services, options, tracking status enums
3. **Error** (`karrio/providers/[carrier]/error.py`): Error response parser
4. **Proxy** (`karrio/mappers/[carrier]/proxy.py`): HTTP communication layer
5. **Provider functions**: Rate, tracking, shipment, etc.

For detailed implementation patterns, see:
- [reference/lib-reference.md](reference/lib-reference.md) - Complete karrio.lib API
- [reference/response-models.md](reference/response-models.md) - All response model shapes
- [reference/implementation-patterns.md](reference/implementation-patterns.md) - Provider function patterns
- [reference/testing-patterns.md](reference/testing-patterns.md) - Test writing guide
- [reference/units-template.md](reference/units-template.md) - Units file template

### Phase 4: Testing

Every feature requires the **4-method test pattern**:

```python
class TestCarrierFeature(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.Request = models.FeatureRequest(**Payload)

    def test_create_request(self):
        request = gateway.mapper.create_feature_request(self.Request)
        print(request.serialize())  # ALWAYS print before assert
        self.assertEqual(lib.to_dict(request.serialize()), ExpectedRequest)

    def test_api_call(self):
        with patch("karrio.mappers.[carrier].proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Feature.action(self.Request).from_(gateway)
            self.assertEqual(mock.call_args[1]["url"], ExpectedURL)

    def test_parse_response(self):
        with patch("karrio.mappers.[carrier].proxy.lib.request") as mock:
            mock.return_value = SuccessResponse
            result = karrio.Feature.action(self.Request).from_(gateway).parse()
            print(result)  # ALWAYS print before assert
            self.assertListEqual(lib.to_dict(result), ExpectedResult)

    def test_parse_error(self):
        with patch("karrio.mappers.[carrier].proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            result = karrio.Feature.action(self.Request).from_(gateway).parse()
            print(result)  # ALWAYS print before assert
            self.assertListEqual(lib.to_dict(result), ExpectedError)
```

### Phase 5: Validation

```bash
# All must pass before integration is complete
python -m unittest discover -v -f [path]/tests    # Carrier tests
./bin/run-sdk-tests                                # SDK tests
./bin/cli plugins list | grep [carrier]            # Plugin registered
./bin/cli plugins show [carrier]                   # Plugin details
pip install -e [path]                              # Installation works
```

## Connector Directory Structure

```
[carrier]/
├── pyproject.toml
├── generate                          # Schema generation script
├── schemas/                          # JSON/XML API samples
│   ├── rate_request.json
│   ├── rate_response.json
│   └── ...
├── karrio/
│   ├── plugins/[carrier]/__init__.py # Plugin METADATA
│   ├── mappers/[carrier]/
│   │   ├── __init__.py               # Exports Mapper, Proxy, Settings
│   │   ├── mapper.py                 # DO NOT MODIFY (auto-generated)
│   │   ├── proxy.py                  # HTTP communication
│   │   └── settings.py               # Connection settings
│   ├── providers/[carrier]/
│   │   ├── __init__.py               # Public exports
│   │   ├── utils.py                  # Settings + server URLs
│   │   ├── units.py                  # Enums (services, options)
│   │   ├── error.py                  # Error parsing
│   │   ├── rate.py                   # Rating implementation
│   │   ├── tracking.py              # Tracking implementation
│   │   └── shipment/
│   │       ├── create.py             # Shipment creation
│   │       └── cancel.py             # Shipment cancellation
│   └── schemas/[carrier]/            # Generated Python types (DO NOT EDIT)
└── tests/[carrier]/
    ├── fixture.py                    # Test gateway + mock data
    ├── test_rate.py
    ├── test_tracking.py
    └── test_shipment.py
```

## Supported Features

| Feature | Request Model | Response Model | Provider File |
|---------|--------------|----------------|---------------|
| Rating | RateRequest | RateDetails | rate.py |
| Shipping | ShipmentRequest | ShipmentDetails | shipment/create.py, cancel.py |
| Tracking | TrackingRequest | TrackingDetails | tracking.py |
| Pickup | PickupRequest | PickupDetails | pickup/create.py, update.py, cancel.py |
| Manifest | ManifestRequest | ManifestDetails | manifest.py |
| Document | DocumentUploadRequest | DocumentUploadDetails | document.py |
| Address | AddressValidationRequest | AddressValidationDetails | address.py |

## Anti-Patterns

- Manual file creation instead of CLI scaffolding
- Raw dict manipulation instead of generated schema types
- Imperative for-loops instead of list comprehensions
- Modifying `mapper.py` (auto-generated, do not touch)
- Editing generated schema files in `karrio/schemas/`
- Using pytest instead of unittest
- Bare exception handling
- Reinventing `karrio.lib` utilities
- Not using `lib.to_object()` for response parsing
- Not using `lib.to_address()` for address handling
- Hardcoding service/option codes instead of enums
