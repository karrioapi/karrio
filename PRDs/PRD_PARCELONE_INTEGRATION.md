# PRD: ParcelOne (Germany) Integration

## Overview

**Carrier Name:** ParcelOne (parcel.one)
**Country:** Germany
**API Type:** SOAP/WCF (Windows Communication Foundation) with WS-Security
**Integration Priority:** High
**Current Status:** Skeleton with WSDL/XSD present, no Python implementation

## Executive Summary

ParcelOne is a German multi-carrier shipping platform that provides access to multiple CEPs (Courier, Express, Parcel services) through a unified API. The API uses SOAP over WCF with WS-Security (UsernameToken) authentication. Full WSDL and XSD schemas are available.

## API Documentation

### Endpoints

| Environment | Service URL | WSDL URL |
|-------------|-------------|----------|
| Sandbox | https://sandboxapi.awiwe.solutions/version4/shippingwcfsandbox/ShippingWCF.svc | https://sandboxapi.awiwe.solutions/version4/shippingwcfsandbox/ShippingWCF.svc?wsdl |
| Production | https://productionapi.awiwe.solutions/version4/shippingwcf/ShippingWCF.svc | https://productionapi.awiwe.solutions/version4/shippingwcf/ShippingWCF.svc?wsdl |

### Authentication

**WS-Security with UsernameToken:**

| Credential | Type | Description |
|------------|------|-------------|
| `username` | string | API username |
| `password` | string | API password |
| `api_key` | string | Additional API key (header) |

**SOAP Header Structure:**
```xml
<wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
  <wsse:UsernameToken>
    <wsse:Username>{username}</wsse:Username>
    <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{password}</wsse:Password>
  </wsse:UsernameToken>
</wsse:Security>
```

### XML Namespaces

```xml
xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:tns="http://tempuri.org/"
xmlns:wcf="http://schemas.datacontract.org/2004/07/ShippingWCF"
xmlns:arr="http://schemas.microsoft.com/2003/10/Serialization/Arrays"
xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"
```

## Supported Capabilities

### 1. Shipment Creation (Required)

**Operation:** `registerShipments`

**Karrio Mapping:**
- `karrio.Shipment.create()` → `registerShipments`

**Request Structure:**
```xml
<tns:registerShipments>
  <tns:ShippingData>
    <wcf:Shipment>
      <wcf:MandatorID>{mandator_id}</wcf:MandatorID>
      <wcf:ConsignerID>{consigner_id}</wcf:ConsignerID>
      <wcf:CEPID>{carrier_code}</wcf:CEPID>
      <wcf:ProductID>{product_code}</wcf:ProductID>
      <wcf:Software>Karrio</wcf:Software>
      <wcf:ShipToData>
        <wcf:Name1>{recipient_name}</wcf:Name1>
        <wcf:ShipmentAddress>
          <wcf:Street>{street}</wcf:Street>
          <wcf:Streetno>{street_number}</wcf:Streetno>
          <wcf:PostalCode>{postal_code}</wcf:PostalCode>
          <wcf:City>{city}</wcf:City>
          <wcf:Country>{country_code}</wcf:Country>
        </wcf:ShipmentAddress>
        <wcf:ShipmentContact>
          <wcf:Email>{email}</wcf:Email>
          <wcf:Phone>{phone}</wcf:Phone>
        </wcf:ShipmentContact>
      </wcf:ShipToData>
      <wcf:ShipFromData>
        <wcf:Name1>{shipper_name}</wcf:Name1>
        <wcf:ShipmentAddress>...</wcf:ShipmentAddress>
      </wcf:ShipFromData>
      <wcf:Packages>
        <wcf:ShipmentPackage>
          <wcf:PackageWeight>
            <wcf:Value>{weight}</wcf:Value>
            <wcf:Unit>KG</wcf:Unit>
          </wcf:PackageWeight>
          <wcf:PackageDimensions>
            <wcf:Length>{length}</wcf:Length>
            <wcf:Width>{width}</wcf:Width>
            <wcf:Height>{height}</wcf:Height>
            <wcf:Measurement>CM</wcf:Measurement>
          </wcf:PackageDimensions>
        </wcf:ShipmentPackage>
      </wcf:Packages>
      <wcf:Services>
        <wcf:ShipmentService>
          <wcf:ServiceID>{service_option}</wcf:ServiceID>
        </wcf:ShipmentService>
      </wcf:Services>
      <wcf:LabelFormat>
        <wcf:Type>PDF</wcf:Type>
        <wcf:Size>100x150</wcf:Size>
      </wcf:LabelFormat>
      <wcf:PrintLabel>1</wcf:PrintLabel>
    </wcf:Shipment>
  </tns:ShippingData>
</tns:registerShipments>
```

**Response (ShipmentResult):**
- `ActionResult.Success` - 1 for success, 0 for failure
- `ActionResult.TrackingID` - Tracking number
- `ActionResult.ShipmentID` - Internal shipment ID
- `PackageResults[].Label` - Base64 label per package
- `PackageResults[].TrackingID` - Package tracking number
- `TotalCharges` - Shipping cost
- `LabelURL` - Optional label download URL

### 2. Label Retrieval (Required)

**Operations:**
- `printLabel` - Get label by shipment reference
- `printDocuments` - Get shipping documents
- `printInternationalDocuments` - Get customs documents

**Karrio Mapping:**
- Embedded in `registerShipments` response when `PrintLabel=1`
- `karrio.Shipment.create()` returns label in `docs.label`

### 3. Shipment Cancellation (Required)

**Operation:** `voidShipments`

**Karrio Mapping:**
- `karrio.Shipment.cancel()` → `voidShipments`

**Request:**
```xml
<tns:voidShipments>
  <tns:ShippingData>
    <wcf:identifyShipment>
      <wcf:ShipmentRefField>TrackingID</wcf:ShipmentRefField>
      <wcf:ShipmentRefValue>{tracking_number}</wcf:ShipmentRefValue>
    </wcf:identifyShipment>
  </tns:ShippingData>
</tns:voidShipments>
```

### 4. Tracking (Required)

**Operation:** `getTrackings`

**Karrio Mapping:**
- `karrio.Tracking.fetch()` → `getTrackings`

**Request:**
```xml
<tns:getTrackings>
  <tns:ShippingData>
    <wcf:identifyShipment>
      <wcf:ShipmentRefField>TrackingID</wcf:ShipmentRefField>
      <wcf:ShipmentRefValue>{tracking_number}</wcf:ShipmentRefValue>
    </wcf:identifyShipment>
  </tns:ShippingData>
</tns:getTrackings>
```

**Response (ShipmentTrackingResult):**
- `Trackings[].TrackingDateTime`
- `Trackings[].TrackingLocation`
- `Trackings[].TrackingStatus`
- `Trackings[].TrackingStatusCode`

### 5. Rating (Required)

**Operation:** `getCharges`

**Karrio Mapping:**
- `karrio.Rating.fetch()` → `getCharges`

**Request:**
```xml
<tns:getCharges>
  <tns:ChargesData>
    <wcf:Charges>
      <wcf:MandatorID>{mandator_id}</wcf:MandatorID>
      <wcf:ConsignerID>{consigner_id}</wcf:ConsignerID>
      <wcf:CEPID>{carrier_code}</wcf:CEPID>
      <wcf:ProductID>{product_code}</wcf:ProductID>
      <wcf:ShipToAddress>
        <wcf:PostalCode>{postal_code}</wcf:PostalCode>
        <wcf:Country>{country_code}</wcf:Country>
      </wcf:ShipToAddress>
      <wcf:Packages>
        <wcf:ShipmentPackage>
          <wcf:PackageWeight>
            <wcf:Value>{weight}</wcf:Value>
            <wcf:Unit>KG</wcf:Unit>
          </wcf:PackageWeight>
        </wcf:ShipmentPackage>
      </wcf:Packages>
    </wcf:Charges>
  </tns:ChargesData>
</tns:getCharges>
```

**Response (ChargesResult):**
- `TotalCharges.Value` - Total amount
- `TotalCharges.Currency` - Currency code
- `PackageResults[].Charges[]` - Per-package charges

### 6. Manifest / Close Shipments (Optional)

**Operations:**
- `closeShipments` - Close out shipments
- `getClosableShipments` - List shipments ready to close
- `getClosedStamps` - Get closed stamps history

**Karrio Mapping:**
- `karrio.Manifest.create()` → `closeShipments`

### 7. Service Discovery (Helper)

**Operations:**
- `getCustomers` - Get customer accounts
- `getProfiles` - Get shipping profiles
- `getCEPs` - Get available carriers
- `getProducts` - Get products per carrier
- `getServices` - Get service options

These are useful for dynamic service configuration.

### 8. International Documents (Optional)

**Operation:** `registerIntDoc`

For customs documentation on international shipments.

## Data Models

### Shipment

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| MandatorID | string | Yes | Account/mandator identifier |
| ConsignerID | string | Yes | Consigner identifier |
| CEPID | string | Yes | Carrier identifier (DHL, DPD, etc.) |
| ProductID | string | Yes | Product/service code |
| ShipToData | ShipTo | Yes | Recipient information |
| ShipFromData | ShipFrom | No | Shipper information |
| Packages | ShipmentPackage[] | Yes | Package list |
| Services | ShipmentService[] | No | Additional services |
| LabelFormat | Format | No | Label output format |
| PrintLabel | int | No | 1 to include label in response |
| PrintDocuments | int | No | 1 to include documents |
| Software | string | No | Integration identifier |
| ShipmentRef | string | No | Customer reference |
| ReturnShipmentIndicator | int | No | 1 for return shipment |

### ShipmentPackage

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| PackageWeight | Measurement | Yes | Weight with unit |
| PackageDimensions | Dimensions | No | L x W x H |
| PackageRef | string | No | Package reference |
| PackageType | string | No | Package type code |
| IntDocData | IntDoc | No | International documentation |

### Address

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Street | string | Yes | Street name |
| Streetno | string | No | Street/house number |
| PostalCode | string | Yes | Postal code |
| City | string | Yes | City |
| Country | string | Yes | ISO country code |
| State | string | No | State/province |
| District | string | No | District |

### Contact

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| FirstName | string | No | First name |
| LastName | string | No | Last name |
| Company | string | No | Company name |
| Email | string | No | Email address |
| Phone | string | No | Phone number |
| Mobile | string | No | Mobile number |

### Format (Label)

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| Type | string | PDF, ZPL, PNG | Format type |
| Size | string | 100x150, 100x200 | Label size |
| Orientation | int | 0, 90 | Rotation |

### IntDoc (International Documentation)

| Field | Type | Description |
|-------|------|-------------|
| Currency | string | Customs value currency |
| TotalValue | string | Total declared value |
| ItemCategory | int | Contents category |
| ContentsDesc | IntDocContents[] | Item descriptions |
| InvoiceNo | string | Invoice number |

### IntDocContents

| Field | Type | Description |
|-------|------|-------------|
| Contents | string | Item description |
| Quantity | int | Item quantity |
| ItemValue | string | Per-item value |
| NetWeight | string | Net weight |
| Origin | string | Country of origin |
| TariffNumber | string | HS tariff code |

## CEP Carriers (Multi-Carrier)

ParcelOne supports multiple carriers through a single API:

| CEPID | Carrier | Description |
|-------|---------|-------------|
| DHL | DHL | DHL Germany |
| DPD | DPD | DPD Germany |
| UPS | UPS | UPS |
| GLS | GLS | GLS Germany |
| HERMES | Hermes | Hermes Germany |

**Note:** Available CEPs depend on account configuration.

## Implementation Architecture

### File Structure

```
modules/connectors/parcelone/
├── karrio/
│   ├── schemas/parcelone/
│   │   ├── __init__.py
│   │   └── shipping_wcf.py       # Generated from XSD
│   ├── mappers/parcelone/
│   │   ├── __init__.py
│   │   ├── mapper.py
│   │   ├── proxy.py
│   │   └── settings.py
│   └── providers/parcelone/
│       ├── __init__.py
│       ├── units.py
│       ├── error.py
│       ├── utils.py
│       ├── rate.py
│       ├── tracking.py
│       ├── shipment/
│       │   ├── __init__.py
│       │   └── create.py
│       └── manifest.py           # Optional
├── tests/
│   └── parcelone/
│       ├── __init__.py
│       ├── fixture.py
│       ├── test_rate.py
│       ├── test_shipment.py
│       └── test_tracking.py
├── generate                      # Schema generation script
└── setup.py
```

### Settings Model

```python
@attr.s(auto_attribs=True)
class Settings(core.Settings):
    username: str
    password: str
    mandator_id: str
    consigner_id: str

    # Optional
    api_key: str = None
    default_cep: str = None  # Default carrier

    id: str = None
    test_mode: bool = False
    carrier_id: str = "parcelone"
    account_country_code: str = "DE"
    metadata: dict = {}
    config: dict = {}

    @property
    def carrier_name(self):
        return "parcelone"

    @property
    def server_url(self):
        return (
            "https://sandboxapi.awiwe.solutions/version4/shippingwcfsandbox/ShippingWCF.svc"
            if self.test_mode
            else "https://productionapi.awiwe.solutions/version4/shippingwcf/ShippingWCF.svc"
        )

    @property
    def security_header(self):
        """Generate WS-Security header."""
        return f'''
        <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
          <wsse:UsernameToken>
            <wsse:Username>{self.username}</wsse:Username>
            <wsse:Password>{self.password}</wsse:Password>
          </wsse:UsernameToken>
        </wsse:Security>
        '''
```

### Units Definition

```python
class CEP(lib.StrEnum):
    """Available carriers through ParcelOne"""
    parcelone_dhl = "DHL"
    parcelone_dpd = "DPD"
    parcelone_ups = "UPS"
    parcelone_gls = "GLS"
    parcelone_hermes = "HERMES"

class ShippingService(lib.StrEnum):
    """Carrier + Product combinations"""
    parcelone_dhl_paket = "DHL_PAKET"
    parcelone_dhl_express = "DHL_EXPRESS"
    parcelone_dpd_classic = "DPD_CLASSIC"
    parcelone_dpd_express = "DPD_EXPRESS"
    parcelone_ups_standard = "UPS_STANDARD"
    parcelone_ups_express = "UPS_EXPRESS"

class ShippingOption(lib.Enum):
    parcelone_cod = lib.OptionEnum("COD", float)
    parcelone_insurance = lib.OptionEnum("INS", float)
    parcelone_signature = lib.OptionEnum("SIG", bool)
    parcelone_saturday = lib.OptionEnum("SAT", bool)
    parcelone_notification = lib.OptionEnum("NOT", bool)
    insurance = parcelone_insurance

class TrackingStatus(lib.Enum):
    pending = ["CREATED", "REGISTERED"]
    in_transit = ["IN_TRANSIT", "DEPARTED", "ARRIVED"]
    out_for_delivery = ["OUT_FOR_DELIVERY"]
    delivered = ["DELIVERED", "POD"]
    on_hold = ["HELD", "CUSTOMS"]
    delivery_failed = ["FAILED", "EXCEPTION"]
```

### Proxy Implementation Pattern

```python
class Proxy(proxy.Proxy):
    settings: Settings

    def _send_request(
        self,
        request: lib.Serializable,
        operation: str,
    ) -> str:
        return lib.request(
            url=f"{self.settings.server_url}/ShippingWCF",
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": f"http://tempuri.org/IShippingWCF/{operation}",
            },
        )

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(request, "getCharges")
        return lib.Deserializable(response, lib.to_element)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(request, "registerShipments")
        return lib.Deserializable(response, lib.to_element)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(request, "voidShipments")
        return lib.Deserializable(response, lib.to_element)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(request, "getTrackings")
        return lib.Deserializable(response, lib.to_element)
```

### WS-Security Envelope Builder

```python
def create_envelope(body: str, settings: Settings) -> str:
    """Build SOAP envelope with WS-Security header."""
    return f'''<?xml version="1.0" encoding="utf-8"?>
    <soapenv:Envelope
        xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:tns="http://tempuri.org/"
        xmlns:wcf="http://schemas.datacontract.org/2004/07/ShippingWCF">
        <soapenv:Header>
            {settings.security_header}
        </soapenv:Header>
        <soapenv:Body>
            {body}
        </soapenv:Body>
    </soapenv:Envelope>
    '''
```

## Schema Generation

The WSDL and XSD files are available in `vendor/`:
- `ShippingWCF.wsdl` - Service definition
- `ShippingWCF-1.xsd` - Operations schema
- `ShippingWCF-3.xml` - Data types schema

**Generation Command:**
```bash
# Using generateDS
generateDS -o karrio/schemas/parcelone/shipping_wcf.py \
    --no-namespace-defs \
    vendor/ShippingWCF-3.xml

# Or use quicktype for simpler types
quicktype --src vendor/ShippingWCF-3.xml \
    --src-lang xml \
    --lang python \
    --out karrio/schemas/parcelone/types.py
```

## Testing Strategy

### Unit Tests Required

1. **test_create_rate_request** - Rating request structure
2. **test_get_rates** - Rating API call
3. **test_parse_rate_response** - Rate parsing
4. **test_create_shipment_request** - Shipment request structure
5. **test_create_shipment** - Shipment API call
6. **test_parse_shipment_response** - Shipment + label parsing
7. **test_cancel_shipment** - Cancellation flow
8. **test_create_tracking_request** - Tracking request structure
9. **test_get_tracking** - Tracking API call
10. **test_parse_tracking_response** - Event parsing
11. **test_parse_error_response** - Error handling

### Test Fixtures

Use PHP client examples and Postman collections from `vendor/`:
- `ShippingWCF_Client_Sandbox_Example_php/`
- `Express One International.postman_collection.json`

## Integration Checklist

- [ ] Generate Python schemas from XSD
- [ ] Settings model with WS-Security
- [ ] Proxy with SOAP client + security headers
- [ ] Rate fetching (`getCharges`)
- [ ] Shipment creation (`registerShipments`)
- [ ] Label retrieval (embedded + `printLabel`)
- [ ] Shipment cancellation (`voidShipments`)
- [ ] Tracking (`getTrackings`)
- [ ] Manifest/close shipments - Optional
- [ ] International documents - Optional
- [ ] Unit tests for all operations
- [ ] Documentation updates

## Dependencies

- Reference integrations: `chronopost`, `purolator` (SOAP + WS-Security patterns)
- Karrio SOAP utilities: `lib.Envelope`, `lib.Body`, `lib.envelope_serializer`

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| WS-Security complexity | Medium | Use proven patterns from purolator |
| Multi-carrier service mapping | Medium | Make CEP/Product configurable |
| Dynamic service discovery | Low | Cache service lists |

## Timeline Estimate

| Phase | Tasks | Effort |
|-------|-------|--------|
| Phase 1 | Schema generation + Settings | 1-2 days |
| Phase 2 | Proxy + WS-Security | 1-2 days |
| Phase 3 | Rating implementation | 1-2 days |
| Phase 4 | Shipment + Label | 2-3 days |
| Phase 5 | Tracking | 1-2 days |
| Phase 6 | Cancellation + Tests | 1-2 days |
| Phase 7 | Optional features | 2-3 days |

**Total Estimate:** 9-16 days

## Approval Requirements

Before implementation:
1. Obtain sandbox credentials from ParcelOne
2. Confirm available CEPs for target use case
3. Validate service/product codes
