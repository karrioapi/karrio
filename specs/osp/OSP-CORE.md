# OSP-CORE: Open Shipping Protocol Core Specification

**Version**: 0.1 (Draft)
**License**: Apache 2.0

---

## Table of Contents

1. [Design Philosophy](#1-design-philosophy)
2. [Versioning](#2-versioning)
3. [Authentication](#3-authentication)
4. [Data Models](#4-data-models)
5. [Status Enums](#5-status-enums)
6. [Operations](#6-operations)
7. [Webhooks](#7-webhooks)
8. [Error Handling](#8-error-handling)
9. [Extension Model](#9-extension-model)

---

## 1. Design Philosophy

### 1.1 MCP-First

Every OSP operation is defined as both a REST endpoint and an MCP Tool. AI agents are first-class consumers. The protocol is designed so that an AI agent using MCP can perform any shipping operation without human intervention.

### 1.2 Clean Break from EDI/SOAP

OSP makes a deliberate clean break from legacy shipping protocols:

| Legacy | OSP |
|--------|-----|
| EDI X12 (204, 210, 214, 856) | JSON over HTTPS |
| SOAP/WSDL | REST + MCP Tools |
| XML namespaces | Flat JSON schemas |
| FTP batch files | Real-time webhooks |
| Proprietary auth | OAuth 2.0 + API keys |

No XML. No WSDL. No EDI segment parsing. No SOAP envelopes. Pure JSON, modern auth, real-time events.

### 1.3 Stable Core + Extensions

The 8 core operations and base data models defined in this specification are stable. They will not change in backwards-incompatible ways within a major version. Carrier-specific and domain-specific features use the `x_` extension prefix (see [Section 9](#9-extension-model)).

### 1.4 Domestic and International

OSP treats international shipping as a first-class concern, not an afterthought. Customs declarations, duties, HS codes, incoterms, and commercial invoices are part of the core schema.

---

## 2. Versioning

### 2.1 Version Scheme

OSP follows a `major.minor` versioning scheme:

- **Major versions** (`v1`, `v2`): Breaking changes to core schemas or operation semantics. Major versions are long-lived (minimum 2 years of support).
- **Minor versions** (`v1.1`, `v1.2`): Additive, non-breaking changes. New optional fields, new extension points, new enum values.

### 2.2 URL Versioning

REST endpoints include the major version in the URL path:

```
/osp/v1/rates
/osp/v1/shipments
```

### 2.3 MCP Tool Versioning

MCP Tool names include the `osp/` namespace prefix. The version is implicit — the connected server advertises its supported version via the MCP server metadata.

```
osp/get_rates        → OSP v1 operation
osp/create_shipment  → OSP v1 operation
```

### 2.4 Compatibility Policy

- Adding new optional fields to request/response schemas is NOT a breaking change.
- Adding new enum values is NOT a breaking change. Consumers MUST handle unknown enum values gracefully.
- Removing fields or changing field types IS a breaking change and requires a major version bump.

---

## 3. Authentication

OSP supports two authentication mechanisms. Implementations MUST support API Key authentication. OAuth 2.0 is RECOMMENDED for production deployments.

### 3.1 API Key Authentication

```http
Authorization: Bearer osp_key_xxxxxxxxxxxxxxxxxxxx
```

API keys are prefixed with `osp_key_` for easy identification. Keys MUST be transmitted over TLS (HTTPS). Keys SHOULD be scoped to specific operations (read-only, write, admin).

### 3.2 OAuth 2.0

OSP uses the OAuth 2.0 Authorization Code flow with PKCE for user-facing applications and Client Credentials flow for server-to-server communication.

**Token endpoint**: `POST /osp/v1/oauth/token`

**Scopes**:

| Scope | Description |
|-------|-------------|
| `osp:rates:read` | Fetch rate quotes |
| `osp:shipments:read` | Read shipment details |
| `osp:shipments:write` | Create, cancel, return shipments |
| `osp:tracking:read` | Track packages |
| `osp:pickups:write` | Schedule pickups |
| `osp:manifests:write` | Create manifests |
| `osp:webhooks:manage` | Manage webhook subscriptions |

**Token response**:

```json
{
  "access_token": "osp_at_xxxxxxxxxxxx",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "osp_rt_xxxxxxxxxxxx",
  "scope": "osp:rates:read osp:shipments:write osp:tracking:read"
}
```

### 3.3 MCP Authentication

When OSP is accessed via MCP, authentication is handled at the MCP transport layer. See [OSP-MCP.md](./OSP-MCP.md) for details.

---

## 4. Data Models

All data models are defined as JSON schemas. Field names use `snake_case`. All timestamps are ISO 8601 format. All currency amounts are decimal numbers (not integers in cents).

### 4.1 Address

Represents a shipping party — the sender, recipient, or return address.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Address",
  "type": "object",
  "properties": {
    "person_name": { "type": "string", "description": "Contact person's full name" },
    "company_name": { "type": "string", "description": "Company or organization name" },
    "address_line1": { "type": "string", "description": "Street address line 1" },
    "address_line2": { "type": "string", "description": "Street address line 2" },
    "city": { "type": "string", "description": "City or locality" },
    "state_code": { "type": "string", "description": "State, province, or region code (e.g., 'CA', 'ON')" },
    "postal_code": { "type": "string", "description": "Postal or ZIP code" },
    "country_code": { "type": "string", "description": "ISO 3166-1 alpha-2 country code (e.g., 'US', 'CA', 'GB')" },
    "email": { "type": "string", "format": "email", "description": "Contact email address" },
    "phone_number": { "type": "string", "description": "Contact phone number with country code" },
    "residential": { "type": "boolean", "default": false, "description": "Whether this is a residential address" },
    "street_number": { "type": "string", "description": "Street number (if separate from address_line1)" },
    "suite": { "type": "string", "description": "Suite, apartment, or unit number" },
    "federal_tax_id": { "type": "string", "description": "Federal tax ID / VAT number (for customs)" },
    "state_tax_id": { "type": "string", "description": "State-level tax ID" }
  },
  "required": ["address_line1", "postal_code", "country_code"]
}
```

### 4.2 Parcel

Represents a physical package to be shipped.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Parcel",
  "type": "object",
  "properties": {
    "weight": { "type": "number", "description": "Package weight" },
    "weight_unit": {
      "type": "string",
      "enum": ["LB", "KG", "OZ", "G"],
      "default": "LB",
      "description": "Weight unit"
    },
    "length": { "type": "number", "description": "Package length" },
    "width": { "type": "number", "description": "Package width" },
    "height": { "type": "number", "description": "Package height" },
    "dimension_unit": {
      "type": "string",
      "enum": ["IN", "CM"],
      "default": "IN",
      "description": "Dimension unit"
    },
    "packaging_type": { "type": "string", "description": "Carrier-specific packaging type code" },
    "package_preset": { "type": "string", "description": "Predefined package size (e.g., 'fedex_pak', 'ups_express_box')" },
    "is_document": { "type": "boolean", "default": false, "description": "Whether this parcel contains only documents" },
    "description": { "type": "string", "description": "Package content description" },
    "content": { "type": "string", "description": "Content summary for customs" },
    "reference_number": { "type": "string", "description": "Shipper's reference number for this parcel" },
    "freight_class": { "type": "string", "description": "NMFC freight class (for LTL)" },
    "items": {
      "type": "array",
      "items": { "$ref": "#/$defs/Commodity" },
      "description": "Itemized contents of this parcel"
    },
    "options": { "type": "object", "description": "Carrier-specific parcel options" }
  },
  "required": ["weight", "weight_unit"]
}
```

### 4.3 Commodity

Represents a product or item within a parcel, used for customs declarations and content descriptions.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Commodity",
  "type": "object",
  "properties": {
    "sku": { "type": "string", "description": "Stock keeping unit identifier" },
    "title": { "type": "string", "description": "Product title or name" },
    "description": { "type": "string", "description": "Detailed product description" },
    "quantity": { "type": "integer", "minimum": 1, "default": 1, "description": "Number of units" },
    "weight": { "type": "number", "description": "Weight per unit" },
    "weight_unit": { "type": "string", "enum": ["LB", "KG", "OZ", "G"], "description": "Weight unit" },
    "value_amount": { "type": "number", "description": "Declared value per unit" },
    "value_currency": { "type": "string", "description": "ISO 4217 currency code (e.g., 'USD', 'EUR')" },
    "hs_code": { "type": "string", "description": "Harmonized System tariff code for customs" },
    "origin_country": { "type": "string", "description": "ISO 3166-1 alpha-2 country of manufacture" },
    "category": { "type": "string", "description": "Product category" },
    "product_url": { "type": "string", "format": "uri", "description": "URL to the product page" },
    "image_url": { "type": "string", "format": "uri", "description": "URL to the product image" },
    "product_id": { "type": "string", "description": "External product identifier" },
    "variant_id": { "type": "string", "description": "External product variant identifier" },
    "metadata": { "type": "object", "description": "Arbitrary key-value metadata" }
  },
  "required": ["title", "quantity"]
}
```

### 4.4 Customs

Customs declaration information for international shipments.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Customs",
  "type": "object",
  "properties": {
    "commodities": {
      "type": "array",
      "items": { "$ref": "#/$defs/Commodity" },
      "minItems": 1,
      "description": "List of commodities in the shipment"
    },
    "content_type": {
      "type": "string",
      "enum": ["merchandise", "documents", "gift", "sample", "return_merchandise", "other"],
      "description": "Type of contents"
    },
    "content_description": { "type": "string", "description": "Description of contents" },
    "incoterm": {
      "type": "string",
      "enum": ["DDP", "DDU", "DAP", "CFR", "CIF", "CPT", "CIP", "EXW", "FCA", "FAS", "FOB"],
      "description": "International Commercial Terms code"
    },
    "invoice": { "type": "string", "description": "Invoice number" },
    "invoice_date": { "type": "string", "format": "date", "description": "Invoice date (YYYY-MM-DD)" },
    "certify": { "type": "boolean", "description": "Certify the customs declaration is accurate" },
    "signer": { "type": "string", "description": "Name of the person certifying the declaration" },
    "commercial_invoice": { "type": "boolean", "default": false, "description": "Whether a commercial invoice is included" },
    "duty": { "$ref": "#/$defs/Duty" },
    "options": { "type": "object", "description": "Carrier-specific customs options" }
  },
  "required": ["commodities"]
}
```

### 4.5 Duty

Duty and tax payment details for international shipments.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Duty",
  "type": "object",
  "properties": {
    "paid_by": {
      "type": "string",
      "enum": ["sender", "recipient", "third_party"],
      "default": "sender",
      "description": "Who pays duties and taxes"
    },
    "currency": { "type": "string", "description": "ISO 4217 currency code" },
    "account_number": { "type": "string", "description": "Duty payment account number" },
    "declared_value": { "type": "number", "description": "Total declared value of the shipment" }
  }
}
```

### 4.6 Payment

Payment details for shipping charges.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Payment",
  "type": "object",
  "properties": {
    "paid_by": {
      "type": "string",
      "enum": ["sender", "recipient", "third_party"],
      "default": "sender",
      "description": "Who pays for shipping"
    },
    "currency": { "type": "string", "description": "ISO 4217 currency code" },
    "account_number": { "type": "string", "description": "Shipping payment account number" }
  }
}
```

### 4.7 Rate

A rate quote returned by a carrier for a shipment.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Rate",
  "type": "object",
  "properties": {
    "id": { "type": "string", "description": "Unique rate identifier" },
    "carrier_name": { "type": "string", "description": "Carrier slug (e.g., 'fedex', 'ups', 'dhl_express')" },
    "carrier_id": { "type": "string", "description": "Carrier account identifier" },
    "service": { "type": "string", "description": "Service code (e.g., 'fedex_ground', 'ups_express')" },
    "service_name": { "type": "string", "description": "Human-readable service name" },
    "total_charge": { "type": "number", "description": "Total shipping cost" },
    "currency": { "type": "string", "description": "ISO 4217 currency code" },
    "transit_days": { "type": "integer", "description": "Estimated transit time in business days" },
    "estimated_delivery": { "type": "string", "format": "date", "description": "Estimated delivery date" },
    "extra_charges": {
      "type": "array",
      "items": { "$ref": "#/$defs/Charge" },
      "description": "Itemized charges (fuel surcharge, residential delivery, etc.)"
    },
    "meta": { "type": "object", "description": "Carrier-specific metadata" }
  },
  "required": ["carrier_name", "service", "total_charge", "currency"]
}
```

### 4.8 Charge

An individual charge component within a rate or shipment.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Charge",
  "type": "object",
  "properties": {
    "name": { "type": "string", "description": "Charge name (e.g., 'Base Rate', 'Fuel Surcharge')" },
    "amount": { "type": "number", "description": "Charge amount" },
    "currency": { "type": "string", "description": "ISO 4217 currency code" },
    "charge_type": {
      "type": "string",
      "enum": ["base", "surcharge", "addon", "tax", "discount"],
      "description": "Type of charge"
    }
  },
  "required": ["name", "amount", "currency"]
}
```

### 4.9 Shipment

A booked shipment with tracking number and label.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Shipment",
  "type": "object",
  "properties": {
    "id": { "type": "string", "description": "OSP shipment identifier" },
    "status": { "$ref": "#/$defs/ShipmentStatus" },
    "carrier_name": { "type": "string", "description": "Carrier slug" },
    "carrier_id": { "type": "string", "description": "Carrier account identifier" },
    "service": { "type": "string", "description": "Service code used" },
    "tracking_number": { "type": "string", "description": "Carrier tracking number" },
    "shipment_identifier": { "type": "string", "description": "Carrier-assigned shipment identifier" },
    "shipper": { "$ref": "#/$defs/Address" },
    "recipient": { "$ref": "#/$defs/Address" },
    "parcels": {
      "type": "array",
      "items": { "$ref": "#/$defs/Parcel" }
    },
    "label": { "type": "string", "description": "Base64-encoded shipping label" },
    "label_type": {
      "type": "string",
      "enum": ["PDF", "ZPL", "PNG"],
      "description": "Label format"
    },
    "label_url": { "type": "string", "format": "uri", "description": "URL to download the label" },
    "invoice": { "type": "string", "description": "Base64-encoded commercial invoice" },
    "selected_rate": { "$ref": "#/$defs/Rate" },
    "customs": { "$ref": "#/$defs/Customs" },
    "payment": { "$ref": "#/$defs/Payment" },
    "reference": { "type": "string", "description": "Shipper's reference" },
    "options": { "type": "object", "description": "Shipping options applied" },
    "metadata": { "type": "object", "description": "Arbitrary key-value metadata" },
    "created_at": { "type": "string", "format": "date-time" },
    "updated_at": { "type": "string", "format": "date-time" },
    "meta": { "type": "object", "description": "Carrier-specific metadata" }
  },
  "required": ["id", "status", "carrier_name", "service", "tracking_number"]
}
```

### 4.10 TrackingEvent

A single event in the tracking history of a package.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "TrackingEvent",
  "type": "object",
  "properties": {
    "date": { "type": "string", "format": "date", "description": "Event date (YYYY-MM-DD)" },
    "time": { "type": "string", "description": "Event time (HH:MM)" },
    "timestamp": { "type": "string", "format": "date-time", "description": "Full ISO 8601 timestamp" },
    "description": { "type": "string", "description": "Human-readable event description" },
    "status": { "$ref": "#/$defs/TrackingStatus", "description": "Normalized tracking status" },
    "code": { "type": "string", "description": "Carrier-specific event code" },
    "location": { "type": "string", "description": "Event location (city, state, country)" },
    "latitude": { "type": "number", "description": "Event latitude" },
    "longitude": { "type": "number", "description": "Event longitude" }
  },
  "required": ["date", "description"]
}
```

### 4.11 Tracking

The complete tracking state of a shipment.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Tracking",
  "type": "object",
  "properties": {
    "tracking_number": { "type": "string", "description": "Carrier tracking number" },
    "carrier_name": { "type": "string", "description": "Carrier slug" },
    "carrier_id": { "type": "string", "description": "Carrier account identifier" },
    "status": { "$ref": "#/$defs/TrackingStatus" },
    "estimated_delivery": { "type": "string", "format": "date", "description": "Estimated delivery date" },
    "delivered": { "type": "boolean", "description": "Whether the package has been delivered" },
    "events": {
      "type": "array",
      "items": { "$ref": "#/$defs/TrackingEvent" },
      "description": "Chronological list of tracking events (most recent first)"
    },
    "signed_by": { "type": "string", "description": "Name of person who signed for delivery" },
    "images": {
      "type": "object",
      "properties": {
        "delivery_image": { "type": "string", "description": "Base64-encoded delivery proof image" },
        "signature_image": { "type": "string", "description": "Base64-encoded signature image" }
      }
    },
    "info": {
      "type": "object",
      "description": "Additional tracking metadata",
      "properties": {
        "carrier_tracking_link": { "type": "string", "format": "uri" },
        "shipment_service": { "type": "string" },
        "shipment_origin_country": { "type": "string" },
        "shipment_destination_country": { "type": "string" },
        "shipping_date": { "type": "string", "format": "date" },
        "package_weight": { "type": "string" },
        "package_weight_unit": { "type": "string" }
      }
    },
    "meta": { "type": "object", "description": "Carrier-specific metadata" }
  },
  "required": ["tracking_number", "carrier_name", "status", "events"]
}
```

### 4.12 Pickup

A scheduled carrier pickup.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Pickup",
  "type": "object",
  "properties": {
    "id": { "type": "string", "description": "OSP pickup identifier" },
    "confirmation_number": { "type": "string", "description": "Carrier confirmation number" },
    "carrier_name": { "type": "string" },
    "carrier_id": { "type": "string" },
    "pickup_date": { "type": "string", "format": "date", "description": "Scheduled pickup date" },
    "ready_time": { "type": "string", "description": "Earliest pickup time (HH:MM)" },
    "closing_time": { "type": "string", "description": "Latest pickup time (HH:MM)" },
    "address": { "$ref": "#/$defs/Address" },
    "pickup_charge": { "$ref": "#/$defs/Charge" },
    "meta": { "type": "object" }
  },
  "required": ["confirmation_number", "carrier_name", "pickup_date"]
}
```

### 4.13 Manifest

An end-of-day manifest (SCAN form) summarizing shipments for carrier pickup.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Manifest",
  "type": "object",
  "properties": {
    "id": { "type": "string", "description": "OSP manifest identifier" },
    "carrier_name": { "type": "string" },
    "carrier_id": { "type": "string" },
    "shipment_identifiers": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Shipment identifiers included in this manifest"
    },
    "address": { "$ref": "#/$defs/Address", "description": "Pickup address" },
    "reference": { "type": "string", "description": "Manifest reference" },
    "doc": {
      "type": "object",
      "properties": {
        "manifest": { "type": "string", "description": "Base64-encoded manifest document" }
      }
    },
    "meta": { "type": "object" }
  },
  "required": ["id", "carrier_name"]
}
```

### 4.14 Webhook Envelope

The standard envelope for all webhook event deliveries.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "WebhookEnvelope",
  "type": "object",
  "properties": {
    "id": { "type": "string", "description": "Unique event identifier (UUID)" },
    "type": { "type": "string", "description": "Event type (e.g., 'shipment.created', 'tracking.updated')" },
    "occurred_at": { "type": "string", "format": "date-time", "description": "When the event occurred" },
    "api_version": { "type": "string", "description": "OSP API version (e.g., 'v1')" },
    "data": { "type": "object", "description": "Event payload — the relevant OSP object" }
  },
  "required": ["id", "type", "occurred_at", "data"]
}
```

---

## 5. Status Enums

### 5.1 ShipmentStatus

```json
{
  "type": "string",
  "enum": [
    "draft",
    "purchased",
    "shipped",
    "in_transit",
    "delivered",
    "cancelled",
    "return_requested",
    "returned",
    "needs_attention"
  ]
}
```

| Value | Description |
|-------|-------------|
| `draft` | Shipment created but label not yet purchased |
| `purchased` | Label purchased, awaiting carrier pickup |
| `shipped` | Package handed off to carrier |
| `in_transit` | Package in transit |
| `delivered` | Package delivered to recipient |
| `cancelled` | Shipment cancelled, label voided |
| `return_requested` | Return label created, awaiting return |
| `returned` | Return package received |
| `needs_attention` | Shipment requires manual intervention (held at customs, delivery exception, etc.) |

### 5.2 TrackingStatus

```json
{
  "type": "string",
  "enum": [
    "pending",
    "info_received",
    "in_transit",
    "out_for_delivery",
    "delivered",
    "available_for_pickup",
    "delivery_failed",
    "on_hold",
    "returned",
    "exception",
    "unknown"
  ]
}
```

| Value | Description |
|-------|-------------|
| `pending` | Tracking number registered, no scan yet |
| `info_received` | Carrier has received shipment information |
| `in_transit` | Package is in transit |
| `out_for_delivery` | Package is out for delivery |
| `delivered` | Package delivered |
| `available_for_pickup` | Package available at pickup location |
| `delivery_failed` | Delivery attempt failed |
| `on_hold` | Package held (customs, weather, carrier decision) |
| `returned` | Package returned to sender |
| `exception` | An exception occurred during transit |
| `unknown` | Status cannot be determined |

### 5.3 ContentType

```json
{
  "type": "string",
  "enum": ["merchandise", "documents", "gift", "sample", "return_merchandise", "other"]
}
```

### 5.4 Incoterm

```json
{
  "type": "string",
  "enum": ["DDP", "DDU", "DAP", "CFR", "CIF", "CPT", "CIP", "EXW", "FCA", "FAS", "FOB"]
}
```

### 5.5 LabelType

```json
{
  "type": "string",
  "enum": ["PDF", "ZPL", "PNG"]
}
```

### 5.6 WeightUnit

```json
{
  "type": "string",
  "enum": ["LB", "KG", "OZ", "G"]
}
```

### 5.7 DimensionUnit

```json
{
  "type": "string",
  "enum": ["IN", "CM"]
}
```

---

## 6. Operations

OSP defines 8 core operations. Each operation is specified as both a REST endpoint and an MCP Tool.

### 6.1 Get Rates

Fetch shipping rate quotes from one or more carriers.

**REST**: `POST /osp/v1/rates`
**MCP Tool**: `osp/get_rates`

#### Request

```json
{
  "shipper": {
    "postal_code": "10001",
    "city": "New York",
    "state_code": "NY",
    "country_code": "US"
  },
  "recipient": {
    "postal_code": "90210",
    "city": "Beverly Hills",
    "state_code": "CA",
    "country_code": "US"
  },
  "parcels": [
    {
      "weight": 5.0,
      "weight_unit": "LB",
      "length": 10,
      "width": 8,
      "height": 6,
      "dimension_unit": "IN"
    }
  ],
  "services": ["fedex_ground", "ups_ground"],
  "options": {},
  "reference": "ORDER-12345"
}
```

#### Response

```json
{
  "rates": [
    {
      "id": "rate_abc123",
      "carrier_name": "fedex",
      "carrier_id": "fedex-production",
      "service": "fedex_ground",
      "service_name": "FedEx Ground",
      "total_charge": 12.50,
      "currency": "USD",
      "transit_days": 5,
      "estimated_delivery": "2026-03-07",
      "extra_charges": [
        { "name": "Base Rate", "amount": 10.25, "currency": "USD", "charge_type": "base" },
        { "name": "Fuel Surcharge", "amount": 2.25, "currency": "USD", "charge_type": "surcharge" }
      ]
    },
    {
      "id": "rate_def456",
      "carrier_name": "ups",
      "carrier_id": "ups-production",
      "service": "ups_ground",
      "service_name": "UPS Ground",
      "total_charge": 14.75,
      "currency": "USD",
      "transit_days": 4,
      "estimated_delivery": "2026-03-06",
      "extra_charges": [
        { "name": "Base Rate", "amount": 12.00, "currency": "USD", "charge_type": "base" },
        { "name": "Fuel Surcharge", "amount": 2.75, "currency": "USD", "charge_type": "surcharge" }
      ]
    }
  ],
  "messages": []
}
```

---

### 6.2 Create Shipment

Create a shipment and purchase a shipping label.

**REST**: `POST /osp/v1/shipments`
**MCP Tool**: `osp/create_shipment`

#### Request

```json
{
  "service": "fedex_ground",
  "shipper": {
    "person_name": "John Doe",
    "company_name": "Acme Corp",
    "address_line1": "123 Main St",
    "city": "New York",
    "state_code": "NY",
    "postal_code": "10001",
    "country_code": "US",
    "phone_number": "+1-555-123-4567"
  },
  "recipient": {
    "person_name": "Jane Smith",
    "address_line1": "456 Oak Ave",
    "city": "Beverly Hills",
    "state_code": "CA",
    "postal_code": "90210",
    "country_code": "US",
    "phone_number": "+1-555-987-6543"
  },
  "parcels": [
    {
      "weight": 5.0,
      "weight_unit": "LB",
      "length": 10,
      "width": 8,
      "height": 6,
      "dimension_unit": "IN"
    }
  ],
  "label_type": "PDF",
  "reference": "ORDER-12345",
  "metadata": { "order_id": "ORD-789" }
}
```

#### Response

```json
{
  "id": "shp_abc123",
  "status": "purchased",
  "carrier_name": "fedex",
  "carrier_id": "fedex-production",
  "service": "fedex_ground",
  "tracking_number": "794644790138",
  "shipment_identifier": "794644790138",
  "label": "JVBERi0xLjcKJeLjz9MK...",
  "label_type": "PDF",
  "label_url": "https://api.karrio.io/osp/v1/shipments/shp_abc123/label",
  "selected_rate": {
    "carrier_name": "fedex",
    "service": "fedex_ground",
    "total_charge": 12.50,
    "currency": "USD",
    "transit_days": 5,
    "estimated_delivery": "2026-03-07"
  },
  "shipper": { "...": "..." },
  "recipient": { "...": "..." },
  "parcels": [{ "...": "..." }],
  "reference": "ORDER-12345",
  "metadata": { "order_id": "ORD-789" },
  "created_at": "2026-03-01T10:30:00Z",
  "updated_at": "2026-03-01T10:30:00Z",
  "messages": []
}
```

---

### 6.3 Get Shipment

Retrieve details of an existing shipment.

**REST**: `GET /osp/v1/shipments/{id}`
**MCP Tool**: `osp/get_shipment`

#### Request

```
GET /osp/v1/shipments/shp_abc123
```

MCP:
```json
{
  "method": "tools/call",
  "params": {
    "name": "osp/get_shipment",
    "arguments": { "shipment_id": "shp_abc123" }
  }
}
```

#### Response

```json
{
  "id": "shp_abc123",
  "status": "in_transit",
  "carrier_name": "fedex",
  "carrier_id": "fedex-production",
  "service": "fedex_ground",
  "tracking_number": "794644790138",
  "shipment_identifier": "794644790138",
  "label_type": "PDF",
  "label_url": "https://api.karrio.io/osp/v1/shipments/shp_abc123/label",
  "selected_rate": {
    "carrier_name": "fedex",
    "service": "fedex_ground",
    "total_charge": 12.50,
    "currency": "USD",
    "transit_days": 5
  },
  "shipper": { "person_name": "John Doe", "postal_code": "10001", "country_code": "US" },
  "recipient": { "person_name": "Jane Smith", "postal_code": "90210", "country_code": "US" },
  "parcels": [{ "weight": 5.0, "weight_unit": "LB" }],
  "reference": "ORDER-12345",
  "metadata": { "order_id": "ORD-789" },
  "created_at": "2026-03-01T10:30:00Z",
  "updated_at": "2026-03-02T08:15:00Z"
}
```

---

### 6.4 Cancel Shipment

Cancel a shipment and void its label.

**REST**: `POST /osp/v1/shipments/{id}/cancel`
**MCP Tool**: `osp/cancel_shipment`

#### Request

```
POST /osp/v1/shipments/shp_abc123/cancel
```

MCP:
```json
{
  "method": "tools/call",
  "params": {
    "name": "osp/cancel_shipment",
    "arguments": { "shipment_id": "shp_abc123" }
  }
}
```

#### Response

```json
{
  "id": "shp_abc123",
  "status": "cancelled",
  "carrier_name": "fedex",
  "carrier_id": "fedex-production",
  "success": true,
  "operation": "cancel_shipment",
  "messages": []
}
```

---

### 6.5 Track Shipment

Track a package by tracking number.

**REST**: `GET /osp/v1/tracking/{tracking_number}`
**MCP Tool**: `osp/track_shipment`

#### Request

```
GET /osp/v1/tracking/794644790138?carrier_name=fedex
```

MCP:
```json
{
  "method": "tools/call",
  "params": {
    "name": "osp/track_shipment",
    "arguments": {
      "tracking_number": "794644790138",
      "carrier_name": "fedex"
    }
  }
}
```

#### Response

```json
{
  "tracking_number": "794644790138",
  "carrier_name": "fedex",
  "carrier_id": "fedex-production",
  "status": "in_transit",
  "estimated_delivery": "2026-03-07",
  "delivered": false,
  "events": [
    {
      "date": "2026-03-03",
      "time": "14:30",
      "timestamp": "2026-03-03T14:30:00Z",
      "description": "In transit - Arrived at FedEx facility",
      "status": "in_transit",
      "location": "Memphis, TN, US",
      "code": "AR"
    },
    {
      "date": "2026-03-02",
      "time": "08:15",
      "timestamp": "2026-03-02T08:15:00Z",
      "description": "Picked up",
      "status": "in_transit",
      "location": "New York, NY, US",
      "code": "PU"
    },
    {
      "date": "2026-03-01",
      "time": "10:30",
      "timestamp": "2026-03-01T10:30:00Z",
      "description": "Shipment information sent to FedEx",
      "status": "info_received",
      "location": "New York, NY, US",
      "code": "OC"
    }
  ],
  "info": {
    "carrier_tracking_link": "https://www.fedex.com/fedextrack/?trknbr=794644790138",
    "shipment_service": "FedEx Ground",
    "shipment_origin_country": "US",
    "shipment_destination_country": "US"
  }
}
```

---

### 6.6 Schedule Pickup

Schedule a carrier pickup for one or more shipments.

**REST**: `POST /osp/v1/pickups`
**MCP Tool**: `osp/schedule_pickup`

#### Request

```json
{
  "carrier_name": "fedex",
  "pickup_date": "2026-03-05",
  "ready_time": "09:00",
  "closing_time": "17:00",
  "address": {
    "person_name": "John Doe",
    "company_name": "Acme Corp",
    "address_line1": "123 Main St",
    "city": "New York",
    "state_code": "NY",
    "postal_code": "10001",
    "country_code": "US",
    "phone_number": "+1-555-123-4567"
  },
  "shipment_identifiers": ["794644790138", "794644790139"],
  "instruction": "Ring doorbell. Packages at front desk.",
  "package_location": "Front Desk"
}
```

#### Response

```json
{
  "id": "pck_abc123",
  "confirmation_number": "FDXPCK123456",
  "carrier_name": "fedex",
  "carrier_id": "fedex-production",
  "pickup_date": "2026-03-05",
  "ready_time": "09:00",
  "closing_time": "17:00",
  "pickup_charge": {
    "name": "Pickup Fee",
    "amount": 0.00,
    "currency": "USD"
  },
  "messages": []
}
```

---

### 6.7 Create Manifest

Create an end-of-day manifest (SCAN form) for a batch of shipments.

**REST**: `POST /osp/v1/manifests`
**MCP Tool**: `osp/create_manifest`

#### Request

```json
{
  "carrier_name": "fedex",
  "shipment_identifiers": ["794644790138", "794644790139", "794644790140"],
  "address": {
    "company_name": "Acme Corp",
    "address_line1": "123 Main St",
    "city": "New York",
    "state_code": "NY",
    "postal_code": "10001",
    "country_code": "US"
  },
  "reference": "MANIFEST-2026-03-05"
}
```

#### Response

```json
{
  "id": "mnf_abc123",
  "carrier_name": "fedex",
  "carrier_id": "fedex-production",
  "shipment_identifiers": ["794644790138", "794644790139", "794644790140"],
  "doc": {
    "manifest": "JVBERi0xLjcKJeLjz9MK..."
  },
  "reference": "MANIFEST-2026-03-05",
  "messages": []
}
```

---

### 6.8 Create Return

Create a return shipment label for an existing shipment.

**REST**: `POST /osp/v1/shipments/{id}/return`
**MCP Tool**: `osp/create_return`

#### Request

```
POST /osp/v1/shipments/shp_abc123/return
```

```json
{
  "label_type": "PDF",
  "reference": "RETURN-ORDER-12345"
}
```

MCP:
```json
{
  "method": "tools/call",
  "params": {
    "name": "osp/create_return",
    "arguments": {
      "shipment_id": "shp_abc123",
      "label_type": "PDF",
      "reference": "RETURN-ORDER-12345"
    }
  }
}
```

#### Response

```json
{
  "id": "shp_ret_abc123",
  "status": "purchased",
  "carrier_name": "fedex",
  "carrier_id": "fedex-production",
  "service": "fedex_ground",
  "tracking_number": "794644790200",
  "shipment_identifier": "794644790200",
  "label": "JVBERi0xLjcKJeLjz9MK...",
  "label_type": "PDF",
  "label_url": "https://api.karrio.io/osp/v1/shipments/shp_ret_abc123/label",
  "original_shipment_id": "shp_abc123",
  "reference": "RETURN-ORDER-12345",
  "created_at": "2026-03-10T09:00:00Z",
  "messages": []
}
```

---

## 7. Webhooks

OSP uses webhooks to push real-time event notifications to subscribers.

### 7.1 Event Types

| Event | Description |
|-------|-------------|
| `shipment.created` | A new shipment was created |
| `shipment.purchased` | A shipping label was purchased |
| `shipment.cancelled` | A shipment was cancelled |
| `shipment.status_changed` | Shipment status changed |
| `tracking.updated` | Tracking information was updated |
| `tracking.delivered` | Package was delivered |
| `tracking.exception` | A tracking exception occurred |
| `pickup.scheduled` | A pickup was scheduled |
| `pickup.cancelled` | A pickup was cancelled |
| `manifest.created` | A manifest was created |
| `return.created` | A return shipment was created |

### 7.2 Webhook Delivery

Webhooks are delivered as `POST` requests with a JSON body conforming to the Webhook Envelope schema (Section 4.14). Delivery includes an HMAC signature for verification.

**Headers**:

```http
POST /your-webhook-endpoint HTTP/1.1
Content-Type: application/json
X-OSP-Signature: sha256=5d5e1f3c14c5e82eb8e4c9f44e1a39d1b77c6a6f0e1c3d5a7b9e0f2a4c6d8e0
X-OSP-Event: tracking.updated
X-OSP-Delivery-Id: evt_abc123
X-OSP-Timestamp: 1709312400
```

**Example payload**:

```json
{
  "id": "evt_abc123",
  "type": "tracking.updated",
  "occurred_at": "2026-03-03T14:30:00Z",
  "api_version": "v1",
  "data": {
    "tracking_number": "794644790138",
    "carrier_name": "fedex",
    "status": "in_transit",
    "delivered": false,
    "events": [
      {
        "date": "2026-03-03",
        "time": "14:30",
        "description": "In transit - Arrived at FedEx facility",
        "status": "in_transit",
        "location": "Memphis, TN, US"
      }
    ]
  }
}
```

### 7.3 HMAC Verification

OSP uses HMAC-SHA256 to sign webhook payloads. The signing secret is provided when the webhook subscription is created.

**Verification algorithm**:

```
1. Concatenate: timestamp + "." + raw_request_body
2. Compute: HMAC-SHA256(signing_secret, concatenated_string)
3. Compare: result with the value in X-OSP-Signature header (after "sha256=" prefix)
```

**Example verification (Python)**:

```python
import hmac
import hashlib

def verify_webhook(payload: bytes, signature: str, timestamp: str, secret: str) -> bool:
    signed_content = f"{timestamp}.{payload.decode('utf-8')}"
    expected = hmac.new(
        secret.encode("utf-8"),
        signed_content.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

**Example verification (TypeScript)**:

```typescript
import { createHmac, timingSafeEqual } from "crypto";

function verifyWebhook(payload: string, signature: string, timestamp: string, secret: string): boolean {
  const signedContent = `${timestamp}.${payload}`;
  const expected = `sha256=${createHmac("sha256", secret).update(signedContent).digest("hex")}`;
  return timingSafeEqual(Buffer.from(expected), Buffer.from(signature));
}
```

### 7.4 Retry Policy

| Attempt | Delay |
|---------|-------|
| 1 | Immediate |
| 2 | 1 minute |
| 3 | 5 minutes |
| 4 | 30 minutes |
| 5 | 2 hours |

After 5 failed attempts, the webhook is marked as failed. A `2xx` response code is considered successful. The endpoint must respond within 30 seconds.

---

## 8. Error Handling

### 8.1 Error Envelope

All errors are returned in a standard envelope:

```json
{
  "errors": [
    {
      "code": "invalid_address",
      "message": "The recipient postal code is not valid for the given state.",
      "field": "recipient.postal_code",
      "carrier_name": "fedex",
      "carrier_id": "fedex-production",
      "details": {}
    }
  ]
}
```

### 8.2 Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `authentication_failed` | 401 | Invalid or missing API key / token |
| `authorization_failed` | 403 | Valid credentials but insufficient scope |
| `not_found` | 404 | Resource not found |
| `validation_error` | 422 | Request body failed schema validation |
| `invalid_address` | 422 | Address is invalid or incomplete |
| `invalid_parcel` | 422 | Parcel dimensions or weight are invalid |
| `carrier_error` | 502 | Carrier API returned an error |
| `carrier_unavailable` | 503 | Carrier API is temporarily unavailable |
| `rate_not_available` | 422 | No rates available for the given parameters |
| `shipment_not_cancellable` | 409 | Shipment is in a state that cannot be cancelled |
| `label_generation_failed` | 502 | Carrier failed to generate a shipping label |
| `tracking_not_found` | 404 | Tracking number not found at the carrier |
| `pickup_not_available` | 422 | Pickup not available for the given date/location |
| `manifest_error` | 502 | Carrier failed to create the manifest |
| `rate_limit_exceeded` | 429 | Too many requests |
| `internal_error` | 500 | Unexpected server error |

### 8.3 Multi-Carrier Errors

When an operation involves multiple carriers (e.g., rate shopping), the response MAY contain both successful results and errors. The `errors` array holds carrier-specific errors while the main response holds successful results.

```json
{
  "rates": [
    { "carrier_name": "fedex", "service": "fedex_ground", "total_charge": 12.50, "currency": "USD" }
  ],
  "messages": [
    {
      "carrier_name": "ups",
      "carrier_id": "ups-production",
      "code": "carrier_error",
      "message": "UPS account is not authorized for this origin."
    }
  ]
}
```

---

## 9. Extension Model

OSP is designed to be extensible without modifying the core specification.

### 9.1 Extension Fields (`x_` prefix)

Any OSP object can include extension fields prefixed with `x_`. These fields are passed through by conforming implementations but are not validated against the core schema.

```json
{
  "shipper": {
    "person_name": "John Doe",
    "postal_code": "10001",
    "country_code": "US",
    "x_location_id": "LOC-123",
    "x_delivery_instructions": "Leave at back door"
  }
}
```

### 9.2 Extension Rules

1. Extension field names MUST start with `x_` followed by a lowercase identifier using `snake_case`.
2. Extension fields MUST NOT override core fields. If a core field exists with the same semantic meaning, use the core field.
3. Implementations MUST preserve extension fields in request/response round-trips.
4. Implementations MUST NOT reject requests containing unknown extension fields.
5. Extension fields SHOULD be namespaced to avoid collisions: `x_<vendor>_<field>` (e.g., `x_shopify_order_id`).

### 9.3 Extension Options

The `options` field present on most OSP objects is the recommended place for carrier-specific or integration-specific parameters:

```json
{
  "service": "fedex_express",
  "parcels": [{ "weight": 2.0, "weight_unit": "LB" }],
  "options": {
    "signature_required": true,
    "saturday_delivery": true,
    "insurance": 500.00,
    "x_fedex_smart_post_hub_id": "5531",
    "x_fedex_hold_at_location": true
  }
}
```

### 9.4 Carrier-Specific Services

Carrier service codes follow the convention `<carrier_slug>_<service_name>`:

```
fedex_ground
fedex_express
fedex_2day
ups_ground
ups_next_day_air
dhl_express_worldwide
usps_priority_mail
canada_post_expedited_parcel
```

Implementations SHOULD provide a service catalog resource listing all available services (see [OSP-MCP.md](./OSP-MCP.md) for the MCP resource definition).

---

## Appendix A: Operation Summary

| # | Operation | REST Endpoint | MCP Tool | Hint |
|---|-----------|--------------|----------|------|
| 1 | Get Rates | `POST /osp/v1/rates` | `osp/get_rates` | readOnly, openWorld |
| 2 | Create Shipment | `POST /osp/v1/shipments` | `osp/create_shipment` | destructive |
| 3 | Get Shipment | `GET /osp/v1/shipments/{id}` | `osp/get_shipment` | readOnly, idempotent |
| 4 | Cancel Shipment | `POST /osp/v1/shipments/{id}/cancel` | `osp/cancel_shipment` | destructive |
| 5 | Track Shipment | `GET /osp/v1/tracking/{number}` | `osp/track_shipment` | readOnly, openWorld |
| 6 | Schedule Pickup | `POST /osp/v1/pickups` | `osp/schedule_pickup` | destructive |
| 7 | Create Manifest | `POST /osp/v1/manifests` | `osp/create_manifest` | destructive |
| 8 | Create Return | `POST /osp/v1/shipments/{id}/return` | `osp/create_return` | destructive |

## Appendix B: Type Reference Summary

| Type | Required Fields | Used In |
|------|----------------|---------|
| Address | `address_line1`, `postal_code`, `country_code` | Shipment, Pickup, Manifest |
| Parcel | `weight`, `weight_unit` | Rate request, Shipment |
| Commodity | `title`, `quantity` | Customs, Parcel items |
| Customs | `commodities` | Shipment (international) |
| Duty | *(none)* | Customs |
| Payment | *(none)* | Shipment |
| Rate | `carrier_name`, `service`, `total_charge`, `currency` | Rate response |
| Charge | `name`, `amount`, `currency` | Rate, Shipment, Pickup |
| Shipment | `id`, `status`, `carrier_name`, `service`, `tracking_number` | Create/Get response |
| TrackingEvent | `date`, `description` | Tracking response |
| Tracking | `tracking_number`, `carrier_name`, `status`, `events` | Track response |
| Pickup | `confirmation_number`, `carrier_name`, `pickup_date` | Pickup response |
| Manifest | `id`, `carrier_name` | Manifest response |
| WebhookEnvelope | `id`, `type`, `occurred_at`, `data` | Webhook delivery |
