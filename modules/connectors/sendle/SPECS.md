# Sendle integration — specification

Reference for the Sendle connector. Sendle is a JSON REST carrier serving
Australia (`api.sendle.com`) and the United States, billed per-order rather
than per-rate-quote. The connector supports **rate**, **shipment
create/cancel**, and **tracking**. Anything specific to the vendor's API
contract, the conventions layered on top, or the historical decisions about
what we send and why lives here, not as comments in the code.

The **vendor source of truth** is the Sendle developer docs at
<https://www.sendle.com/developers> (the `PluginMetadata.documentation`
URL). The JSON request/response samples under `schemas/*.json` are the
ground truth that the generated dataclasses under `karrio/schemas/sendle/`
are inferred from.

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio RateRequest / ShipmentRequest /
│   (karrio core)         │   ShipmentCancelRequest / TrackingRequest
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  providers/sendle       │   Pure data transforms.
│   rate.py               │   Unified model → typed Sendle request,
│   shipment/create.py    │   typed Sendle response → unified model.
│   shipment/cancel.py    │   No HTTP, no side effects.
│   tracking.py           │
│   error.py              │
│   units.py              │   ShippingService, ShippingOption,
│   utils.py              │   TrackingStatus, TrackingIncidentReason,
│                         │   Settings (auth), order-failure helpers
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  mappers/sendle/proxy.py│   HTTP transport only.
│   - get_rates           │   - HTTP Basic auth (sendle_id:api_key)
│   - create_shipment     │   - per-parcel async fan-out
│   - cancel_shipment     │   - order → label two-call chaining
│   - get_tracking        │   - failed-order rollback
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Sendle REST API        │
│  ─────────────────────  │
│  GET  /api/products     │   rate quotes
│  POST /api/orders       │   create order
│  GET  <label url>       │   fetch label PDF (base64)
│  DELETE /api/orders/{id}│   cancel order
│  GET  /api/tracking/{r} │   tracking events
└─────────────────────────┘
```

**Key architectural choices:**

- **Per-parcel fan-out.** Each operation builds one request per parcel and
  runs them concurrently via `lib.run_asynchronously`. Multiple responses
  are aggregated into a single unified result with
  `lib.to_multi_piece_rates` (rates) / `lib.to_multi_piece_shipment`
  (shipments).
- **Two-call shipment creation.** Sendle's `POST /api/orders` returns the
  order plus a list of label URLs but not the label bytes; the proxy issues
  a second `GET` to the `a4` label URL to fetch the PDF. See
  [Shipment creation](#shipment-creation-two-call-flow).
- **Failed-order rollback.** If any parcel in a multi-parcel shipment fails
  to create, the proxy does **not** fetch labels — instead it `DELETE`s the
  orders that did succeed, so a partial multi-piece shipment is never left
  half-created. See [Order-failure rollback](#order-failure-rollback).
- **Static service catalog.** There is no dynamic per-account product
  catalog fetch. `ShippingService` is a fixed 3-value enum and
  `DEFAULT_SERVICES` (the `service_levels` in plugin metadata) is loaded
  from a checked-in `services.csv`.
- **Generated schemas** — `karrio/schemas/sendle/*.py` is generated from
  `schemas/*.json` (kcli infers types). Don't hand-edit; regenerate with
  `./bin/run-generate-on modules/connectors/sendle`.

## Data flow

### Shipment creation (two-call flow)

```
ShipmentRequest                                   Sendle API
     │                                                │
     ├─► shipment_request()  (per parcel)             │
     │     to_address(shipper/recipient)              │
     │     to_packages / to_shipping_options          │
     │     to_customs_info (intl only)                │
     │                                                │
     ├─► [OrderRequestType, ...] → lib.to_json        │
     │                                                │
     │   ─── POST /api/orders ───────────────────────►│
     │                                                │  validate
     │   ◄── { order_id, sendle_reference,            │  create order
     │         labels: [{size:"a4", url}, ...] } ──────│
     │                                                │
     ├─► check_for_order_failures(orders)             │
     │     any order missing order_id? → has_failure  │
     │                                                │
     ├─► shipment_next_call(response, has_failure):   │
     │     ok  → GET labels[0].url   (a4 label)       │
     │     fail→ DELETE /api/orders/{order_id}        │
     │     no order_id → abort (no 2nd call)          │
     │                                                │
     │   ─── GET <labels[0].url> ─────────────────────►│
     │   ◄── PDF bytes (label_decoder → base64) ───────│
     │                                                │
     ├─► _extract_details(order, label):              │
     │     sendle_reference → tracking_number         │
     │     order_id         → shipment_identifier     │
     │     label (base64)   → docs.label (PDF)        │
     │                                                │
     ▼                                                ▼
ShipmentDetails                                  (order + label fetched)
```

### Rate quoting

```
RateRequest                                       Sendle API
     │                                                │
     ├─► rate_request()  (one ProductRequestType      │
     │     per parcel; sender/receiver address,        │
     │     weight KG, volume m³, dims CM)             │
     │                                                │
     │   ─── GET /api/products?<urlencoded params> ──►│
     │   ◄── [ {quote, price_breakdown,                │
     │          tax_breakdown, eta, product}, ... ] ───│
     │                                                │
     ├─► _extract_details per element with a `quote`: │
     │     product.code → service                     │
     │     quote.gross  → total_charge + currency     │
     │     price_breakdown + tax_breakdown            │
     │       (amount > 0) → extra_charges             │
     │     eta.days_range[-1] → transit_days          │
     │                                                │
     ▼                                                ▼
list[RateDetails]                                 (multi-piece rates)
```

## Endpoints

Test mode: `https://sandbox.sendle.com`. Prod: `https://api.sendle.com`
(`provider_utils.Settings.server_url`, switched by `test_mode`).

| Purpose | Method | Path |
|---|---|---|
| Rate quote | GET | `/api/products?{urlencoded query}` |
| Create order | POST | `/api/orders` |
| Fetch label | GET | `labels[0].url` from the order response (the `a4` PDF) |
| Cancel order (rollback / cancel) | DELETE | `/api/orders/{order_id}` |
| Tracking | GET | `/api/tracking/{ref}` |

All calls send `Accept: application/json`; POST/DELETE/tracking also send
`Content-type: application/json`. Every call carries
`Authorization: Basic <base64(sendle_id:api_key)>`.

## Authentication

HTTP Basic Auth. There is no OAuth, no token caching, and no separate auth
call. `provider_utils.Settings.authorization` base64-encodes
`"{sendle_id}:{api_key}"` and the proxy injects it on every request as
`Authorization: Basic <authorization>`.

```
Settings.authorization = base64( f"{sendle_id}:{api_key}" )

Authorization: Basic <authorization>     ◄── sent on every request
```

Connection settings (`mappers/sendle/settings.py`):

| Field | Required | Notes |
|---|---|---|
| `sendle_id` | yes | account ID, the Basic-auth username |
| `api_key` | yes | the Basic-auth password |
| `test_mode` | no (default `False`) | selects sandbox vs prod base URL |
| `account_country_code` | no | AU / US account region |
| `metadata`, `config` | no | generic connection blobs |

There is no `ConnectionConfig` enum for this connector.

## Supported operations

| Operation | Wired | Provider | Notes |
|---|---|---|---|
| Rate | yes | `rate.py` | `GET /api/products` per parcel |
| Shipment create | yes | `shipment/create.py` | two-call (order, then label) |
| Shipment cancel | yes | `shipment/cancel.py` | `DELETE /api/orders/{id}` |
| Tracking | yes | `tracking.py` | `GET /api/tracking/{ref}` |
| Pickup | no | — | not implemented |
| Document upload / manifest | no | — | not implemented |

## Services & options

### Services — `ShippingService` (`units.py`)

| karrio service | Sendle `product_code` (wire) |
|---|---|
| `sendle_standard_pickup` | `STANDARD-PICKUP` |
| `sendle_standard_dropoff` | `STANDARD-DROPOFF` |
| `sendle_express_pickup` | `EXPRESS-PICKUP` |

On shipment create the service is mapped via `ShippingService.map(service).value_or_key`,
so an **unknown service string is forwarded verbatim** as `product_code`
(the test suite exercises this: `service="allied_road_service"` ships
`product_code: "allied_road_service"` unchanged).

`DEFAULT_SERVICES` (exposed as `service_levels` in the plugin metadata) is
built from `karrio/providers/sendle/services.csv` via
`load_services_from_csv()`. Each CSV row becomes a `ServiceZone` keyed by
the karrio service code; rows for the same service collapse into one
`ServiceLevel` with multiple zones. All checked-in rows are AU-domestic
(`domicile=true`, `international` blank → `None`), currency `AUD`, weight
`KG` / dimension `CM`, weight bands `0.01–25 kg`, max dims `120×60×60 cm`,
transit `3–7` days for STANDARD and `1–3` for EXPRESS. The CSV `rate` column
is `0.0` (placeholder; live pricing comes from `/api/products`).

### Options — `ShippingOption` (`units.py`)

| karrio option | Sendle wire key | Type | Where it lands |
|---|---|---|---|
| `sendle_hide_pickup_address` | `hide_pickup_address` | bool | `OrderRequestType.hide_pickup_address` |
| `sendle_first_mile_option` | `first_mile_option` | bool | `OrderRequestType.first_mile_option` |

Both carry `meta=dict(category="DELIVERY_OPTIONS")`.
`shipping_options_initializer` filters incoming option keys to those defined
in `ShippingOption` before constructing `units.ShippingOptions`. The standard
`instructions` option flows to `sender.instructions`; the standard
`shipment_date` option flows to `pickup_date`; the standard `currency` option
flows to `parcel_contents[].currency`.

## Data mapping

### Shipment — `ShipmentRequest` → `OrderRequestType` (`shipment/create.py`)

Sendle uses `sender` / `receiver` envelopes, each `{address, contact,
instructions, tax_ids}`.

```
karrio Address (shipper/recipient)      Sendle address{} / contact{}
──────────────────────────────────     ─────────────────────────────
country_code        ───►                address.country
address_line1       ───►                address.address_line1
address_line2       ───►                address.address_line2
city                ───►                address.suburb
postal_code         ───►                address.postcode
state_code          ───►                address.state_name
person_name         ───►                contact.name
email               ───►                contact.email
phone               ───►                contact.phone
company_name        ───►                contact.company
tax_id              ───►                tax_ids.ioss   (only if present)
```

Order-level fields:

| Sendle field | Source |
|---|---|
| `description` | `package.parcel.description` |
| `customer_reference` | `payload.reference` |
| `product_code` | mapped service (`value_or_key`) |
| `first_mile_option` | `options.sendle_first_mile_option` |
| `pickup_date` | `lib.fdate(options.shipment_date)` |
| `weight` | `{units: "KG", value: package.weight.KG}` |
| `volume` | `{units: "m3", value: package.volume.m3}` |
| `dimensions` | `{units: "CM", width, length, height}` (CM) |
| `metadata` | `getattr(payload, "metadata", None)` |
| `hide_pickup_address` | `options.sendle_hide_pickup_address` |
| `parcel_contents` | international only (see below) |

`sender.instructions` is set from `package.options.instructions`;
`receiver.instructions` is always `None`.

### Customs / `parcel_contents` (international only)

`is_international` is `recipient.country_code != shipper.country_code`. When
true, `parcel_contents[]` is populated; when false it is `[]` (omitted by
`lib.to_dict`). Items are sourced from `package.items` if any are present,
otherwise from `customs.commodities` (built by `lib.to_customs_info` with
`weight_unit=KG`).

| Sendle `parcel_contents[]` field | Source |
|---|---|
| `description` | `item.title or item.description` |
| `value` | `str(item.value_amout)` (note: the SDK field is spelled `value_amout`) |
| `currency` | `package.options.currency` |
| `quantity` | `item.quantity` |
| `country_of_origin` | `item.origin_country or shipper.country_code` |
| `hs_code` | `item.hs_code or item.sku` |

Note the request `OrderRequestType` does not emit a top-level
`contents_type` (present in the sample JSON but not set by the mapper).

### Rate — `RateRequest` → `ProductRequestType` (`rate.py`)

Flat query params (URL-encoded onto `/api/products`), one request per parcel:

| Sendle param | Source |
|---|---|
| `sender_address_line1/2`, `sender_suburb`, `sender_postcode`, `sender_country` | shipper address |
| `receiver_address_line1/2`, `receiver_suburb`, `receiver_postcode`, `receiver_country` | recipient address |
| `weight_value` / `weight_units` | `package.weight.KG` / `"kg"` |
| `volume_value` / `volume_units` | `package.volume.m3` / `"m3"` |
| `length_value` / `width_value` / `height_value` / `dimension_units` | package dims / `"cm"` |

### Rate response — `ProductResponseElementType` → `RateDetails`

| RateDetails field | Source |
|---|---|
| `service` | `ShippingService.map(product.code).name_or_key` |
| `total_charge` | `quote.gross.amount` |
| `currency` | `quote.gross.currency` |
| `transit_days` | `eta.days_range[-1]` |
| `extra_charges` | every `price_breakdown` + `tax_breakdown` entry whose `amount > 0` |
| `meta.service_name` | `service.name or product.name` |
| `meta.days_range` / `meta.date_range` | from `eta` |
| `meta.plan` | `plan` (e.g. `"Sendle Pro"`) |

Only response elements that carry a `quote` are turned into rates;
quote-less elements are skipped.

### Shipment response — `OrderResponseType` → `ShipmentDetails`

| ShipmentDetails field | Source |
|---|---|
| `tracking_number` | `order.sendle_reference` (e.g. `SNFJJ3`) |
| `shipment_identifier` | `order.order_id` (UUID) |
| `label_type` | `"PDF"` |
| `docs.label` | base64 PDF from the label-fetch call |
| `meta.carrier_tracking_link` | `order.tracking_url` |
| `meta.customer_reference` | `order.customer_reference` |
| `meta.order_url` / `meta.order_id` | from order |
| `meta.metadata` | `order.metadata` |
| `meta.tracking_numbers` | `[order.sendle_reference]` |
| `meta.shipment_identifiers` | `[order.order_id]` |

### Identifiers (two-tier)

Sendle returns two distinct identifiers per order:

| Field | Meaning | Where we surface it |
|---|---|---|
| `sendle_reference` | customer-facing reference (on the label, in `tracking_url`) | `tracking_number`; the value passed to `GET /api/tracking/{ref}` |
| `order_id` | internal order UUID | `shipment_identifier`; the value passed to `DELETE /api/orders/{id}` |

## Shipment creation — two-call flow

`POST /api/orders` returns the order body including `labels`, a list of
`{format, size, url}` entries (sizes `a4` and `cropped`). The body carries
no label bytes, so the proxy fires a second `GET` to the **first** label
URL (`labels[0].url`, the `a4` PDF) and `label_decoder` reads the binary
body and base64-encodes it into `docs.label`. `label_decoder` is failsafe:
if the body happens to be JSON it merges it in, and a `label` key is always
present (possibly empty).

## Order-failure rollback

`utils.check_for_order_failures` flags `has_failure = True` if **any**
order response is missing `order_id`. `utils.shipment_next_call` then
decides the second call per order:

- **Success path** (`labels` present and `not has_failure`) → `GET` the
  label URL.
- **Rollback path** (this order has an `order_id` but `has_failure` is true,
  i.e. a *sibling* parcel failed) → `DELETE /api/orders/{order_id}` so a
  partial multi-piece shipment isn't left created.
- **Abort** (no `order_id` — this order itself failed) → returns
  `{abort: True}`; the proxy skips the second call entirely and just passes
  the order response through to error parsing.

This keeps the proxy a thin transport layer while ensuring an all-or-nothing
multi-parcel create.

## Cancellation

`shipment_cancel_request` collects the order IDs to cancel from
`payload.shipment_identifier` plus any `options.shipment_identifiers`,
deduplicated via `set`, and emits one `CancelRequestType{id}` each. The
proxy `DELETE`s `/api/orders/{id}` per ID. The response is treated as a
success if **any** response has `state == "Cancelled"`
(`OrderResponseType.state`); the cancel response also carries
`cancelled_at` and `cancellation_message`.

## Tracking

`GET /api/tracking/{ref}` per tracking number, fanned out async. The
response carries a top-level `state`, a `scheduling` block, and
`tracking_events[]`. Only responses that contain `tracking_events` are
turned into `TrackingDetails`; the rest go to error parsing.

- **Events** are iterated in **reversed** order (the API lists newest-first;
  karrio wants oldest-first).
- **Timestamps**: each event prefers `local_scan_time` over `scan_time`,
  parsed with `try_formats=["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"]`;
  `date` formats to `%Y-%m-%d`, `time` to `%H:%M %p`, plus an ISO
  `timestamp`.
- **Location**: `"{origin_location} to {destination_location}"` when both
  are present, else `event.location`.
- **Estimated delivery**: first of
  `scheduling.estimated_delivery_date_minimum`,
  `…_maximum`, then `delivered_on`.

### Status mapping — `TrackingStatus` (matched against `state` and `event_type`)

| karrio status | Sendle values |
|---|---|
| `on_hold` | `Pickup Attempted`, `Delivery Attempted` |
| `delivered` | `Delivered` |
| `in_transit` | `Pickup`, `Drop Off`, `Dropped Off`, `In Transit` |
| `delivery_failed` | `Damaged`, `Unable to Deliver` |
| `delivery_delayed` | `Card Left` |
| `out_for_delivery` | `Out for Delivery`, `Local Delivery` |
| `ready_for_pickup` | `Left with Agent` |

The shipment-level `status` is resolved from `details.state`, defaulting to
`in_transit` when no enum matches. `delivered` is `True` when the resolved
status is `delivered`. Per-event `status` is resolved from `event_type` (no
default).

### Incident reasons — `TrackingIncidentReason`

Per-event `reason` is matched against both `event_type` and `description`
across a normalized taxonomy of carrier / consignee / customs / weather /
delivery-exception buckets (e.g. `Damaged → carrier_damaged_parcel`,
`Refused → consignee_refused`, `Customs Hold → customs_delay`,
`Card Left → consignee_not_home`). Falls back to `unknown` when nothing
matches.

## Error parsing

Sendle errors are a flat JSON object with `error`, `error_description`, and
`messages` (`error_responses.json`):

```json
{ "error": "payment_required",
  "error_description": "One of the payment methods ... add a new payment method." }
```

`error.parse_error_response` (`error.py`) accepts either a single dict or a
list, keeps only entries where `error` is set, and maps each to a
`models.Message`:

| Message field | Source |
|---|---|
| `code` | `error` (e.g. `payment_required`, `unprocessable_entity`) |
| `message` | `messages` if it is a string, else `error_description` (stripped) |
| `details.messages` | raw `messages` (can be `{}` or a string) |
| `details.error_description` | `error_description` (stripped) |
| `details.<kwargs>` | extra context (e.g. `tracking_number` on cancel/track) |

```
Response(s)                ┌──────────────────────────────┐
   │                       │ error.parse_error_response     │
   ├─► normalize to list ─►│   - drop entries w/o `error`   │
   │                       │   - message: str(messages) or  │
   │                       │     error_description           │
   ▼                       └───────────────┬────────────────┘
list | dict                                ▼
                                     list[Message]
```

Each provider parser sums `parse_error_response` over its responses;
shipment/cancel/tracking parsers thread a `tracking_number` kwarg into
`details`. `messages` can be an empty object `{}`, a string, or absent —
the parser handles all three.

## Internationalization

`providers/sendle/i18n.py` carries `SERVICE_NAME_TRANSLATIONS` and
`OPTION_NAME_TRANSLATIONS` (German via `gettext_lazy`) for the three
services and two options, for display in the shipping app.

## References

- **Vendor docs** — <https://www.sendle.com/developers>
- **Vendor site** — <https://www.sendle.com>
- **Request/response samples (source of truth)** — `schemas/*.json`:
  `order_request`, `order_response`, `product_request`, `product_response`,
  `cancel_request`, `cancel_response`, `tracking_request`,
  `tracking_response`, `error_responses`.
- **Service catalog** — `karrio/providers/sendle/services.csv`
  (loaded into `DEFAULT_SERVICES`).
- **Generated schemas** — `karrio/schemas/sendle/*.py` is generated from
  `schemas/*.json` by kcli (see the `generate` script). Regenerate with
  `./bin/run-generate-on modules/connectors/sendle` — never hand-edit.
