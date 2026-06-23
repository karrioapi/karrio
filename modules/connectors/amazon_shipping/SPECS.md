# Amazon Shipping integration — specification

Reference for the Amazon Shipping connector. Amazon Shipping exposes a
**JSON REST** API (the Selling Partner API **Shipping v2** surface) for
rate quotes, label purchase, tracking, and shipment cancellation,
behind a **Login with Amazon (LWA) OAuth2 refresh-token** flow. This
connector supports **rate quotes, shipment create (one-click rate +
buy), shipment cancel, and tracking**. There is no pickup surface on
the v2 API.

The **vendor source of truth** lives under `vendor/`:
`shippingV2.json` (the current Swagger 2.0 model pulled from
[`amzn/selling-partner-api-models`](https://github.com/amzn/selling-partner-api-models/blob/main/models/shipping-api-model/shippingV2.json)),
`openapi.yaml` (the developer-docs OpenAPI 3 export), and
`postman.json` (the published Postman collection).

This connector was ported from the karrio community plugin at
[`karrioapi/community @ 5522868 · plugins/amazon_shipping`](https://github.com/karrioapi/community/tree/5522868b13752fe009b9c4c911c1ef4218f297d2/plugins/amazon_shipping).

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Data flow](#data-flow)
3. [Endpoints](#endpoints)
4. [Authentication](#authentication)
5. [Supported operations](#supported-operations)
6. [Services](#services)
7. [Options](#options)
8. [Connection config](#connection-config)
9. [Data mapping](#data-mapping)
10. [Wire-shape invariants & gotchas](#wire-shape-invariants--gotchas)
11. [Tracking](#tracking)
12. [Error parsing](#error-parsing)
13. [References](#references)

---

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio RateRequest / ShipmentRequest /
│   (karrio core)         │   ShipmentCancelRequest / TrackingRequest
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  providers/amazon_…     │   Pure data transforms.
│   rate.py               │   Unified model → typed Amazon request,
│   shipment/create.py    │   typed Amazon response → unified model.
│   shipment/cancel.py    │   No HTTP, no side effects.
│   tracking.py           │
│   error.py              │
│   units.py              │   ShippingService, ShippingOption,
│   utils.py              │   ConnectionConfig, TrackingStatus,
│                         │   TrackingIncidentReason, region→host map
└───────────┬─────────────┘
            │
            ▼
┌──────────────────────────────┐
│  mappers/amazon_shipping/     │   HTTP transport only.
│   proxy.py                    │   - LWA OAuth2 refresh-token (cached)
│    - get_rates                │   - x-amz-access-token on every call
│    - create_shipment          │   - x-amzn-shipping-business-id header
│    - cancel_shipment          │   - parallel per-tracking-number GETs
│    - get_tracking             │
└───────────┬──────────────────┘
            │
            ▼
┌─────────────────────────┐
│  Amazon SP-API          │
│  ─────────────────────  │
│  Shipping v2 REST       │   /shipping/v2/shipments/rates,
│   (sellingpartnerapi-*) │   /oneClickShipment, /tracking,
│                         │   /shipments/{id}/cancel
│  LWA OAuth2             │   api.amazon.com/auth/o2/token
└─────────────────────────┘
```

**Key architectural choices:**

- **One-click shipment, not rate-then-buy.** Shipment create posts to
  `oneClickShipment`, which rates and purchases a label in a single
  call, so the connector never carries a `request_token` between a rate
  and a buy. `getRates` is wired only for standalone rate quotes.
- **LWA refresh-token grant**, not client-credentials. Amazon Shipping
  v2 is **seller-scoped**: it requires a seller-authorized
  `refresh_token` exchanged for a short-lived `access_token`. The token
  is cached per `amazon_shipping|<client_id>` key and refreshed 5
  minutes before expiry.
- **Region drives the host.** `aws_region` selects the SP-API regional
  endpoint; `test_mode` rewrites the host to the `sandbox.` variant.
- **Tracking fans out.** `getTracking` takes a single tracking id per
  call, so the proxy issues one parallel GET per requested number and
  zips `(tracking_id, response)` pairs back for parsing.
- **Generated schemas** — `karrio/schemas/amazon_shipping/*.py` is
  generated from `schemas/*.json` with
  `kcli ... --no-append-type-suffix --no-nice-property-names` (the
  Amazon API uses camelCase field names, preserved verbatim). Don't
  hand-edit; regenerate with
  `./bin/run-generate-on modules/connectors/amazon_shipping`.

## Data flow

### Rate quote

```
RateRequest                              Amazon SP-API
     │                                        │
     ├─► rate_request()                       │
     │     to_address(shipper/recipient)      │
     │     to_packages(required=[weight])     │
     │     to_services(ShippingService)       │
     │     to_shipping_options(initializer)   │
     │     to_customs_info() → declared_value │
     │                                        │
     ├─► { shipFrom, shipTo, packages[],      │
     │     channelDetails, labelSpecs,        │
     │     serviceSelection? }                │
     │                                        │
     │   ─ POST /shipping/v2/shipments/rates ►│
     │   ◄ { "payload": { rates[], … } } ─────│
     │                                        │
     ├─► parse_rate_response:                 │
     │     unwrap payload                     │
     │     rates[] → RateDetails              │
     ▼                                        ▼
[RateDetails]                          (one per rate)
```

### One-click shipment (rate + buy)

```
ShipmentRequest                          Amazon SP-API
     │                                        │
     ├─► shipment_request()                   │
     │     (same builders as rate +           │
     │      serviceSelection from service)    │
     │                                        │
     │   ─ POST /shipping/v2/oneClickShipment►│
     │   ◄ { "payload": {                     │
     │        shipmentId,                      │
     │        packageDocumentDetails[],        │
     │        carrier, service, totalCharge }} │
     │                                        │
     ├─► parse_shipment_response:             │
     │     unwrap payload                     │
     │     packageDocuments[type=LABEL]        │
     │       → docs.label (PNG→PDF)           │
     │     trackingId → tracking_number        │
     │     shipmentId → shipment_identifier    │
     ▼                                        ▼
ShipmentDetails                        (single-piece)
```

## Endpoints

`{base}` resolves from `Settings.server_url` (region + test_mode):

| `aws_region` | Prod base | Sandbox base (`test_mode=True`) |
|---|---|---|
| `us-east-1` (default) | `https://sellingpartnerapi-na.amazon.com` | `https://sandbox.sellingpartnerapi-na.amazon.com` |
| `eu-west-1` | `https://sellingpartnerapi-eu.amazon.com` | `https://sandbox.sellingpartnerapi-eu.amazon.com` |
| `us-west-2` | `https://sellingpartnerapi-fe.amazon.com` | `https://sandbox.sellingpartnerapi-fe.amazon.com` |

Unknown regions fall back to the `us-east-1` host.

| Purpose | Method | Path |
|---|---|---|
| LWA token | POST | `https://api.amazon.com/auth/o2/token` |
| Get rates | POST | `{base}/shipping/v2/shipments/rates` |
| Create shipment (one-click) | POST | `{base}/shipping/v2/oneClickShipment` |
| Cancel shipment | PUT | `{base}/shipping/v2/shipments/{shipmentId}/cancel` |
| Get tracking | GET | `{base}/shipping/v2/tracking?trackingId=…&carrierId=…` |

Every non-auth call sends `Content-Type: application/json`,
`x-amz-access-token: <token>`, and — when configured —
`x-amzn-shipping-business-id` (from `Settings.shipping_business_id` or
`connection_config.shipping_business_id`).

## Authentication

LWA OAuth2 **refresh-token grant**. Credentials live on `Settings`:
`client_id`, `client_secret`, `refresh_token`.

```
                                         ┌──────────────────┐
authenticate()                           │  connection_cache│
       │                                 │  (thread-safe)   │
       ▼                                 │                  │
┌──────────────┐    miss / expiring      │ key:             │
│ access_token │◄────────────────────────│  amazon_shipping|│
│              │   (buffer 5 min)        │  <client_id>     │
│              │    cache hit            │                  │
│              │────────────────────────►│                  │
└──────┬───────┘                         └──────────────────┘
       │  get_token()
       ▼  POST api.amazon.com/auth/o2/token
   ┌───────────────────────────────────────────────────┐
   │ Content-Type: application/x-www-form-urlencoded     │
   │ Body: grant_type=refresh_token & refresh_token &    │
   │       client_id & client_secret                     │
   └───────────────────────────────────────────────────┘
       │
       ▼  { access_token, expires_in, ... }
   stamped with expiry = now + expires_in (default 3600s)
```

`get_token()` raises `ParsedMessagesError` when the body carries an
`error` key (surfacing `error_description`/`error`) or when no
`access_token` is returned (`AUTH_ERROR`). The cache helper tolerates
either a `Token` object (`.get_state()`) or a bare dict/string.

> **Seller scope (live-test caveat).** Amazon Shipping v2 is **not** on
> the LWA grantless allow-list — a bare `client_credentials` grant
> returns `400 invalid_scope` for every published scope. Exercising
> rates/ship/track/cancel against the sandbox requires a real
> seller-authorized `refresh_token` (`Atzr|…`).

## Supported operations

| Operation | Wired? | Provider entry point | Notes |
|---|---|---|---|
| Rate | yes | `rate.rate_request` / `parse_rate_response` | `POST .../shipments/rates` |
| Shipment create | yes | `shipment.create.shipment_request` | one-click rate + buy |
| Shipment cancel | yes | `shipment.cancel.shipment_cancel_request` | `PUT .../{id}/cancel`, empty body on success |
| Tracking | yes | `tracking.tracking_request` | one parallel GET per number |
| Pickup | **no** | — | No pickup surface on Shipping v2 |

## Services

Amazon Shipping service IDs are **dynamic** — the real list is returned
by `getRates`. `ShippingService` (`units.py`) carries the common
patterns as a static fallback so a method can be pre-selected:

| karrio code | wire `serviceId` |
|---|---|
| `amazon_shipping_standard` | `AMZN_US_STD` |
| `amazon_shipping_premium` | `AMZN_US_PREM` |
| `amazon_shipping_ground` | `AMZN_US_GND` |
| `amazon_shipping_uk_standard` | `AMZN_UK_STD` |
| `amazon_shipping_uk_premium` | `AMZN_UK_PREM` |
| `amazon_shipping` | `AMZN` (generic fallback) |

On rate parse, `ShippingService.map(serviceId).name_or_key` maps the
returned id back to a karrio code (unknown ids pass through verbatim).
On shipment create, `serviceSelection.serviceId` is sent only when a
service was selected.

`PackagingType` collapses every unified packaging preset
(`envelope`, `pak`, `tube`, `pallet`, `small_box`, `medium_box`,
`your_packaging`) to the single Amazon `PACKAGE` type.

## Options

`ShippingOption` (`units.py`) — the first `OptionEnum` arg is the wire
key:

| Option | Wire key | Type | Notes |
|---|---|---|---|
| `amazon_shipping_channel_type` | `channel_type` | str | `AMAZON` / `EXTERNAL`; defaults to `EXTERNAL` |
| `amazon_shipping_label_format` | `label_format` | str | `PNG` / `PDF` / `ZPL`; wins over `connection_config.label_format`, default `PNG` |
| `amazon_shipping_label_size` | `label_size` | str | optional label size hint |

`shipping_options_initializer()` merges package-level options over the
shipment options (mutating a local copy so nothing leaks across
requests through the shared `{}` default). Standard options
`shipment_date`, `declared_value`, `currency`, and
`delivery_instructions` are also consumed (see data mapping).

## Connection config

`ConnectionConfig` (`utils.py`):

| Key | Type | Default | Purpose |
|---|---|---|---|
| `shipping_business_id` | str | — | `x-amzn-shipping-business-id` header (e.g. `AmazonShipping_US`) |
| `label_format` | str | `PNG` | label format when no option supplied |
| `label_size_width` | float | `4` | label width in `labelSpecifications.size` |
| `label_size_length` | float | `6` | label length in `labelSpecifications.size` |
| `label_size_unit` | str | `INCH` | label size unit |

`ShippingBusinessId` (`units.py`) enumerates the known marketplace
header values (`AmazonShipping_US/UK/IN/IT/ES/FR`).

## Data mapping

### Address — karrio `Address` → Amazon address block

```
karrio Address               Amazon shipFrom / shipTo
─────────────────            ────────────────────────
company_name or person_name ►  name
street                      ►  addressLine1
address_line2               ►  addressLine2
company_name                ►  companyName
state_code                  ►  stateOrRegion
city                        ►  city
country_code                ►  countryCode
postal_code                 ►  postalCode
email                       ►  email
phone_number                ►  phoneNumber
```

`addressLine3` is always sent `None`.

### Package — karrio `Package` → Amazon `Package`

```
karrio Package          Amazon Package           Unit
──────────────          ──────────────           ────
length/width/height ──► dimensions{…, INCH}      inches (omitted if no dims)
weight              ──► weight{value, POUND}      pounds
declared_value      ──► insuredValue{value,unit}  money (see below)
items[]             ──► items[]                    (see below)
parcel.id or index  ──► packageClientReferenceId   str
```

Dimensions are sent in **inches** (`package.length.IN`) and weight in
**pounds** (`package.weight.LB`).

### Customs / declared value

`insuredValue` is **required** by the v2 spec, so it is always emitted.
Value resolves from `package.options.declared_value` → customs
`duty.declared_value` → `0`; currency from `package.options.currency` →
`USD`.

`items` is **required** by the v2 spec, so it is always emitted (empty
list when the parcel has none). Each parcel item maps to:

```
karrio item              Amazon item
──────────               ───────────
quantity (or 1)    ───►  quantity
description        ───►  description
sku or hs_code     ───►  itemIdentifier
weight             ───►  weight{value, POUND}   (omitted if absent)
value_amount       ───►  itemValue{value, unit} (omitted if absent)
```

### Label specification

`labelSpecifications` is built from the resolved label format and the
`connection_config` size keys:

```
format          = option.label_format → config.label_format → "PNG"
size.length     = config.label_size_length → 6
size.width      = config.label_size_width → 4
size.unit       = config.label_size_unit → "INCH"
dpi             = 300
pageLayout      = "DEFAULT"
needFileJoining = (shipment) len(packages) > 1   |  (rate) False
requestedDocumentTypes = ["LABEL"]
```

### Shipment response → unified

```
oneClickShipment payload
  ├─ shipmentId                    ───► shipment_identifier, meta.shipment_id
  ├─ packageDocumentDetails[].trackingId ─► tracking_number (first), meta.tracking_numbers[]
  ├─ packageDocuments[type=LABEL].contents ─► docs.label
  ├─ carrier.{id,name}             ───► meta.carrier_id / carrier_name
  ├─ service.{id,name}             ───► meta.service_id / service_name
  └─ totalCharge.{value,unit}      ───► meta.total_charge / currency
```

Labels: multiple package labels are bundled with `lib.bundle_base64`;
a single label passes through. A `PNG` label is converted to `PDF` via
`lib.image_to_pdf` and `label_type` is reported as `PDF`.

## Wire-shape invariants & gotchas

- **Success responses are wrapped in `{"payload": {...}}`.** Rate,
  one-click shipment, and tracking all nest their result under
  `payload`; the parsers unwrap it before deserializing. (The upstream
  community plugin parsed the body un-wrapped — confirmed against the
  live sandbox that the envelope is real, see [References](#references).)
- **Errors are `{"errors": [{code, message, details}]}`** at any HTTP
  status, including `403` auth failures — handled uniformly by
  `parse_error_response`.
- **`insuredValue` and `items` are required** on every package by the
  v2 spec, so both are always emitted (with `0`/empty defaults) even
  when the unified model carries no declared value or line items.
- **Dimensions in inches, weight in pounds**, unlike many EU carriers.
- **Cancel returns an empty body on success.** The proxy substitutes
  `"{}"` for a blank response so the parser sees a dict; success is
  inferred from the **absence** of an `errors` array.
- **Tracking is one id per call.** `getTracking` has no batch form, so
  the proxy fans out N parallel GETs and the parser walks
  `(tracking_id, response)` pairs, attaching errors per tracking number.
- **Generated schema field names are camelCase verbatim** — the
  `generate` script runs `kcli` with `--no-append-type-suffix
  --no-nice-property-names`. Don't rename them in
  `karrio/schemas/amazon_shipping/`.

## Tracking

`GET /shipping/v2/tracking` with `trackingId` + `carrierId` (default
`AMZN_US`) query params, one call per requested number. The response
`payload` (`GetTrackingResult`) carries `eventHistory[]`, `summary`,
and `promisedDeliveryDate`.

Events are taken **most-recent-first** as returned. Each maps to a
`TrackingEvent` with `date`/`time` parsed from `eventTime`
(`%Y-%m-%dT%H:%M:%SZ`), `code`/`description` from `eventCode`,
`location` joined from `event.location.{city, stateOrRegion,
postalCode, countryCode}`, an ISO `timestamp`, plus normalised `status`
and `reason`. `estimated_delivery` comes from `promisedDeliveryDate`;
`delivered` is set when `summary.status == "Delivered"`.
`meta.received_by` is taken from `summary.proofOfDelivery.receivedBy`
when present.

### Status mapping

`TrackingStatus` (`units.py`) keys off Amazon v2 event codes:

| karrio status | Amazon event codes |
|---|---|
| `pending` | `LabelCreated`, `PickedUp`, `Manifested` |
| `in_transit` | `InTransit`, `ArrivedAtCarrierFacility`, `DepartedCarrierFacility`, `ArrivedAtDeliveryStation`, `ArrivedAtLocalFacility` |
| `out_for_delivery` | `OutForDelivery` |
| `delivered` | `Delivered` |
| `on_hold` | `Delayed`, `OnHold`, `PaymentNotReady` |
| `delivery_failed` | `DeliveryAttempted`, `Undeliverable`, `AddressNotFound`, `BusinessClosed`, `CustomerUnavailable`, `UnableToAccess`, `UnableToContactRecipient` |
| `delivery_delayed` | `Delayed`, `WeatherDelay` |
| `return_initiated` | `ReturnInitiated`, `Rejected`, `CancelledByRecipient` |

`TrackingIncidentReason` maps exception codes to normalized reasons
(`carrier_damaged_parcel`, `consignee_refused`, `consignee_not_home`,
`wrong_address`, `unable_to_access`, `payment_issue`, `hazmat`).

## Error parsing

`error.parse_error_response` reads the v2 error envelope:

```
response
   └─ "errors": [ {code, message, details} ]
        for each entry with a code or message:
          → Message(code, message, details={**kwargs, note: details?})
```

`kwargs` lets callers attach context — tracking passes
`tracking_number=<id>` so per-number failures are attributable. Rate,
shipment, and cancel parsers all funnel carrier errors through it; the
absence of an `errors` array is treated as success.

## References

- **Vendor specs** (`vendor/`):
  - `shippingV2.json` — Swagger 2.0 model from `amzn/selling-partner-api-models`
  - `openapi.yaml` — developer-docs OpenAPI 3 export
  - `postman.json` — published Postman collection
- **Upstream model** — <https://github.com/amzn/selling-partner-api-models/blob/main/models/shipping-api-model/shippingV2.json>
- **API docs** — <https://developer-docs.amazon.com/amazon-shipping>
- **LWA token endpoint** — `https://api.amazon.com/auth/o2/token`
- **Ported from** — <https://github.com/karrioapi/community/tree/5522868b13752fe009b9c4c911c1ef4218f297d2/plugins/amazon_shipping>
- **Generated schemas** — `karrio/schemas/amazon_shipping/*.py` are
  generated from `schemas/*.json` via
  `kcli ... --no-append-type-suffix --no-nice-property-names` (see
  `generate`). Never hand-edit; regenerate with
  `./bin/run-generate-on modules/connectors/amazon_shipping`.
