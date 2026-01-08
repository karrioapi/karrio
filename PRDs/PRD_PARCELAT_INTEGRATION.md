# PRD: ParcelAT (Austrian Post - Post-Labelcenter) Integration

## Overview

**Carrier Name:** ParcelAT (Österreichische Post - Post-Labelcenter/PLC)
**Country:** Austria
**API Type:** SOAP/XML
**Integration Priority:** High
**Current Status:** Skeleton only (vendor docs present, no Python implementation)

## Executive Summary

ParcelAT is the integration for Austrian Post's Post-Labelcenter (PLC) Webservice. This is Austria's national postal carrier offering domestic and international shipping services. The API uses SOAP/XML over HTTPS with organization-based authentication.

## API Documentation

### Endpoints

| Environment | Endpoint | Notes |
|-------------|----------|-------|
| Production | Provided by Austrian Post upon onboarding | WSDL not publicly available |
| Sandbox | Provided by Austrian Post upon onboarding | For testing |

**Note:** Austrian Post does not publicly expose WSDL URLs. The endpoint and WSDL are provided during customer onboarding through their Post-Labelcenter portal.

### Authentication

Authentication uses organization-based identifiers:

| Credential | Type | Description |
|------------|------|-------------|
| `client_id` | string | ClientID assigned by Austrian Post |
| `org_unit_id` | string | OrgUnitID for the organizational unit |
| `org_unit_guid` | string | OrgUnitGuid (UUID format) |

### XML Namespaces

```xml
xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:post="http://post.ondot.at"
xmlns:arr="http://schemas.microsoft.com/2003/10/Serialization/Arrays"
xmlns:core="http://Core.Model"
xmlns:ser="http://schemas.microsoft.com/2003/10/Serialization/"
```

## Supported Capabilities

### 1. Shipment Creation (Required)

**Operation:** `ImportShipment` / `ImportShipmentAndGenerateBarcode`

**Karrio Mapping:**
- `karrio.Shipment.create()` → `ImportShipment`

**Request Structure:**
```xml
<post:ImportShipment>
  <post:row>
    <post:ClientID>{client_id}</post:ClientID>
    <post:OrgUnitID>{org_unit_id}</post:OrgUnitID>
    <post:OrgUnitGuid>{org_unit_guid}</post:OrgUnitGuid>
    <post:DeliveryServiceThirdPartyID>{service_code}</post:DeliveryServiceThirdPartyID>
    <post:ColloList>
      <post:ColloRow>
        <post:Weight>{weight_kg}</post:Weight>
      </post:ColloRow>
    </post:ColloList>
    <post:OURecipientAddress>
      <post:Name1>{recipient_name}</post:Name1>
      <post:AddressLine1>{street}</post:AddressLine1>
      <post:HouseNumber>{house_number}</post:HouseNumber>
      <post:PostalCode>{postal_code}</post:PostalCode>
      <post:City>{city}</post:City>
      <post:CountryID>{country_code}</post:CountryID>
      <post:Email>{email}</post:Email>
    </post:OURecipientAddress>
    <post:OUShipperAddress>
      <post:Name1>{shipper_name}</post:Name1>
      <post:AddressLine1>{street}</post:AddressLine1>
      <post:PostalCode>{postal_code}</post:PostalCode>
      <post:City>{city}</post:City>
      <post:CountryID>{country_code}</post:CountryID>
    </post:OUShipperAddress>
    <post:PrinterObject>
      <post:LabelFormatID>{label_size}</post:LabelFormatID>
      <post:LanguageID>{label_format}</post:LanguageID>
      <post:PaperLayoutID>{paper_layout}</post:PaperLayoutID>
    </post:PrinterObject>
  </post:row>
</post:ImportShipment>
```

**Response Contains:**
- Tracking number / barcode
- Label data (base64 PDF or ZPL2)
- Shipment ID

### 2. Shipment Cancellation (Required)

**Operation:** `CancelShipments`

**Karrio Mapping:**
- `karrio.Shipment.cancel()` → `CancelShipments`

### 3. Manifest / End of Day (Optional but Recommended)

**Operations:**
- `PerformEndOfDay` - Close out shipments for the day
- `PerformEndOfDaySelect` - Selective end of day

**Karrio Mapping:**
- `karrio.Manifest.create()` → `PerformEndOfDay`

### 4. Pickup Scheduling (Optional)

**Operations:**
- `GetAvailableTimeWindowsForPickupOrder` - Get available pickup times
- `ImportPickupOrder` - Schedule a pickup
- `CancelPickupOrder` - Cancel scheduled pickup

**Karrio Mapping:**
- `karrio.Pickup.schedule()` → `ImportPickupOrder`
- `karrio.Pickup.cancel()` → `CancelPickupOrder`

### 5. Service Discovery (Helper)

**Operation:** `GetAllowedServicesForCountry`

Used to validate and discover available services for destination countries.

## Data Models

### ShipmentRow (Main Request Object)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ClientID | int | Yes | Client identifier |
| OrgUnitID | int | Yes | Organization unit ID |
| OrgUnitGuid | string | Yes | Organization GUID |
| DeliveryServiceThirdPartyID | string | Yes | Service code |
| OURecipientAddress | Address | Yes | Recipient address |
| OUShipperAddress | Address | No | Shipper address (if different from default) |
| ColloList | ColloRow[] | Yes | Package list |
| PrinterObject | PrinterObject | No | Label output settings |

### ColloRow (Package)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Weight | decimal | Yes | Package weight in kg |
| ColloCode | string | No | Package identifier |
| ColloArticles | array | No | Items in package (for customs) |

### Address

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Name1 | string | Yes | Primary name |
| Name2 | string | No | Secondary name |
| AddressLine1 | string | Yes | Street address |
| AddressLine2 | string | No | Additional address |
| HouseNumber | string | No | House number |
| PostalCode | string | Yes | Postal code |
| City | string | Yes | City |
| CountryID | string | Yes | ISO country code |
| Email | string | No | Email address |

### PrinterObject (Label Settings)

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| LabelFormatID | string | `100x200`, `100x150` | Label dimensions |
| LanguageID | string | `pdf`, `zpl2` | Output format |
| PaperLayoutID | string | `2xA5inA4`, `1xA6` | Paper layout |

## Service Codes

**Note:** Service codes (`DeliveryServiceThirdPartyID`) are configured per account by Austrian Post. Common examples include:

| Code | Service | Description |
|------|---------|-------------|
| 10 | Standard Domestic | Standard domestic parcel |
| 20 | Express Domestic | Express domestic delivery |
| 30 | International Standard | International standard |
| 40 | International Express | International express |

**Implementation Note:** Services should be configurable via `ConnectionConfig.shipping_services` to allow customers to map their account-specific service codes.

## Label Formats

| Format | Description |
|--------|-------------|
| PDF | Base64-encoded PDF label |
| ZPL2 | ZPL string for thermal printers |

## Implementation Architecture

### File Structure

```
modules/connectors/parcelat/
├── karrio/
│   ├── schemas/parcelat/
│   │   ├── __init__.py
│   │   └── plc_types.py          # Generated from XSD or manual
│   ├── mappers/parcelat/
│   │   ├── __init__.py
│   │   ├── mapper.py
│   │   ├── proxy.py
│   │   └── settings.py
│   └── providers/parcelat/
│       ├── __init__.py
│       ├── units.py
│       ├── error.py
│       ├── utils.py
│       ├── shipment/
│       │   ├── __init__.py
│       │   └── create.py
│       ├── pickup.py             # Optional
│       └── manifest.py           # Optional
├── tests/
│   └── parcelat/
│       ├── __init__.py
│       ├── fixture.py
│       ├── test_shipment.py
│       └── test_pickup.py
├── generate                      # Schema generation script
└── setup.py
```

### Settings Model

```python
@attr.s(auto_attribs=True)
class Settings(core.Settings):
    client_id: str
    org_unit_id: str
    org_unit_guid: str

    # Optional
    label_format: str = "pdf"
    label_size: str = "100x200"
    paper_layout: str = "2xA5inA4"

    id: str = None
    test_mode: bool = False
    carrier_id: str = "parcelat"
    account_country_code: str = "AT"
    metadata: dict = {}
    config: dict = {}

    @property
    def carrier_name(self):
        return "parcelat"

    @property
    def server_url(self):
        # URL provided during onboarding
        return (
            self.connection_config.server_url.state
            or "https://plc.post.at/services"  # Placeholder
        )
```

### Units Definition

```python
class ShippingService(lib.StrEnum):
    parcelat_standard_domestic = "10"
    parcelat_express_domestic = "20"
    parcelat_international_standard = "30"
    parcelat_international_express = "40"

class LabelFormat(lib.StrEnum):
    PDF = "pdf"
    ZPL2 = "zpl2"

class LabelSize(lib.StrEnum):
    SIZE_100x200 = "100x200"
    SIZE_100x150 = "100x150"

class ShippingOption(lib.Enum):
    parcelat_cod = lib.OptionEnum("COD", float)
    parcelat_signature = lib.OptionEnum("SIG", bool)
    parcelat_saturday_delivery = lib.OptionEnum("SAT", bool)
    insurance = lib.OptionEnum("INS", float)
```

### Proxy Implementation Pattern

```python
class Proxy(proxy.Proxy):
    settings: Settings

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/ImportShipment",
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": "http://post.ondot.at/ImportShipment",
            },
        )
        return lib.Deserializable(response, lib.to_element)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/CancelShipments",
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": "http://post.ondot.at/CancelShipments",
            },
        )
        return lib.Deserializable(response, lib.to_element)
```

## Testing Strategy

### Unit Tests Required

1. **test_create_shipment_request** - Verify XML request structure
2. **test_create_shipment** - Mock HTTP call verification
3. **test_parse_shipment_response** - Response parsing
4. **test_parse_error_response** - Error handling
5. **test_cancel_shipment** - Cancellation flow
6. **test_create_manifest** - End of day processing

### Test Fixtures

Use sample request/response from `vendor/` directory:
- `request-example.txt` - Sample request
- `result-response.txt` - Sample response

## Integration Checklist

- [ ] Schema generation from XSD (or manual type definitions)
- [ ] Settings model with credentials
- [ ] Proxy with SOAP client
- [ ] Shipment creation (`ImportShipment`)
- [ ] Shipment cancellation (`CancelShipments`)
- [ ] Label retrieval (embedded in response)
- [ ] Manifest/EOD (`PerformEndOfDay`) - Optional
- [ ] Pickup scheduling - Optional
- [ ] Unit tests for all operations
- [ ] Documentation updates

## Dependencies

- Reference integrations: `chronopost`, `purolator` (SOAP patterns)
- Karrio SOAP utilities: `lib.Envelope`, `lib.Body`, `lib.envelope_serializer`

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| WSDL not publicly available | High | Work from vendor docs + sample requests |
| Service codes vary by account | Medium | Make services configurable |
| No public sandbox | Medium | Use mock responses for testing |

## Timeline Estimate

| Phase | Tasks | Effort |
|-------|-------|--------|
| Phase 1 | Schema + Settings + Proxy | 2-3 days |
| Phase 2 | Shipment create/cancel | 2-3 days |
| Phase 3 | Label handling + tests | 1-2 days |
| Phase 4 | Optional features (EOD, Pickup) | 2-3 days |

**Total Estimate:** 7-11 days

## Approval Requirements

Before implementation:
1. Confirm WSDL/endpoint access from Austrian Post
2. Obtain test credentials for sandbox
3. Validate service codes for target accounts
