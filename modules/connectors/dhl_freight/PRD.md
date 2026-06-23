# PRD — DHL Freight (Palletized Road Freight) Karrio Integration

| Field          | Value                                                  |
|----------------|--------------------------------------------------------|
| Owner          | Daniel K (dan@karrio.io)                               |
| Status         | Implemented — booking + tracking live-validated; Print API deferred |
| Branch         | `feat/dhl-freight-integration`                         |
| Related        | DHL Developer Portal — Shipment Booking DHL Freight    |
| Vendor docs    | `vendors/DHL_Freight_APIs_Product_Manual_2026_R03.pdf` |
| Sandbox sample | `vendors/DHL_Freight_Shipment_Booking_SANDBOX_2026_R03.postman_collection.json` |
| Sprint         | 2026/R03 (May 2026)                                    |
| Reference      | `SPECS.md` (technical reference — wire shapes, gotchas) |

> **Status note.** Auth, shipment booking, and tracking are implemented and
> **live-validated against the DHL sandbox** (see §11). The booking payload
> passes all DHL structural/field validation; a full green booking + the
> Print API (labels) are blocked only on a sandbox account provisioned as a
> valid Consignor (the supplied number is a billing/payer account) and the
> unpublished Print request schema — see §6.3 and §11.

## 1. Executive Summary

Integrate DHL Freight — DHL's **palletized road-freight (LTL / groupage / FTL)
European network** — as a first-class karrio carrier. The integration sits
alongside DHL Express (parcel/air) and DHL Parcel DE (domestic parcel) and is
NOT a derivative of either: the booking model, the units of cargo (pieces /
pallets / loading meters), the party model (four roles), and the document
delivery model (separate Print API) are materially different.

Key architecture decisions:

- **Implemented: Shipment Booking + Tracking + (rate-sheet) Rating + opt-in
  Print follow-up.** Booking is
  `POST /freight/shipping/orders/v1/sendtransportinstruction`. Tracking is the
  DHL Group Unified Tracking API (UTAPI). Rating is rate-sheet-only (the live
  **Price Quote API** is confirmed but needs an eID — §6.5). Labels come from
  the **Print (Labelling) API** chained after booking — opt-in & fail-open
  because its request schema is unpublished (§6.3).
- **Auth: OAuth2 `client_credentials`** against `api(-sandbox).dhl.com/auth/v1/token`.
  Credentials are **base64'd into a `Authorization: Basic …` header** (NOT
  the request body — DHL rejects body credentials with 401), with
  `grant_type`/`response_type` as query string and an empty length-bearing
  POST body. Token cached via `connection_cache.thread_safe`. Proxy follows
  the **FedEx pattern**: all token logic lives in `authenticate()`; per-op
  methods call `self.authenticate(...)` and pass `Bearer <token>` directly.
  Tracking instead uses a `DHL-API-Key` header (the UTAPI convention). All
  three confirmed live against the sandbox (§11).
- **No karrio-core forking.** Freight-specific concepts that don't fit the
  Parcel model (loading meters, pallet places, ADR per piece, payerCode
  incoterms, party account ids) ride on existing extension points
  (`parcel.options`, `payload.options`, `customs`, connection settings).
  Where a concept genuinely has no home — flagged in §6 — we open a separate
  PR against karrio core.

## 2. Why DHL Freight is structurally different from parcel carriers

```
                ┌──────────────────────────────────────────────────────┐
                │             "parcel-shaped" carriers                  │
                │   (dhl_parcel_de, dhl_express, ups, fedex, dpd, …)    │
                ├──────────────────────────────────────────────────────┤
                │  shipper + recipient                                  │
                │  parcels: weight + dims                               │
                │  → label PDF/ZPL returned by ship() call              │
                │  → tracking via shipmentNo                            │
                └──────────────────────────────────────────────────────┘
                                       ┊
                              very different shape
                                       ┊
                ┌──────────────────────────────────────────────────────┐
                │                  DHL Freight (LTL)                    │
                ├──────────────────────────────────────────────────────┤
                │  parties[]:  (Consignor + Consignee mandatory;        │
                │              Pickup/Delivery optional — only when     │
                │              divergent, so this iteration sends the    │
                │              two mandatory roles only — §6.2)          │
                │    • Consignor  (legal sender; Id = DHL account, REQ)  │
                │    • Consignee  (legal receiver; Id optional)         │
                │    • Pickup     (physical loading site — omitted)      │
                │    • Delivery   (physical unloading site — omitted)    │
                │                                                       │
                │  pieces[]:                                            │
                │    • packageType (PAL/BOX/CRT/DRM…)                   │
                │    • palletPlaces, loadingMeters, stackable           │
                │    • SSCC / ANSIFACT barcode ids                      │
                │    • per-piece dangerousGoods (ADR class, UN no.,     │
                │      packageGroup, tunnelCode, flashpoint, …)         │
                │                                                       │
                │  additionalServices[]:  (booking-level accessorials)  │
                │    • tail-lift loading/unloading                      │
                │    • side loading/unloading                           │
                │    • temperature-controlled (chilled/frozen/custom)   │
                │    • time-slot booking pickup AND delivery            │
                │    • after-12 delivery, pre-advice                    │
                │    • cash on delivery, insurance (cargo)              │
                │                                                       │
                │  payerCode { code: DAP/DDP/…, location }              │
                │      ↑ incoterms 2020 — payment side of the carriage  │
                │                                                       │
                │  additionalInformation[]:                             │
                │    • country-specific tax refs (RO UIT, HU EKAER,     │
                │      PL SENT)                                         │
                │                                                       │
                │  Response:  shipmentId + per-piece license plates     │
                │             (NO label payload — labels come from the  │
                │              separate Freight Print API)              │
                └──────────────────────────────────────────────────────┘
```

## 3. Existing code analysis

What we reused vs. what we wrote new:

| Concern                  | Reused                                          | New                                                 |
|--------------------------|-------------------------------------------------|-----------------------------------------------------|
| Plugin metadata          | `metadata.PluginMetadata` (same as dhl_parcel_de) | `karrio/plugins/dhl_freight/__init__.py`            |
| Settings + sys-config    | `core.Settings`, `connection_system_config`, fallback chain copied from `dhl_parcel_de` | `DHL_FREIGHT_*` env keys + `account_number` |
| Token / auth             | `connection_cache.thread_safe` token cache; **FedEx proxy pattern** (token logic in `authenticate()`, `Bearer` passed directly) | `client_credentials` via **Basic Auth header** (vs. ROPC body) |
| Rating                   | `karrio.universal.providers.rating` (CSV zone/weight rate sheet) | `services.csv` for ECI/ECX/ECP/DOM/FTL |
| Tracking                 | **UTAPI shape from `dhl_universal`** (`/track/shipments`, `DHL-API-Key`) | `tracking.py`, `tracking_response.json`, `service=freight` |
| Error parsing            | `dhl_parcel_de/error.py` shape | booking `validationErrors[]` + RFC-7807 `problem+json` + OAuth2 token errors (3 shapes) |
| Request construction     | **UPS inline-DTO style** (`ups/shipment/create.py`) — one `ShippingRequestType(...)` literal, comprehensions for parties/pieces | no per-section helper functions |
| Option enum patterns     | `lib.OptionEnum(...).meta` categories (`DELIVERY_OPTIONS`, `LOADING`, `INSURANCE`, `COD`, `INVOICE`) | `LOADING`, `TEMPERATURE`, `HAZARDOUS` categories |
| Service enum             | `lib.Enum` with carrier code as value, karrio code as name | 5 product codes (ECI/ECX/ECP/DOM/FTL)               |
| Tests                    | `unittest`-based 4-method pattern (dhl_parcel_de) | 56 tests: booking, auth, units, error, rate, tracking |
| Schemas pipeline         | `generate` script + `bin/cli codegen generate` (offline — no server) | example-payload JSON (DHL ships no OpenAPI) |

## 4. Architecture diagram (this connector)

```
                        karrio shipment / tracking flow
                                │
                                ▼
┌────────────────────────────────────────────────────────────┐
│ karrio.mappers.dhl_freight.Mapper                          │
│   create_shipment_request(payload)  → Serializable         │
│   create_rate_request(payload)      → universal.rate_request│
│   create_tracking_request(payload)  → tracking_request      │
└────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────┐
│ karrio.providers.dhl_freight.shipment.create               │
│   shipment_request(): ONE inline ShippingRequestType(...)  │
│     (UPS-style — no per-section helpers)                   │
│   • lib.to_packages(...)        (weight, dims)            │
│   • pieces=[PieceType(...) …]   (pallets/LDM/ADR from      │
│                                  parcel.options)           │
│   • additionalServices=…        (loading, temp, COD, …)    │
│   • parties=[Consignor, Consignee]  (2 mandatory roles;    │
│       Consignor.id = DHL account; vat NOT sent — typed)    │
│   • references=[CNR/CNZ/ORD/SHP]                           │
│   • payerCode=…                 (DAP default)              │
│   • additionalInformation=[UIT/EKAER/SENT]                 │
└────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────┐
│ karrio.mappers.dhl_freight.Proxy  (interface methods only) │
│   authenticate()    → OAuth2 client_credentials (Basic     │
│                        Auth header, cached); FedEx pattern  │
│   create_shipment() → POST …/sendtransportinstruction      │
│                        Bearer + Accept-Language             │
│   get_tracking()    → GET {utapi}/shipments?…&service=…    │
│                        DHL-API-Key header (no Bearer)       │
│   get_rates()       → universal rate-sheet (no HTTP)        │
└────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┴────────────────┐
                ▼                                ▼
       DHL Freight Booking API           DHL Group UTAPI
       {shipmentId, licensePlates[]}     {shipments[]}
                │                                │
                ▼                                ▼
┌────────────────────────────────┐  ┌──────────────────────────────┐
│ parse_shipment_response        │  │ parse_tracking_response       │
│   tracking_number = shipmentId │  │   status ← UTAPI statusCode   │
│   docs.label = ""  (Print API) │  │   events[], estimated_delivery │
│   meta.license_plates = SSCCs  │  │   meta.license_plates=pieceIds │
└────────────────────────────────┘  └──────────────────────────────┘
```

## 5. Service / option catalog

### 5.1 ShippingService → ``productCode``

| karrio service code               | DHL code | Description                                  |
|-----------------------------------|----------|----------------------------------------------|
| `dhl_freight_eurapid`             | `ECI`    | International express groupage (premium LTL) |
| `dhl_freight_euroconnect`         | `ECX`    | Standard European groupage                   |
| `dhl_freight_euroconnect_plus`    | `ECP`    | Premium scheduled groupage                   |
| `dhl_freight_domestic`            | `DOM`    | Domestic national groupage                   |
| `dhl_freight_ftl`                 | `FTL`    | Full-truck-load / part-load (per quotation)  |

### 5.2 ShippingOption coverage (booking-time accessorials)

| Karrio option                                  | DHL field                  | Category        |
|------------------------------------------------|----------------------------|-----------------|
| `dhl_freight_after_12_delivery`                | `after12Delivery`          | DELIVERY_OPTIONS|
| `dhl_freight_available_pickup_time`            | `availablePickupTime`      | DELIVERY_OPTIONS|
| `dhl_freight_available_delivery_time`          | `availableDeliveryTime`    | DELIVERY_OPTIONS|
| `dhl_freight_pre_advice`                       | `preAdvice`                | DELIVERY_OPTIONS|
| `dhl_freight_time_slot_booking_pickup`         | `timeSlotBookingPickup`    | DELIVERY_OPTIONS|
| `dhl_freight_time_slot_booking_delivery`       | `timeSlotBookingDelivery`  | DELIVERY_OPTIONS|
| `dhl_freight_tail_lift_loading` / `_unloading` | `tailLift…`                | LOADING         |
| `dhl_freight_side_loading_pickup` / `_unloading_delivery` | `side…`         | LOADING         |
| `dhl_freight_drop_off_by_consignor`            | `dropOffByConsignor`       | LOADING         |
| `dhl_freight_temperature_controlled`           | `temperatureControlled`    | TEMPERATURE     |
| `dhl_freight_dangerous_goods`                  | `dangerousGoods`           | HAZARDOUS       |
| `dhl_freight_insurance`                        | `insurance{value,currency}`| INSURANCE       |
| `dhl_freight_cash_on_delivery`                 | `cashOnDelivery{amount,currency}` | COD      |
| `dhl_freight_payer_code`                       | `payerCode.code` (DAP/DDP/CPT/CIP/DPU) | INVOICE |
| `dhl_freight_payer_code_location`              | `payerCode.location`       | INVOICE         |
| `dhl_freight_consignor_account`                | `parties[Consignor].id` (overrides connection `account_number`) | SHIPMENT |
| `dhl_freight_consignee_account`                | `parties[Consignee].id`    | SHIPMENT        |
| `dhl_freight_consignor_reference`              | `references[CNR]`          | SHIPMENT        |
| `dhl_freight_consignee_reference`              | `references[CNZ]`          | SHIPMENT        |
| `dhl_freight_order_reference`                  | `references[ORD]`          | SHIPMENT        |
| `dhl_freight_pickup_instruction`               | `pickupInstruction`        | INSTRUCTIONS    |
| `dhl_freight_delivery_instruction`             | `deliveryInstruction`      | INSTRUCTIONS    |
| `dhl_freight_uit_number`                       | `additionalInformation[UIT_NUMBER]` (RO) | INVOICE |
| `dhl_freight_ekaer_number`                     | `additionalInformation[EKAER_NUMBER]` (HU) | INVOICE |
| `dhl_freight_sent_number`                      | `additionalInformation[SENT_NUMBER]` (PL) | INVOICE |

**`customs.options`** (preferred for the customs-scoped concepts — `CustomsOption`
enum): `dhl_freight_payer_code`, `dhl_freight_uit_number`,
`dhl_freight_ekaer_number`, `dhl_freight_sent_number`. These take precedence
over the same-named `ShippingOption` fallbacks; `customs.incoterm` feeds
`payerCode.code` (§6.6/§6.7).

**Connection config** (carrier-level): `account_number`,
`consignee_account_number`, `default_payer_code` / `default_payer_location`,
`language`, `cost_center`, and the Print follow-up gate `auto_print_documents`
(bool) + `print_document_type` (`label`/`shipmentList`/`waybill`) — §6.3.

## 6. Freight-specific concerns that may need karrio-core adjustments

These are NOT blocked on this iteration — they ride on options / meta — but
they are tech debt and we want to discuss them upstream.

### 6.1 🔴 Pallet places & loading meters are first-class freight units, not parcel attributes

`models.Parcel` exposes `weight`, `length`, `width`, `height`, `packaging_type`.
LTL pricing is driven by **chargeable units** that combine weight, volume,
**pallet places**, and **loading meters (LDM)** — none of which Parcel exposes.

| Field           | Where it lives today                           | Why it should be promoted |
|-----------------|------------------------------------------------|---------------------------|
| `palletPlaces`  | `parcel.options["palletPlaces"]`               | Rate calculation requires it for any LTL/groupage rate-sheet model. |
| `loadingMeters` | `parcel.options["loadingMeters"]`              | Same as above; truck-occupation pricing. |
| `stackable`     | `parcel.options["stackable"]`                  | Truck-stacking rules also depend on this. |
| SSCC/ANSIFACT id| `parcel.options["sscc"]` (added later)         | Per-piece tracking ids in LTL flows.     |

**This iteration (chosen approach — options):** these ride on
`parcel.options` (`palletPlaces`, `loadingMeters`, `stackable`,
`numberOfPieces`, `marksAndNumbers`) and are summed into the booking header.
This is the durable approach for now — no core change required.

**Future proposal (optional):** a `FreightUnits` mixin (`@attr.s`) on
`karrio.core.models` with `pallet_places`/`loading_meters`/`stackable` under
`Parcel.freight` would make them first-class for parcel-aware UIs. Deferred —
not blocking.

### 6.2 ✅ Party model & account ids — billing_address + 4-role mapping

DHL Freight has four party roles — Consignor / Consignee (legal) and
Pickup / Delivery (physical); the **Product Manual marks only Consignor and
Consignee as mandatory**, Pickup/Delivery only when they deviate.

**This iteration (implemented):** maps karrio's existing fields:

| DHL party | karrio source | When sent |
|---|---|---|
| Consignor | `billing_address` if present, else `shipper` | always |
| Consignee | `recipient` | always |
| Pickup    | `shipper` | only when its location ≠ Consignor's (i.e. `billing_address` diverges) |
| Delivery  | `recipient` | only when its location ≠ Consignee's (never, today) |

So a shipment with a distinct `billing_address` sends Consignor (billing) +
Pickup (shipper) + Consignee; otherwise just Consignor + Consignee. Divergence
is keyed on `(country, postal_code, city)`.

`Parties[Consignor].Id` (the DHL Freight **account number**) is **mandatory**
(live: `22001` when absent, `22014` for an unprovisioned number). It resolves
from the `dhl_freight_consignor_account` option → connection `account_number`
setting → `DHL_FREIGHT[_SANDBOX]_ACCOUNT_NUMBER` system config. The Consignee
`id` is optional and resolves from the `dhl_freight_consignee_account` option →
the new connection `consignee_account_number` setting.

The `vat` field is **not sent**: it is a strongly-typed DHL `PartyVAT` field
that rejects a plain tax id on deserialization (live: *"Error converting
value … to type DHL.ShipmentModels.PartyVAT"*); the tax id goes only in
`vatEoriSocialSecurityNumber`.

**Future proposal:** optional `physical_pickup`/`physical_delivery` fields on
`ShipmentRequest` would make fully-divergent Pickup/Delivery first-class
(today only `billing_address`-vs-`shipper` divergence is expressible).

### 6.3 🟡 No label payload from `ship()`

karrio's `ShipmentDetails` contract assumes `docs.label` is populated. DHL
Freight's booking call returns NO label — labels and the road consignment note
(BoL) come from the separate **DHL Freight Print API** in a follow-up call,
keyed on the returned `shipmentId` + `licensePlates[]`.

**This iteration (implemented — opt-in, fail-open):** the connector chains
booking → Print inside `proxy.create_shipment`
(`POST /freight/shipping/labels/v1/print/printdocumentsbyid` with the returned
shipment id → Base64 PDF → `docs.label`), modelled on the **sendle** two-call
label pattern. Because DHL publishes **no request schema** for the Print API
(not in the manual, no Postman, no OpenAPI) and it can't be live-validated
without a bookable account, it is:

- **Opt-in** — off unless the connection config `auto_print_documents = true`
  (with `print_document_type` ∈ `label`/`shipmentList`/`waybill`).
- **Fail-open** — wrapped in `lib.failsafe`; any print error is swallowed so
  the booking still returns success with an empty label.
- **Defensive parse** — the base64 is read from the common response keys
  (`documents[0].content` / `content` / `base64`).

When the Labelling API request schema (Postman/OpenAPI) or a bookable sandbox
account is available, validate the request/response shape and flip the default.
`meta.license_plates` carries the SSCCs regardless. See §11.

### 6.4 🟡 ADR (dangerous goods) is per-piece, not per-shipment

DHL Freight expects a full ADR record **per piece**: `dgmId`, `properShippingName`,
`adrClass`, `unNumber`, `flashpointValue`, `packageGroup`, `tunnelCode`,
`grossWeight`, `quantityMeasurement…`, etc. karrio's `Customs` model is
shipment-level and doesn't carry this detail.

**This iteration (implemented):** a piece's ADR record is sourced from
`parcel.options["dangerousGoods"]` **or**, when absent, the first parcel item
that carries it — `parcel.items[].metadata["dangerousGoods"]` (a
`commodity.metadata` dict matching the DHL `DangerousGoodsType` schema). The
top-level `additionalServices.dangerousGoods` is set `true` automatically when
any piece declares one. Validation deferred to DHL.

**Future proposal:** a typed `DangerousGoods` model in `karrio.core.models`
once a second carrier (e.g. `fedex_freight`) needs the same shape.

### 6.5 🟡 Live rating — Price Quote API confirmed (needs an eID)

**Confirmed in the Product Manual:** live rates are the **Price Quote API
(= Rating API)** at
`POST …/freight/info/pricequote/v1/pricequote/quoteforprice`. It returns the
freight amount split into base + additional services per the customer's
contract, with an optional own-surcharge markup.

**Why it's not wired yet (blocked on credentials, not effort):** the Price
Quote API requires, in addition to the OAuth `client_credentials`, an **eID
(separate username/password)** that DHL Freight Customer Service issues and
links to the account number(s) and products. We don't have an eID for the
sandbox app, and the request schema is unpublished — so it can't be
live-validated (same risk as the Print API). Auth itself is fine; only the
eID + schema are missing.

**This iteration:** `create_rate_request` uses
`karrio.universal.providers.rating` over `services.csv` (zone × weight band ×
service code); merchants upload their negotiated card via the rate-sheet UI.
Unblock live rates with an eID + the Price Quote request schema.

### 6.6 🟡 Country-specific tax references (RO/HU/PL)

EU member-state customs/tax systems require specific reference codes that
karrio's `Customs` model has no slot for:

| Country | Code in `additionalInformation` | Required for                                    |
|---------|---------------------------------|-------------------------------------------------|
| RO      | `UIT_NUMBER`                    | All road freight moving through Romania         |
| HU      | `EKAER_NUMBER`                  | Most road freight moving through Hungary        |
| PL      | `SENT_NUMBER`                   | Sensitive goods (fuel, alcohol, tobacco) in PL  |

**This iteration (implemented — customs.options):** these read from
**`customs.options`** via a dhl_freight `CustomsOption` enum
(`dhl_freight_uit_number` / `_ekaer_number` / `_sent_number`), falling back to
the same-named shipment-level `ShippingOption` for compatibility, then project
into `additionalInformation[]`. No core change needed.

### 6.7 ✅ Incoterms / payer code — customs.options + customs.incoterm

DHL Freight wants `payerCode: {code: DAP|DDP|CPT|CIP|DPU, location: …}` on
every booking.

**This iteration (implemented — customs.options):** `payerCode` is built from
two **flat string** options (not a dict). The `code` resolves in order —
`customs.options.dhl_freight_payer_code` → shipment-level
`dhl_freight_payer_code` option → **`customs.incoterm`** → connection
`default_payer_code` (default `DAP`). The `location` resolves the same way via
`dhl_freight_payer_code_location` → connection `default_payer_location`. So a
karrio request that sets `customs.incoterm="DDP"` books with
`payerCode.code="DDP"` automatically. A core `Customs.incoterm_location` would
let us drop the location option entirely — flagged but not blocking.

### 6.8 🟢 Rate-limit awareness

250 calls/day is **low** for a multi-tenant SaaS. We do not currently surface
rate-limit telemetry on the karrio connection model.

**Mitigation:** rely on Sentry to capture the 429 response from DHL. Long-term,
the `entitlements` module (see `modules/entitlements/`) is the natural place
to surface a daily quota counter and pre-warn before exhaustion.

## 7. Implementation plan

### Phase 1 — booking + auth + rating ✅ done (live-validated)

| Step | File(s)                                                              | Status |
|------|----------------------------------------------------------------------|--------|
| 1    | Vendor assets (Postman collection + Product Manual PDF) in `vendors/` | ✅ done |
| 2    | `pyproject.toml`, `MANIFEST.in`, `generate`, `README.md`, `PRD.md`, `SPECS.md` | ✅ done |
| 3    | `plugins/dhl_freight/__init__.py`, `mappers/dhl_freight/*` (FedEx-pattern proxy) | ✅ done |
| 4    | `providers/dhl_freight/{utils,units,error}.py`                        | ✅ done |
| 5    | `providers/dhl_freight/shipment/create.py` (inline DTO, UPS-style)    | ✅ done |
| 6    | `schemas/{shipping_request,shipping_response,error_response}.json` (example payloads) | ✅ done |
| 7    | `services.csv` with 5 product codes                                    | ✅ done |
| 8    | Tests + fixtures (booking, auth, units, error, rate)                   | ✅ done |
| 9    | Register in all requirements manifests + `bin/run-sdk-tests` + logos   | ✅ done |
| 10   | `./bin/run-generate-on modules/connectors/dhl_freight` (**offline — no server**) | ✅ done |
| 11   | Live sandbox validation of auth + booking (§11)                        | ✅ done |

### Phase 3 — Tracking API ✅ done (live-wired)

DHL Freight tracking is the **DHL Group Unified Tracking API (UTAPI)** —
`/track/shipments?trackingNumber=…&service=freight` with a `DHL-API-Key`
header (the same API `dhl_universal` uses). Implemented in
`providers/dhl_freight/tracking.py` + `mappers/.../proxy.py:get_tracking`
+ mapper wiring + `schemas/tracking_response.json` + 5 tests. UTAPI
statusCodes (`pre-transit`/`transit`/`delivered`/`failure`/`unknown`) map in
`TrackingStatus`. Live-wired (reaches UTAPI; returns 401 only because the
sandbox key isn't subscribed to the Tracking-Unified product). See
`SPECS.md` → Tracking.

### Phase 2 — Print API (labels + BoL) ✅ implemented (opt-in, fail-open)

Chained booking → Print in `proxy.create_shipment`
(`printdocumentsbyid`), gated by the `auto_print_documents` connection config
and wrapped in `lib.failsafe`. See §6.3. Flip the default + validate the
request/response once the Labelling API schema (or a bookable account) is
available.

### Phase 4 — Live Rates (Price Quote API) — confirmed, needs eID

The endpoint is `…/freight/info/pricequote/v1/pricequote/quoteforprice` (§6.5).
Blocked on an **eID** (separate user/pass from DHL Freight) + the unpublished
request schema. When available: new `providers/dhl_freight/rate.py` replacing
the universal rating, reusing the booking pieces/parties shape.

### Phase 5 — Core upstream (karrio repo)

| Step | Concern                                                              |
|------|----------------------------------------------------------------------|
| 1    | `Parcel.freight = FreightUnits(...)` mixin (§6.1)                    |
| 2    | `ShipmentRequest.physical_pickup` / `physical_delivery` (§6.2)       |
| 3    | Typed `DangerousGoods` model (§6.4)                                  |
| 4    | `Customs.incoterm_location` (§6.7)                                   |

## 8. Testing strategy

- **unittest** (no pytest, per testing.md). **56 tests** in
  `karrio/modules/connectors/dhl_freight/tests/dhl_freight/test_*.py`
  (`test_shipment`, `test_authentication`, `test_units`, `test_error`,
  `test_rate`, `test_tracking`). Fixture imports are **relative**
  (`from .fixture import …`) — absolute `tests.*` imports collide with the
  shared top-level `tests` package in CI discovery.
- 4-method pattern per feature: `test_create_<feature>_request` (payload →
  DHL shape, full `assertDictEqual`), `test_<feature>` (proxy URL/headers,
  mocked HTTP), `test_parse_<feature>_response`, `test_parse_error_response`.
- Error tests cover all three shapes: booking `validationErrors[]`,
  RFC-7807 `problem+json`, OAuth2 token errors.
- A regression guard (`test_create_shipment_request_builds_typed_dto`) fails
  if `schemas/*.json` ever drift back to JSON-Schema definitions.
- **Live sandbox validation** (§11) is the source of truth for the wire
  shape; fixtures mirror the Postman sample + the real sandbox responses.

## 9. Migration & rollback

No schema migrations. The carrier is opt-in: an org gains it by adding a
`dhl_freight` connection. Rollback = remove the line from `requirements.build.txt`
and the directory. No data migration needed.

## 10. Resolved decisions

| #  | Decision                                                                  | Choice                                                                  | Rationale                                                                                                            | Date       |
|----|---------------------------------------------------------------------------|-------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|------------|
| Q1 | New top-level connector vs. extending `dhl_express` / `dhl_parcel_de`     | New `dhl_freight` connector                                              | Auth flow, payload shape, units of cargo, and label model all differ from existing DHL connectors.                   | 2026-05-20 |
| Q2 | Use `client_credentials` or `password` grant for OAuth?                   | `client_credentials`                                                     | DHL Freight only documents `client_credentials`; `dhl_parcel_de`'s ROPC flow is for the DHL Business Portal.         | 2026-05-20 |
| Q3 | Live rates this iteration                                                 | No — universal CSV-driven rate sheet                                     | Rates are a separate API + per-customer tariff; out of scope to keep booking iteration small.                        | 2026-05-20 |
| Q4 | Where to put `palletPlaces` / `loadingMeters` until core lands a mixin    | `parcel.options[...]`                                                    | Backward-compatible passthrough; no core change blocks first delivery.                                               | 2026-05-20 |
| Q5 | Party model when only shipper/recipient on karrio request                 | Send Consignor + Consignee only (not 4 parties)                          | Product Manual: Pickup/Delivery optional (only when divergent); karrio has no divergent source. Revised after live testing (was: duplicate to 4). | 2026-06-09 |
| Q6 | Source of schema (no OpenAPI from DHL)                                    | Example-payload `schemas/*.json` from Postman sample + Product Manual     | DHL only publishes the Postman collection + PDF; codegen needs concrete payloads (not JSON-Schema). Offline — no server needed. | 2026-05-20 |
| Q7 | OAuth credential transport                                                | Basic Auth header (base64 client_id:secret), query-string grant, empty body | Live sandbox rejects body credentials (ROPC) with 401 and empty POST with 411. Confirmed 200 + Bearer token.        | 2026-06-09 |
| Q8 | `vat` field                                                              | Not sent; tax id → `vatEoriSocialSecurityNumber` only                     | DHL `vat` is a typed `PartyVAT`; a plain tax id fails deserialization live.                                          | 2026-06-09 |
| Q9 | Consignor account number (`Parties[Consignor].Id`)                       | Mandatory; `dhl_freight_consignor_account` option → `account_number` setting → system config | Live booking returns 22001/22014 without a valid Consignor account id.                              | 2026-06-09 |
| Q10| Proxy structure                                                          | FedEx pattern — token logic in `authenticate()`, interface methods only  | Matches the project's reference OAuth carrier; per-op methods pass `Bearer` directly.                                | 2026-06-09 |
| Q11| Request construction style                                               | One inline `ShippingRequestType(...)` literal, UPS-style (no `_helper`s) | Matches `ups/shipment/create.py`; reviewer preference.                                                               | 2026-06-09 |
| Q12| Tracking transport                                                       | DHL Group UTAPI (`/track/shipments`, `DHL-API-Key`, `service=freight`)   | Manual designates UTAPI for Freight tracking; reuse the proven `dhl_universal` shape.                               | 2026-06-09 |
| Q13| Print API                                                                | Implemented opt-in + fail-open (sendle-style chain)                       | No published schema; gate behind `auto_print_documents` and `lib.failsafe` so an unvalidated call can't break booking. | 2026-06-09 |
| Q14| Consignor source                                                         | `billing_address` if present, else `shipper`                             | Consignor is the freight-payer/legal sender; manual ties the account id to the payer party.                          | 2026-06-09 |
| Q15| Pickup/Delivery                                                          | Send Pickup=shipper / Delivery=recipient only when they diverge from the legal party | Manual: optional, only when different; avoids redundant duplicates.                                  | 2026-06-09 |
| Q16| RO/HU/PL tax refs + payerCode source                                     | `customs.options` (CustomsOption) with ShippingOption fallback           | These are customs-scoped; `customs.incoterm` feeds payerCode.code.                                                    | 2026-06-09 |
| Q17| ADR dangerous goods source                                               | `parcel.options` OR `parcel.items[].metadata["dangerousGoods"]`          | Lets merchants attach ADR to a commodity/item rather than a raw parcel option.                                       | 2026-06-09 |
| Q18| Consignee account                                                        | `dhl_freight_consignee_account` option + `consignee_account_number` setting | User request — both per-shipment and connection-default.                                                          | 2026-06-09 |
| Q19| Live Rates (Price Quote API)                                             | Confirmed endpoint; deferred (needs eID + schema)                        | Documented `/freight/info/pricequote/v1/...`; requires a DHL-issued eID we don't have.                              | 2026-06-09 |

## 11. Live sandbox validation

Validated end-to-end against `api-sandbox.dhl.com` with a real sandbox app
(cURL first, then the karrio SDK):

| Check | Result |
|-------|--------|
| **Auth** (`/auth/v1/token`) | ✅ HTTP 200 → `{access_token, token_type: Bearer, expires_in: 1799}`. Basic Auth header + query-string grant + empty body. |
| **Auth across services** | ✅ same token authorizes Booking, Products (`/info/products` → 200), and by extension Print / Additional Services (shared gateway). |
| **Booking** (`/sendtransportinstruction`) | ✅ payload passes all DHL structural / deserialization / field validation via the SDK. |
| **Tracking** (UTAPI `/track/shipments`) | ✅ SDK reaches UTAPI; parses the response/error cleanly. |
| **Error parsing** | ✅ real shapes surfaced: `validationErrors[]` (22001/22014), `PartyVAT` deserialization error, UTAPI 401. |

**Two external blockers** (not code):

1. **Consignor account** — the supplied `62085855350106` is a billing/payer
   number; DHL rejects it as a Consignor sender account (`22014`). A full
   green booking needs a sandbox account provisioned as a valid Consignor.
2. **Product subscriptions** — the sandbox app's key returns 401 on UTAPI
   tracking and (likely) the Print API until those products are added to the
   app on the DHL developer portal. Auth + booking validation are unaffected.
