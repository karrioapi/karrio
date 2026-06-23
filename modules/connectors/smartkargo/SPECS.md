# SmartKargo integration — specification

Reference for the SmartKargo connector. SmartKargo is an air-cargo /
e-commerce parcel platform; the connector talks to its **iHub** JSON
REST API (the "IHUB Swagger" surface). It supports **rating**,
**shipment booking + label fetch**, **void/cancel**, and **tracking**.
There is no pickup, manifest, or document-upload flow.

The **vendor source of truth** is the iHub OpenAPI spec and integration
manual kept under `vendor/`:

- `vendor/openapi.yaml` / `vendor/openapi.html` — the IHUB Swagger
  (title "IHUB Swagger", version 1.0.0).
- `vendor/SmartKargo_API_Integration_Manual_V1.1.pdf` — error-format
  reference (manual pages 11-12, 20-24 are cited inline in `error.py`).
- `vendor/Insomnia_2026-03-01.har` — captured request/response samples.

Status is `beta` (see `karrio/plugins/smartkargo/__init__.py`).

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio RateRequest / ShipmentRequest /
│   (karrio core)         │   ShipmentCancelRequest / TrackingRequest
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  providers/smartkargo   │   Pure data transforms (no HTTP).
│   rate.py               │   Unified model → typed iHub request,
│   shipment/create.py    │   typed iHub response → unified model.
│   shipment/cancel.py    │   units.ShippingService/Option/Tracking-
│   tracking.py           │   Status enums live in units.py.
│   error.py              │   utils.py: Settings + response helpers
│   units.py              │   (extract_booking_data, parse_void_response)
│   utils.py              │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  mappers/smartkargo/    │   HTTP transport only.
│   proxy.py              │   - api_key in `code` header
│                         │   - optional `SiteId` header
│   get_rates             │   - per-package async fan-out
│   create_shipment       │   - 2-leg create (book → GET label)
│   cancel_shipment       │   - cancel/track via query string GETs
│   get_tracking          │
│   get_label             │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  SmartKargo iHub API    │
│  ─────────────────────  │
│  POST /quotation        │   rate quote (one package per call)
│  POST /exchange/single  │   shipment booking (?version=2.0)
│  GET  <labelUrl>        │   label fetch (absolute URL from booking)
│  GET  /shipment/void    │   cancel (query-string params)
│  GET  /tracking         │   tracking events (query-string params)
└─────────────────────────┘
```

**Key architectural choices:**

- **Per-package fan-out.** The iHub API accepts exactly one package per
  request for both `/quotation` and `/exchange/single`. The providers
  build a `list` of requests (one per `package`) and the proxy fires
  them with `lib.run_asynchronously`. Responses are recombined with
  `lib.to_multi_piece_rates` (rates) / `lib.to_multi_piece_shipment`
  (shipments).
- **Two-leg shipment create.** Booking returns a `labelUrl`; the proxy
  immediately issues a second `GET` against that URL to fetch the
  base64 label payload. Both legs run inside `create_shipment`.
- **No OAuth / no token cache.** Auth is a static API key carried in the
  `code` header on every request, plus an optional `SiteId` header.
- **Shared request type.** `shipment/create.py` reuses the rate
  `RateRequestType` / `PackageType` schema for booking — the booking
  payload is the rate payload plus `deliveryType` / `channel` /
  `labelRef2`.
- **Generated schemas** — `karrio/schemas/smartkargo/*.py` is generated
  from `schemas/*.json` with `--no-nice-property-names` (the iHub API is
  camelCase). Don't hand-edit; regenerate with
  `./bin/run-generate-on modules/connectors/smartkargo`.

## Data flow

### Rate (one HTTP call per package)

```
RateRequest                              SmartKargo iHub
     │                                         │
     ├─► rate_request                          │
     │     to_address(shipper/recipient)       │
     │     to_packages(required=["weight"])    │
     │     [RateRequestType per package]       │
     │                                         │
     │   ─── POST /quotation (xN) ────────────►│
     │                                         │  price + SLA
     │   ◄── {status:"QUOTED", details:[…]} ───│
     │                                         │
     ├─► parse_rate_response:                  │
     │     keep status == "QUOTED"             │
     │     _extract_details per detail         │
     │     to_multi_piece_rates                │
     ▼                                         ▼
list[RateDetails]                        (no further call)
```

### Shipment create (book, then fetch label — two HTTP calls per package)

```
ShipmentRequest                                       SmartKargo iHub
     │                                                      │
     ├─► shipment_request                                   │
     │     [RateRequestType per package]                    │
     │     ctx = {label_type: PDF|ZPL}                      │
     │                                                      │
     │   ─── POST /exchange/single?version=2.0 (xN) ───────►│
     │                                                      │
     │   ◄── [{status:"Processed", valid:"Yes",             │
     │         shipments:[{status:"Booked", labelUrl,       │
     │                     prefix, airWaybill,…}]}] ─────────│
     │                                                      │
     ├─► extract_booking_data: unwrap [ … ],                │
     │     pull labelUrl when shipment.status=="Booked"     │
     │                                                      │
     │   ─── GET <labelUrl>[&format=zpl] (xN) ─────────────►│
     │   ◄── {base64Content: "…"} ──────────────────────────│
     │                                                      │
     ├─► parse_shipment_response:                           │
     │     _is_valid_booking gate                           │
     │     tracking_number = prefix + airWaybill            │
     │     strip data-URI prefix from base64Content         │
     │     to_multi_piece_shipment                          │
     ▼                                                      ▼
ShipmentDetails                                       (both legs done)
```

If a booking response carries no `labelUrl` (status != `Booked`), the
proxy skips the label `GET` and substitutes an empty `{}` so the label
fan-out stays aligned with the booking fan-out.

### Cancel / Tracking (query-string GET per tracking number)

```
ShipmentCancelRequest                       TrackingRequest
     │                                            │
     ├─ tracking_numbers from                     ├─ per number, build query:
     │  options.tracking_numbers                  │   prefix+Airwaybill, or
     │  (fallback prefix+air_waybill)             │   packageReference
     │                                            │
     │ GET /shipment/void?prefix=…&airWaybill=…   │ GET /tracking?prefix=…&Airwaybill=…
     ▼                                            ▼
ConfirmationDetails                          list[TrackingDetails]
```

## Endpoints

`server_url` is selected by `test_mode` (see `utils.Settings.server_url`):

- **Test/UAT**: `https://uatihub.smartkargo.com/ihub-uat-mt-api-function`
- **Prod**: `https://ihub.smartkargo.com/ihub-mt-api-function`

| Purpose | Method | Path |
|---|---|---|
| Rate quote | POST | `{server_url}/quotation` |
| Book shipment | POST | `{server_url}/exchange/single?version=2.0` |
| Fetch label | GET | absolute `labelUrl` from booking response (`&format=zpl` when ZPL) |
| Void / cancel | GET | `{server_url}/shipment/void?prefix=…&airWaybill=…&userName=…&reason=…` |
| Tracking | GET | `{server_url}/tracking?<query>` |
| Label by URL (re-fetch) | GET | `{labelUrl}[&format=zpl]` — `proxy.get_label` |

The vendor OpenAPI exposes many more iHub endpoints (`/shipment/void`,
`/shipment/tracking`, `/label`, `/zipCodeCoverage`, `/serviceCoverage`,
truck/nest depart/arrive, invoicing, etc.) — the connector wires only
the five above.

## Authentication

Static API key, no OAuth, no token caching. Two credential fields live
on the connection (`mappers/smartkargo/settings.py`):

| Setting | Used for |
|---|---|
| `api_key` | sent as the `code` request header on every call |
| `account_number` | shipper `account` + default `primaryId` on the request body |

Plus generic karrio fields: `test_mode`, `carrier_id` (default
`smartkargo`), `account_country_code`, `metadata`, `config`.

Every proxy call sets:

```
Content-Type: application/json
code:         <api_key>
SiteId:       <connection_config.site_id>   # only when configured
```

`SiteId` is optional — emitted only when `ConnectionConfig.site_id` is
set on the connection.

## Supported operations

| Operation | Wired? | Notes |
|---|---|---|
| Rate | yes | `POST /quotation`, one call per package |
| Shipment create | yes | `POST /exchange/single?version=2.0` + label `GET` |
| Shipment cancel | yes | `GET /shipment/void` |
| Tracking | yes | `GET /tracking` |
| Pickup | no | not implemented |
| Document upload | no | not implemented |
| Manifest | no | not implemented |

`is_hub = False` (single-carrier connector, not an aggregator).

## Services & options

### Shipping services — `units.ShippingService`

karrio service key → iHub `serviceType` wire code:

| karrio key | Wire code | SmartKargo product |
|---|---|---|
| `smartkargo_express` | `EXP` | eCommerce Express |
| `smartkargo_priority` | `EPR` | eCommerce Priority |
| `smartkargo_standard` | `EST` | eCommerce Standard |
| `smartkargo_economy` | `ECL` | eCommerce Economy (Five Days) |

### Shipping options — `units.ShippingOption`

`OptionEnum` wire codes (first positional arg = wire key):

| karrio option | Wire key | Type | Where it lands |
|---|---|---|---|
| `smartkargo_insurance` | `hasInsurance` | bool | — (see insurance note) |
| `smartkargo_declared_value` | `insuranceAmmount` | float | `PackageType.insuranceAmmount` + drives `hasInsurance` |
| `smartkargo_delivery_type` | `deliveryType` | str | `PackageType.deliveryType` (default `DoorToDoor`) |
| `smartkargo_channel` | `channel` | str | `PackageType.channel` (default `Direct`) |
| `smartkargo_label_ref2` | `labelRef2` | str | `PackageType.labelRef2` |
| `smartkargo_special_handling` | `specialHandlingType` | str | `PackageType.specialHandlingType` |
| `smartkargo_commodity_type` | `commodityType` | str | `PackageType.commodityType` (default `9999`) |
| `smartkargo_incoterm` | `incoterm` | str | (declared; commercial-invoice uses `customs.incoterm`) |
| `smartkargo_additional_info_01..04` | `additionalInfo01..04` | str | additional-info passthrough |

**Unified mapping:** the standard karrio `insurance` option maps onto
`smartkargo_declared_value`. The wire field is the (mis-spelled by the
vendor) `insuranceAmmount`; `hasInsurance` is set `True` whenever a
declared value is present (`options.smartkargo_declared_value.state is
not None`).

The `shipping_options_initializer` filters to keys present in
`ShippingOption` and merges parcel-level options.

### Connection config — `units.ConnectionConfig`

| Config key | Type | Purpose |
|---|---|---|
| `primary_id` | str | request `primaryId` (falls back to `account_number`) |
| `site_id` | str | `SiteId` header (omitted when unset) |
| `additional_id` | str | request `additionalId` (falls back to `primary_id`) |
| `origin` | str | `PackageType.origin` |
| `destination` | str | `PackageType.destination` |
| `currency` | str | rate/shipment currency (default `USD`) |
| `shipping_options` | list | option allow-list |
| `shipping_services` | list | service allow-list |

**Quirk — `label_type` is not a declared config key.**
`shipment/create.py` reads
`settings.connection_config.label_type.state`, but `ConnectionConfig`
defines no `label_type` member, so that lookup resolves to an unset
option (falsy). In practice the label type comes from
`payload.label_type` and otherwise defaults to `"PDF"`; only `ZPL`
changes behaviour (appends `&format=zpl` to the label URL).

### Packaging / units

- **`PackagingType`**: every unified packaging type collapses to the
  single iHub value `PACKAGE`.
- **`PaymentMode`**: `PX` (billed, the value the connector always
  sends), `PP` (prepaid), `CC` (collect from consignee). Only `PX` is
  emitted.
- **Weight unit** (`WeightUnit`): `KG` / `LBR`. **Dimension/volume unit**
  (`DimensionUnit`): `CMQ` (cm) / `CFT` (in). The connector pairs them by
  metric heuristic: when `packages.weight_unit == "KG"` it sends
  `KG` + `CMQ`, otherwise `LBR` + `CFT`.

## Data mapping

### Address / participant — karrio `Address` → `ParticipantType`

Both shipper and recipient ride in the same `participants[]` list,
distinguished by `type` (`"Shipper"` / `"Consignee"`).

```
karrio Address                ParticipantType
─────────────────             ──────────────────
company_name or person_name ─► name
postal_code                 ─► postCode
street (line1)              ─► street
address_line2               ─► street2
city                        ─► city
state_code                  ─► state
country_code                ─► countryId
phone_number                ─► phoneNumber
email                       ─► email
tax_id                      ─► taxId
```

Shipper-only participant fields:

```
settings primary_id (or account_number)  ─► primaryId
settings additional_id (or primary_id)   ─► additionalId
settings.account_number                  ─► account
```

The Consignee participant sends `primaryId` / `additionalId` /
`account` as `None`.

### Package — karrio package → `PackageType` + `DimensionType`

```
karrio                              PackageType
─────────────────                   ──────────────────
parcel.reference_number / PKG-{n} ─► reference
options.smartkargo_commodity_type ─► commodityType (default "9999")
service / payload.service         ─► serviceType (mapped enum)
PaymentMode.PX                    ─► paymentMode
config.origin                     ─► origin
config.destination                ─► destination
parcel.description / "General…"   ─► packageDescription
1                                 ─► totalPackages, totalPieces
DimensionUnit (CMQ/CFT)           ─► grossVolumeUnityMeasure
package.weight.value              ─► totalGrossWeight
WeightUnit (KG/LBR)               ─► grossWeightUnityMeasure
declared value present?           ─► hasInsurance (bool)
declared value (money)            ─► insuranceAmmount
options.smartkargo_special_handling ─► specialHandlingType

DimensionType (one entry):
  1                               ─► pieces
  package.height/width/length     ─► height / width / length
  package.weight.value            ─► grossWeight
```

Note the wire field names `grossVolumeUnityMeasure` /
`grossWeightUnityMeasure` (vendor spelling "Unity", not "Unit"); the
**response** schema uses the corrected `grossVolumeUnitMeasure` /
`grossWeightUnitMeasure`.

### Customs — karrio `CustomsInfo` → `customItems[]` + `commercialInvoice`

Only emitted when `customs` is present and has commodities.

```
karrio commodity                  CustomItemType
─────────────────                 ──────────────────
hs_code / metadata.export_hs_code / "N/A"  ─► exportHsCode
metadata.import_hs_code / hs_code / "N/A"  ─► importHsCode
description / title               ─► description
quantity                          ─► quantity
weight_unit (default "kg")        ─► quantityUnit
weight                            ─► weight
value_amount                      ─► commercialValue
value_currency                    ─► commercialValueCurrency
origin_country                    ─► manufactureCountryCode
sku                               ─► sku

customs.incoterm (default "DDU")  ─► commercialInvoice.termsOfSale
```

### Rate response — `DetailType` → `RateDetails`

```
quotation response (status=="QUOTED")
  details[i] → DetailType
─────────────────                 RateDetails
serviceType  ─► ShippingService.map ─► service
slaInDays    ─►                        transit_days
total        ─►                        total_charge += to_money(total)
totalTax     ─►                        total_charge += to_money(totalTax)
             charges → extra_charges: "Base Rate"=total, "Tax"=totalTax
currency: config.currency or "USD"
meta: service_name, service_type, estimated_delivery (deliveryDateBasedOnShipment)
```

Only responses whose `status` (uppercased) is `QUOTED` produce rates.

### Shipment response — `ShipmentType` → `ShipmentDetails`

Validity gate `_is_valid_booking`: the envelope must have
`status == "Processed"` **and** `valid == "Yes"` **and** at least one
`shipments[].status == "Booked"`.

```
ShipmentType                      ShipmentDetails
─────────────────                 ──────────────────
prefix + airWaybill            ─► tracking_number
packageReference               ─► shipment_identifier
label base64Content            ─► docs.label  (data-URI prefix stripped)
serviceType  ─► map            ─► selected_rate.service
total                          ─► selected_rate.total_charge
currency / config.currency / USD ─► selected_rate.currency
shippingFee / insurance / totalTax ─► selected_rate.extra_charges
                                     ("Shipping Fee"/"Insurance"/"Tax")

meta:
  barCode                      ─► last_mile_tracking_number
  estimatedDeliveryDate        ─► estimated_delivery
  tracking_url.format(tn)      ─► carrier_tracking_link
  serviceType, prefix, airWaybill, headerReference,
  packageReference, origin, destination, labelUrl  (smartkargo_* keys)
```

`tracking_url` is the fixed template
`https://www.deliverdirect.com/tracking?ref={}`.

### Tracking response — `TrackingResponseElementType[]` → `TrackingDetails`

The tracking endpoint returns a **JSON array of events** (or an error
object). `_has_valid_tracking` requires a non-empty list. Events are
sorted by `eventDate` descending; the latest event's `eventType` drives
overall status (default `in_transit` when unmapped).

```
event                             TrackingEvent
─────────────────                 ──────────────────
eventDate (%Y-%m-%dT%H:%M:%S)  ─► date, time, timestamp
description                    ─► description
eventType                      ─► code, status, reason (incident)
eventLocation                  ─► location

latest event:
  estimatedDeliveryDate        ─► estimated_delivery
  pieces                       ─► info.shipment_package_count
  weight                       ─► info.package_weight (unit "KG")
  flightNumber/airWaybill/prefix/headerReference/
  packageReference/pieceReference ─► meta (smartkargo_* keys)
```

#### Tracking status mapping — `units.TrackingStatus`

| karrio status | iHub `eventType` codes |
|---|---|
| `pending` | `BKD` (electronic info submitted) |
| `picked_up` | `RCS` (picked up by carrier) |
| `in_transit` | `DEP`, `RCF`, `INF`, `MDL` (departed / recovered / info / arrived) |
| `out_for_delivery` | `GDL` (left partner store for consignee door) |
| `delivered` | `DDL`, `DLD` (delivered / delivered & left at door) |
| `delivery_failed` | `ADL` (delivery attempted, failed) |
| `on_hold` | `RCU` (reminder sent to customer) |

#### Tracking incident reasons — `units.TrackingIncidentReason`

| karrio reason | iHub code |
|---|---|
| `consignee_not_available` | `ADL` |
| `delivery_exception_hold` | `RCU` |
| `unknown` | (default) |

## Tracking request resolution

`tracking_request` picks one of three query shapes per tracking number
(see the `_AWB_PATTERN = ^([A-Za-z]{3})[-_ ]?([0-9]+)$` regex):

1. **From shipment meta** — if `smartkargo_prefix` + `smartkargo_air_waybill`
   are present in `options` (per-number or global) →
   `?prefix=<P>&Airwaybill=<AWB>`.
2. **Parsed from the number** — 3 alpha + digits (e.g. `XIA00291643`) →
   `?prefix=XIA&Airwaybill=00291643`.
3. **Fallback** — otherwise treat the whole value as a package reference
   → `?packageReference=<value>`.

Note the query param is `Airwaybill` (capital A) on `/tracking`, but
`airWaybill` (camelCase) on `/shipment/void`.

## Cancel request resolution

`shipment_cancel_request` builds one void call per tracking number:

- Tracking numbers come from `options.tracking_numbers` (populated by
  `lib.to_multi_piece_shipment`). **`payload.shipment_identifier` is the
  `packageReference`, NOT a tracking number, so it is deliberately not
  used.**
- Single-piece fallback: reconstruct `{prefix}{air_waybill}` from
  `options.prefix` + `options.air_waybill` in meta.
- A tracking number ≥ 11 chars is split as `prefix = tn[:3]`,
  `airWaybill = tn[3:]`; shorter values fall back to `options.prefix` /
  `options.air_waybill`.
- Optional `userName` (from `user_name`/`userName`) and `reason` are
  forwarded as query params; `None` values are stripped.

Success (`_is_cancelled`) is true when `result.cancelled` is truthy or
`status == "success"`. The Swagger per-call shape is
`{ result: { cancelled: bool, messages: str } }`; non-cancelled
responses surface their `result.messages` as a `Message`.

## Identifiers

```
booking shipment
  ├─ prefix + airWaybill ─► tracking_number  (customer-facing AWB, e.g. AXB01234567)
  ├─ packageReference    ─► shipment_identifier  (internal package handle)
  └─ barCode             ─► meta.last_mile_tracking_number
```

`tracking_number` = `prefix` concatenated with `airWaybill`. The void
and tracking endpoints both expect the AWB split back into its `prefix`
(first 3 chars) and AWB (remainder) parts.

## Error parsing

`error.parse_error_response` (citing manual pages 11-12 / 20-24) handles
three SmartKargo error shapes per response object (responses are
normalised to a list first):

1. **Error object** — `{"error": {"code": …, "message": …}}` → one
   `Message` (defaults `ERROR` / `"Unknown error"`).
2. **Validation errors** —
   `{"status": "Rejected", "validations": [{"property", "message",
   "packageReference"}]}` → one `Message` per validation. The
   `property` (or `code`) becomes the message `code`; `packageReference`
   is attached to `details`.
3. **Status-based** — `status` in `ERROR` / `FAILED` / `REJECTED` with a
   `details` string → an `API_ERROR` message; a fallback generic
   `ERROR` message is emitted when such a status carries no
   validations / details / error object.

Successful statuses (`PROCESSED`, `QUOTED`, `SUCCESS`, `OK`, empty) with
`valid != "NO"` are skipped — unless they still carry `validations`,
which are surfaced as warnings.

Two response-shaping helpers live in `utils.py`:

- **`parse_void_response`** — the void API may return an empty body or a
  plain-text error (e.g. `Entity "Shipment (...) not found`). Empty →
  `{"error": {"code": "EMPTY_RESPONSE", …}}`; non-JSON text →
  `{"error": {"code": "API_ERROR", "message": <text>}}`.
- **`extract_booking_data`** — the booking API returns an
  **array-wrapped** envelope (`[{…}]`); this unwraps it and pulls
  `labelUrl` only when the first shipment's `status == "Booked"`.

## References

- **OpenAPI (authoritative)** — `vendor/openapi.yaml` ("IHUB Swagger"
  v1.0.0; UAT/staging servers under `uatihub.smartkargo.com`). HTML
  render at `vendor/openapi.html`.
- **Integration manual** — `vendor/SmartKargo_API_Integration_Manual_V1.1.pdf`
  (error formats: pages 11-12, 20-24).
- **Captured samples** — `vendor/Insomnia_2026-03-01.har`.
- **Vendor site** — <https://www.smartkargo.com>.
- **Tracking portal** — `https://www.deliverdirect.com/tracking?ref={}`.

Generated schemas under `karrio/schemas/smartkargo/*.py` are generated
from `schemas/*.json` via the `generate` script
(`kcli codegen generate … --no-nice-property-names`, because the iHub
API is camelCase). Regenerate with
`./bin/run-generate-on modules/connectors/smartkargo` — never hand-edit.
