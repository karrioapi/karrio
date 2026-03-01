# OSP-CARRIER-ADAPTER: Carrier Adoption Guide

**Version**: 0.1 (Draft)
**License**: Apache 2.0
**Audience**: Carrier engineering teams (FedEx, UPS, DHL, Geopost, USPS, Canada Post, and others)
**Prerequisite**: [OSP-CORE.md](./OSP-CORE.md)

---

## Table of Contents

1. [Why Adopt OSP](#1-why-adopt-osp)
2. [Four Adoption Paths](#2-four-adoption-paths)
3. [Conformance Matrix](#3-conformance-matrix)
4. [Field Mapping Guide](#4-field-mapping-guide)
5. [Implementation Walkthrough](#5-implementation-walkthrough)
6. [Testing and Certification](#6-testing-and-certification)
7. [FAQ](#7-faq)

---

## 1. Why Adopt OSP

### The Problem for Carriers Today

Every carrier maintains dozens of bespoke integrations — one for each major commerce platform, ERP, WMS, and TMS. Each integration requires:

- Custom SOAP/REST endpoint documentation
- Platform-specific SDKs
- Dedicated integration engineering teams
- Ongoing maintenance as platforms evolve

### The OSP Value Proposition

```
BEFORE OSP                              AFTER OSP
┌─────────┐                             ┌─────────┐
│  FedEx  │──┐                          │  FedEx  │──┐
└─────────┘  │  ┌──────────┐            └─────────┘  │
┌─────────┐  ├──│ Shopify  │            ┌─────────┐  │  ┌───────┐  ┌──────────┐
│   UPS   │──┤  └──────────┘            │   UPS   │──┼──│  OSP  │──│ Shopify  │
└─────────┘  │  ┌──────────┐            └─────────┘  │  │       │  ├──────────┤
┌─────────┐  ├──│   WooC   │            ┌─────────┐  │  │       │  │   WooC   │
│   DHL   │──┤  └──────────┘            │   DHL   │──┤  │       │  ├──────────┤
└─────────┘  │  ┌──────────┐            └─────────┘  │  │       │  │  Medusa  │
┌─────────┐  ├──│  Medusa  │            ┌─────────┐  │  │       │  ├──────────┤
│ Geopost │──┤  └──────────┘            │ Geopost │──┘  │       │  │AI Agents │
└─────────┘  │  ┌──────────┐            └─────────┘     └───────┘  └──────────┘
             ├──│  Saleor  │
             │  └──────────┘                One interface.
             ├──  ...x20 more               Every platform.
             └── (each custom)              Every AI agent.
```

**Implement OSP once, and your carrier services are instantly accessible to**:
- Every commerce platform that supports OSP
- Every AI agent via MCP (Claude, ChatGPT, Gemini, Cursor)
- Every ERP/WMS/TMS that speaks OSP
- The karrio ecosystem (100+ carriers, thousands of merchants)

---

## 2. Four Adoption Paths

Carriers can adopt OSP through four paths, ordered from most to least integration effort:

### Path 1: Native OSP Implementation

**Effort**: High | **Control**: Full | **Best for**: Large carriers with API teams

The carrier implements the OSP REST endpoints and MCP tools natively in their own infrastructure.

```
┌──────────────────────────────┐
│         Carrier API          │
│                              │
│  POST /osp/v1/rates          │
│  POST /osp/v1/shipments      │
│  GET  /osp/v1/tracking/{n}   │
│  ...                         │
│                              │
│  MCP Server (osp/* tools)    │
│                              │
│  ┌────────────────────────┐  │
│  │  Existing Carrier      │  │
│  │  Backend Systems       │  │
│  └────────────────────────┘  │
└──────────────────────────────┘
```

**Steps**:
1. Implement the 8 OSP REST endpoints against your existing backend
2. Map your internal data models to OSP schemas (see [Section 4](#4-field-mapping-guide))
3. Build an MCP server exposing the `osp/*` tools
4. Publish your MCP server package (npm/PyPI)
5. Submit for conformance testing (see [Section 6](#6-testing-and-certification))

**Advantages**:
- Full control over implementation
- Direct integration with existing systems
- No third-party dependency

**Considerations**:
- Requires understanding of MCP protocol
- Must maintain both REST and MCP interfaces
- Must handle OSP versioning and backward compatibility

---

### Path 2: OSP Adapter Layer

**Effort**: Medium | **Control**: High | **Best for**: Carriers with modern REST APIs

Build a lightweight translation layer between your existing REST API and OSP.

```
┌──────────────────────────────────┐
│         OSP Adapter Layer        │
│                                  │
│  OSP Request → Translate →       │
│  → Carrier API Request           │
│                                  │
│  Carrier API Response →          │
│  → Translate → OSP Response      │
│                                  │
└────────────┬─────────────────────┘
             │
             ▼
┌──────────────────────────────────┐
│    Existing Carrier REST API     │
│    (your current endpoints)      │
└──────────────────────────────────┘
```

**Steps**:
1. Create a mapping between your API schemas and OSP schemas
2. Implement a proxy that translates requests/responses
3. Handle auth translation (your auth → OSP auth model)
4. Deploy alongside or in front of your existing API

**Advantages**:
- Minimal changes to existing API
- Can be built incrementally (start with rating, add shipping later)
- Existing backend logic stays untouched

---

### Path 3: karrio Plugin

**Effort**: Low-Medium | **Control**: Medium | **Best for**: Carriers wanting fast ecosystem access

Build a karrio connector plugin. karrio handles the OSP interface; you implement the carrier-specific translation layer.

```
┌──────────────────────────────────────┐
│            karrio Server             │
│                                      │
│  OSP REST Endpoints (built-in)       │
│  OSP MCP Tools (built-in)            │
│                                      │
│  ┌────────────────────────────────┐  │
│  │     Your karrio Plugin        │  │
│  │                                │  │
│  │  Mapper:  OSP → Carrier API   │  │
│  │  Proxy:   HTTP calls          │  │
│  │  Parser:  Carrier → OSP       │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

**Steps**:
1. Follow the [karrio Carrier Integration Guide](../../CARRIER_INTEGRATION_GUIDE.md)
2. Implement `mapper.py`, `proxy.py`, and provider parsers
3. Map your service codes, options, and error codes to karrio's unified model
4. Submit the plugin to the karrio repository

**Advantages**:
- Fastest path to OSP compliance
- karrio handles REST, MCP, auth, webhooks, and rate optimization
- Access to the entire karrio ecosystem immediately
- Community-maintained, open-source

**Considerations**:
- Plugin follows karrio's conventions and release cycle
- Must use Python for the connector

---

### Path 4: Hosted via karrio Cloud

**Effort**: Minimal | **Control**: Low | **Best for**: Carriers wanting zero-code adoption

Use karrio Cloud as a managed OSP gateway. karrio Cloud already supports your carrier through an existing connector.

```
┌───────────────┐     ┌──────────────────┐     ┌──────────────┐
│  OSP Consumer │────>│  karrio Cloud    │────>│  Your API    │
│  (any client) │     │  (managed OSP    │     │  (existing)  │
│               │<────│   gateway)       │<────│              │
└───────────────┘     └──────────────────┘     └──────────────┘
```

**Steps**:
1. Verify your carrier is supported at [karrio.io/carriers](https://karrio.io)
2. If not, request integration or contribute a karrio plugin (Path 3)
3. Merchants connect their carrier accounts through karrio Cloud
4. All OSP operations work immediately

**Advantages**:
- Zero implementation effort if your carrier is already supported
- karrio handles all protocol translation
- Immediate access to all OSP consumers

**Considerations**:
- Depends on karrio Cloud availability
- Limited control over the translation layer

---

## 3. Conformance Matrix

An OSP-compliant carrier implementation MUST support at least the operations marked **Required**. Other operations are **Recommended** or **Optional**.

| Operation | Requirement | Notes |
|-----------|-------------|-------|
| `osp/get_rates` | **Required** | Rate quotes are the foundation of carrier selection |
| `osp/create_shipment` | **Required** | Label creation is the core shipping operation |
| `osp/get_shipment` | **Required** | Consumers need to retrieve shipment details |
| `osp/cancel_shipment` | **Required** | Label voiding is essential for error recovery |
| `osp/track_shipment` | **Required** | Tracking is expected by all consumers |
| `osp/schedule_pickup` | Recommended | Required for carriers that offer pickup scheduling |
| `osp/create_manifest` | Recommended | Required for carriers that require end-of-day manifests |
| `osp/create_return` | Optional | Not all carriers support return label generation via API |

### Conformance Levels

| Level | Requirements |
|-------|-------------|
| **OSP Basic** | All 5 Required operations |
| **OSP Standard** | All Required + both Recommended operations |
| **OSP Full** | All 8 operations |

### Data Model Conformance

| Requirement | Description |
|-------------|-------------|
| Address fields | MUST accept all Address fields; MUST return `postal_code` and `country_code` |
| Parcel fields | MUST accept `weight`, `weight_unit`; SHOULD accept dimensions |
| Rate response | MUST return `carrier_name`, `service`, `total_charge`, `currency` |
| Shipment response | MUST return `tracking_number`, `label` (base64), `label_type` |
| Tracking response | MUST return `status` (using OSP TrackingStatus enum), `events` array |
| Error responses | MUST use the OSP error envelope format |
| Extension fields | MUST preserve `x_` prefixed fields in round-trips |

---

## 4. Field Mapping Guide

This section provides mapping tables between common carrier API field names and OSP field names.

### 4.1 Address Mapping

| OSP Field | FedEx | UPS | DHL Express | USPS |
|-----------|-------|-----|-------------|------|
| `person_name` | `PersonName` | `Name` | `PersonName` | `FirstName` + `LastName` |
| `company_name` | `CompanyName` | `CompanyName` | `Company` | `FirmName` |
| `address_line1` | `StreetLines[0]` | `AddressLine[0]` | `StreetLines` | `Address2` |
| `address_line2` | `StreetLines[1]` | `AddressLine[1]` | `StreetLines2` | `Address1` |
| `city` | `City` | `City` | `City` | `City` |
| `state_code` | `StateOrProvinceCode` | `StateProvinceCode` | `Division` | `State` |
| `postal_code` | `PostalCode` | `PostalCode` | `PostalCode` | `Zip5` |
| `country_code` | `CountryCode` | `CountryCode` | `CountryCode` | `Country` |
| `phone_number` | `PhoneNumber` | `Phone.Number` | `PhoneNumber` | `Phone` |
| `residential` | `Residential` | `ResidentialAddressIndicator` | *(n/a)* | *(n/a)* |

### 4.2 Parcel / Package Mapping

| OSP Field | FedEx | UPS | DHL Express |
|-----------|-------|-----|-------------|
| `weight` | `Weight.Value` | `PackageWeight.Weight` | `Weight` |
| `weight_unit` | `Weight.Units` | `PackageWeight.UnitOfMeasurement.Code` | *(always KG)* |
| `length` | `Dimensions.Length` | `Dimensions.Length` | `Length` |
| `width` | `Dimensions.Width` | `Dimensions.Width` | `Width` |
| `height` | `Dimensions.Height` | `Dimensions.Height` | `Height` |
| `dimension_unit` | `Dimensions.Units` | `Dimensions.UnitOfMeasurement.Code` | *(always CM)* |
| `packaging_type` | `PackagingType` | `PackagingType.Code` | `PackageType` |

### 4.3 Tracking Status Mapping

| OSP TrackingStatus | FedEx | UPS | DHL Express | USPS |
|--------------------|-------|-----|-------------|------|
| `pending` | `OC` | *(no event)* | *(no event)* | `Pre-Shipment` |
| `info_received` | `OC` | `M` (Manifest) | `PU` | `Accepted` |
| `in_transit` | `IT`, `AR`, `DP` | `I` (In Transit) | `TR` | `In Transit` |
| `out_for_delivery` | `OD` | `O` (Out for Delivery) | `WC` | `Out for Delivery` |
| `delivered` | `DL` | `D` (Delivered) | `OK` | `Delivered` |
| `available_for_pickup` | `HL` | `P` (Pickup Ready) | `TP` | `Available for Pickup` |
| `delivery_failed` | `DE`, `SE` | `X` (Exception) | `NH` | `Alert` |
| `on_hold` | `CH` | `X` (Exception) | `OH` | `Alert` |
| `returned` | `RS` | `RS` | `RT` | `Returned to Sender` |
| `exception` | `SE` | `X` | `OH` | `Alert` |

### 4.4 Service Code Convention

OSP service codes follow the pattern: `<carrier_slug>_<service_name>`.

| Carrier | Example OSP Service Codes |
|---------|--------------------------|
| FedEx | `fedex_ground`, `fedex_express`, `fedex_2day`, `fedex_overnight`, `fedex_international_priority` |
| UPS | `ups_ground`, `ups_next_day_air`, `ups_2nd_day_air`, `ups_worldwide_express` |
| DHL Express | `dhl_express_worldwide`, `dhl_express_12_00`, `dhl_economy_select` |
| USPS | `usps_priority_mail`, `usps_first_class`, `usps_priority_mail_express` |
| Canada Post | `canada_post_expedited_parcel`, `canada_post_xpresspost`, `canada_post_regular_parcel` |
| Geopost/DPD | `dpd_classic`, `dpd_express`, `dpd_pickup` |

---

## 5. Implementation Walkthrough

This section walks through implementing the two most critical operations for Path 1 (Native) or Path 2 (Adapter).

### 5.1 Implementing Get Rates

**Step 1**: Accept an OSP rate request and extract the fields you need:

```python
# Pseudocode for a FedEx adapter
def osp_get_rates(osp_request):
    fedex_request = {
        "accountNumber": {"value": ACCOUNT_NUMBER},
        "requestedShipment": {
            "shipper": {
                "address": {
                    "postalCode": osp_request["shipper"]["postal_code"],
                    "countryCode": osp_request["shipper"]["country_code"],
                    "stateOrProvinceCode": osp_request["shipper"].get("state_code"),
                    "residential": osp_request["shipper"].get("residential", False),
                }
            },
            "recipient": {
                "address": {
                    "postalCode": osp_request["recipient"]["postal_code"],
                    "countryCode": osp_request["recipient"]["country_code"],
                    "stateOrProvinceCode": osp_request["recipient"].get("state_code"),
                    "residential": osp_request["recipient"].get("residential", False),
                }
            },
            "requestedPackageLineItems": [
                {
                    "weight": {
                        "value": parcel["weight"],
                        "units": parcel.get("weight_unit", "LB"),
                    },
                    "dimensions": {
                        "length": parcel.get("length"),
                        "width": parcel.get("width"),
                        "height": parcel.get("height"),
                        "units": parcel.get("dimension_unit", "IN"),
                    }
                }
                for parcel in osp_request["parcels"]
            ],
        }
    }

    # Call your existing FedEx API
    fedex_response = call_fedex_rate_api(fedex_request)

    # Translate to OSP response
    return {
        "rates": [
            {
                "carrier_name": "fedex",
                "carrier_id": "fedex-production",
                "service": map_fedex_service_to_osp(rate["serviceType"]),
                "service_name": rate["serviceName"],
                "total_charge": rate["ratedShipmentDetails"][0]["totalNetCharge"],
                "currency": rate["ratedShipmentDetails"][0]["currency"],
                "transit_days": rate.get("transitTime", {}).get("value"),
                "estimated_delivery": rate.get("deliveryTimestamp"),
                "extra_charges": [
                    {
                        "name": surcharge["description"],
                        "amount": surcharge["amount"],
                        "currency": "USD",
                        "charge_type": "surcharge"
                    }
                    for surcharge in rate.get("surcharges", [])
                ]
            }
            for rate in fedex_response["output"]["rateReplyDetails"]
        ],
        "messages": []
    }
```

### 5.2 Implementing Create Shipment

**Step 1**: Accept an OSP shipment request and translate:

```python
def osp_create_shipment(osp_request):
    # Build carrier-specific request from OSP schema
    carrier_request = build_carrier_request(osp_request)

    # Call carrier API
    carrier_response = call_carrier_ship_api(carrier_request)

    # Translate to OSP response
    return {
        "id": generate_osp_id("shp"),
        "status": "purchased",
        "carrier_name": "your_carrier",
        "carrier_id": "your-carrier-production",
        "service": osp_request["service"],
        "tracking_number": carrier_response["trackingNumber"],
        "shipment_identifier": carrier_response["shipmentId"],
        "label": carrier_response["labelData"],  # base64
        "label_type": osp_request.get("label_type", "PDF"),
        "selected_rate": {
            "carrier_name": "your_carrier",
            "service": osp_request["service"],
            "total_charge": carrier_response["totalCharge"],
            "currency": carrier_response["currency"]
        },
        "shipper": osp_request["shipper"],
        "recipient": osp_request["recipient"],
        "parcels": osp_request["parcels"],
        "reference": osp_request.get("reference"),
        "metadata": osp_request.get("metadata", {}),
        "created_at": datetime.utcnow().isoformat() + "Z",
        "messages": []
    }
```

---

## 6. Testing and Certification

### 6.1 Conformance Test Suite

The OSP conformance test suite is an open-source tool that validates an OSP implementation against the specification. It tests:

| Test Category | What it validates |
|---------------|-------------------|
| Schema compliance | Request/response bodies match OSP JSON schemas |
| Required operations | All required operations return valid responses |
| Error handling | Errors use the OSP error envelope format |
| Status mapping | Tracking statuses map to OSP enum values |
| Extension preservation | `x_` prefixed fields survive round-trips |
| Auth support | API key authentication works correctly |

### 6.2 Running the Test Suite

```bash
# Install the OSP conformance test runner (future)
npm install -g @osp/conformance

# Run against your implementation
osp-conformance test \
  --base-url https://your-api.example.com/osp/v1 \
  --api-key osp_key_test_xxxxxxxxxxxx \
  --level standard
```

### 6.3 Certification Levels

| Level | Badge | Requirements |
|-------|-------|-------------|
| OSP Basic | `osp:basic` | Pass all Required operation tests |
| OSP Standard | `osp:standard` | Pass Required + Recommended operation tests |
| OSP Full | `osp:full` | Pass all operation tests including Optional |

### 6.4 Certification Process (Future)

1. Run the conformance test suite against your implementation
2. Submit test results to the OSP certification registry
3. Receive a certification badge and listing in the OSP carrier directory
4. Re-certify annually or when OSP major versions change

> **Note**: The certification program is planned for a future OSP release. The test suite specification is included here to guide implementation decisions.

---

## 7. FAQ

### Do I need to implement MCP if I only want REST?

REST-only implementations are valid and can achieve OSP Basic conformance. However, MCP support is what makes your carrier accessible to AI agents — the fastest-growing consumer segment. We recommend at minimum supporting REST, and using the karrio Plugin path (Path 3) to get MCP support without building it yourself.

### Can I add carrier-specific fields?

Yes. Use the `x_` prefix for extension fields and the `options` object for carrier-specific parameters. See [OSP-CORE.md Section 9](./OSP-CORE.md#9-extension-model).

### What if my API uses XML/SOAP?

OSP is JSON-only. If your backend uses SOAP/XML, build an adapter layer (Path 2) that translates between JSON and your existing format. The karrio Plugin path (Path 3) already handles this translation for many carriers.

### How does OSP handle carrier-specific services?

Service codes follow the convention `<carrier_slug>_<service_name>`. You define your own service codes within this namespace. The service catalog resource (`osp://services`) lets consumers discover available services.

### What about rate limits?

OSP does not mandate specific rate limits. Implementations SHOULD return HTTP 429 with a `Retry-After` header when rate limits are exceeded. The error code is `rate_limit_exceeded`.

### Can I implement only rating and tracking?

Yes. Start with the operations that make sense for your business. The conformance matrix defines minimum requirements, but partial implementations are useful during development. Use the MCP server metadata to advertise which operations you support.
