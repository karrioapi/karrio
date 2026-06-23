# DHL Freight integration — specification

Reference for the DHL Freight (palletized road-freight, LTL / groupage /
FTL) connector. DHL Freight exposes a **JSON REST** Shipment Booking API
(`sendtransportinstruction`) behind the shared **DHL Authentication API**
(OAuth2 `client_credentials`). This iteration supports **rate quotes
(rate-sheet based) and shipment booking**. Labels/BoL (Print API),
live rates (Rates API), and tracking (Tracking API) are separate DHL
products and are out of scope here — see [PRD.md](./PRD.md) for the
phased plan and the karrio-core architecture flags.

The **vendor source of truth** lives under `vendors/`:
`DHL_Freight_Shipment_Booking_SANDBOX_2026_R03.postman_collection.json`
(the canonical request sample) and
`DHL_Freight_APIs_Product_Manual_2026_R03.pdf`. DHL does **not** publish
an OpenAPI/Swagger spec for this API; the example payloads under
`schemas/` are hand-derived from those two sources.

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Endpoints](#endpoints)
3. [Authentication](#authentication)
4. [Supported operations](#supported-operations)
5. [Services & catalog (rate-sheet)](#services--catalog-rate-sheet)
6. [Options](#options)
7. [Connection config](#connection-config)
8. [Data mapping](#data-mapping)
9. [Multi-piece handling](#multi-piece-handling)
10. [Wire-shape invariants & gotchas](#wire-shape-invariants--gotchas)
11. [Response & identifiers](#response--identifiers)
12. [Error parsing](#error-parsing)
13. [References](#references)

---

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio ShipmentRequest / RateRequest
│   (karrio core)         │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  providers/dhl_freight  │   Pure data transforms.
│   shipment/create.py    │   Unified model → typed DHL Freight request,
│   error.py              │   typed response → unified model. No HTTP.
│   units.py              │   ShippingService, ShippingOption,
│   utils.py              │   ConnectionConfig, PackagingType, Incoterm,
│                         │   PartyType, TrackingStatus, services.csv loader
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  mappers/dhl_freight/   │   HTTP transport only.
│   proxy.py              │   - OAuth2 client_credentials token (cached)
│   - get_rates           │   - Bearer auth on the booking call
│   - create_shipment     │   - Accept-Language on the booking call
│   - get_tracking        │   - UTAPI: DHL-API-Key header (no Bearer)
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  DHL Freight APIs       │
│  ─────────────────────  │
│  Auth API               │   /auth/v1/token  (client_credentials)
│  Shipment Booking API   │   /freight/shipping/orders/v1/
│   (api.dhl.com)         │     sendtransportinstruction
│  Rate sheet (local)     │   services.csv → universal rating provider
└─────────────────────────┘
```

**Key architectural choices:**

- **DHL Freight is its own connector**, not a variant of `dhl_express`
  (parcel/air) or `dhl_parcel_de` (domestic parcel). The booking model,
  cargo units (pieces / pallets / loading meters), party model (four
  roles), and label model (separate Print API) all differ — see PRD §2.
- **OAuth2 `client_credentials`** via the shared DHL Authentication API
  at `/auth/v1/token` — distinct from the ROPC password flow
  `dhl_parcel_de` uses. Token cached per
  `dhl_freight|<client_id>|<client_secret>`, refreshed 5 min before
  expiry (tokens live ~30 min).
- **Rating is rate-sheet only.** DHL Freight's live Rates API is a
  separate product; the booking call returns no price. The connector
  mixes in karrio's `universal.mappers.rating_proxy` /
  `universal.providers.rating` and projects the catalog from
  `services.csv` (`provider_units.DEFAULT_SERVICES`).
- **Booking returns no label.** The response is a shipment ID + per-piece
  SSCC "license plates"; labels/BoL come from the separate Print API.
  `docs.label` is `""` and the plates ride in `meta.license_plates`.
- **Typed DTOs.** `shipment/create.py` and `error.py` build the
  generated `karrio.schemas.dhl_freight` dataclasses
  (`ShippingRequestType`, `PieceType`, `PartyType`,
  `AdditionalServicesType`, `PayerCodeType`, `DangerousGoodsType`, …)
  rather than free-form dicts. Schemas are generated from `schemas/*.json`
  with `kcli ... --no-nice-property-names` (camelCase preserved). Don't
  hand-edit; regenerate with `./bin/run-generate-on
  modules/connectors/dhl_freight`.

## Endpoints

`{base}` resolves from `Settings.server_url`; `{auth}` from
`Settings.token_server_url`:

| Mode | Booking base | Auth base |
|---|---|---|
| Test (`test_mode=True`) | `https://api-sandbox.dhl.com/freight/shipping/orders/v1` | `https://api-sandbox.dhl.com/auth/v1/token` |
| Prod | `https://api.dhl.com/freight/shipping/orders/v1` | `https://api.dhl.com/auth/v1/token` |

| Purpose | Method | Path |
|---|---|---|
| OAuth token | POST | `{auth}?grant_type=client_credentials&response_type=access_token` |
| Create shipment booking | POST | `{base}/sendtransportinstruction` |
| Rate quote | — | local rate-sheet (no HTTP) |

The booking call sends `Content-Type: application/json`,
`Authorization: Bearer <token>`, and `Accept-Language` from
`Settings.language` (`<lang>-<COUNTRY>`, default `en-DE`).

**Rate limit:** 250 calls/day; HTTP 429 when exceeded.

## Authentication

OAuth2 **client_credentials** grant against the shared DHL
Authentication API. Credentials live on `Settings`: `client_id`,
`client_secret` (with system-config fallback to
`DHL_FREIGHT[_SANDBOX]_CLIENT_ID/SECRET`). **Confirmed live** against the
sandbox: returns `{access_token, token_type: "Bearer", expires_in: 1799}`
(HTTP 200). The same token authorizes every DHL Freight API (Booking,
Print, Products/Services, Additional Services).

The DHL gateway has three non-obvious requirements, all validated live
against the sandbox:

1. **Query-string grant params.** `grant_type=client_credentials` and
   `response_type=access_token` go in the **URL query string**, not the
   body.
2. **Basic Auth header, not body credentials.** `client_id:client_secret`
   is base64-encoded into `Authorization: Basic <b64>`. Sending the
   credentials in the request body (ROPC-style, as `dhl_parcel_de` does)
   is rejected with **HTTP 401** even when the credentials are valid.
3. **Non-zero `Content-Length` required.** A POST with no body length is
   rejected with **HTTP 411 Length Required**. The proxy sends an empty
   string body (`data=""`) so urllib emits `Content-Length: 0`; a
   non-`None` `data` is also what marks the request as POST in
   `lib.request`.

```
get_token()
   │  base64(client_id:client_secret) → Basic header
   ▼  POST {auth}?grant_type=client_credentials&response_type=access_token
   ┌───────────────────────────────────────────────────┐
   │ Authorization: Basic <b64>                          │
   │ Accept: application/json                            │
   │ (empty body → Content-Length: 0)                   │
   └───────────────────────────────────────────────────┘
   │
   ▼  { access_token, token_type, expires_in, scope }
   cached per dhl_freight|<client_id>|<client_secret>,
   refreshed 5 min before expiry
```

> **Operational note:** a 401 with body
> `{"status":401,"title":"Unauthorized","detail":"Access to the resource is not allowed."}`
> for valid-looking credentials usually means the DHL app behind those
> keys has not had the **DHL Freight Shipment Booking API** product
> added on the developer portal (each product is a separate API
> subscription on the app).

## Supported operations

| Operation | Supported | Notes |
|---|---|---|
| Rate quote | ✅ | Rate-sheet (`services.csv`). Live **Price Quote API** confirmed but needs an eID — see [Price Quote API](#price-quote-api-deferred). |
| Shipment booking | ✅ | `sendtransportinstruction`. |
| Tracking | ✅ | DHL Group Unified Tracking API (UTAPI) — see [Tracking](#tracking). |
| Label / BoL | ⚙️ | **Print API** chained after booking — opt-in (`auto_print_documents`) + fail-open; schema unvalidated. See [Print API](#print-api-opt-in--fail-open). |
| Pickup | ⚙️ | Booked inline via `pickupDate` + the `Pickup` party; no separate pickup endpoint. |
| Cancel / return | ❌ | Not exposed on the booking API. |

## Services & catalog (rate-sheet)

`ShippingService` maps the karrio service code (enum name) to the DHL
on-wire `productCode` (enum value):

| karrio service code | `productCode` | Description |
|---|---|---|
| `dhl_freight_eurapid` | `ECI` | International express groupage (premium LTL) |
| `dhl_freight_euroconnect` | `ECX` | Standard European groupage |
| `dhl_freight_euroconnect_plus` | `ECP` | Premium scheduled groupage |
| `dhl_freight_domestic` | `DOM` | Domestic national groupage |
| `dhl_freight_ftl` | `FTL` | Full-truck-load / part-load (per quotation) |

`DEFAULT_SERVICES` is loaded from `services.csv` (zone × weight band ×
service code). The CSV ships with `rate=0` placeholders — merchants
upload their negotiated tariff through the standard rate-sheet UI.
`DOM` is `domicile=true`; the rest are `international=true` with an
EU-country zone. `FTL` carries the heavy band (2 500–24 000 kg).

## Options

`ShippingOption` flags map 1:1 onto fields of the `additionalServices`
object (or, for references, onto `references[]` /
`additionalInformation[]`):

| Karrio option | DHL field | Category |
|---|---|---|
| `dhl_freight_after_12_delivery` | `after12Delivery` | DELIVERY_OPTIONS |
| `dhl_freight_available_pickup_time` | `availablePickupTime` | DELIVERY_OPTIONS |
| `dhl_freight_available_delivery_time` | `availableDeliveryTime` | DELIVERY_OPTIONS |
| `dhl_freight_pre_advice` | `preAdvice` (default `true`) | DELIVERY_OPTIONS |
| `dhl_freight_time_slot_booking_pickup` | `timeSlotBookingPickup` | DELIVERY_OPTIONS |
| `dhl_freight_time_slot_booking_delivery` | `timeSlotBookingDelivery` | DELIVERY_OPTIONS |
| `dhl_freight_tail_lift_loading` / `_unloading` | `tailLift…` | LOADING |
| `dhl_freight_side_loading_pickup` / `_unloading_delivery` | `side…` | LOADING |
| `dhl_freight_drop_off_by_consignor` | `dropOffByConsignor` | LOADING |
| `dhl_freight_temperature_controlled` | `temperatureControlled` `{type,min,max}` | TEMPERATURE |
| `dhl_freight_dangerous_goods` | `dangerousGoods` (auto-set, see gotchas) | HAZARDOUS |
| `dhl_freight_insurance` | `insurance` `{value,currency}` | INSURANCE |
| `dhl_freight_cash_on_delivery` | `cashOnDelivery` `{amount,currency}` | COD |
| `dhl_freight_payer_code` | `payerCode.code` (DAP/DDP/CPT/CIP/DPU) | INVOICE |
| `dhl_freight_payer_code_location` | `payerCode.location` | INVOICE |
| `dhl_freight_consignor_reference` | `references[CNR]` | SHIPMENT |
| `dhl_freight_consignee_reference` | `references[CNZ]` | SHIPMENT |
| `dhl_freight_order_reference` | `references[ORD]` | SHIPMENT |
| `dhl_freight_pickup_instruction` | `pickupInstruction` (max 512) | INSTRUCTIONS |
| `dhl_freight_delivery_instruction` | `deliveryInstruction` (max 512) | INSTRUCTIONS |
| `dhl_freight_uit_number` | `additionalInformation[UIT_NUMBER]` (RO) | INVOICE |
| `dhl_freight_ekaer_number` | `additionalInformation[EKAER_NUMBER]` (HU) | INVOICE |
| `dhl_freight_sent_number` | `additionalInformation[SENT_NUMBER]` (PL) | INVOICE |

Unified-option aliases: `cash_on_delivery` → `dhl_freight_cash_on_delivery`,
`insurance` → `dhl_freight_insurance`.

## Connection config

`ConnectionConfig` (set once per carrier connection via `config`):

| Key | Purpose |
|---|---|
| `language` | `Accept-Language` language part (`de`/`en`/`fr`/`es`/`it`/`nl`, default `en`). |
| `default_payer_code` | Incoterm used when no per-shipment `payerCode` given (default `DAP`). |
| `default_payer_location` | `payerCode.location` default. |
| `cost_center` | Cost-centre code. |
| `shipping_options` / `shipping_services` | Method-editor lists. |

## Data mapping

### Parties — karrio `Address` → DHL `PartyType`

DHL Freight has four party roles (Consignor / Consignee / Pickup /
Delivery). Per the Product Manual, **only Consignor and Consignee are
mandatory**; Pickup/Delivery are sent only when they deviate from the
legal parties. The connector maps karrio's existing fields:

```
billing_address or shipper ─►  parties[Consignor]  (payer/legal sender, mandatory)
recipient                  ─►  parties[Consignee]  (legal receiver, mandatory)
shipper                    ─►  parties[Pickup]     (only if loc ≠ Consignor)
recipient                  ─►  parties[Delivery]   (only if loc ≠ Consignee — never today)
```

Divergence is keyed on `(country_code, postal_code, city)`. So a request with
a distinct `billing_address` sends Consignor (billing) + Pickup (shipper) +
Consignee; otherwise just Consignor + Consignee.

Each `PartyType`:

```
karrio                         DHL PartyType                      Notes
──────                         ─────────────                      ─────
account number*          ───►  id                                 *Consignor: mandatory
company_name|person_name ───►  name                      (max 70)
federal_tax_id|state_tax_id ─► vatEoriSocialSecurityNumber (max 35)
person_name              ───►  contactName               (max 70)
address_line1            ───►  address.street            (max 70)
address_line2            ───►  address.additionalAddressInfo (max 70)
city                     ───►  address.cityName          (max 40)
postal_code              ───►  address.postalCode        (max 10)
country_code             ───►  address.countryCode
phone_number             ───►  phone                     (max 25)
email                    ───►  email                     (max 80)
```

> **`Parties[Consignor].Id` (the DHL Freight account number) is
> mandatory** — booking without it returns errorCode `22001`
> (*Missing Id in Consignor*), and an unprovisioned number returns
> `22014` (*Accountnumber … not valid for party Consignor*). It resolves
> from the per-shipment `dhl_freight_consignor_account` option, else the
> connection `account_number` (else `DHL_FREIGHT[_SANDBOX]_ACCOUNT_NUMBER`
> system config). Consignee `id` is optional — `dhl_freight_consignee_account`
> option, else the connection `consignee_account_number` setting. Pickup /
> Delivery carry no `id`.
>
> **`vat` is NOT sent.** It is a strongly-typed DHL field (`PartyVAT`);
> a plain tax id triggers *"Error converting value … to type
> DHL.ShipmentModels.PartyVAT"* on deserialization. The tax id goes only
> in `vatEoriSocialSecurityNumber`.
>
> Divergent pickup/delivery sites need a karrio-core
> `physical_pickup`/`physical_delivery` extension — PRD §6.2.

### Pieces — karrio `Package` → DHL `PieceType`

```
karrio Package                   DHL PieceType            Unit
──────────────                   ─────────────            ────
parcel.reference_number  ───►    id[]                     (else [""])
parcel.description       ───►    goodsType                (max 70)
packaging_type           ───►    packageType              PackagingType map
parcel.options.marksAndNumbers ► marksAndNumbers          (max 45)
parcel.options.numberOfPieces ─► numberOfPieces           (default 1)
weight                   ───►    weight                   kg
L×W×H × numberOfPieces    ───►    volume                   m³ (rounded 3dp)
parcel.options.loadingMeters ──► loadingMeters            LDM (default 0)
parcel.options.palletPlaces ───► palletPlaces             (default 0)
width / height / length  ───►    width / height / length  cm
parcel.options.stackable ───►    stackable                (default True)
parcel.options.dangerousGoods    dangerousGoods           DangerousGoodsType
  OR parcel.items[].metadata
     ["dangerousGoods"]      ───►
```

> **Pallet places, loading meters, stackable, and marks-and-numbers live on
> `parcel.options`** (PRD §6.1) — `package.options` is a `ShippingOptions`
> object, so the provider reads the raw `package.parcel.options` dict.
>
> **ADR dangerous goods** (PRD §6.4) come from `parcel.options["dangerousGoods"]`
> OR, when absent, the first parcel item that carries it —
> `parcel.items[].metadata["dangerousGoods"]` (a `commodity.metadata` dict in
> the DHL `DangerousGoodsType` shape).

### Booking header & totals

`PieceType` rows are summed into the header:
`totalNumberOfPieces`, `totalWeight` (kg), `totalVolume` (m³),
`totalLoadingMeters`, `totalPalletPlaces` (floating sums rounded to 3dp
to avoid binary-fp drift). `pickupDate` ← `options.shipment_date`,
`requestedDeliveryDate` ← `options.requested_delivery_date`, both
formatted `%Y-%m-%dT%H:%M:%S.000Z`. `goodsDescription` /
`goodsValue` / `goodsValueCurrency` come from `payload.customs`
(currency defaults to `EUR`).

### Payer code (incoterms) & customs-scoped options

These are read primarily from **`customs.options`** (a dhl_freight
`CustomsOption` enum) so they live with the customs declaration, with the
same-named shipment-level `ShippingOption` as a fallback.

`payerCode` is built from two **flat string** options (not a dict). The
**`code`** resolves in order: `customs.options.dhl_freight_payer_code` →
`dhl_freight_payer_code` shipping option → **`customs.incoterm`** →
`connection_config.default_payer_code` (default `DAP`). The **`location`**
resolves the same way via `…_payer_code_location` →
`connection_config.default_payer_location`. Supported `Incoterm` values:
`DAP`, `DDP`, `CPT`, `CIP`, `DPU`.

### Country-specific tax references

RO/HU/PL road freight requires state-system reference codes. Read from
`customs.options` (fallback: shipping option), projected into
`additionalInformation[]`:

| Country | Code | `customs.options` (or ShippingOption) |
|---|---|---|
| RO | `UIT_NUMBER` | `dhl_freight_uit_number` |
| HU | `EKAER_NUMBER` | `dhl_freight_ekaer_number` |
| PL | `SENT_NUMBER` | `dhl_freight_sent_number` |

## Multi-piece handling

Single booking call carries all pieces. Each karrio `Parcel` becomes one
`PieceType` in the `pieces[]` array; the header totals are the sums
across pieces (see [Booking header & totals](#booking-header--totals)).
No per-piece HTTP fan-out.

## Wire-shape invariants & gotchas

- **Four parties, always.** Even a same-site shipment emits Consignor +
  Consignee + Pickup + Delivery (PRD §6.2).
- **Dangerous goods is per-piece; the header flag is derived.**
  `additionalServices.dangerousGoods` is forced `true` when **any**
  piece carries a `dangerousGoods` ADR record; otherwise it follows the
  explicit `dhl_freight_dangerous_goods` option.
- **Pallet places / loading meters / stackable / ADR ride on
  `parcel.options`** — not first-class `Parcel` fields (PRD §6.1).
- **No label in the booking response.** `docs.label = ""`; labels come
  from the separate Print API. SSCC license plates are preserved in
  `meta.license_plates` for the eventual Print hand-off.
- **OAuth credentials go in the Basic Auth header, not the body**, and
  the token POST needs a non-zero `Content-Length` — see
  [Authentication](#authentication).
- **Floating-point totals are rounded to 3dp** (`totalVolume`,
  `totalLoadingMeters`) so `0.8 + 1.6` serialises as `2.4`, not
  `2.4000000000000004`.
- **`payerCode.location` is dropped when empty** by `lib.to_dict`, so a
  default payer code serialises as `{"code": "DAP"}`.
- **Generated schema field names are camelCase verbatim** — the
  `generate` script runs `kcli` with `--no-nice-property-names`. Don't
  rename them in `karrio/schemas/dhl_freight/`.

## Response & identifiers

```
booking response (ShippingResponseType)
  ├─ shipmentId | transportInstructionId ─► tracking_number
  │                                          shipment_identifier
  │                                          meta.tracking_numbers
  └─ licensePlates[].licensePlate|sscc|pieceId ─► meta.license_plates
                                                  meta.shipment_identifiers
                                                  (tracking_number + plates)
```

`docs.label` is empty (no label on this API). `meta.product_code` carries
the karrio service code from the request `ctx`.
`Settings.tracking_url` points at the DHL consumer freight-tracking
portal (`dhl.com/global-en/home/tracking/tracking-freight.html`).

## Tracking

DHL Freight tracking is served by the **DHL Group Unified Tracking API
(UTAPI)** — a cross-business-unit API (the same one `dhl_universal` uses),
*not* the OAuth-gated Freight farm. Auth is a simple **`DHL-API-Key`
header** (the connection `client_id`), not the Bearer token.

```
GET {tracking_base}/shipments?trackingNumber=<id>&service=freight&language=<lang>
DHL-API-Key: <client_id>
```

| Mode | `tracking_base` |
|---|---|
| Test | `https://api-sandbox.dhl.com/track` |
| Prod | `https://api-eu.dhl.com/track` |

`service=freight` scopes the lookup to the Freight BU. One GET per tracking
number, run concurrently (`lib.run_asynchronously`). Each response carries
`shipments[]`; `shipment.status.statusCode` / per-event `statusCode` map via
`TrackingStatus`:

| karrio status | UTAPI statusCode |
|---|---|
| `pending` | `pre-transit` |
| `in_transit` | `transit` |
| `delivered` | `delivered` |
| `delivery_failed` | `failure` |
| `delivery_delayed` | `unknown` |

Unmatched codes fall back to `in_transit`. `meta.license_plates` carries
`details.pieceIds` (the SSCCs), `meta.reference` carries
`details.references.number`. UTAPI error bodies (`{title, detail, status,
instance}`) are routed through `parse_error_response`.

> **Subscription note:** UTAPI is a separate API product on the DHL
> developer portal — the app's `client_id` must have *Shipment Tracking -
> Unified* added, else every call returns 401 (independent of the Freight
> farm subscription). Confirmed live: the connector reaches UTAPI and
> surfaces the 401 cleanly; a subscribed key returns the `shipments[]` body.

## Print API (opt-in & fail-open)

Labels / barcode license plates / waybill (CMR) come from the separate
**DHL Freight Print (Labelling) API**
(`POST {print_base}/print/printdocumentsbyid`, where `print_base` is
`…/freight/shipping/labels/v1`), which takes the booking's shipment id(s) and
returns Base64 PDF(s). The connector chains booking → print inside
`proxy.create_shipment` (modelled on `sendle`'s two-call label pattern) and
attaches the PDF to `docs.label`.

Because DHL publishes **no request schema** for this API (not in the manual,
no Postman, no OpenAPI) and it can't be live-validated without a bookable
account, the chain is:

- **Opt-in** — runs only when the connection config
  `auto_print_documents = true` (and `print_document_type` ∈
  `label`/`shipmentList`/`waybill`, default `label`). Off by default.
- **Fail-open** — wrapped in `lib.failsafe`; any print error is swallowed, so
  the booking still returns success with an empty label.
- **Best-effort request** — `{shipmentId: ["<id>"], printOption: "<type>"}`,
  Bearer auth. **Defensive parse** — base64 read from `documents[0].content`
  / `content` / `base64`.

`proxy.create_shipment` returns `(booking, print|None)`;
`parse_shipment_response` normalizes the tuple and sets `docs.label` +
`label_type="PDF"` when a label came back. Validate the request/response shape
and flip the default once the Labelling API schema (or a bookable account) is
available.

## Price Quote API (deferred)

Live rates are the **Price Quote API (= Rating API)** at
`POST …/freight/info/pricequote/v1/pricequote/quoteforprice`. Confirmed in the
Product Manual; **not wired** because it requires a DHL-issued **eID
(username/password)** in addition to OAuth, plus an unpublished request
schema. The connector uses the CSV rate-sheet until an eID + schema are
available.

## Error parsing

`error.parse_error_response` accepts a dict or a list of dicts and
handles three shapes (all observed live against the sandbox):

1. **Booking validation** (`sendtransportinstruction`):
   `{status: "Error", validationErrors: [{errorCode, message, field}]}`.
   Emits one karrio `Message` per entry (`code = errorCode`,
   `details.field`). Observed codes: `22001` (Missing Id in Consignor),
   `22014` (Accountnumber not valid for party). Model-deserialization
   failures also arrive here, e.g. a bad `vat` value
   (*Error converting value … to type DHL.ShipmentModels.PartyVAT*).
2. **RFC-7807 `problem+json`** (DHL gateway): `statusCode|status`,
   `title`, `detail`, `instance`, `invalidParams[]`.
3. **OAuth2 token error** (auth endpoint): `error`, `error_description`.

An entry is treated as an error when it has `validationErrors`, or
`statusCode >= 400`, or `error`, or `status == "Error"`, or `title`
non-empty and not `"ok"`.

```
response
   │
   ├─ validationErrors[]  ──► one Message per {errorCode, message, field}
   │
   ├─ statusCode >= 400        ──┐
   ├─ "error" present           ─┼─► Message:
   ├─ status == "Error"         ─┤     code    = statusCode | error | code
   └─ title not in ("","ok")    ──┘     message = error_description
                                                 | detail | message | title
                                         details = {title, instance, invalidParams}
```

> The typed `ErrorResponseType` flattens `error_description` to
> `errordescription` (kcli strips the underscore), so the OAuth
> `error_description` is read from the **raw dict**, while the rest come
> from the typed object. The gateway message is the first present of
> `error_description → detail → message → title` (never concatenated).

## Localization (i18n)

User-facing service / option / connection-config **labels** are localized
(English + German). The carrier catalog
`karrio/providers/dhl_freight/i18n.py` defines `SERVICE_NAME_TRANSLATIONS`
(5 products) and `OPTION_NAME_TRANSLATIONS` (all `ShippingOption` +
`CustomsOption` labels), wrapped in `gettext_lazy`. Connection fields
(`consignee_account_number`) and config keys (`default_payer_code`,
`default_payer_location`, `auto_print_documents`, `print_document_type`) are
added to the shared `CONNECTION_FIELD_LABELS` / `CONFIG_FIELD_LABELS` in
`karrio.core.i18n.translations`.

`karrio.core.i18n.translate_references` discovers the catalog via
`_load_carrier_i18n("dhl_freight")` and resolves the active language from the
Django catalog `karrio/apps/api/locale/de/LC_MESSAGES/django.{po,mo}` (German
added surgically — never via `makemessages`, per `.claude/rules/localization.md`).
`tests/dhl_freight/test_i18n.py` guards that every service/option has a label.

## References

- **Vendor assets** (`vendors/`):
  - `DHL_Freight_Shipment_Booking_SANDBOX_2026_R03.postman_collection.json`
    — canonical request sample (source for `schemas/shipping_request.json`)
  - `DHL_Freight_APIs_Product_Manual_2026_R03.pdf` — product manual
- **Tracking (UTAPI)** — `schemas/tracking_response.json`; shape shared with
  `dhl_universal`. Docs:
  <https://developer.dhl.com/api-reference/shipment-tracking>
- **Live API docs** —
  <https://developer.dhl.com/api-reference/shipment-booking-dhl-freight>
- **Auth API docs** —
  <https://developer.dhl.com/api-reference/authentication-api-dhl-freight>
- **PRD** — [PRD.md](./PRD.md) (phased plan + karrio-core architecture flags)
- **Rate sheet** — `karrio/providers/dhl_freight/services.csv`
- **Generated schemas** — `karrio/schemas/dhl_freight/*.py` are generated
  from `schemas/*.json` via `kcli ... --no-nice-property-names` (see
  `generate`). Never hand-edit; regenerate with
  `./bin/run-generate-on modules/connectors/dhl_freight`.
