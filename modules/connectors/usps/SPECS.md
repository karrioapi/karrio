# USPS integration — specification

Reference for the **USPS** connector. It targets the modern USPS
**APIs platform** (`apis.usps.com`) — the OAuth2 JSON REST suite that
replaced the legacy USPS Web Tools XML API — and covers **domestic US**
shipping only (origin and destination must be `US`). Cross-border
shipping lives in the separate `usps_international` connector; see
[Relationship to `usps_international`](#relationship-to-usps_international).

Wired operations: rate, label create, label cancel, return label,
tracking, carrier pickup (schedule / modify / cancel), and SCAN Form
manifest. The connector id / display label is `usps` / `USPS`
(`pyproject.toml`, `karrio/plugins/usps/__init__.py`).

The **vendor source of truth** is the set of OpenAPI YAML specs under
`karrio/providers/usps/vendor/*.yaml` (addresses, carrier-pickup,
domestic-labels, domestic-prices, international-labels, tracking). The
generated Python types under `karrio/schemas/usps/*.py` are built from
the trimmed JSON samples in `schemas/*.json`.

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Data flow](#data-flow)
3. [Endpoints](#endpoints)
4. [Authentication (two-token OAuth)](#authentication-two-token-oauth)
5. [Supported operations](#supported-operations)
6. [Services](#services)
7. [Options & extra services](#options--extra-services)
8. [Data mapping](#data-mapping)
9. [Carrier-specific invariants / gotchas](#carrier-specific-invariants--gotchas)
10. [Tracking](#tracking)
11. [Error parsing](#error-parsing)
12. [Relationship to `usps_international`](#relationship-to-usps_international)
13. [References](#references)

---

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio RateRequest / ShipmentRequest /
│   (karrio core)         │   TrackingRequest / PickupRequest / ManifestRequest
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  providers/usps         │   Pure data transforms.
│   rate.py               │   Unified model → typed USPS request,
│   shipment/create.py    │   typed USPS response → unified model.
│   shipment/cancel.py    │   No HTTP, no side effects.
│   shipment/return_…py   │
│   tracking.py           │
│   pickup/{create,update,│
│           cancel}.py    │
│   manifest.py           │
│   error.py              │
│   units.py              │   PackagingType, ShippingService,
│   utils.py              │   ShippingOption, TrackingStatus,
│                         │   TrackingIncidentReason, multipart parse
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  mappers/usps/proxy.py  │   HTTP transport only.
│   - authenticate        │   - OAuth2 access-token caching
│   - get_payment_token   │   - payment-authorization-token caching
│   - get_rates           │   - Bearer + X-Payment-Authorization-Token
│   - create_shipment     │   - async fan-out per package
│   - cancel_shipment     │   - multipart label-response decode
│   - get_tracking        │
│   - schedule/modify/    │
│     cancel_pickup       │
│   - create_manifest     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  USPS APIs (apis.usps.com)
│  ─────────────────────  │
│  OAuth2 v3              │   client_credentials token
│  Payments v3            │   payment-authorization token
│  Prices/Shipments v3    │   /shipments/v3/options/search (rates)
│  Labels v3              │   create / cancel / return label
│  Tracking v3            │   tracking by number
│  Pickup v3              │   carrier-pickup CRUD
│  Scan-forms v3          │   SCAN Form (manifest)
└─────────────────────────┘
```

**Key architectural choices:**

- **Per-package fan-out.** `get_rates` and `create_shipment` build one
  request object per parcel and dispatch them with
  `lib.run_asynchronously`. The parsers re-aggregate N responses into a
  single unified result via `lib.to_multi_piece_rates` /
  `lib.to_multi_piece_shipment`.
- **Two OAuth tokens.** Every billed write (label create/cancel)
  carries both a normal `Bearer` access token **and** a separate
  `X-Payment-Authorization-Token`. Both are cached independently per
  connection (see [Authentication](#authentication-two-token-oauth)).
- **Static service catalog.** There is no dynamic per-account product
  fetch. `ShippingService` in `units.py` is the static enum;
  `DEFAULT_SERVICES` is built at import time from
  `providers/usps/services.csv` (per-zone weight/dimension envelopes).
- **Generated schemas** — `karrio/schemas/usps/*.py` is generated from
  `schemas/*.json` via the `generate` script. Don't hand-edit;
  regenerate with `./bin/run-generate-on modules/connectors/usps`.

## Data flow

### Rate (`/shipments/v3/options/search`)

```
RateRequest                                  USPS Prices
     │                                            │
     ├─► rate_request                             │
     │     guard: shipper US / recipient US       │
     │     to_packages() → one request/parcel     │
     │     map service → mailClass                │
     │     resolve priceType (RETAIL default)     │
     │     extraServices ← option codes           │
     │                                            │
     ├─► [RateRequestType, …]  (one per package)  │
     │                                            │
     │   ─── POST /shipments/v3/options/search ──►│  (async, per request)
     │   ◄── pricingOptions[].shippingOptions[]   │
     │         .rateOptions[].rates[] ────────────│
     │                                            │
     ├─► _extract_details per rate:               │
     │     productName → service_code             │
     │     totalPrice → total_charge              │
     │     commitment.name → transit_days         │
     │     machinable filter (see gotchas)        │
     ▼                                            ▼
list[RateDetails]  (multi-piece aggregated)
```

### Shipment create (`/labels/v3/label`)

```
ShipmentRequest                              USPS Labels
     │                                            │
     ├─► authenticate()  → access_token           │
     ├─► get_payment_token() → payment_token       │
     │                                            │
     ├─► shipment_request                         │
     │     guard: shipper US / recipient US       │
     │     to/from/sender/return AddressType      │
     │     mailClass ← service                    │
     │     packageDescription + extraServices     │
     │                                            │
     │   ─── POST /labels/v3/label ──────────────►│  (async, per package)
     │        Authorization: Bearer <token>       │
     │        X-Payment-Authorization-Token: …    │
     │   ◄── multipart (labelMetadata + image) ───│
     │                                            │
     ├─► parse_response (JSON or multipart decode)│
     ├─► _extract_details:                        │
     │     labelMetadata.trackingNumber           │
     │       → tracking_number + shipment_id      │
     │     labelImage → docs.label                │
     │     receiptImage → docs.invoice            │
     │     returnLabelImage → extra_documents     │
     ▼                                            ▼
ShipmentDetails (multi-piece aggregated)
```

### Tracking (`/tracking/v3/tracking/{n}`)

```
TrackingRequest                              USPS Tracking
     │                                            │
     ├─► tracking_request → [tracking_numbers]    │
     │                                            │
     │   ─── GET /tracking/v3/tracking/{n}?expand=DETAIL ─► (async, per number)
     │   ◄── (number, TrackingResponseType) ──────│
     │                                            │
     ├─► _extract_details per number:             │
     │     status / statusCategory → TrackingStatus
     │     trackingEvents[] → events[]            │
     │     eventCode → TrackingIncidentReason     │
     ▼                                            ▼
list[TrackingDetails]
```

## Endpoints

Test mode (`test_mode=True`): `https://api-cat.usps.com`.
Prod: `https://apis.usps.com`. Selected by `Settings.server_url`.

| Purpose | Method | Path |
|---|---|---|
| OAuth access token | POST | `/oauth2/v3/token` |
| Payment-authorization token | POST | `/payments/v3/payment-authorization` |
| Rate (options search) | POST | `/shipments/v3/options/search` |
| Create label | POST | `/labels/v3/label` |
| Return label | POST | `/labels/v3/label` (same endpoint, `returnLabel=true`) |
| Cancel label | DELETE | `/labels/v3/label/{trackingNumber}` |
| Tracking | GET | `/tracking/v3/tracking/{trackingNumber}?expand=DETAIL` |
| Schedule pickup | POST | `/pickup/v3/carrier-pickup` |
| Modify pickup | PUT | `/pickup/v3/carrier-pickup/{confirmationNumber}` |
| Cancel pickup | DELETE | `/pickup/v3/carrier-pickup/{confirmationNumber}` |
| SCAN Form (manifest) | POST | `/scan-forms/v3/scan-form` |

The customer-facing tracking link is
`https://tools.usps.com/go/TrackConfirmAction?tLabels={}` (`Settings.tracking_url`).

## Authentication (two-token OAuth)

USPS uses OAuth2 `client_credentials`, but billed label operations need
a **second** token on top of the access token.

### 1. Access token — `POST /oauth2/v3/token`

`grant_type=client_credentials` posted as
`application/x-www-form-urlencoded` with `client_id`, `client_secret`,
and an explicit `scope` listing all 14 product scopes
(`addresses international-prices subscriptions payments pickup tracking
labels scan-forms companies service-delivery-standards locations
international-labels prices shipments`).

Cached per `access|usps|<client_id>|<client_secret>` via
`connection_cache.thread_safe(buffer_minutes=30)`. Expiry is computed
locally from the `expires_in` response field and stamped as `expiry`;
the cache treats the token as expired 30 min early.

### 2. Payment-authorization token — `POST /payments/v3/payment-authorization`

Obtained with a valid access token in the `Authorization` header. The
body declares two roles built from connection settings:

```
roles:
  - roleName: LABEL_OWNER   CRID, MID, accountType (EPS default),
                            accountNumber, manifestMID
  - roleName: PAYER         CRID, MID, accountType, accountNumber
```

Cached per `payment|usps|<client_id>|<client_secret>` with
`buffer_minutes=45`, `token_field="paymentAuthorizationToken"`. Expiry
is stamped 50 minutes out locally (the API does not return an expiry for
this token). It is sent as the `X-Payment-Authorization-Token` header on
`create_shipment` / `cancel_shipment`.

```
client_credentials                          ┌──────────────────┐
       │                                     │  Connection cache │
       ▼                                     │  (per conn)       │
┌──────────────┐  POST /oauth2/v3/token      │  access|usps|…    │
│ access_token │◄────────────────────────────│  payment|usps|…   │
└──────┬───────┘                             └──────────────────┘
       │ Bearer
       ▼  POST /payments/v3/payment-authorization
┌──────────────────────────┐
│ paymentAuthorizationToken │──► X-Payment-Authorization-Token
└──────────────────────────┘     (label create / cancel only)
```

Connection settings (`mappers/usps/settings.py`):

| Field | Default | Notes |
|---|---|---|
| `client_id` | — | OAuth client id (required) |
| `client_secret` | — | OAuth client secret (required) |
| `account_number` | `None` | EPS / permit / meter account |
| `account_type` | `"EPS"` | one of `EPS`, `PERMIT`, `METER` (`AccountType` enum) |
| `manifest_MID` | `None` | manifest Mailer ID (LABEL_OWNER role) |
| `CRID` | `None` | Customer Registration ID |
| `MID` | `None` | Mailer ID |
| `account_country_code` | `"US"` | fixed |

Connection config (`ConnectionConfig` in `settings.py`, set via `config`):
`permit_ZIP`, `permit_number`, `shipping_options` (list),
`shipping_services` (list). Rate flow also reads `price_type` off
`connection_config` as a fallback.

## Supported operations

| Operation | Mapper method | Provider | Endpoint |
|---|---|---|---|
| Rate | `create_rate_request` / `parse_rate_response` | `rate.py` | `/shipments/v3/options/search` |
| Ship | `create_shipment_request` / `parse_shipment_response` | `shipment/create.py` | `/labels/v3/label` |
| Return | `create_return_shipment_request` / `parse_return_shipment_response` | `shipment/return_shipment.py` | `/labels/v3/label` |
| Cancel | `create_cancel_shipment_request` / `parse_cancel_shipment_response` | `shipment/cancel.py` | `DELETE /labels/v3/label/{n}` |
| Track | `create_tracking_request` / `parse_tracking_response` | `tracking.py` | `/tracking/v3/tracking/{n}` |
| Schedule pickup | `create_pickup_request` / `parse_pickup_response` | `pickup/create.py` | `/pickup/v3/carrier-pickup` |
| Update pickup | `create_pickup_update_request` / `parse_pickup_update_response` | `pickup/update.py` | `PUT /pickup/v3/carrier-pickup/{c}` |
| Cancel pickup | `create_cancel_pickup_request` / `parse_cancel_pickup_response` | `pickup/cancel.py` | `DELETE /pickup/v3/carrier-pickup/{c}` |
| Manifest (SCAN Form) | `create_manifest_request` / `parse_manifest_response` | `manifest.py` | `/scan-forms/v3/scan-form` |

No rate-sheet upload, no document-upload/paperless flow (domestic only).

## Services

USPS encodes the product as a **mailClass** string. `ShippingService`
(`units.py`):

| Karrio service | Wire `mailClass` |
|---|---|
| `usps_parcel_select_lightweight` | `PARCEL_SELECT_LIGHTWEIGHT` |
| `usps_parcel_select` | `PARCEL_SELECT` |
| `usps_priority_mail_express` | `PRIORITY_MAIL_EXPRESS` |
| `usps_priority_mail` | `PRIORITY_MAIL` |
| `usps_library_mail` | `LIBRARY_MAIL` |
| `usps_media_mail` | `MEDIA_MAIL` |
| `usps_bound_printed_matter` | `BOUND_PRINTED_MATTER` |
| `usps_connect_local` | `USPS_CONNECT_LOCAL` |
| `usps_connect_mail` | `USPS_CONNECT_MAIL` |
| `usps_connect_next_day` | `USPS_CONNECT_NEXT_DAY` |
| `usps_connect_regional` | `USPS_CONNECT_REGIONAL` |
| `usps_connect_same_day` | `USPS_CONNECT_SAME_DAY` |
| `usps_ground_advantage` | `USPS_GROUND_ADVANTAGE` |
| `usps_domestic_matter_for_the_blind` | `DOMESTIC_MATTER_FOR_THE_BLIND` |
| `usps_all` | `ALL` |

**mailClass resolution helpers** (`ShippingService`):

- `to_mail_class(product_code)` — collapses a *priced product* code
  (e.g. `usps_priority_mail_padded_flat_rate_envelope`) back to the
  enclosing mail class by name-substring match (`PRIORITY_MAIL`). USPS
  rate/label requests want the broad mail class, not the SKU-level
  product.
- `to_product_code(product_name)` — slugs a returned `productName` into
  a `usps_*` code (dedupes the doubled `usps_usps_` prefix).
- `to_product_name(product_code)` — inverse, for display.

When no service is supplied the rate flow falls back to mail class
`ALL` (USPS returns every eligible product).

**`INCOMPATIBLE_SERVICES`** = `[usps_ground_advantage]`. For this mail
class the package's per-package options are dropped (no `extraServices`
attached) because Ground Advantage rejects the extra-service set — see
`package_options()` in both `rate.py` and `shipment/create.py`.

**Packaging** (`PackagingType`) maps the unified packaging presets onto
USPS rate-indicator codes (`envelope`/`pak`/`small_box`/`your_packaging`
→ `SP` single-piece; `tube` → `SN`; `medium_box` → `SR`; `pallet` →
`PL`), alongside the full native code list (cubic tiers, tray boxes,
flat-rate boxes, etc.).

**Service-level envelopes** (`DEFAULT_SERVICES`) are loaded from
`services.csv` at import. Each CSV row contributes a `ServiceZone`
(weight band, dimension caps, country codes, transit days) grouped under
its mail class; units are `LB` / `IN`.

## Options & extra services

`ShippingOption` (`units.py`) splits into two groups:

**1. Numeric extra-service codes** — the `OptionEnum` wire code is the
USPS numeric extra-service id. These are emitted into
`packageDescription.extraServices` as integers. Examples:

| Karrio option | Code | Category |
|---|---|---|
| `usps_label_delivery_service` | `415` | — |
| `usps_tracking_plus_6_months` … `_10_years` | `480`–`485` | — |
| `usps_tracking_plus_signature_*` | `486`–`489` | SIGNATURE |
| `usps_hazardous_materials_*` (air ethanol → small-quantity) | `810`–`832` | DANGEROUS_GOOD |
| `usps_hazardous_materials` | `857` | DANGEROUS_GOOD |
| `usps_certified_mail*` | `910`–`913` | SIGNATURE |
| `usps_collect_on_delivery` | `915` (float) | COD |
| `usps_collect_on_delivery_restricted_delivery` | `917` | COD |
| `usps_tracking_electronic` | `920` | — |
| `usps_signature_confirmation` | `921` | SIGNATURE |
| `usps_adult_signature_required` / `_restricted_delivery` | `922` / `923` | SIGNATURE |
| `usps_signature_confirmation_restricted_delivery` | `924` | SIGNATURE |
| `usps_priority_mail_express_merchandise_insurance` | `925` | INSURANCE |
| `usps_insurance_below_500` / `usps_insurance_above_500` | `930` / `931` (float) | INSURANCE |
| `usps_insurance_restricted_delivery` | `934` | INSURANCE |
| `usps_registered_mail` / `_restricted_delivery` | `940` / `941` | SIGNATURE |
| `usps_return_receipt` / `_electronic` | `955` / `957` | RETURN |
| `usps_signature_requested_priority_mail_express_only` | `981` | SIGNATURE |
| `usps_parcel_locker_delivery` | `984` | LOCKER |
| `usps_po_to_addressee_priority_mail_express_only` | `986` | DELIVERY_OPTIONS |
| `usps_sunday_delivery` | `981` | DELIVERY_OPTIONS |

> Note: `usps_signature_requested_priority_mail_express_only` and
> `usps_sunday_delivery` both carry wire code `981` in the enum as
> written.

**2. Custom (non-extra-service) options** — listed in `CUSTOM_OPTIONS`;
these are *excluded* from the `extraServices` integer list and instead
map onto dedicated request fields (`mailClass`, `facilityId`,
`machinable`, `holdForPickup`, `processingCategory`, `carrierRelease`,
`physicalSignatureRequired`, `priceType`, `destinationEntryFacilityType`,
`extraServices` passthrough, `shippingFilter`, `return_receipt*`):

| Karrio option | Wire field | Type / enum |
|---|---|---|
| `usps_mail_class` | `mailClass` | `ShippingService` |
| `usps_facility_id` | `facilityId` | str |
| `usps_machinable_piece` | `machinable` | bool |
| `usps_hold_for_pickup` | `holdForPickup` | bool (PUDO) |
| `usps_processing_category` | `processingCategory` | str |
| `usps_carrier_release` | `carrierRelease` | bool |
| `usps_physical_signature_required` | `physicalSignatureRequired` | bool |
| `usps_price_type` | `priceType` | `RETAIL` / `COMMERCIAL` / `CONTRACT` |
| `usps_destination_entry_facility_type` | `destinationEntryFacilityType` | `NONE` / `DESTINATION_NETWORK_DISTRIBUTION_CENTER` / `DESTINATION_SECTIONAL_CENTER_FACILITY` / `DESTINATION_DELIVERY_UNIT` / `DESTINATION_SERVICE_HUB` |
| `usps_extra_services` | `extraServices` | explicit int list (overrides derived) |
| `usps_shipping_filter` | `shippingFilter` | `PRICE` / `SERVICE_STANDARDS` |

**Unified-option aliases:** `cash_on_delivery` → `usps_collect_on_delivery`,
`signature_confirmation` → `usps_signature_confirmation`,
`sunday_delivery` → `usps_sunday_delivery`,
`hold_at_location` → `usps_hold_for_pickup`.

**Insurance auto-split** (`shipping_options_initializer`): a unified
`insurance` value is rewritten to `usps_insurance_above_500` when
`> 500`, else `usps_insurance_below_500` — USPS prices insurance with
two distinct extra-service codes split at the \$500 boundary.

## Data mapping

### Address — karrio `Address` → USPS `AddressType`

```
karrio Address                          USPS AddressType
─────────────────                       ────────────────
address_line1          ───►             streetAddress
address_line2          ───►             secondaryAddress
city                   ───►             city
state_code             ───►             state
postal_code            ───►             ZIPCode  (lib.to_zip5)
                                        ZIPPlus4 (lib.to_zip4)
first_name             ───►             firstName
last_name              ───►             lastName
company_name           ───►             firm
phone_number           ───►             phone (parse_phone_number: digits-only, last 10)
email                  ───►             email
(always)               ───►             ignoreBadAddress = True
```

A label request carries four address slots: `toAddress` (recipient),
`fromAddress` and `senderAddress` (both the shipper), and an optional
`returnAddress` (only when `payload.return_address` is set).

### Package — `Package` → `PackageDescriptionType` (label)

| karrio | wire field | notes |
|---|---|---|
| `weight.LB` | `weight` (`weightUOM="lb"`) | |
| `length/height/width.IN` | `length/height/width` (`dimensionsUOM="in"`) | |
| `girth.value` | `girth` | rate flow only sends girth for `tube` packaging |
| service | `mailClass` | via `to_mail_class` |
| `usps_rate_indicator` | `rateIndicator` | default `DR` |
| `usps_processing_category` | `processingCategory` | default `NON_MACHINABLE` |
| `usps_destination_facility_type` | `destinationEntryFacilityType` | default `NONE` |
| total/declared value | `packageOptions.packageValue` | default `1.0` when value present |
| `payload.reference` | `customerReference[].referenceNumber` | `printReferenceNumber=True` |
| derived option codes | `extraServices` | int list, minus `CUSTOM_OPTIONS` |
| `shipment_date` | `mailingDate` | defaults to today |
| `usps_carrier_release` | `carrierRelease` | |
| `usps_physical_signature_required` | `physicalSignatureRequired` | |
| return/shipper postal | `inductionZIPCode` | return postal preferred |

`imageInfo`: `imageType` from `label_type` (default `PDF`),
`labelType="4X6LABEL"`, `receiptOption="NONE"`, and `returnLabel=True`
when `usps_return_receipt` is set.

### Label type — `LabelType`

`PDF`, `TIFF`, `JPG`, `SVG`, `ZPL203DPI`, `ZPL300DPI`, `LABEL_BROKER`,
`NONE`. Unified aliases: `ZPL` → `ZPL203DPI`, `PNG` → `JPG`. Default
`PDF`.

### Rate response — `RateOptionType` → `RateDetails`

```
USPS rate                                 RateDetails
─────────                                 ───────────
rate.productName/description/mailClass ─► service (via to_product_code)
rateOption.totalPrice                  ─► total_charge   (currency "USD")
rateOption.totalBasePrice              ─► extra_charges["Base Price"]
rateOption.extraServices[].price       ─► extra_charges[name]
rateOption.commitment.name (1st token) ─► transit_days   (failsafe int)
rateOption.commitment.scheduleDeliveryDate ─► estimated_delivery
rate.mailClass/zone/SKU/priceType/…    ─► meta.usps_*
```

## Carrier-specific invariants / gotchas

- **Domestic only.** `rate_request` and `shipment_request` raise
  `OriginNotServicedError` / `DestinationNotServicedError` when either
  endpoint country is set and not `US`. International is the separate
  `usps_international` connector.
- **Multipart label responses.** `/labels/v3/label` can return a
  `multipart/form-data` body (JSON metadata part + binary label part)
  rather than JSON. `provider_utils.parse_response` first tries a plain
  JSON parse, then falls back to `normalize_multipart_response` +
  boundary splitting to reconstruct a dict keyed by each part `name`
  (the JSON parts are parsed; the binary parts are kept as strings). The
  cancel/tracking proxies, by contrast, always decode plain JSON.
- **Two tokens required for billed writes.** A label create/cancel
  fails without both the `Bearer` access token and the
  `X-Payment-Authorization-Token`. The payment token requires the
  account roles (CRID/MID/accountNumber) to be configured on the
  connection.
- **`machinable` rate filtering.** The rate request stashes
  `machinable_piece` in `request.ctx`. `_extract_details` then *drops*
  any returned rate whose machinability does not match: a machinable
  request discards `*machinable*`-named products that are
  non-machinable, and vice-versa. This is a client-side filter — the
  USPS options-search returns both.
- **Transit days are parsed from free text.** USPS has no dedicated
  transit-days field. The connector takes `commitment.name`
  (e.g. `"2 Days"`, `"NO STD"`), splits on space, and `to_int`s the
  first token under `lib.failsafe` — non-numeric commitments
  (`"NO STD"`) yield `None` rather than crashing (inline comment in
  `rate.py`).
- **`extraServices` is an int list of option codes.** Codes come from
  iterating the package options and reading `.code`, excluding anything
  in `CUSTOM_OPTIONS`. An explicit `usps_extra_services` list overrides
  the derived set entirely (label flow).
- **Ground Advantage drops options.** See `INCOMPATIBLE_SERVICES` above
  — options are zeroed for `usps_ground_advantage`.
- **`packageValue` defaults to `1.0`.** When no total/declared value is
  present the connector still sends `packageOptions.packageValue=1.0`
  on label create.
- **ZIP splitting.** `ZIPCode` is the 5-digit ZIP (`lib.to_zip5`) and
  `ZIPPlus4` the 4-digit add-on (`lib.to_zip4`); both default to `""`.
- **Cancel "success" is all-or-nothing.** `parse_shipment_cancel_response`
  reports success only when **every** tracking number in the batch
  returned `status == "CANCELED"`. The cancel request set is the union
  of `shipment_identifier` and `options.shipment_identifiers`,
  de-duplicated.
- **Pickup: one-time only.** USPS carrier-pickup API supports only
  `one_time` pickups. A non-`one_time` `pickup_type` raises a
  `FieldError` pointing the user at USPS for recurring schedules
  (`pickup/create.py`). `pickupLocation` is only sent when a package
  location or special instruction is present. The update flow nests the
  request under `carrierPickupRequest` and threads the
  `confirmationNumber` through `request.ctx`.
- **Pickup cancel uses a synthetic body.** The DELETE has no JSON
  response; the proxy injects `on_ok=lambda _: '{"ok": true}'` and the
  parser keys success off `response["ok"] is True`.
- **Return shipments reuse label create.** `return_shipment_request`
  just forces `usps_return_receipt=True` and delegates to
  `shipment.create.shipment_request` against the same `/labels/v3/label`
  endpoint. The parser is `parse_shipment_response`.
- **Manifest = SCAN Form 5630.** `manifest_request` posts a fixed
  `form="5630"`, `imageType="PDF"`, `labelType="8.5x11LABEL"` with the
  shipment tracking numbers; the response carries `SCANFormImage`
  (returned as `ManifestDocument.manifest`) plus `manifestNumber` and
  `trackingNumbers` in meta. The `firstName`/`lastName` are split off
  `person_name` by whitespace.

## Tracking

`GET /tracking/v3/tracking/{n}?expand=DETAIL`, one async call per
tracking number; each yields a `(number, response)` tuple.

**Status mapping** (`TrackingStatus`) matches case-insensitively against
both `status` and `statusCategory` from the response. Default when no
match is `in_transit`.

| Karrio status | Matched text |
|---|---|
| `on_hold` | `on hold` |
| `delivered` | `delivered` |
| `in_transit` | `in transit` |
| `delivery_failed` | `delivery failed` |
| `delivery_delayed` | `delivery delayed` |
| `out_for_delivery` | `out for delivery` |
| `ready_for_pickup` | `ready for pickup` |
| `picked_up` | `PICKED_UP`, `PU`, `picked up`, `origin scan`, `acceptance` |

**Per-event status** is re-derived from each `eventType`; the per-event
**reason** is derived from `eventCode` via `TrackingIncidentReason`
(maps USPS exception codes — e.g. `DAMAGED`/`DMG`, `REFUSED`/`RF`,
`CUSTOMS_DELAY`/`CD`, `WEATHER`/`WE` — onto normalized incident reasons,
defaulting to `unknown`).

Event timestamps are parsed with `try_formats`
`["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S"]`. `TrackingInfo` carries
mail class (mapped back through `ShippingService`), origin/destination
ZIP + country, and the `tools.usps.com` carrier link.

## Error parsing

`error.parse_error_response` (`error.py`) normalizes three USPS error
shapes into `list[models.Message]`:

```
response                              ┌────────────────────────────┐
   │                                  │ error.parse_error_response  │
   ├─ {"error": {code, message}} ───► │  single error object        │
   │   (no nested "errors")           │                             │
   ├─ {"error": "<string>"} ────────► │  string error (OAuth-style) │
   │                                  │   reads error_description    │
   ├─ {"error": {"errors":[…]}} ────► │  fan out nested errors[]     │
   │                                  └──────────────┬─────────────┘
   ▼                                                 ▼
code  ← error.code or error.error            list[Message]
message ← error.message / error.detail / error.error_description
details ← {source, error_uri, **kwargs}
```

Two complementary helpers in `utils.py` produce the raw dict the parser
consumes:

- `parse_response` — success/multipart decoder (see gotchas); on an
  un-parseable multipart body it returns
  `{"error": {"code": "SHIPPING_SDK_ERROR", "message": "Failed to parse multipart response"}}`.
- `parse_error_response` — used as the `on_error` hook for label create;
  reads the HTTP body, tries JSON, and otherwise wraps plain text as
  `{"error": {"code": <http code>, "message": <text>}}`.

`**kwargs` passed to `error.parse_error_response` (e.g.
`tracking_number=...` on cancel/tracking) are folded into the message
`details`.

## Relationship to `usps_international`

`usps` and `usps_international` are **two separate connectors / plugins**
sharing the same OAuth client and APIs platform, split by lane:

| | `usps` (this) | `usps_international` |
|---|---|---|
| carrier_id | `usps` | `usps_international` |
| Lane | US → US (origin & dest must be `US`) | US → non-US |
| Label endpoint | `/labels/v3/label` | international-labels surface |
| Service catalog | domestic mail classes | international products |
| Settings shape | identical fields (`client_id`, `client_secret`, `account_number`, `account_type`, `CRID`, `MID`, `manifest_MID`) | identical |

They are intentionally **not** merged: this connector hard-rejects
non-US origin/destination, so international shipments must be routed
through `usps_international`. The OAuth scope list requested here
includes `international-*` scopes, but the domestic providers never call
the international endpoints.

## References

- **Vendor OpenAPI specs (source of truth)** —
  `karrio/providers/usps/vendor/`:
  - `usps-domestic-prices.yaml` — `/shipments/v3/options/search`
  - `usps-domestic-labels.yaml` — `/labels/v3/label`
  - `usps-tracking.yaml` — `/tracking/v3/tracking`
  - `usps-carrier-pickup.yaml` — `/pickup/v3/carrier-pickup`
  - `usps-addresses.yaml`, `usps-international-labels.yaml`
  - `vendor/domestic-prices.yaml` (connector-root copy)
- **Service-level envelopes** — `karrio/providers/usps/services.csv`
  (per-mailClass / per-zone weight + dimension bands; loaded into
  `DEFAULT_SERVICES`).
- **USPS developer portal** —
  <https://www.usps.com/business/web-tools-apis> (connector `documentation`).
- **Generated schemas** — `karrio/schemas/usps/*.py` is generated from
  `schemas/*.json` via the `generate` script (kcli, `--no-nice-property-names`).
  Regenerate with `./bin/run-generate-on modules/connectors/usps`; never
  hand-edit the generated `*.py`. To add a new typed module, add a
  representative `schemas/<thing>.json` and a `generate_schema` line to
  `generate`.
