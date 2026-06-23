# Asendia integration — specification

Reference for the Asendia connector. Asendia is an international
e-commerce parcel carrier; the connector talks to the **Asendia Sync**
JSON REST API (JWT-bearer auth, single production environment at
`https://www.asendia-sync.com`). It supports shipment create / cancel,
return shipments, tracking, and manifest close. There is **no native
rating API** — rates are served from a local rate sheet
(`services.csv`) via karrio's universal `RatingMixinProxy`.

The **vendor source of truth** is the Asendia Sync OpenAPI 3.0.1 spec
(<https://www.asendia-sync.com/v3/api-docs>, Swagger UI at
<https://www.asendia-sync.com/swagger-ui/index.html>), mirrored under
`vendor/openapi.json` / `vendor/openapi.yaml`.

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Data flow](#data-flow)
3. [Endpoints](#endpoints)
4. [Authentication](#authentication)
5. [Supported operations](#supported-operations)
6. [Services & options](#services--options)
7. [Data mapping](#data-mapping)
8. [Per-package fan-out & two-tier identifiers](#per-package-fan-out--two-tier-identifiers)
9. [Returns](#returns)
10. [Rating (rate sheet only)](#rating-rate-sheet-only)
11. [Tracking](#tracking)
12. [Error parsing](#error-parsing)
13. [References](#references)

---

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio ShipmentRequest / ShipmentCancelRequest /
│   (karrio core)         │   TrackingRequest / ManifestRequest / RateRequest
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  providers/asendia      │   Pure data transforms.
│   shipment/create.py    │   Unified model → typed Asendia request,
│   shipment/cancel.py    │   typed Asendia response → unified model.
│   shipment/return_*.py  │   No HTTP, no side effects.
│   tracking.py           │
│   manifest.py           │   ShippingService, ServiceCode, PackagingType,
│   error.py              │   ShippingOption, TrackingStatus,
│   units.py              │   TrackingIncidentReason, LabelType, ...
│   utils.py (Settings)   │   JWT login + token cache lives here.
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  mappers/asendia/proxy  │   HTTP transport only.
│   - create_shipment     │   - JWT bearer on every call
│   - cancel_shipment     │   - per-package async create + per-parcel
│   - get_tracking        │     label fetch
│   - create_manifest     │   - concurrent tracking fetch
│   - get_label / etc.    │
│  rate via RatingMixin   │   - rating served locally (no Asendia call)
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Asendia Sync API       │
│  ─────────────────────  │
│  POST /api/authenticate │   JWT id_token (≈24h)
│  POST /api/parcels      │   create one parcel per package
│  GET  .../label         │   base64 label per parcel
│  DELETE /api/parcels/id │   cancel (HTTP 204)
│  GET  .../tracking/{tn} │   tracking events
│  POST /api/manifests    │   close manifest
└─────────────────────────┘
```

**Key architectural choices:**

- **Per-package fan-out (Pattern B).** `shipment_request` returns a
  *list* of `ShipmentRequestType`, one per parcel. The proxy creates
  each parcel asynchronously, then fires a second async call per parcel
  to fetch its label, and the parser folds the N responses into one
  `ShipmentDetails` via `lib.to_multi_piece_shipment`. (Same shape the
  Canada Post connector uses — noted inline in `proxy.create_shipment`.)
- **JWT bearer with a cached token.** No OAuth client-credentials —
  `POST /api/authenticate` with `{username, password}` returns an
  `id_token`. Cached per `asendia|<username>|<password>` and treated as
  valid for 23h (refreshed when within 30 min of expiry).
- **No rating API.** Asendia has no quote endpoint; the connector
  registers via `RatingMixinProxy`/`RatingMixinSettings` and serves
  rates from `services.csv` (loaded into `DEFAULT_SERVICES`).
- **Single environment.** `server_url` is always
  `https://www.asendia-sync.com` — there is no sandbox host;
  `test_mode` does not switch the URL.
- **Generated schemas** — `karrio/schemas/asendia/*.py` is generated
  from `schemas/*.json` (kcli). Don't hand-edit; regenerate with
  `./bin/run-generate-on modules/connectors/asendia`.

## Data flow

### Shipment create (2 HTTP calls per parcel)

```
ShipmentRequest                                  Asendia Sync
     │                                                 │
     │  shipment_request → [ShipmentRequestType, ...]  │
     ├─► to_address(shipper/recipient)                 │
     │   to_packages(parcels)                          │
     │   to_shipping_options()                         │
     │   map service → product (EPAQ*)                 │
     │   resolve service modifier (CUP / RETPP / …)    │
     │   to_customs_info() → items[]                   │
     │                                                 │
     │   for each package (run_asynchronously):        │
     │   ─── POST /api/parcels ────────────────────────►│  validate
     │   ◄── {id, trackingNumber, labelLocation, …} ───│  create parcel
     │                                                 │
     │   for each parcel id (run_asynchronously):      │
     │   ─── GET /api/parcels/{id}/label ──────────────►│  render label
     │   ◄── base64 (PDF/PNG/ZPL) ─────────────────────│
     │                                                 │
     ├─► parse: [(parcel_dict, label_b64), ...]        │
     │     trackingNumber → tracking_number            │
     │     id             → shipment_identifier        │
     │     label_b64      → docs.label                 │
     │     lib.to_multi_piece_shipment(...)            │
     ▼                                                 ▼
ShipmentDetails (one, aggregating N parcels)
```

If a parcel create returns no `id`, the proxy passes `label=None` for
that parcel (it skips the label GET). The parser only emits parcel
details for responses that carry a `trackingNumber`.

## Endpoints

Single host: `https://www.asendia-sync.com` (no test/prod split).

| Purpose | Method | Path |
|---|---|---|
| Authenticate (JWT) | POST | `/api/authenticate` |
| Create parcel (shipment) | POST | `/api/parcels` |
| Fetch label | GET | `/api/parcels/{parcel_id}/label` |
| Fetch return label | GET | `/api/parcels/{parcel_id}/return-label` |
| Cancel parcel | DELETE | `/api/parcels/{parcel_id}` |
| Tracking | GET | `/api/customers/{customer_id}/tracking/{tracking_number}` |
| Create manifest | POST | `/api/manifests` |
| Manifest document | GET | `/api/manifests/{manifest_id}/document` |

Notes:
- DELETE returns HTTP 204 with an empty body; the proxy substitutes
  `"{}"` so the parser has valid JSON to deserialize.
- The label GET uses `decoder=lib.encode_base64` in the create flow so
  the binary body is base64-encoded into `docs.label`. The standalone
  `get_label` / `get_return_label` / `get_manifest_document` helpers
  return the raw body (`decoder=lambda r: r`).
- The label `Accept` header is driven by `LABEL_MIME` (see below); it
  defaults to `application/pdf` for unknown label types.

## Authentication

JWT bearer. There is no OAuth grant — credentials are a plain
`username` / `password` pair (`customer_id` is a separate field used in
the tracking URL path, not for auth).

```
access_token property                    ┌──────────────────┐
       │                                 │  connection_cache │
       ▼                                 │   (per conn)      │
┌──────────────┐    miss / expired       │                  │
│ token cached?│◄────────────────────────│ key:             │
│ + expiry     │                         │  asendia|<user>| │
│ > now+30min  │    cache hit            │  <password>      │
└──────┬───────┘────────────────────────►└──────────────────┘
       │ miss
       ▼  POST /api/authenticate
   ┌─────────────────────────────────────────┐
   │ Content-Type: application/json          │
   │ Body: {username, password}              │
   │ ◄── {id_token}                          │
   └─────────────────────────────────────────┘
       │
       ▼  cached with expiry = now + 23h
   every shipment / cancel / tracking / manifest call carries
   Authorization: Bearer <id_token>
```

`login()` parses the auth response through `error.parse_error_response`
and raises `errors.ParsedMessagesError` if the API returned an error,
so bad credentials surface as a normal parsed message rather than a
raw exception. The expiry is stored as `now + 23h` (the JWT is assumed
to live ≈24h); the `access_token` property refreshes when the cached
expiry is within 30 minutes.

Settings fields (`mappers/asendia/settings.py`):

| Field | Required | Purpose |
|---|---|---|
| `username` | yes | auth |
| `password` | yes | auth |
| `customer_id` | no | tracking URL path segment |
| `account_country_code` | no | generic karrio field |
| `services` | no | rate-sheet override (defaults to `DEFAULT_SERVICES`) |
| `config` | no | `ConnectionConfig` blob |

## Supported operations

| Operation | Wired? | Provider entry point | Proxy method |
|---|---|---|---|
| Rate | yes (local sheet) | `universal_provider.rate_request` | `get_rates` (RatingMixin) |
| Shipment create | yes | `shipment_request` / `parse_shipment_response` | `create_shipment` |
| Shipment cancel | yes | `shipment_cancel_request` / `parse_shipment_cancel_response` | `cancel_shipment` |
| Return shipment | yes | `return_shipment_request` / `parse_return_shipment_response` | `create_return_shipment` (→ `create_shipment`) |
| Tracking | yes | `tracking_request` / `parse_tracking_response` | `get_tracking` |
| Manifest | yes | `manifest_request` / `parse_manifest_response` | `create_manifest` |
| Pickup | no | — | — |

Plugin metadata (`plugins/asendia/__init__.py`): `id="asendia"`,
`label="Asendia"`, `status="beta"`, `is_hub=False`.

## Services & options

### Shipping services — `asendiaService.product` (`ShippingService`)

| karrio service code | Wire `product` |
|---|---|
| `asendia_epaq_standard` | `EPAQSTD` |
| `asendia_epaq_plus` | `EPAQPLS` |
| `asendia_epaq_select` | `EPAQSCT` |
| `asendia_epaq_elite` | `EPAQELT` |
| `asendia_epaq_go` | `EPAQGO` |
| `asendia_epaq_returns_domestic` | `EPAQRETDOM` |
| `asendia_epaq_returns_international` | `EPAQRETINT` |

Default product when `payload.service` is unset: `EPAQSTD`.

### Service modifier — `asendiaService.service` (`ServiceCode`, mandatory)

`asendiaService.service` is a **mandatory** API field. The user may
override it via the `asendia_service_type` option; otherwise the
connector defaults based on product family: `RETPP` when the product
starts with `EPAQRET`, else `CUP`.

| code | meaning |
|---|---|
| `CUP` | Customs unpaid / paid at destination (outbound default) |
| `CPPR` | Customs prepaid by retailer |
| `RETPP` | Prepaid return (return default) |
| `RETPAP` | Partially paid return |

### Packaging / format — `asendiaService.format` (`PackagingType`)

| karrio packaging | Wire `format` |
|---|---|
| `small_box` / `medium_box` / `your_packaging` | `B` (boxable) |
| `envelope` / `pak` | `N` (non-boxable) |
| `tube` | `L` (large) |
| `pallet` | `XL` (extra-large) |

Default packaging when unset: `your_packaging` → `B`.

`units.resolve_format(product, packaging_type, smartgate)` then clamps that mapped
code to the value set the account has a quote for — which is **product-specific**:

| Product / service | Allowed `format` | Behaviour |
|---|---|---|
| SmartGate Flex / Direct (`SGF` / `SGD`) | `N` or `L` | coerce `B` / `XL` → `N`; keep `N` / `L` |
| e-PAQ Elite (`EPAQELT`) | `L` or `XL` | coerce `B` / `N` → `L`; keep `L` / `XL` |
| all other e-PAQ products (Standard, Plus, Select, …) | `B` or `N` | coerce `L` / `XL` → `N`; keep `B` / `N` |

`asendiaService.format` is **always sent** — the Asendia API returns
`VE-004 "asendiaService.format: Mandatory field"` if it is omitted or empty (verified
live; Asendia's written examples showed Select with no format and Elite with `""`, but
the API rejects both). The accepted value is **quote-driven**: a product/lane the
account has no rate for returns `"There is no valid quote"`, so the per-product clamp
above targets the set each product is rated for (Elite quotes are L/XL, Standard US
quotes are N, etc.). A mismatch surfaces as a clean `no valid quote` from Asendia.

### Label types — `labelType` (`LabelType` / `LABEL_MIME`)

| karrio label type | Wire `labelType` value | `Accept` MIME |
|---|---|---|
| `PDF` | `PDF` | `application/pdf` |
| `PNG` | `PNG` | `image/png` |
| `ZPL` | `Zebra` | `text/plain` |

Note the ZPL value on the wire is `Zebra`, not `ZPL`. Default `PDF`.

### Options (`ShippingOption`)

| Option | Wire field | Type | Notes |
|---|---|---|---|
| `asendia_insurance` (= unified `insurance`) | `asendiaService.insurance` | str | values from `InsuranceOption`: `EL45`, `EL150`, `EL500` |
| `asendia_return_label` | `asendiaService.returnLabelOption.enabled` | bool | `service_level=True`, category `RETURN` |
| `asendia_return_label_type` | `returnLabelOption.type` | str | default `EPAQRETDOM`/`EPAQRETINT` by domesticity |
| `asendia_return_label_payment` | `returnLabelOption.payment` | str | default `RETPP` |
| `asendia_sender_eori` | `senderEORI` | str | |
| `asendia_seller_eori` | `sellerEORI` | str | |
| `asendia_sender_tax_id` | `senderTaxId` | str | |
| `asendia_receiver_tax_id` | `receiverTaxId` | str | |
| `asendia_service_type` | `asendiaService.service` | str | overrides the mandatory service modifier; `service_level=True` |

The standard `declared_value` option maps to `shippingCost`.

### Product / service feature flags — `asendiaService.options`

Boolean feature flags ride the `asendiaService.options` wire array. Each
flag's wire code is the first `OptionEnum` argument (read off
`option.code`, never duplicated). Set flags are collected in
`SHIPMENT_FLAG_OPTIONS` order; an empty array is stripped by
`lib.to_dict`.

| Option | Wire code |
|---|---|
| `asendia_economy` | `ECO` |
| `asendia_signature` | `SIG` |
| `asendia_pudo` | `PUDO` |
| `asendia_mailbox` | `MBX` |
| `asendia_dangerous_goods` | `DG` |
| `asendia_personal_delivery` | `PD` |
| `asendia_smartgate_flex` | `SGF` |
| `asendia_smartgate_direct` | `SGD` |
| `asendia_direct_access` | `DA` |
| `asendia_printed_matter` | `PM` |

### SmartGate Flex (Switzerland) — shipping-cost customs line

Asendia's dedicated Swiss services **SmartGate Flex** (`SGF`) and
**SmartGate Direct** (`SGD`) require the shipping cost to be declared as
an **extra customs line** in `customsInfo.items`, alongside the
customer's article items. When `asendia_smartgate_flex` is set,
`create.py` appends this line inline in the request builder:

```json
{
  "articleNumber": "MCGSHP",
  "articleDescription": "Shipping costs",
  "unitValue": 9.99,
  "currency": "EUR",
  "harmonizationCode": "00000000",
  "originCountry": "DE",
  "unitWeight": 0.01,
  "quantity": 1
}
```

Every field is fixed except:

- `currency` — matches the customer's article currency (the resolved
  `customsInfo.currency`).
- `unitValue` — the shipment's shipping cost (`declared_value` →
  `shippingCost`).
- `originCountry` — the shipper's country code.

Mandatory customs fields per Asendia: `articleDescription`,
`articleNumber`, `unitValue`, `currency`, `unitWeight`,
`harmonizationCode`, `originCountry`, `quantity`.

**Format / routing.** SmartGate Flex / Direct require `asendiaService.format` of
`N` or `L` (see the per-product format table above for the full rules). Asendia routes
SmartGate as `EPAQSCT | CPPR | SGF` (or `SGD`); the product and `CUP`/`CPPR` modifier
remain caller-selected (routing is per-subsidiary), and the service is
**onboarding-gated** on Asendia's side before it can be booked. Only **SGF** carries
the `MCGSHP` shipping-cost line — **SGD** does not.

### Connection config (`ConnectionConfig`)

| Key | Type |
|---|---|
| `label_type` | str |
| `shipping_options` | list |
| `shipping_services` | list |

## Data mapping

### Address — karrio `Address` → Asendia `ImporterType`

Both `addresses.sender` and `addresses.receiver` use the same
`ImporterType` shape.

```
karrio Address                  Asendia ImporterType
─────────────────               ────────────────────
person_name      ──► name      (lib.text max 50)
company_name     ──► company   (lib.text max 50)
address_line1    ──► address1  (lib.text max 50)
address_line2    ──► address2
city             ──► city
state_code       ──► province
postal_code      ──► postalCode
country_code     ──► country
email            ──► email
phone_number     ──► phone
```

(The schema also carries `address3`, `mobile`, and an `importer` /
`seller` / `pudoAddress` block, plus `AddressesType.importer` /
`.seller` — none are populated by the connector.)

### Shipment-level fields — `ShipmentRequestType`

```
settings.customer_id                    ──► customerId
label type (resolved)                   ──► labelType
payload.reference / order_id / uuid4    ──► referencenumber
package.weight.KG                       ──► weight            (always KG)
options.declared_value                  ──► shippingCost
options.asendia_sender_eori             ──► senderEORI
options.asendia_seller_eori             ──► sellerEORI
options.asendia_sender_tax_id           ──► senderTaxId
options.asendia_receiver_tax_id         ──► receiverTaxId
```

`referencenumber` falls back through `reference` → `order_id` →
`uuid4().hex` so it is never empty.

### Customs — `CustomsInfo` → `customsInfo`

`customsInfo` is built via `lib.to_customs_info(weight_unit=KG)` by the
`_customs_items()` helper, and is populated when the package has line
items, the customs payload carries commodities, **or** SmartGate Flex is
enabled. The item source is `package.items` if present, else
`customs.commodities`; the SmartGate Flex shipping-cost line (`MCGSHP`)
is appended last when `asendia_smartgate_flex` is set.

```
customs.duty.currency (or "EUR")        ──► customsInfo.currency
commodity i ──► customsInfo.items[i] {
   description / title (max 150)        ──► articleDescription
   sku                                  ──► articleNumber
   value_amount                         ──► unitValue
   value_currency (or customs currency) ──► currency
   hs_code                              ──► harmonizationCode
   origin_country                       ──► originCountry
   weight                               ──► unitWeight
   quantity (or 1)                      ──► quantity
}
```

### Shipment response → `ShipmentDetails`

```
ShipmentResponseType                    ShipmentDetails
────────────────────                    ───────────────
trackingNumber          ──►             tracking_number
id                      ──►             shipment_identifier
label (fetched by proxy)──►             docs.label
                                        label_type (from ctx)
trackingNumber          ──►             meta.carrier_tracking_link
                                          (tracking.asendia.com/tracking/{tn})
labelLocation           ──►             meta.label_location
returnLabelLocation     ──►             meta.return_label_location
returnTrackingNumber    ──►             meta.return_tracking_number
customsDocumentLocation ──►             meta.customs_document_location
commercialInvoiceLocation ─►            meta.commercial_invoice_location
```

`tracking_url` (for `carrier_tracking_link`) is
`https://tracking.asendia.com/tracking/{}` — distinct from the API
host.

## Per-package fan-out & two-tier identifiers

Asendia is one-parcel-per-request. The connector fans out N requests
for an N-parcel shipment and aggregates with
`lib.to_multi_piece_shipment`, keyed by 1-based index.

Each created parcel returns two identifiers, surfaced on different
fields:

| Asendia field | Meaning | Where surfaced |
|---|---|---|
| `trackingNumber` | customer-facing tracking number | `tracking_number` |
| `id` | parcel handle (Asendia internal) | `shipment_identifier` |

`shipment_identifier` (the parcel `id`) is what cancel and manifest
consume:
- **Cancel** — `shipment_cancel_request` returns
  `payload.shipment_identifier` verbatim; the proxy puts it in
  `DELETE /api/parcels/{parcel_id}`.
- **Manifest** — `manifest_request` returns
  `payload.shipment_identifiers` (the list of parcel ids) and POSTs
  them to `/api/manifests`.

## Returns

Two ways to get a return label:

1. **Return-label option on an outbound shipment.** Setting
   `asendia_return_label = True` adds a `returnLabelOption` block to the
   outbound parcel:
   - `type` ← `asendia_return_label_type`, else `EPAQRETDOM` (domestic)
     / `EPAQRETINT` (international), chosen by
     `shipper.country_code == recipient.country_code`.
   - `payment` ← `asendia_return_label_payment`, else `RETPP`.

2. **Dedicated return shipment.** `return_shipment_request`
   (`shipment/return_shipment.py`) is a thin wrapper that forces
   `asendia_return_label = True` into the options and delegates to the
   standard `shipment_request`. The proxy's `create_return_shipment`
   simply calls `create_shipment`, and `parse_return_shipment_response`
   delegates to `parse_shipment_response`.

Return products are `EPAQRETDOM` / `EPAQRETINT` (`ShippingService`);
return payment codes are `RETPP` / `RETPAP` (`ServiceCode`). The
response carries `returnTrackingNumber` / `returnLabelLocation`
(surfaced in `meta`); the dedicated return-label fetch endpoint is
`GET /api/parcels/{id}/return-label`.

## Rating (rate sheet only)

There is **no Asendia rating endpoint**. The connector mixes in
`RatingMixinSettings` / `RatingMixinProxy` and `get_rates` delegates to
the universal rating provider, which evaluates the rate sheet in
`Settings.shipping_services` (defaults to `DEFAULT_SERVICES`).

`DEFAULT_SERVICES` is built by `load_services_from_csv()` from
`karrio/providers/asendia/services.csv` at import time. The CSV columns
are:

```
service_code, service_name, zone_label, country_codes, min_weight,
max_weight, max_length, max_width, max_height, rate, currency,
transit_days, domicile, international
```

Each row's `service_code` is mapped to its karrio name via
`ShippingService.map(...).name_or_key`; rows sharing a service code are
grouped into one `ServiceLevel` with multiple `ServiceZone`s. The
shipped CSV defines all seven e-PAQ products with weight band
`0.01–31.5 KG`, `EUR`, `rate=0.0` (placeholder — operators are expected
to supply real rates via a rate sheet / `services` override). If the
CSV is missing, a single hardcoded `asendia_epaq_standard` fallback
`ServiceLevel` is returned.

## Tracking

`GET /api/customers/{customer_id}/tracking/{tracking_number}`, fired
concurrently (`lib.run_concurently`) for each requested number. The
proxy returns `[(tracking_number, response_dict), ...]` and drops
entries whose body is whitespace-only.

The API returns a **bare JSON array** of tracking-event objects (not a
wrapped object); the tracking number comes from the proxy tuple, not
the body. The parser only builds details for responses that are a
non-empty list. Events are sorted most-recent-first by `time`.

### Event → `TrackingEvent`

```
TrackingEventType                       TrackingEvent
─────────────────                       ─────────────
time (%Y-%m-%dT%H:%M:%SZ)  ──►          date, time, timestamp (ISO 8601)
carrierEventDescription    ──►          description
code                       ──►          code; also drives status + reason
locationName, locationCountry ──►       location (joined ", ")
```

Overall status = status of the latest event, falling back to
`in_transit` when no event maps. `delivered` is `True` when the
resolved status is `delivered`.

### Status mapping (`TrackingStatus`) — code matched against value lists

| karrio status | Asendia codes |
|---|---|
| `pending` | `PENDING`, `CREATED`, `ACCEPTED`, `LABEL_PRINTED` |
| `picked_up` | `PICKED_UP`, `COLLECTED`, `COLLECTION`, `PU` |
| `in_transit` | `IN_TRANSIT`, `IT`, `TRANSIT`, `DEPARTED`, `ARRIVED`, `PROCESSED`, `CUSTOMS`, `CLEARED` |
| `out_for_delivery` | `OUT_FOR_DELIVERY`, `OFD`, `WITH_COURIER` |
| `delivered` | `DELIVERED`, `DL`, `DELIVERY_CONFIRMED` |
| `ready_for_pickup` | `READY_FOR_PICKUP`, `PICKUP`, `AT_LOCATION` |
| `on_hold` | `ON_HOLD`, `HELD`, `AWAITING` |
| `delivery_delayed` | `DELAYED`, `DELAY`, `RESCHEDULED` |
| `delivery_failed` | `DELIVERY_FAILED`, `FAILED`, `UNDELIVERABLE`, `RETURNED`, `RTS` |

### Incident reason mapping (`TrackingIncidentReason`)

The event `code` is also matched against `TrackingIncidentReason` and
attached as `event.reason`. Examples: `carrier_damaged_parcel`
(`DAMAGED`/`DMG`), `consignee_refused` (`REFUSED`/`RJ`), `customs_delay`
(`CUSTOMS_DELAY`/`CD`), `weather_delay` (`WEATHER`/`WE`); full
carrier/consignee/customs/weather taxonomy lives in `units.py`.

## Error parsing

Asendia surfaces errors in two distinct shapes, both handled by
`error.parse_error_response`:

1. **API-level (RFC 7807 Problem Details).** Keys: `type`, `title`,
   `status`, `detail`, `path`, `message`, `fieldErrors[]`
   (`{objectName, field, message}`). Treated as an error when
   `status >= 400`, or `title` is present, or `fieldErrors` is
   non-empty. One `Message` per field error
   (`"{field}: {message}"`), else a single general message
   (`detail` → `message` → `title`).

2. **Parcel-level.** A successful-looking response body may carry
   `errorMessages: [{field, message}]`. Each becomes a `Message` with
   code `PARCEL_ERROR` and text `"{field}: {message}"`.

```
response
   │
   ├─ None ─────────────────► []   (no errors)
   ├─ list (e.g. tracking) ──► []   (bare arrays carry no errors)
   │
   ├─ status is numeric ≥400 ─┐
   ├─ title present           ├──► API-level Message(s)
   ├─ fieldErrors non-empty  ─┘     (per-field or general)
   │
   └─ errorMessages[] present ───► PARCEL_ERROR Message(s)
```

Quirk: `status` is only treated as an HTTP error code when it is
numeric (or a numeric string). Non-numeric `status` values — e.g.
manifest responses returning `status: "CREATED"` — are explicitly
**not** errors. Manifest also adds its own `MANIFEST_ERROR`
(`manifest.errorMessage`) and per-parcel `PARCEL_ERROR`
(`manifest.errorParcelIds`) messages in `parse_manifest_response`.

Shipment parsing aggregates errors across all per-parcel responses
(`sum([parse_error_response(parcel, …) for parcel, _ in responses])`),
so a partial failure surfaces alongside the parcels that succeeded.

## References

- **OpenAPI (authoritative)** — Asendia Sync API
  <https://www.asendia-sync.com/v3/api-docs> (Swagger UI:
  <https://www.asendia-sync.com/swagger-ui/index.html>), mirrored at
  `vendor/openapi.json` / `vendor/openapi.yaml`.
- **Vendor notes** — `vendor/README.md` (endpoint table, enum summary,
  spec-refresh command).
- **Rate sheet** — `karrio/providers/asendia/services.csv` (the only
  source of service/weight-band/zone/rate data — not in the OpenAPI).
- **Generated schemas** — `karrio/schemas/asendia/*.py` is generated
  from `schemas/*.json` via the connector's `generate` script (kcli,
  `--no-nice-property-names` for the camelCase Asendia fields,
  `--nice-property-names` only for `auth_response` so `id_token` keeps
  its snake_case). Regenerate with
  `./bin/run-generate-on modules/connectors/asendia` — never hand-edit
  the generated `.py` files.
