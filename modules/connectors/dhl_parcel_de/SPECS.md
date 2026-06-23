# DHL Parcel DE (DHL Paket Germany) integration — specification

Reference for the `dhl_parcel_de` connector. It targets **DHL Paket
Germany** ("Post & Paket Deutschland") over the DHL developer-portal
JSON REST APIs (shipping `Parcel DE Shipping v2`, returns, pickup v3),
plus a separate XML-over-HTTP **Tracking API** (`tracking/v0`). Plugin
status is `beta`; carrier id `dhl_parcel_de`, label "DHL Germany".

The vendor source of truth lives under `vendors/`:

- `vendors/parcel-de-shipping-v2_2.yaml` — shipping OpenAPI (orders create/cancel)
- `vendors/pp-parcel-returns.yaml` — returns OpenAPI
- `vendors/parcel-de-pickup-v3.yaml` — pickup OpenAPI
- `vendors/Shipment Tracking_2_0.yaml` — tracking spec
- `vendors/parcel_de_ice_event_ric_combinations_July_2024.csv` — ICE / RIC / event-code ground truth driving the tracking-status enum
- `vendors/Verfügbare Services_en_0.png`, `vendors/Abrechnungsnummern_en_1.png` — service & billing-number screenshots from DHL

This connector is also the canonical reference for the
`shipping_options_initializer` pattern (per the repo rules); see
[Options defaulting & droppoint resolution](#options-defaulting--droppoint-resolution).

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Data flow](#data-flow)
3. [Endpoints](#endpoints)
4. [Authentication](#authentication)
5. [Supported operations](#supported-operations)
6. [Services](#services)
7. [Options](#options)
8. [Connection config](#connection-config)
9. [Billing-number resolution](#billing-number-resolution)
10. [Options defaulting & droppoint resolution](#options-defaulting--droppoint-resolution)
11. [Data mapping](#data-mapping)
12. [Carrier-specific invariants & gotchas](#carrier-specific-invariants--gotchas)
13. [Tracking](#tracking)
14. [Error parsing](#error-parsing)
15. [References](#references)

---

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio ShipmentRequest / RateRequest /
│   (karrio core)         │   PickupRequest / TrackingRequest / ShipmentCancel
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  providers/dhl_parcel_de│   Pure data transforms.
│   shipment/create.py    │   Unified model → typed DHL JSON request,
│   shipment/cancel.py    │   typed DHL response → unified model.
│   shipment/return_…py   │   No HTTP, no side effects.
│   pickup/create.py      │
│   pickup/cancel.py      │
│   tracking.py           │   XML request build + XML response parse.
│   error.py              │
│   units.py              │   ShippingService, ShippingOption,
│   utils.py              │   ConnectionConfig, TrackingStatus,
│                         │   shipping_options_initializer, billing-number lookup.
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  mappers/dhl_parcel_de  │   HTTP transport only.
│   proxy.py              │   - OAuth ROPC token caching (8 h, 1 h buffer)
│   settings.py           │   - per-API base URLs (sandbox vs prod)
│   mapper.py             │   - JSON for shipping/returns/pickup
│                         │   - XML + Basic-auth for tracking
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  DHL Parcel DE APIs     │
│  ─────────────────────  │
│  Shipping v2            │   POST /v2/orders, DELETE /v2/orders
│  Returns v1             │   POST /returns/v1/orders
│  Pickup v3              │   POST/DELETE /transportation/pickup/v3/orders
│  Tracking v0 (XML)      │   GET /tracking/v0/shipments?xml=…
│  Auth ROPC v1 (OAuth)   │   POST /account/auth/ropc/v1/token
└─────────────────────────┘
```

**Key architectural choices:**

- **No live rate API.** Rating is served by karrio's universal rating
  provider (`karrio.universal.providers.rating`) over a **static
  catalog loaded from `services.csv`** (`provider_units.DEFAULT_SERVICES`).
  `mapper.create_rate_request` / `parse_rate_response` delegate to the
  universal provider; there is no DHL rate HTTP call.
- **OAuth2 Resource-Owner-Password-Credentials (ROPC)** grant, cached
  per connection. Tokens are 8 h (`expires_in=28800`) and refreshed
  with a 60-minute buffer.
- **Two-layer tracking auth** — the tracking API needs HTTP Basic auth
  (`client_id:client_secret`) *and* XML-embedded `appname`/`password`
  credentials inside the request.
- **Generated schemas** — JSON schemas under
  `karrio/schemas/dhl_parcel_de/*.py` are generated from
  `schemas/*.json` via kcli; the two tracking modules are generated
  from `schemas/*.xsd` via `generateDS`. Regenerate with
  `./bin/run-generate-on modules/connectors/dhl_parcel_de` — never
  hand-edit. (`returns_request.py` / `returns_response.py` are
  preserved by the `generate` script's `find … ! -name` exclusion.)

## Data flow

### Shipment create (one HTTP call, multi-piece)

```
ShipmentRequest                          DHL Shipping v2
     │                                          │
     │  shipment_request()                      │
     ├─► lib.to_address(shipper/recipient)      │
     ├─► ShippingService.map(service) → product │
     ├─► get_billing_number(service, billing_id)│
     ├─► shipping_options_initializer           │  (defaults + droppoint resolve)
     ├─► shipper / consignee oneOf (inline)      │
     ├─► one ShipmentType per parcel            │
     │                                          │
     ├─► ShippingRequestType (typed)            │
     ├─► lib.to_dict → JSON                     │
     │                                          │
     │  POST /v2/orders?includeDocs=include     │
     │       &docFormat=…&printFormat=…         │
     │       &combine=false  ───────────────────►│  validate + label gen
     │                                          │
     │  ◄── { items: [{ sstatus.statusCode,     │
     │         shipmentNo, label, customsDoc,   │
     │         returnLabel, codLabel,           │
     │         validationMessages }] } ─────────│
     │                                          │
     ├─► _extract_details per item:             │
     │     shipmentNo → tracking_number         │
     │                  + shipment_identifier    │
     │     label.b64/zpl2 → docs.label          │
     │     customsDoc → docs.invoice            │
     │     returnLabel/codLabel → extra_documents│
     │     returnShipmentNo → return_shipment   │
     │                                          │
     ▼   lib.to_multi_piece_shipment            ▼
ShipmentDetails                          (no further call)
```

A shipment is only produced when **at least one item** has
`sstatus.statusCode == 200`; `validationMessages` with state
`error`/`warning` are always surfaced as `Message`s.

### Tracking (XML, async batches of 20)

```
TrackingRequest                          DHL Tracking v0 (XML)
     │                                          │
     ├─► batch tracking_numbers (20 per call)   │
     ├─► TrackingRequestType per batch:         │
     │     appname / password (XML creds)       │
     │     request="d-get-piece-detail"         │
     │     piece_code=";"-joined batch          │
     ├─► lib.to_xml → <data …>                  │
     │                                          │
     │  GET /tracking/v0/shipments?xml=<…>      │
     │      Authorization: Basic b64(id:secret) │
     │      (one GET per batch, run async) ──────►│
     │                                          │
     │  ◄── XML: <data name="piece-shipment" …> │
     │            <data name="piece-event-list"> │
     │              <data name="piece-event" …>  │
     │                                          │
     ├─► _extract_tracking per piece-shipment:  │
     │     ice / standard-event-code → status   │
     │     ric → incident reason                │
     │     events reversed (chronological)      │
     ▼                                          ▼
list[TrackingDetails]                    list[Message] for errors
```

### Rate (no HTTP — static catalog)

```
RateRequest ──► universal_provider.rate_request ──► matches against
                services.csv (DEFAULT_SERVICES)  ──► list[RateDetails]
```

## Endpoints

Base host — sandbox: `api-sandbox.dhl.com`, prod: `api-eu.dhl.com`.
All paths are under `/parcel/de`.

| Purpose | Method | Path |
|---|---|---|
| OAuth token (ROPC) | POST | `/account/auth/ropc/v1/token` |
| Create shipment | POST | `/shipping/v2/orders?{query}` |
| Cancel shipment | DELETE | `/shipping/v2/orders?{query}` |
| Create return | POST | `/shipping/returns/v1/orders?{query}` |
| Schedule pickup | POST | `/transportation/pickup/v3/orders` |
| Cancel pickup | DELETE | `/transportation/pickup/v3/orders?orderID={id}` |
| Tracking | GET | `/tracking/v0/shipments?xml={urlencoded-xml}` |

Shipment-create query params (built in `shipment_request`):
`includeDocs=include`, `docFormat`, `printFormat`, `combine=false`.
(`validate=true` is present-but-commented in code.) An extra `_meta`
key carrying `billing_number` is popped by the proxy before building
the query and threaded into response parsing.

Shipment-cancel query: `shipment` (comma-joined shipment numbers) +
`profile`.

Content type is `application/json` for shipping/returns/pickup and
`application/xml` (`Accept`) for tracking. Every JSON call sends
`Accept-Language: {language}-{COUNTRY}` (see [language](#language)).

## Authentication

OAuth2 **ROPC** (`grant_type=password`) against
`/account/auth/ropc/v1/token`, body form-urlencoded with
`username`, `password`, `client_id`, `client_secret`. The response is
cached via `connection_cache.thread_safe` keyed by
`dhl_parcel_de|<client_id>|<client_secret>`, refreshed when within
**60 minutes** of expiry (tokens last 8 h). Shipping/returns/pickup
calls go through `lib.authenticated_request` (Bearer token).

```
credentials (username/password/client_id/client_secret)
       │
       ▼
┌──────────────┐   miss / <60 min to expiry   ┌──────────────┐
│ _token_      │◄─────────────────────────────│ Token Cache  │
│  manager()   │                              │  key:        │
│              │   cache hit                  │  dhl_parcel_ │
│              │─────────────────────────────►│  de|<cid>|   │
└──────┬───────┘                              │  <secret>    │
       │  POST /account/auth/ropc/v1/token    └──────────────┘
       ▼
   grant_type=password (form-urlencoded)
```

**Credential resolution** (`utils.Settings`):

- `connection_username` / `connection_password` — user-provided only,
  no system fallback.
- `connection_client_id` / `connection_client_secret` — user value, else
  system config: `DHL_PARCEL_DE_SANDBOX_CLIENT_ID/_SECRET` in test mode,
  `DHL_PARCEL_DE_CLIENT_ID/_SECRET` in prod (see `SYSTEM_CONFIG`).

**Tracking is special** — two layers:

1. HTTP Basic `base64(client_id:client_secret)` for the API gateway.
2. XML-embedded `appname` + `password` for the tracking service. In
   **sandbox** these are hardcoded to DHL's documented test values
   (`appname="zt12345"`, `password="geheim"`); in prod they fall back
   to `connection_username` / `connection_password`.

## Supported operations

| Operation | Wired? | Provider entry point |
|---|---|---|
| Rate | yes (static catalog) | `universal_provider.rate_request` / `parse_rate_response` |
| Shipment create | yes | `shipment_request` / `parse_shipment_response` |
| Shipment cancel | yes | `shipment_cancel_request` / `parse_shipment_cancel_response` |
| Return shipment | yes | `return_shipment_request` / `parse_return_shipment_response` |
| Tracking | yes | `tracking_request` / `parse_tracking_response` |
| Pickup schedule | yes (one-time only) | `pickup_request` / `parse_pickup_response` |
| Pickup cancel | yes | `pickup_cancel_request` / `parse_pickup_cancel_response` |
| Document upload / manifest | no | — |

`is_hub=False`.

## Services

`ShippingService` (`units.py`) — karrio code → DHL product code:

| karrio service | DHL `product` | CSV catalog |
|---|---|---|
| `dhl_parcel_de_paket` | `V01PAK` | DHL Paket (DE, 0.01–31.5 kg) |
| `dhl_parcel_de_kleinpaket` | `V62KP` | DHL Kleinpaket (DE, ≤1 kg) |
| `dhl_parcel_de_europaket` | `V54EPAK` | DHL EuroPaket (EU, ≤31.5 kg) |
| `dhl_parcel_de_paket_international` | `V53WPAK` | DHL Paket International (RoW) |
| `dhl_parcel_de_warenpost_international` | `V66WPI` | Warenpost International (RoW, ≤1 kg) |
| `dhl_parcel_de_retoure` | `V07PAK` | DHL Retoure (return) |

`dhl_parcel_de_warenpost` is a **backwards-compat alias** for
`dhl_parcel_de_kleinpaket` (Warenpost was replaced by Kleinpaket as of
2025), so both names resolve to `V62KP`.

`PackagingType` collapses every unified packaging preset onto a single
`PACKAGE` wire value. The static rate catalog
(`DEFAULT_SERVICES`) is built from `services.csv` — zones, weight bands,
dimension caps, transit days, domicile/international flags. If the CSV
is missing the loader falls back to a single DHL Paket service.

## Options

`ShippingOption` (`units.py`). The first positional arg to each
`OptionEnum` is the **wire field name**; the meta `category` /
`configurable` / `service_level` / `compatible_services` drive the
shipping-app options editor. Standard-karrio aliases at the bottom of
the enum map onto DHL options.

### Delivery / handling (on `shipments[].services`)

| Option | Wire field | Type |
|---|---|---|
| `dhl_parcel_de_preferred_neighbour` | `preferredNeighbour` | str |
| `dhl_parcel_de_preferred_location` | `preferredLocation` | str |
| `dhl_parcel_de_preferred_day` | `preferredDay` | str (YYYY-MM-DD) |
| `dhl_parcel_de_named_person_only` | `namedPersonOnly` | bool |
| `dhl_parcel_de_no_neighbour_delivery` | `noNeighbourDelivery` | bool |
| `dhl_parcel_de_signed_for_by_recipient` | `signedForByRecipient` | bool |
| `dhl_parcel_de_bulky_goods` | `bulkyGoods` | bool (Sperrgut) |
| `dhl_parcel_de_visual_check_of_age` | `visualCheckOfAge` | enum `A16`/`A18` |
| `dhl_parcel_de_ident_check` | `identCheck` | object (`IdentCheckType`) |
| `dhl_parcel_de_closest_drop_point` | `closestDropPoint` | bool (CDP) |
| `dhl_parcel_de_parcel_outlet_routing` | `parcelOutletRouting` | str (Filial routing) |
| `dhl_parcel_de_delivery_tier` | → `premium`/`economy` flags | enum |
| `dhl_parcel_de_gogreen_plus` | `goGreenPlus` | bool |
| `dhl_parcel_de_individual_sender_requirement` | `individualSenderRequirement` | str |
| `dhl_parcel_de_endorsement` | `endorsement` | enum `RETURN`/`ABANDON`, default `RETURN` |

`dhl_parcel_de_delivery_tier` is an enum (`premium`/`economy`) that
maps to the boolean `premium` / `economy` service flags on the wire.
Legacy `dhl_parcel_de_premium` / `dhl_parcel_de_economy` boolean
options are migrated to the enum in the initializer.

### Insurance / COD

| Option | Wire field | Notes |
|---|---|---|
| `dhl_parcel_de_additional_insurance` (`insurance`) | `additionalInsurance{currency,value}` | EUR; bands 0-2500 / 0-25000 / 0-50000 |
| `dhl_parcel_de_cash_on_delivery` (`cash_on_delivery`) | `cashOnDelivery{amount,bankAccount,accountReference,transferNote1,transferNote2}` | first parcel only (see gotchas) |
| `dhl_parcel_de_cod_account_reference` | `accountReference` | connection-level |
| `dhl_parcel_de_cod_transfer_note1` | `transferNote1` | defaults to shipment reference |
| `dhl_parcel_de_cod_transfer_note2` | `transferNote2` | optional |
| `dhl_parcel_de_cod_bank_account_holder` | `bankAccount.accountHolder` | connection-level |
| `dhl_parcel_de_cod_bank_name` | `bankAccount.bankName` | connection-level |
| `dhl_parcel_de_cod_bank_iban` | `bankAccount.iban` | connection-level |
| `dhl_parcel_de_cod_bank_bic` | `bankAccount.bic` | connection-level |

### PUDO / locker (consignee `oneOf`)

| Option | Wire field | Type |
|---|---|---|
| `dhl_parcel_de_locker_id` (`locker_id`) | `lockerID` | int (Packstation) |
| `dhl_parcel_de_retail_id` | `retailID` | int (Postfiliale) |
| `dhl_parcel_de_po_box_id` | `poBoxID` | int (Postfach) |
| `dhl_parcel_de_post_number` | `postNumber` | int (Postnummer) |

### Customs / export (on `shipments[].customs`)

| Option | Wire field |
|---|---|
| `dhl_parcel_de_postal_delivery_duty_paid` | `postalDeliveryDutyPaid` (pDDP) |
| `dhl_parcel_de_shipper_customs_ref` | `shipperCustomsRef` (sender EORI) |
| `dhl_parcel_de_consignee_customs_ref` | `consigneeCustomsRef` |
| `dhl_parcel_de_permit_no` | `permitNo` |
| `dhl_parcel_de_attestation_no` | `attestationNo` |
| `dhl_parcel_de_has_electronic_export_notification` | `hasElectronicExportNotification` (EEN) |
| `dhl_parcel_de_MRN` | `MRN` |
| `dhl_parcel_de_postal_charges` (`shipping_charges`) | `postalCharges` |

There is also a parallel `CustomsOption` enum used by
`lib.to_customs_info` (`mrn`, `permit_number`, `attestation_number`,
`shipper_customs_ref`, `consignee_customs_ref`,
`electronic_export_notification`).

### Returns (DHL Retoure, on `shipments[].services.dhlRetoure`)

| Option | Wire field |
|---|---|
| `dhl_parcel_de_return_enabled` (`returnEnabled`) | triggers `dhlRetoure` block |
| `dhl_parcel_de_return_receiver_id` | `returnReceiverId` |
| `dhl_parcel_de_return_billing_number` | `dhlRetoure.billingNumber` |
| `dhl_parcel_de_return_reference` | `dhlRetoure.refNo` |
| `dhl_parcel_de_dhl_retoure` | full `dhlRetoure` object (internal) |
| `dhl_parcel_de_return_service_code` | resolves return billing number |

### Method-level overrides

| Option | Overrides |
|---|---|
| `dhl_parcel_de_label_type` | `LabelType` (PDF/ZPL variant) — wins over connection `label_type` |
| `dhl_parcel_de_cost_center` | `costCenter` — wins over connection `cost_center` |
| `dhl_parcel_de_profile` | `profile` — wins over connection `profile` |
| `dhl_parcel_de_reference` | `refNo` — wins over `payload.reference` |
| `dhl_parcel_de_shipper_ref` | `shipper.shipperRef` — GKP shipper reference (predefined sender data + company logo) |
| `dhl_parcel_de_service_billing_id` | selects billing row by id (auto-set, non-configurable) |

## Connection config

`ConnectionConfig` (`units.py`), stored on `Settings.config`:

| Key | Purpose |
|---|---|
| `label_type` | default `LabelType` (PDF/ZPL × A4 / 910-300-* layouts) |
| `language` | `de`/`en`, default `en` — drives `Accept-Language` & tracking URL |
| `default_billing_number` | fallback billing number |
| `service_billing_numbers` | `List[ServiceBillingNumberType]` (service→billing_number, optional id/name) |
| `pickup_billing_number` | billing number for pickups |
| `return_billing_number` | billing number for returns |
| `profile` | DHL Gruppenprofil (default `STANDARD_GRUPPENPROFIL`) |
| `cost_center` | cost-center code |
| `creation_software` | `creationSoftware` marker |
| `cod_account_reference` / `cod_bank_account_holder` / `cod_bank_name` / `cod_bank_iban` / `cod_bank_bic` | CoD bank details |
| `shipping_options` / `shipping_services` | method allowlists |

`LabelType` is a 2-tuple enum `(docFormat, printFormat)` — e.g.
`PDF_A4 = ("PDF","A4")`, `ZPL2_910_300_700 = ("ZPL2","910-300-700")`.
Unified `PDF`/`ZPL`/`PNG` map onto `PDF_A4`/`ZPL2_A4`/`PDF_A4`.

## Billing-number resolution

`Settings.get_billing_number(service_code, billing_id)` — DHL bills per
service via an "Abrechnungsnummer". Lookup order:

1. **`billing_id`** — exact match on the configured row `id` (used when
   multiple rows share one service_code; set automatically from the
   `dhl_parcel_de_service_billing_id` option).
2. **`service_code`** — first exact match on row `service`.
3. **`config.default_billing_number`**.
4. **Test default** (test mode only) — `DEFAULT_TEST_BILLING_NUMBERS`
   per service, else `DEFAULT_TEST_BILLING_NUMBER = "33333333330102"`.

`get_return_billing_number(service_code_override)`:
override→lookup, else `return_billing_number` config, else test default
`33333333330701`.

The resolved billing number is threaded into the response `meta` via
the `_meta` ctx (see [Endpoints](#endpoints)).

## Options defaulting & droppoint resolution

This connector is the reference implementation of
`shipping_options_initializer`. It is wired into both
`lib.to_shipping_options(...)` and `lib.to_packages(...)` so per-shipment
and per-package options share one defaulting path. It does three things:

1. **Merges package options** into the shipment options dict.
2. **Migrates legacy tier booleans** (`dhl_parcel_de_premium` /
   `dhl_parcel_de_economy`) onto the `dhl_parcel_de_delivery_tier`
   enum.
3. **Resolves DHL droppoint identifiers** from the recipient address
   (SHIP2-1135) into a **new** dict — `ShipmentRequest.options`
   defaults to a shared class-level `{}`, so it must never be mutated
   in place.

It also normalises the `dhlRetoure` key: the OptionEnum wire code
`"dhlRetoure"` does not match the enum member name
`dhl_parcel_de_dhl_retoure`, so the initializer maps the key and
converts a raw dict to a typed `DhlRetoureType`.

### Droppoint detection → consignee `oneOf`

DHL's `Consignee` schema is a `oneOf`: **Locker** (Packstation),
**PostOffice** (Postfiliale / Filiale / Paketshop), **POBox**
(Postfach), or a regular contact address. Sending droppoint
identifiers on a contact-address shape is rejected. The shipment
request (`shipment/create.py`) builds the correct variant inline from
the option state:

```
recipient.street_name (or address_line1), anchored at start
  ├─ /^pack[\s-]?station\b/      → kind=locker     → lockerID
  ├─ /^(post[\s-]?filiale|        → kind=post_office → retailID
  │     filiale|paket[\s-]?shop)\b/
  ├─ /^post[\s-]?fach\b/         → kind=po_box     → poBoxID
  └─ else                        → contact address

street_number → parsed (lib.to_int, failsafe) → the droppoint ID
address_line2 matching /^\d{6,10}$/ → postNumber (Postnummer)
```

Explicit options always win; the resolver only fills gaps. JTL Wawi
sends split addresses (`street_name="Packstation"`,
`street_number="105"`) but the single-field form
(`address_line1="Packstation 105"`) also works because
`lib.to_address` splits a trailing digit token. Wire-shape quirks:
the **Locker** variant uses `name` + `lockerID` + `postNumber`; the
**PostOffice** variant accepts `postNumber` **OR** `email` to address
the Postfiliale; the **POBox** variant uses `name1` (not `name`).

## Data mapping

### Address (shipper) — karrio `Address` → `ShipperType`

```
karrio Address                  DHL ShipperType
─────────────────               ───────────────
company_name      ───►          name1 (or person_name if no company)
person_name       ───►          name2 (when name1 is the company)
                                name3 = None
street_name       ───►          addressStreet  (falls back to address_line1
                                                 when no street_number)
street_number     ───►          addressHouse   (falls back to address_line2)
postal_code       ───►          postalCode (max 10)
city              ───►          city (max 40)
country_code      ───►          country (ISO-3 via CountryCode.value_or_key)
person_name       ───►          contactName (max 80)
email             ───►          email (max 80)
```

DHL's `shipper` is a `oneOf` Shipper / ShipperReference. When the
`dhl_parcel_de_shipper_ref` option is set we send the ShipperReference variant
on its own — `{"shipperRef": "..."}` *instead of* the address (GKP holds the
sender data and prints the configured company logo). Sending both would match
both branches of the `oneOf` and can be rejected.

`consignee` is built by `build_consignee` (above). The contact-address
variant adds `state`, `contactName`, `phone`, and a redundant `name`
field alongside `name1`/`name2`.

### Parcel / details — `Package` → `DetailsType`

```
package.height/length/width.CM  ───► dim{uom:"cm", height, length, width}
                                       (omitted unless all three present)
package.weight.KG               ───► weight{uom:"kg", value}
```

`country` everywhere uses **ISO-3166 alpha-3** via
`units.CountryCode.map(...).value_or_key`.

### Customs — `CustomsInfo` → `CustomsType` (international only)

Emitted only when `payload.customs` is present **and** shipper country
≠ recipient country.

```
karrio CustomsInfo              DHL CustomsType
──────────────────              ───────────────
invoice                ───►     invoiceNo (max 35)
content_type           ───►     exportType (CustomsContentType, default COMMERCIAL_GOODS)
content_description    ───►     exportDescription (parcel.description / "Other", max 80)
incoterm               ───►     shippingConditions (Incoterm enum, default DDP)
duty.currency / EUR    ───►     postalCharges{currency,value}
shipper.country        ───►     officeOfOrigin
options shipper/consignee ref ► shipperCustomsRef / consigneeCustomsRef
options permit/attest/MRN/EEN ► permitNo / attestationNo / MRN / hasElectronicExportNotification
commodities[i]         ───►     items[i]{
   description/title              itemDescription (max 256)
   origin_country         ───►    countryOfOrigin (ISO-3)
   hs_code                ───►    hsCode
   quantity               ───►    packagedQuantity
   value_amount/currency  ───►    itemValue{currency, value (default 0.0)}
   weight                 ───►    itemWeight{uom:"kg", value}
}
```

`CustomsContentType`: `gift→PRESENT`, `documents→DOCUMENT`,
`sample→COMMERCIAL_SAMPLE`, `merchandise→COMMERCIAL_GOODS`,
`return_merchandise→RETURN_OF_GOODS`, plus literal
`OTHER`/`PRESENT`/`DOCUMENT`/`RETURN_OF_GOODS`/`COMMERCIAL_GOODS`/`COMMERCIAL_SAMPLE`.
`Incoterm`: `DDU`/`DAP`/`DDP`/`DDX`/`DXV`.

### Response — `items[i]` → `ShipmentDetails`

```
item.shipmentNo          ───► tracking_number + shipment_identifier
item.label.b64/.zpl2     ───► docs.label  (label_type ZPL if fileFormat==ZPL2 else PDF)
item.customsDoc.b64/.zpl2 ──► docs.invoice
item.returnLabel         ───► docs.extra_documents[return_label]
item.codLabel            ───► docs.extra_documents[cod_document]
item.returnShipmentNo    ───► return_shipment{tracking_number, tracking_url, meta}
item.shipmentRefNo       ───► meta.shipmentRefNo
```

`meta.carrier_tracking_link` = `tracking_url.format(tracking_number)`,
pointing at `https://www.dhl.com/<locale>/home/tracking/tracking-parcel.html`.

### Return shipment — `ShipmentRequest` → `ReturnOrderType`

POSTs to the dedicated returns API. `receiverId` from
`dhl_parcel_de_return_receiver_id` else the shipper country as ISO-3
lowercase. `customsDetails` only when `customs` present with
commodities. Query `labelType` = `BOTH` (no `payload.label_type`) or
`SHIPMENT_LABEL`. Response → `ShipmentDetails` with `qrLabel` surfaced
as `qr_label` extra document and `internationalShipmentNo` /
`routingCode` / `qrLink` in meta.

### Pickup — `PickupRequest` → `PickupRequestType`

**One-time pickups only** — any other `pickup_type` raises a
`FieldError`. Pickup-specific options are an inline enum
(`billing_number`, `dhl_parcel_de_pickup_location_type`,
`dhl_parcel_de_as_id`, `dhl_parcel_de_transportation_type`,
`dhl_parcel_de_shipment_size`, `dhl_parcel_de_send_confirmation_email`,
`dhl_parcel_de_send_time_window_email`, `dhl_parcel_de_pickup_date_type`).
Defaults: `pickupDateType` = `ASAP` (or `Date` if `pickup_date` set),
location `type` = `Address`, `transportationType` = `PAKET`,
`totalWeight` in grams. Response → `PickupDetails` with `orderID` as
`confirmation_number`.

## Carrier-specific invariants & gotchas

- **CoD on first parcel only.** `cashOnDelivery` is emitted only when
  `package_index == 0`. For multi-package shipments the CoD amount is
  collected from the first parcel; the rest are delivered without CoD.
- **Customs gated on `is_intl`.** The `customs` block is only built when
  shipper and recipient countries differ — even if a `customs` payload
  is supplied for a domestic shipment it is dropped.
- **`profile` defaults to `STANDARD_GRUPPENPROFIL`** on create and
  cancel when neither option nor connection config provides one.
- **Multi-piece via `shipments[]`.** One `ShipmentType` per parcel in a
  single request; `combine=false`. The parser aggregates with
  `lib.to_multi_piece_shipment`, keyed by 1-based parcel index.
- **Shared-options mutation hazard.** `ShipmentRequest.options`
  defaults to a class-level `{}`. The droppoint resolver builds a new
  dict rather than mutating it, and reads `dhlRetoure` with `.get()`
  (not `.pop()`) because `to_packages` reuses the same dict for
  per-package options.
- **Country codes are ISO-3.** Every `country` field uses
  `CountryCode.value_or_key` (alpha-3), unlike the alpha-2 convention
  many connectors use.
- **Tracking sandbox creds are hardcoded** (`zt12345`/`geheim`) per DHL
  docs; prod uses the connection username/password as the XML creds.
- **Warenpost alias.** `dhl_parcel_de_warenpost` resolves to
  `V62KP` (Kleinpaket) — Warenpost was retired in 2025.
- **`returns_request.py`/`returns_response.py` are kept by hand-curated
  exclusion** in the `generate` script, so a blind regen of the other
  modules won't wipe them.
- **Token refresh buffer is 60 min** specifically so a slow flow
  (queued rate fetch + label create) never runs on a near-expiry token.

## Tracking

XML API. The request element is `<data>` carrying `appname`,
`password`, `request="d-get-piece-detail"`, `language-code="en"`, and a
`;`-joined `piece-code` of up to **20** tracking numbers; batches run
asynchronously (one GET per batch). Responses are parsed with
`lib.find_element` walking nested `<data name="…">` elements:
`piece-shipment` → `piece-event-list` → `piece-event`. Events are
reversed to chronological order.

`TrackingStatus` maps **both** DHL ICE codes (response `ice` attr) and
TTPRO `standard-event-code`s — ICE takes priority per event, TTPRO is
the fallback. The `delivery-event-flag == "1"` short-circuits to
`delivered`. Status mapping:

| karrio status | codes (ICE + TTPRO) |
|---|---|
| `pending` | `va`, `parcv` |
| `picked_up` | `ae`, `es` |
| `in_transit` | `transit`, `srted`, `ulfmv`, `ldtmv`, `pckdu`, `shrcu`, `aa`, `ee`, `nb` |
| `out_for_delivery` | `po` |
| `delivered` | `delivered`, `dlvrd`, `zu` |
| `delivery_failed` | `failure`, `ndelv`, `bv`, `zn`, `an` |
| `delivery_delayed` | `unknown` |
| `on_hold` | `zo` (customs clearance) |
| `ready_for_pickup` | `la`, `zf` |

`DD` / `GT` (data service / money transfer) are intentionally
unmapped. `TrackingIncidentReason` maps the `ric` attribute to
normalized carrier/consignee/customs/weather/delivery incident reasons
(reference: `vendors/parcel_de_ice_event_ric_combinations_July_2024.csv`).

**Skeletal events are dropped.** DHL occasionally returns a
`piece-event` carrying only an `event-timestamp` and none of
`event-status` / `event-text` / `event-short-status` /
`standard-event-code` / `ice`. If emitted, such an event renders with
empty `description` / `code` / `location` that `lib.to_dict()` strips on
save, surfacing on the tracker as a junk all-null event (only `date` /
`time` populated — e.g. `{description: null, code: null, location: null,
date: "2026-06-17", time: "19:13 PM"}`, seen in prod on
`00340434525181200082`). `_extract_tracking` therefore requires at least
one of those content fields before emitting an event; a bare
`event-timestamp` is not enough.

> Note: the `time` value (`"19:13 PM"`, 24-hour hour + `PM`) is a
> separate, lib-wide artefact of `lib.flocaltime`'s default
> `output_format="%H:%M %p"`, not specific to this connector.

## Error parsing

JSON errors (`error.parse_error_response`) come in two shapes that are
both collected:

1. **Top-level status** — `status.title != "ok"` → `{detail/title,
   status/statusCode, instance}`.
2. **Per-item validation** — `items[].validationMessages[]` with
   `validationState` of `error`/`warning` → `{validationMessageCode,
   property, validationMessage, shipmentNo}`.

```
Response                       ┌──────────────────────────────┐
   │                           │ error.parse_error_response    │
   ├─► status.title != "ok"? ─►│   - top-level → Message       │
   │                           │   - items[].validationMessages│
   ├─► validationState         │     (error/warning) → Message │
   │     error/warning? ──────►│                               │
   ▼                           └──────────────┬───────────────┘
                                              ▼
                                         list[Message]
```

Tracking errors (`parse_tracking_error_response`) read the XML
`code` / `error-status` attributes; `code != "0"` maps through
`TRACKING_ERROR_CODES` (`5` login failed, `6` too many invalid logins,
`41` invalid TN format, `45` no TN supplied, `62` authorization error,
`100` no data found, `200` no electronic shipment data) and an
`error-status != "0"` produces a per-piece error keyed by the
searched piece code.

## References

- **Vendor specs** (`vendors/`):
  - `parcel-de-shipping-v2_2.yaml` — Shipping v2 OpenAPI (orders)
  - `pp-parcel-returns.yaml` — Returns OpenAPI
  - `parcel-de-pickup-v3.yaml` — Pickup v3 OpenAPI
  - `Shipment Tracking_2_0.yaml` — Tracking spec
  - `parcel_de_ice_event_ric_combinations_July_2024.csv` — ICE/RIC/event-code ground truth
  - `*_onboarding_collection*.json` — Postman onboarding collections
  - `Verfügbare Services_en_0.png`, `Abrechnungsnummern_en_1.png` — service / billing screenshots
- **DHL developer portal** —
  <https://developer.dhl.com/api-reference/parcel-de-shipping-post-parcel-germany-v2>
  (source of the sandbox billing-number defaults).
- **Generated schemas** — `karrio/schemas/dhl_parcel_de/*.py` are
  generated from `schemas/*.json` (kcli) and `schemas/*.xsd`
  (generateDS for the two tracking modules). Regenerate with
  `./bin/run-generate-on modules/connectors/dhl_parcel_de` — never
  hand-edit. The `generate` script preserves `returns_request.py` /
  `returns_response.py` via a `find … ! -name` exclusion.
```
