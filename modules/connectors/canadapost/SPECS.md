# Canada Post integration — specification

Reference for the Canada Post connector. Canada Post is a **direct
carrier** exposing an **XML-over-HTTP REST** API (the "soa-gw"
gateway). Each operation is a distinct versioned media type
(`application/vnd.cpc.*+xml`) rather than a single JSON contract. The
connector supports rating, shipment create/cancel, authorized returns,
tracking, pickup (schedule/update/cancel), and commercial manifest
(transmit-set) operations.

The **vendor source of truth** is the set of XSD schemas under
`schemas/*.xsd`. The typed Python modules in
`karrio/schemas/canadapost/*.py` are generated from those XSDs by
`generateDS` (see the `generate` script) — never hand-edit them.

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
10. [Submit vs. group (manifest) lifecycle](#submit-vs-group-manifest-lifecycle)
11. [Tracking status mapping](#tracking-status-mapping)
12. [Error parsing](#error-parsing)
13. [References](#references)

---

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio RateRequest / ShipmentRequest /
│   (karrio core)         │   ShipmentCancelRequest / TrackingRequest /
│                         │   PickupRequest / ManifestRequest
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  providers/canadapost   │   Pure data transforms.
│   rate.py               │   Unified model → typed CP request (XSD types),
│   shipment/create.py    │   typed CP response → unified model.
│   shipment/cancel.py    │   No HTTP, no side effects.
│   shipment/return_…py   │
│   tracking.py           │
│   pickup/{create,        │   ShippingService, ShippingOption,
│     update,cancel}.py   │   TrackingStatus, TrackingIncidentReason,
│   manifest.py           │   PaymentType, LabelType, PackagePresets,
│   units.py              │   ConnectionConfig
│   error.py / utils.py   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  mappers/canadapost/    │   HTTP transport only.
│   proxy.py              │   - HTTP Basic auth (base64 user:pass)
│   - get_rates           │   - per-op vnd.cpc.*+xml media types
│   - create_shipment     │   - parallel fan-out (lib.run_asynchronously)
│   - create_return_…     │   - second GET to fetch the label artifact
│   - cancel_shipment     │   - Pipeline orchestration for pickups
│   - get_tracking        │   - manifest group-id discovery + artifact pull
│   - schedule_pickup     │
│   - modify_pickup       │
│   - cancel_pickup       │
│   - create_manifest     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Canada Post SOA gateway │
│  ───────────────────────│
│  ship/price   (rate-v4)  │   rating
│  shipment     (v8)       │   create / get / refund / delete / details
│  authorizedreturn (v2)   │   authorized return label
│  vis/track    (track-v2) │   detailed tracking by PIN
│  pickup / pickuprequest  │   availability + on-demand/scheduled pickup
│  manifest     (v8)       │   transmit-set + manifest artifacts
└─────────────────────────┘
```

**Key architectural choices:**

- **XML on the wire, typed both ways.** Requests are built as
  `generateDS`-typed objects and serialized with `lib.to_xml(...)`
  carrying the operation namespace; responses are parsed with
  `lib.to_element` / `lib.to_object`.
- **Per-parcel fan-out.** Rate and shipment requests emit one XML
  request per parcel and run them in parallel via
  `lib.run_asynchronously`; the parsers aggregate N responses into one
  result via `lib.to_multi_piece_rates` / `lib.to_multi_piece_shipment`.
- **Two-step label retrieval.** The shipment/return POST returns links
  only; the proxy issues a second authenticated `GET` against the
  `rel="label"` link (`href` + `media-type`) and base64-encodes the
  binary label (`decoder=lib.encode_base64`).
- **Submit-vs-group lifecycle.** A shipment is either transmitted
  immediately (`<transmit-shipment/>`) or filed under a daily
  `<group-id>` that must later be transmitted via a manifest. This is
  the connector's central state machine — see
  [the dedicated section](#submit-vs-group-manifest-lifecycle).
- **Static service catalog.** Canada Post has no per-account service
  discovery; services are the fixed `ServiceType` enum. `DEFAULT_SERVICES`
  (service-level + zone metadata) is loaded from a checked-in
  `services.csv`.
- **Generated schemas.** `karrio/schemas/canadapost/*.py` is generated
  from `schemas/*.xsd`. Regenerate with
  `./bin/run-generate-on modules/connectors/canadapost` (or the local
  `generate` script) — never hand-edit.

## Data flow

### Shipment create (per parcel: 1 POST + 1 label GET)

```
ShipmentRequest                                  Canada Post (shipment-v8)
     │                                                    │
     ├─► shipment_request (per parcel)                    │
     │     to_address(shipper/recipient)                  │
     │     map service → DeliverySpec.service-code        │
     │     options → optionsType / customs → CustomsType  │
     │     decide submit_shipment (transmit vs group)     │
     │     → ShipmentType (typed), name_="shipment"       │
     │                                                    │
     │   ─── POST /rs/{cn}/{cn}/shipment ────────────────►│
     │        (transmit-shipment | group-id swapped into  │
     │         the <groupIdOrTransmitShipment/> slot)      │
     │                                                    │
     │   ◄── ShipmentInfo{ shipment-id, tracking-pin,     │
     │         links[rel=label], shipment-price } ────────│
     │                                                    │
     ├─► proxy: GET <label href> (Accept = media-type)    │
     │        base64-encode binary label                  │
     │                                                    │
     ├─► _extract_shipment:                               │
     │     tracking-pin → tracking_number                 │
     │     shipment-id  → shipment_identifier             │
     │     label        → docs.label                      │
     │     shipment-price → selected_rate (CAD)           │
     │     meta.group_id / manifest_required              │
     ▼                                                    ▼
ShipmentDetails (multi-piece aggregated)
```

### Shipment cancel (GET status → conditional refund or DELETE)

```
ShipmentCancelRequest                            Canada Post (shipment-v8)
     │                                                    │
     ├─► request = {shipment_identifier} ∪ options.shipment_identifiers
     │                                                    │
     │   ─── GET  /rs/{cn}/{cn}/shipment/{id} ───────────►│  (read status)
     │   ◄── ShipmentInfo{ shipment-status } ─────────────│
     │                                                    │
     │   transmitted?                                     │
     │     yes → POST /shipment/{id}/refund  (with email) │
     │     no  → DELETE /shipment/{id}                    │
     │                                                    │
     ▼                                                    ▼
ConfirmationDetails(success = any leg returned no <message>)
```

`utils.parse_submitted_shipment` decides the branch: if
`shipment-status == "transmitted"` it builds a
`shipment-refund-request` body (carrying the contact `email` from
cancel `options`); otherwise the shipment is still cancellable by
`DELETE`. The proxy detects "already refunded vs needs delete" from the
response tag (`shipment-refund-request-info`).

### Tracking (per PIN, parallel, throttled)

```
TrackingRequest                                  Canada Post (track-v2)
     │                                                    │
     ├─► tracking_request → payload.tracking_numbers      │
     │                                                    │
     │   ─── GET /vis/track/pin/{pin}/detail ────────────►│  (one per PIN)
     │        throttle += 0.025s between launches         │
     │   ◄── tracking-detail{ significant-events[] } ─────│
     │                                                    │
     ├─► _extract_tracking (only nodes with ≥1 occurrence)│
     │     event_identifier → TrackingStatus / reason     │
     ▼                                                    ▼
list[TrackingDetails]
```

### Manifest / transmit-set (commercial group transmission)

```
ManifestRequest                                  Canada Post (manifest-v8)
     │                                                    │
     ├─► manifest_request:                                │
     │     group_ids from options.group_ids OR mined from │
     │       options.shipments[].meta.group_id            │
     │     retrieve_shipments = (no group_ids)            │
     │     → transmit-set XML with <group-id>[GROUP_IDS]  │
     │       placeholder                                  │
     │                                                    │
     │   if retrieve_shipments:                           │
     │     GET /{cn}/{cn}/shipment/{pin}/details (per id)  │
     │       → harvest <group-id> values                  │
     │                                                    │
     │   ─── POST /rs/{cn}/{cn}/manifest ────────────────►│
     │        ([GROUP_IDS] replaced by real <group-id>s)  │
     │   ◄── links[] (manifest references) ───────────────│
     │                                                    │
     ├─► GET each manifest link, then GET rel="artifact"  │
     │     links → base64 manifest PDFs                    │
     ▼                                                    ▼
ManifestDetails(doc.manifest = bundled base64, meta.group_ids/links)
```

### Pickup (Pipeline: availability → create; or update/cancel)

```
PickupRequest                                    Canada Post (pickup / pickuprequest)
     │                                                    │
     ├─► Pipeline(get_availability → create_pickup)       │
     │   GET /ad/pickup/pickupavailability/{postalcode} ─►│
     │   ◄── pickup-availability{ on-demand-tour } ───────│
     │                                                    │
     │   if on_demand_tour:                               │
     │     POST /enab/{cn}/pickuprequest ────────────────►│
     │   ◄── pickup-request-header{ request-id, ...} ─────│
     ▼                                                    ▼
PickupDetails(confirmation_number, pickup_date, pickup_charge)
```

Update follows the same Pipeline shape (`PUT .../pickuprequest/{id}`
then `GET .../{id}/details`). Cancel is a single
`DELETE .../pickuprequest/{id}`.

## Endpoints

Base URL (`Settings.server_url`):
- Test mode: `https://ct.soa-gw.canadapost.ca`
- Prod: `https://soa-gw.canadapost.ca`

`{cn}` = `Settings.customer_number` (the connector uses it for both the
`mailed-by-customer` and `mobo`/`mailed-on-behalf-of` path segments).

| Purpose | Method | Path |
|---|---|---|
| Rate (price) | POST | `/rs/ship/price` |
| Create shipment | POST | `/rs/{cn}/{cn}/shipment` |
| Get shipment (for cancel) | GET | `/rs/{cn}/{cn}/shipment/{id}` |
| Refund shipment (transmitted) | POST | `/rs/{cn}/{cn}/shipment/{id}/refund` |
| Delete shipment (non-transmitted) | DELETE | `/rs/{cn}/{cn}/shipment/{id}` |
| Get shipment details (manifest) | GET | `/{cn}/{cn}/shipment/{pin}/details` |
| Label / manifest artifact | GET | pre-resolved `href` from `rel="label"` / `rel="artifact"` link |
| Authorized return | POST | `/rs/{cn}/{cn}/authorizedreturn` |
| Tracking by PIN | GET | `/vis/track/pin/{pin}/detail` |
| Pickup availability | GET | `/ad/pickup/pickupavailability/{postalCode}` |
| Create pickup | POST | `/enab/{cn}/pickuprequest` |
| Update pickup | PUT | `/enab/{cn}/pickuprequest/{id}` |
| Get pickup details | GET | `/enab/{cn}/pickuprequest/{id}/details` |
| Cancel pickup | DELETE | `/enab/{cn}/pickuprequest/{id}` |
| Manifest (transmit-set) | POST | `/rs/{cn}/{cn}/manifest` |

**Media types** (the `Content-Type` / `Accept` per operation):

| Operation | Media type |
|---|---|
| Rate | `application/vnd.cpc.ship.rate-v4+xml` |
| Shipment / cancel / refund / details | `application/vnd.cpc.shipment-v8+xml` |
| Authorized return | `application/vnd.cpc.authreturn-v2+xml` |
| Tracking | `application/vnd.cpc.track-v2+xml` |
| Pickup availability | `application/vnd.cpc.pickup+xml` |
| Pickup request | `application/vnd.cpc.pickuprequest+xml` |
| Manifest | `application/vnd.cpc.manifest-v8+xml` |

Every request also sends `Accept-language: {en|fr}-CA` derived from
`Settings.language`.

## Authentication

**HTTP Basic Auth.** `Settings.authorization` is
`base64(username:password)` sent as
`Authorization: Basic <b64>` on every call. No OAuth, no token caching.

Connection fields (`mappers/canadapost/settings.py`):

| Field | Required | Notes |
|---|---|---|
| `username` | yes | API username |
| `password` | yes | API key/password (`sensitive`) |
| `customer_number` | yes (for ship/cancel/manifest/pickup) | path segment + default payer |
| `contract_id` | no | commercial contract pricing; sent on rate and settlement-info |
| `language` | no | `en` (default) or `fr` → `Accept-language` and tracking URL locale |

Tracking URL surfaced to users:
`https://www.canadapost-postescanada.ca/track-reperage/{lang}#/resultList?searchFor={pin}`.

## Supported operations

| Operation | Mapper method | Provider | Wired |
|---|---|---|---|
| Rate | `create_rate_request` / `parse_rate_response` | `rate.py` | yes |
| Shipment create | `create_shipment_request` / `parse_shipment_response` | `shipment/create.py` | yes |
| Shipment cancel | `create_cancel_shipment_request` / `parse_shipment_cancel_response` | `shipment/cancel.py` | yes |
| Return shipment | `create_return_shipment_request` / `parse_return_shipment_response` | `shipment/return_shipment.py` | yes |
| Tracking | `create_tracking_request` / `parse_tracking_response` | `tracking.py` | yes |
| Pickup schedule | `create_pickup_request` / `parse_pickup_response` | `pickup/create.py` | yes |
| Pickup update | `create_pickup_update_request` / `parse_pickup_update_response` | `pickup/update.py` | yes |
| Pickup cancel | `create_cancel_pickup_request` / `parse_pickup_cancel_response` | `pickup/cancel.py` | yes |
| Manifest | `create_manifest_request` / `parse_manifest_response` | `manifest.py` | yes |

Plugin metadata (`plugins/canadapost/__init__.py`): id `canadapost`,
label `Canada Post`, `status="production-ready"`.

## Services

Static `ServiceType` enum (`units.py`) — karrio service key → CP
`service-code` on the wire:

| karrio service | CP `service-code` |
|---|---|
| `canadapost_regular_parcel` | `DOM.RP` |
| `canadapost_expedited_parcel` | `DOM.EP` |
| `canadapost_xpresspost` | `DOM.XP` |
| `canadapost_xpresspost_certified` | `DOM.XP.CERT` |
| `canadapost_priority` | `DOM.PC` |
| `canadapost_library_books` | `DOM.LIB` |
| `canadapost_expedited_parcel_usa` | `USA.EP` |
| `canadapost_priority_worldwide_envelope_usa` | `USA.PW.ENV` |
| `canadapost_priority_worldwide_pak_usa` | `USA.PW.PAK` |
| `canadapost_priority_worldwide_parcel_usa` | `USA.PW.PARCEL` |
| `canadapost_small_packet_usa_air` | `USA.SP.AIR` |
| `canadapost_tracked_packet_usa` | `USA.TP` |
| `canadapost_tracked_packet_usa_lvm` | `USA.TP.LVM` |
| `canadapost_xpresspost_usa` | `USA.XP` |
| `canadapost_xpresspost_international` | `INT.XP` |
| `canadapost_international_parcel_air` | `INT.IP.AIR` |
| `canadapost_international_parcel_surface` | `INT.IP.SURF` |
| `canadapost_priority_worldwide_envelope_intl` | `INT.PW.ENV` |
| `canadapost_priority_worldwide_pak_intl` | `INT.PW.PAK` |
| `canadapost_priority_worldwide_parcel_intl` | `INT.PW.PARCEL` |
| `canadapost_small_packet_international_air` | `INT.SP.AIR` |
| `canadapost_small_packet_international_surface` | `INT.SP.SURF` |
| `canadapost_tracked_packet_international` | `INT.TP` |

`DEFAULT_SERVICES` (`service_levels` in plugin metadata) is built from
`services.csv` via `load_services_from_csv()`. Each CSV row contributes
a `ServiceZone` (rate, weight bounds, transit days, country codes)
aggregated under the karrio service key; the CSV `service_code` column
is mapped back to the karrio key via `ServiceType.map(...).name_or_key`.
Currency defaults to `CAD`, weight unit `KG`, dimension unit `CM`.

### Package presets

`PackagePresets` enum (dimensions in CM, weight in KG) covers Canada
Post box/envelope sizes, e.g. `canadapost_small_mailing_box`,
`canadapost_large_mailing_box`, `canadapost_corrugated_large_box`,
`canadapost_xexpresspost_certified_envelope`, etc.
`MeasurementOptions`: `quant=0.1`, `min_kg=0.01`, `min_in=0.01`.

## Options

`ShippingOption` enum — karrio option key → CP `option-code`. Each
carries a `meta.category` used by the platform option taxonomy.

| Option | CP `option-code` | Type | Category |
|---|---|---|---|
| `canadapost_signature` | `SO` | bool | SIGNATURE |
| `canadapost_coverage` | `COV` | float | INSURANCE |
| `canadapost_collect_on_delivery` | `COD` | float | COD |
| `canadapost_proof_of_age_required_18` | `PA18` | bool | SIGNATURE |
| `canadapost_proof_of_age_required_19` | `PA19` | bool | SIGNATURE |
| `canadapost_card_for_pickup` | `HFP` | bool | PUDO |
| `canadapost_do_not_safe_drop` | `DNS` | bool | DELIVERY_OPTIONS |
| `canadapost_leave_at_door` | `LAD` | bool | DELIVERY_OPTIONS |
| `canadapost_deliver_to_post_office` | `D2PO` | bool | PUDO |
| `canadapost_return_at_senders_expense` | `RASE` | bool | RETURN |
| `canadapost_return_to_sender` | `RTS` | bool | RETURN |
| `canadapost_abandon` | `ABAN` | bool | — |

**Custom (non-wire-option) keys** — filtered out of the `optionsType`
list via `CUSTOM_OPTIONS`:

| Option | Wire key | Purpose |
|---|---|---|
| `canadapost_cost_center` | `cost-centre` | populates `references/cost-centre` |
| `canadapost_submit_shipment` | `transmit-shipment` | forces immediate transmit (see lifecycle) |

**Unified-option aliases:** `insurance → canadapost_coverage (COV)`,
`cash_on_delivery → canadapost_collect_on_delivery (COD)`,
`signature_confirmation → canadapost_signature (SO)`.

**International default (gotcha):** `shipping_options_initializer`
auto-applies `canadapost_return_at_senders_expense` (RASE) on
international shipments **unless** the caller already set one of the
non-delivery options (`RASE`, `RTS`, `ABAN` — `INTERNATIONAL_NON_DELIVERY_OPTION`).
This guarantees a defined non-delivery handling for cross-border
parcels.

`option-code` on the wire is read directly from `option.code` (the
first `OptionEnum` arg); the code never maintains a parallel
`{key: wire_code}` dict.

## Connection config

`ConnectionConfig` enum (`config` blob on the connection):

| Key | Type | Effect |
|---|---|---|
| `cost_center` | str | fallback `references/cost-centre` |
| `label_type` | `LabelType` | label encoding/format default |
| `shipping_options` | list | allowed options projection |
| `shipping_services` | list | allowed services projection |
| `transmit_shipment_by_default` | bool | transmit each shipment immediately instead of grouping |

`LabelType` maps a unified label key to `(encoding, format)`:

| LabelType | encoding | format |
|---|---|---|
| `PDF_4x6` / `PDF` | `PDF` | `4x6` |
| `PDF_8_5x11` | `PDF` | `8.5x11` |
| `ZPL_4x6` / `ZPL` | `ZPL` | `4x6` |

`PaymentType` maps unified `paid_by` → CP `intended-method-of-payment`:
`account/sender/recipient → Account`, `credit_card → CreditCard`,
`third_party → SupplierAccount`.

## Data mapping

### Address — karrio `Address` → CP `AddressDetailsType` (shipment-v8)

```
karrio Address                 CP shipment address
─────────────────              ───────────────────
person_name        ───►        sender/destination name
company_name       ───►        company  (sender defaults to "Not Applicable")
phone_number       ───►        contact-phone / client-voice-number
                               (defaults to "000 000 0000" when absent)
address_line1      ───►        address-line-1
address_line2      ───►        address-line-2
city               ───►        city
state_code         ───►        province
postal_code        ───►        postal-zip-code  (spaces stripped + uppercased)
country_code       ───►        country-code
```

`format_ca_postal_code` strips spaces and uppercases; it is reused (by
name) to normalize the destination `country-code` on international rate
requests — it is *only* text normalization, not validation.

### Shipment-level fields

```
ShipmentRequest                CP DeliverySpec / ShipmentType
───────────────                ──────────────────────────────
service             ───►       delivery-spec/service-code  (ServiceType)
reference           ───►       references/customer-ref-1 (+ cost-centre fallback)
options[*]          ───►       options/option[option-code, option-amount]
                               (option-amount = lib.to_money(state); flags emit
                                with state != False)
label_type          ───►       print-preferences {output-format, encoding}
payment.account_no  ───►       settlement-info/paid-by-customer (→ customer_number)
payment.paid_by     ───►       settlement-info/intended-method-of-payment
contract_id         ───►       settlement-info/contract-id
expected_mailing    ───►       expected-mailing-date (options.shipment_date)
```

`preferences`: `show-postage-rate=true`, `show-insured-value=true`,
`show-packing-instructions=false`. `provide-pricing-info=true` (so the
response carries `shipment-price`).

**Email notification:** emitted as `NotificationType`
(`on-shipment/on-exception/on-delivery = true`) only when
`email_notification` option is set and an address is resolvable
(`email_notification_to` or recipient email).

### Customs — `CustomsInfo` → CP `CustomsType` (sent only when `payload.customs` present)

```
karrio customs                 CP customs
──────────────                 ──────────
options.currency / EUR→CAD ─►  currency (defaults CAD)
content_type           ───►    other-reason  (reason-for-export hardcoded "OTH")
duty.account_number    ───►    duties-and-taxes-prepaid
options.certificate_number ─►  certificate-number
options.license_number ───►    licence-number (max 10 chars)
invoice                ───►    invoice-number (max 10 chars)
commodities[i]         ───►    sku-list/item[i] {
  quantity                       customs-number-of-units
  title/description/sku ───►     customs-description (max 35; "N/B" fallback)
  sku                            sku ("0000" fallback)
  hs_code               ───►     hs-tariff-code
  weight                ───►     unit-weight (1 fallback)
  value_amount          ───►     customs-value-per-unit
  origin_country        ───►     country-of-origin (← shipper.country_code)
}                                province-of-origin ← shipper.state_code ("N/B")
```

`reason-for-export` is fixed to `"OTH"`; `content_type` is carried as
the free-text `other-reason`.

### Rate request destination switch (rate-v4)

The rate request branches the `destination` element by recipient
country: `domestic` (recipient `CA`), `united-states` (recipient `US`,
`zip-code`), or `international` (`country-code`). Origin country must be
`CA` or `rate_request` raises `OriginNotServicedError`.

```
RateDetails (rate.py)          source
─────────────────────          ──────
total_charge          ───►     price-details/due
transit_days          ───►     service-standard/expected-transit-time
extra_charges         ───►     base + GST/PST/HST taxes + options + adjustments
service               ───►     ServiceType.map(service-code)
currency = CAD
```

Shipment-create `selected_rate` is derived from `shipment-price`
(`base-amount` as `total_charge`; GST/PST/HST + priced options +
adjustments as extra charges; `CAD`).

### Authorized return (authreturn-v2)

`authorized-return` swaps shipper↔receiver roles: the unified `shipper`
becomes the `returner` (the customer sending the parcel back) and the
unified `recipient` becomes the `receiver` (the merchant). Single
parcel (`packages[0]`). Response `tracking-pin` maps to both
`tracking_number` and `shipment_identifier`; label fetched via the same
two-step link GET.

## Submit vs. group (manifest) lifecycle

This is the connector's central state machine. A created shipment is
either **transmitted immediately** or **filed under a group-id** that
must later be transmitted via a manifest.

```
shipment_request decides submit_shipment:
  canadapost_submit_shipment option == True
    OR (connection_config.transmit_shipment_by_default
        AND canadapost_submit_shipment is not False)

XML carries a <groupIdOrTransmitShipment/> placeholder, replaced at
serialize time:
   submit_shipment  → <transmit-shipment/>
   else             → <group-id>{YYYYMMDD-canadapost}</group-id>
```

- **Transmit now** (`<transmit-shipment/>`): no manifest needed.
  Serializable ctx sets `manifest_required=False`, `group_id=None`.
- **Group** (`<group-id>`): ctx sets `manifest_required=True` and a
  `group_id` of the form `{YYYYMMDD}-canadapost`. The shipment's
  `meta.group_id` / `meta.manifest_required` are surfaced so a later
  manifest call can transmit the group.

`customer_request_ids` (one `uuid4().hex` per parcel) is stamped onto
each request and echoed in shipment `meta.customer_request_ids`.

**Manifest** (`manifest.py`) collects `group-id`s either from
`options.group_ids` or by mining `meta.group_id` off
`options.shipments[]`. When no group ids are known
(`retrieve_shipments = True`), the proxy first GETs
`/shipment/{pin}/details` for each `shipment_identifier` to harvest the
`<group-id>` values. The `transmit-set` body uses a `[GROUP_IDS]`
placeholder that the proxy replaces with the real
`<group-id>...</group-id>` elements before POSTing. Manifest artifacts
(`rel="artifact"` links) are fetched and base64-bundled into
`doc.manifest`.

## Tracking status mapping

`event_identifier` (numeric CP event code) → karrio status, matched in
`TrackingStatus` enum order; unmatched codes fall back to `in_transit`.

| karrio status | example CP event codes |
|---|---|
| `delivered` | `1408`, `1409`, `1421`–`1434`, `1441`, `1442`, `1496`–`1499` |
| `picked_up` | `100`–`107`, `1400`–`1405` |
| `on_hold` | `117`, `120`, `121`, `125`, `127`, `810`, `1411`, `1414`, `1443`, `1484`, `1487`, `1494`, `2411`, `2414`, `4700` |
| `ready_for_pickup` | `118`, `156`, `1407`, `1410`, `1435`–`1438`, `1479`, `1488`, `1701`, `2410` |
| `delivery_failed` | `150`, `154`, `167`–`169`, `179`, `181`–`184`, `190`, `1100`, `1415`–`1420`, `1450`, `1481`–`1483`, `1491`–`1493`, `2600`, `2802`, `3001`, `4650` |
| `delivery_delayed` | `159`–`163`, `172`, `173`, `2412` |
| `out_for_delivery` | `174`, `500` |
| `in_transit` | `""` (fallback for any unmapped code) |

The connector additionally maps event codes to a normalized
`TrackingIncidentReason` (e.g. `carrier_damaged_parcel`,
`consignee_refused`, `consignee_not_home`, `customs_duties_unpaid`,
`weather_delay`, `natural_disaster`) per event, attached to each
`TrackingEvent.reason`.

Tracking detail fields: `pin → tracking_number`,
`significant-events/occurrence[]` → events (date/time/code/location/
description), `expected-delivery-date` (or `changed-expected-date`) →
`estimated_delivery`, `signatory-name` of the latest event →
`info.signed_by`. Only `tracking-detail` nodes with ≥1 `occurrence` are
emitted.

## Error parsing

Canada Post returns errors as a `<messages>` document of `<message>`
elements (`messages-v?` namespace). `error.parse_error_response`
collects every `<message>` (typed `messageType`) across all responses
and maps `code` / `description` to `models.Message`:

```
<messages>                     ┌────────────────────────────┐
  <message>                    │ error.parse_error_response   │
    <code>…</code>      ───►   │   find_element("message")    │
    <description>…</…>         │   → Message{code, message,   │
  </message>                   │       carrier_*, details=kw} │
</messages>                    └──────────────┬──────────────┘
                                              ▼
                                       list[Message]
```

`process_error(HTTPError)` synthesizes the same `<messages>` envelope
from a raw transport-level `HTTPError` (code + msg) so downstream
parsing is uniform. The shipment parsers treat a response as a success
only when the identity element is present (`shipment-id`,
`tracking-pin`, `pickup-request-header`, etc.); otherwise the
`<message>` list is surfaced as errors. Cancel success is "any leg
returned zero messages".

## References

- **Vendor schemas (source of truth)** — `schemas/*.xsd`
  (`rating.xsd`, `shipment.xsd`, `authreturn.xsd`, `track.xsd`,
  `manifest.xsd`, `pickup.xsd`, `pickuprequest.xsd`, `messages.xsd`,
  `common.xsd`, plus discovery/serviceinfo/postoffice/customerinfo/
  merchantregistration/ncshipment/openreturn).
- **Canada Post Developer Program** —
  <https://www.canadapost-postescanada.ca/information/app/drc/home>
- **Authorized Returns docs** —
  <https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/returns/createreturn.jsf>
- **Service-level catalog** — `karrio/providers/canadapost/services.csv`
  (drives `DEFAULT_SERVICES`).
- **Generated types** — `karrio/schemas/canadapost/*.py` are generated
  from `schemas/*.xsd` via `generateDS` (see the `generate` script).
  Regenerate with `./bin/run-generate-on modules/connectors/canadapost`
  — never hand-edit.
```
