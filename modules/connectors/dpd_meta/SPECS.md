# DPD Meta integration — specification

Reference for the **dpd_meta** connector. It targets DPD's pan-European
**META-API** (a JSON REST shipping surface that fronts every DPD business
unit) rather than a single national DPD endpoint. The connector also speaks
two DPD **public SOAP web services** — `LoginService_V2_0` and
`DepotDataService_V1_0` — to resolve the origin depot for reseller/brokerage
setups. Vendor source of truth lives under `vendor/`
(`METAAPI_CUSTOMER_DOCUMENTATION_1_2.pdf`, `openapi_metaapi_shipping.yaml`,
`dpd-api.developer.guidelines-A4-20250115.pdf`, `LoginService_V2_0_C0.pdf`,
`DepotDataService_V1_0.pdf`) plus the April 2026 DPD Product & Service List.

## What distinguishes `dpd_meta` from `dpd`

| Aspect | `dpd_meta` | `dpd` (classic) |
|---|---|---|
| Shipping protocol | **JSON REST** META-API (`api.dpdgroup.com/shipping/v1`) | SOAP BU-API |
| Scope | **Multi-country / multi-BU** via a single META endpoint; the business unit is selected by the `X-DPD-BUCODE` header (`001`=DE, `002`=FR, `010`=NL, …) | single national business unit |
| Auth | Custom header login → returns **`X-DPD-TOKEN`** bearer JWT, cached until its real `exp` | delisId/password SOAP auth |
| Product selection | Single **pre-bundled SoCode** per shipment (e.g. `101`, `327`); option combos resolved client-side into one code (`resolve_product_code`) | product + parameter combos |
| Depot resolution | Reuses the DPD **public SOAP** Login + DepotData services to derive `sendingDepot` per request | native |

The two protocols coexist: shipments/pickups go over META JSON REST; depot
lookup (and the unified `Location` interface) go over the public SOAP WS.

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │  karrio ShipmentRequest / PickupRequest /
│   (karrio core)         │  LocationRequest / RateRequest
└───────────┬─────────────┘
            │
            ▼
┌──────────────────────────────┐
│  providers/dpd_meta          │  Pure data transforms (no HTTP).
│   shipment/create.py         │  Unified model → typed META JSON request,
│   shipment/return_shipment.py│  typed response → unified model.
│   pickup/create.py           │  SoCode resolution + depot placeholder
│   location.py                │  stamping live in units.py / location.py.
│   error.py                   │
│   units.py                   │  ShippingService (SoCodes), ShippingOption,
│   utils.py                   │  ConnectionConfig, product-code resolver maps,
│                              │  EU member set, CSV-loaded service catalog.
└───────────┬──────────────────┘
            │
            ▼
┌──────────────────────────────┐
│  mappers/dpd_meta/proxy.py   │  HTTP transport only.
│   - authenticate (token)     │  - META login → X-DPD-TOKEN (JWT exp cache)
│   - create_shipment          │  - public-WS SOAP login (2h cache)
│   - create_return_shipment   │  - depot resolution + [DEPOT] substitution
│   - schedule_pickup          │  - rating via RatingMixinProxy (universal)
│   - get_locations            │
│   - authenticate_public_ws   │
│   - get_rates                │
└───────────┬──────────────────┘
            │
            ▼
┌──────────────────────────────┐
│  DPD APIs                    │
│  ──────────────────────────  │
│  META-API (JSON REST)        │  /login, /shipment, /pickupscheduling
│  LoginService V2_0 (SOAP)    │  getAuth → authToken
│  DepotDataService V1_0 (SOAP)│  getDepotData → depot for country+zip
└──────────────────────────────┘
```

**Key architectural choices:**

- **Header-based login, token in response header.** META login is a `POST
  /login` with credentials in custom `X-DPD-*` headers; the bearer token
  comes back in the `X-DPD-TOKEN` *response header* (not a JSON body). The
  connector decodes the JWT `exp` claim and caches until that real expiry; if
  the token is not a decodable JWT, it falls back to a short 15-minute cache.
- **Two parallel auth schemes.** META (`X-DPD-TOKEN` bearer) for
  shipment/pickup; public-WS SOAP `authToken` (delisId+password) for depot
  lookup. The two are cached under separate keys. META calls use
  `lib.authenticated_request()` to invalidate and retry once on HTTP 401/403;
  public-WS depot lookups invalidate and retry once on SOAP LOGIN_5/LOGIN_6.
- **Single SoCode per shipment.** Per META-API Item 4b, `productCode` must be
  one pre-bundled code. Option combinations (COD, small parcel, Saturday,
  PUDO, Ex Works, food, hazmat, ID-check, …) are resolved **client-side** into
  the correct SoCode by `resolve_product_code` (see § Product-code resolution).
- **Static catalog from CSV.** `DEFAULT_SERVICES` is built at import time from
  `services.csv` (one row per service/zone). No live product/service catalog
  fetch.
- **No tracking provider.** The connector exposes a `tracking_url` template
  (`https://www.dpdgroup.com/tracking?parcelNumber={}`) but ships **no**
  `tracking.py` / `parse_tracking_response`. `TrackingStatus` exists in
  `units.py` but is unused by any parser.
- **Rating is universal.** Rates use karrio's `RatingMixinProxy` /
  `universal.providers.rating` against the static `services.csv` catalog — no
  DPD rate API call.
- **Generated schemas.** `karrio/schemas/dpd_meta/*.py` is generated; JSON via
  `kcli --no-nice-property-names` (camelCase preserved), the SOAP `webapi.py`
  via `generateDS` from `webapi.xsd`. Regenerate with
  `./bin/run-generate-on modules/connectors/dpd_meta` — never hand-edit.

## Data flow

### Shipment create (META JSON REST, optional depot pre-call)

```
ShipmentRequest                                   DPD APIs
     │                                               │
     ├─► shipment_request()                          │
     │     to_address(shipper/recipient)             │
     │     to_packages() / to_shipping_options()     │
     │     resolve_product_code(service, options,    │
     │                          recipient_country)   │
     │     resolve_pudo_id() / depot placeholder      │
     │   → [ShipmentRequestElementType]  (JSON list)  │
     │                                               │
     ├─► proxy.create_shipment:                       │
     │     authenticate()  ── POST /login ──────────►│  (X-DPD-TOKEN, cached)
     │                                               │
     │     if ctx.resolve_depot:                      │
     │       get_locations() ── SOAP getAuth ────────►│  (public-WS authToken)
     │                       ── SOAP getDepotData ────►│  (depot for zip)
     │       inject_sending_depot([DEPOT] → 7-digit)  │
     │                                               │
     │   ─ POST /shipment?LabelPrintFormat={fmt} ────►│
     │       Authorization: Bearer <token>            │  validate
     │       X-DPD-BUCODE: <bucode>                   │  label gen
     │   ◄─ {shipmentId, parcelIds[], label{base64},  │
     │       qrcode{base64}, parcelBarcodes[], ...} ──│
     │                                               │
     ├─► _extract_details:                            │
     │     parcelIds[0]      → tracking_number        │
     │     shipmentId        → shipment_identifier    │
     │     label.base64Data  → docs.label             │
     │     qrcode.base64Data → docs.extra_documents   │
     ▼                                               ▼
ShipmentDetails                                  (one create call)
```

The depot pre-call only fires when `ctx.resolve_depot` is set — i.e. no
connection-level `sending_depot` override AND `resolve_shipper_depot` option on
(default) AND origin country is **DE** (the DepotDataService coverage).

### Depot / Location resolution (public SOAP WS, two calls)

```
LocationRequest (country + zip)                  DPD public-WS
     │                                               │
     ├─► location_request() → getDepotData envelope   │
     │     with [AUTH_TOKEN] placeholder, ctx{country,zip}
     │                                               │
     ├─► proxy.get_locations:                         │
     │     cache hit on dpd_meta|depot|{c}|{zip}? ─── return cached
     │     else authenticate_public_ws():             │
     │       ─ POST /LoginService/V2_0 (getAuth) ────►│
     │       ◄ <return><authToken> ──────────────────│  (2h cache)
     │     substitute [AUTH_TOKEN] → authToken         │
     │   ─ POST /DepotDataService/V1_0 (getDepotData)►│
     │   ◄ <DepotData><depot>… ──────────────────────│
     │     cache only when "<depot>" present (24h)     │
     ▼                                               ▼
[LocationDetails]   (depot → location_id, address)
```

## Endpoints

Test mode hosts: META `api-preprod.dpsin.dpdgroup.com:8443`, public-WS
`public-ws-stage.dpd.com`. Prod: META `api.dpdgroup.com`, public-WS
`public-ws.dpd.com`.

| Purpose | Method | Path |
|---|---|---|
| META login (token) | POST | `{server_url}/login` |
| Create shipment | POST | `{server_url}/shipment?LabelPrintFormat={format}` |
| Create return shipment | POST | `{server_url}/shipment?LabelPrintFormat={format}` (delegates to create) |
| Schedule pickup | POST | `{server_url}/pickupscheduling` |
| Public-WS login (SOAP) | POST | `{public_ws_url}/LoginService/V2_0` |
| Depot lookup (SOAP) | POST | `{public_ws_url}/DepotDataService/V1_0` |

`server_url` = `https://{meta-host}/shipping/v1`. SOAP services are reached as
`{public_ws_url}/{ServiceName}/V{N}_0` with the matching `SOAPAction` header.

## Authentication

Two independent schemes use separate connection-cache keys and refresh rules:

**META-API** — `POST /login` with custom headers; one of two credential pairs,
always alongside the business-unit code:

| Header | Source (settings) | When |
|---|---|---|
| `X-DPD-BUCODE` | `dpd_bucode` | always |
| `X-DPD-LOGIN` | `dpd_login` (delisId) | login-pair accounts |
| `X-DPD-PASSWORD` | `dpd_password` | login-pair accounts |
| `X-DPD-CLIENTID` | `dpd_client_id` | client-credential accounts (e.g. SEUR) |
| `X-DPD-CLIENTSECRET` | `dpd_client_secret` | client-credential accounts |

The token is read from the **`X-DPD-TOKEN` response header** and used as
`Authorization: Bearer <token>` on `/shipment` and `/pickupscheduling`
(both also re-send `X-DPD-BUCODE`). Cache key:
`dpd_meta|{u:login | c:clientid}|{bucode}|{test|prod}`.

The token is a DPD-issued JWT. The connector decodes the JWT `exp` claim and
stores that timestamp as the cache expiry, with `buffer_minutes=5` so
short-lived business-unit tokens (for example 30-minute SEUR tokens) remain
usable while still refreshing before expiry. If the token cannot be decoded as
a JWT, the connector uses a short 15-minute fallback expiry rather than the old
fixed 24-hour assumption. Shipment and pickup calls go through
`lib.authenticated_request()`; if DPD rejects a cached token with HTTP 401/403,
the connector invalidates the cached token and retries the request once with a
fresh login.

**Public web services (SOAP)** — `LoginService_V2_0.getAuth(delisId, password,
messageLanguage)` returns an `authToken` (read from `<return><authToken>`).
Only available when `dpd_login` + `dpd_password` are set. Cache key:
`dpd_meta|ws|{delisId}|{test|prod}`. The token is substituted into the
`[AUTH_TOKEN]` placeholder of the `getDepotData` envelope before posting.

The V2_0 LoginService response does not include a real expiry, so the connector
caches this SOAP `authToken` for 2 hours with a 30-minute refresh buffer. If
DepotDataService returns SOAP authentication faults LOGIN_5 or LOGIN_6, the
connector deletes the SOAP token cache entry, logs in again, and retries the
depot lookup once. Successfully resolved depot responses remain cached for 24
hours per country/postal-code pair.

## Supported operations

| Operation | Wired | Notes |
|---|---|---|
| Rate | Yes (universal) | `RatingMixinProxy` against static `services.csv`; no DPD rate API |
| Shipment create | Yes | `POST /shipment` |
| Return shipment | Yes | `return_shipment.py` re-runs create with `dpd_meta_return_enabled=True` |
| Shipment cancel | **No** | no `cancel.py` |
| Pickup schedule | Yes | `POST /pickupscheduling` |
| Pickup cancel | **No** | not implemented |
| Location finder | Yes | DepotDataService SOAP (`get_locations`) |
| Tracking (pull) | **No** | only a `tracking_url` template; no poll parser |
| Tracking push (webhook) | Yes | DPD Tracking Push Service — see [Tracking Push](#tracking-push-webhook) |

> The README mentions a `find_locations(...)` proxy method; the actual method
> is `get_locations(...)`. Treat the README name as documentation drift.

## Services (SoCodes)

`ShippingService` maps karrio service codes to DPD **Group Product Codes
(SoCodes)**. Source: DPD Product & Service List, April 2026. Names use the
PDF's EDI prefix (CL/E12/E18/E830/IE2/MAIL/PL/B2C). Legacy DE-SOAP short codes
(AM2/PM2/AM0/…) are **not** supported by the META-API.

| karrio service | SoCode | DPD product |
|---|---|---|
| `dpd_meta_classic` | `101` | CL — DPD Classic |
| `dpd_meta_small` | `136` | CL — Classic small parcel (Kleinpaket) |
| `dpd_meta_b2c_classic` | `327` | B2C — Classic (CL + predict) |
| `dpd_meta_b2c_small` | `328` | B2C — Classic small parcel |
| `dpd_meta_express_830` | `350` | E830 — DPD 8:30 |
| `dpd_meta_express_12` | `225` | E12 — DPD 12:00 |
| `dpd_meta_express_18` | `155` | E18 — DPD GUARANTEE |
| `dpd_meta_international_express` | `302` | IE2 — EXPRESS International |
| `dpd_meta_parcel_letter` | `154` | PL — PARCELLetter |
| `dpd_meta_mail` | `294` | MAIL — DPD Mail |
| `dpd_meta_parcelshop` | `337` | B2C — ParcelShop direct delivery |
| `dpd_meta_shop_return` | `332` | B2C — DPD Return |
| `dpd_meta_shop2shop_domestic` | `345` | B2C — Shop2Shop (AsCode A15) |
| `dpd_meta_shop2home` | `404` | B2C — Shop2Home (AsCode A15) |

Codes `345` / `404` additionally carry `additionalServiceCode=A15`
(`ADDITIONAL_SERVICE_CODES`). Several food / tyre / exchange-inbound services
(`118`, `365`, `366`, `383`, `378`, `379`) are present in source but commented
out as **non-Bronze** (SHIP2-1194).

### Product-code resolution

`resolve_product_code(service, options, recipient_country)` collapses the base
service plus active options into the single SoCode DPD requires:

1. **Dual-option triples** (`DUAL_OPTION_MAP`) match first — e.g.
   `(327, cod, small)→330`, `(327, pudo, small)→338`, `(101, exw, hazardous)→106`,
   `(225, exw, saturday)→234`, `(101, exw, limited_quantity)→704`. Skipped when
   `food` is set (food has no documented triple).
2. **Single-option precedence:** food > hazardous > limited_quantity >
   exchange > id_check > cod > pudo > saturday > small > exw.

Single-option maps:

| Map | Routing |
|---|---|
| `COD_PRODUCT_CODE_MAP` | `101→109`, `327→329`, `328→330` |
| `SATURDAY_PRODUCT_CODE_MAP` | `101→103`, `327→358`, `225→228` |
| `SMALL_PARCEL_PRODUCT_CODE_MAP` | `101→136`, `327→328` |
| `EX_WORKS_PRODUCT_CODE_MAP` | `101→105`, `155→158`, `225→231`, `350→351` |
| `PUDO_PRODUCT_CODE_MAP` | `327→337`, `328→338` |
| `HAZARDOUS_PRODUCT_CODE_MAP` | `101→102` |
| `EXCHANGE_PRODUCT_CODE_MAP` | `101→113` |
| `ID_CHECK_PRODUCT_CODE_MAP` | `155→168`, `225→249` |
| `FOOD_PRODUCT_CODE_MAP` | `101→383`, `155→378`, `225→379` |
| `LIMITED_QUANTITY_PRODUCT_CODE_MAP` | `101→793`, `105→704`, `155→799`, `225→797`, `327→794`, `332→447` |

**Country guard:** if the resolved code is in `COUNTRY_ALLOWLIST`
(`103`→{NL,BE,PL,CZ,FR}, `358`→{NL,BE,BG}) and `recipient_country` is not in
the allowed set, the resolver **falls back to the base service code** to avoid
DPD `ROUTING_15` ("service combination not possible") rejections. Codes
`103/109/329/330/358` are not in the April 2026 PDF — they survive on
legacy/special-agreement accounts.

**B2C predict:** every `D,2C,…` SoCode in `B2C_PRODUCT_CODES` requires a
`predict.value`; the connector populates `notification_email` from
`recipient.email` for B2C / PUDO codes (excluding return `332`).

**PUDO id:** `resolve_pudo_id` returns `parcel_shop_id` only when the resolved
code is a Parcel-to-Shop SoCode (`337`/`338`/`345`).

## Options

`ShippingOption` (selected; all carrier options are prefixed `dpd_meta_`).
`configurable=False` options are hidden from the connection/method UI but
remain functional via the API. Dangerous-goods, declared-value and several
routing flags are hidden for Bronze certification (SHIP2-1194).

| Option | Wire effect |
|---|---|
| `dpd_meta_saturday_delivery` | Saturday SoCode routing |
| `dpd_meta_small_parcel` | small-parcel SoCode routing |
| `dpd_meta_ex_works` / `dpd_meta_exchange_service` / `dpd_meta_food` | SoCode routing |
| `dpd_meta_id_check` | SoCode routing + `person.personalDeliveryType="s2"` |
| `dpd_meta_hazardous_limited_quantities` | LQ SoCode + `parcel.hazardousLimitedQuantities=true` |
| `dpd_meta_dangerous_goods` (+ `dg_*`) | `parcel.hazardous[]` block |
| `cash_on_delivery` | `parcel.cod{}` + `mpsCompleteDelivery="s2"` |
| `insurance` (+ `insurance_description`) | `parcel.insurance{}` |
| `dpd_meta_parcel_shop_id` | `receiver.pudoId` |
| `dpd_meta_notification_email` / `_sms` | `parcel.messages[]` (EMAIL/SMS) |
| `dpd_meta_delivery_date_from/to`, `_time_from/to` | `delivery{}` window |
| `dpd_meta_cod_*` | COD bank fields (per-shipment, fall back to connection config) |
| `dpd_meta_resolve_shipper_depot` | trigger DepotDataService depot resolution (default on, DE only) |

### ConnectionConfig

`sending_depot` (visible) pins the origin depot. COD bank fields
(`cod_bank_code/name/account_number/account_name/iban/bic`) are visible and
serve as per-connection defaults. Label fields (`label_type`, `label_format`
default `PDF`, `label_paper_format`, `label_printer_position`), `dropoff_type`,
`simulate`, `extra_barcode`, `with_document` are `configurable=False`
(method/server managed). Recipient/shipper phone is transmitted normally;
recipient-phone privacy is governed by the generic `suppress_recipient_phone`
data-privacy option at the SDK seam, not a DPD-specific gate.

## Data mapping

### Address — karrio `Address` → META `ReceiverAddressType` / `SenderType`

```
karrio Address              META field
──────────────              ──────────
company_name        ──►     companyName ; name1 (company, else person_name)
person_name         ──►     name2 (when company present) ; contact.contactPerson
street_name/line1   ──►     street
street_number       ──►     houseNumber (max 8)
address_line2       ──►     addressLine2
floor/building/dept ──►     floor / building / department
postal_code         ──►     zipCode (max 9)
city                ──►     city
state_code          ──►     state (max 2)
country_code        ──►     country
phone_number        ──►     contact.phone1   (suppress via generic suppress_recipient_phone)
email               ──►     contact.email
tax_id              ──►     legalEntity.vatNumber
```

Sender `legalEntity.businessType` is always `B` (business). Recipient
`businessType` is `B` when `company_name` present, else `P` (private). Text
fields are truncated by `lib.text(..., max=35)` (most), `max=8` houseNumber,
`max=9` zip.

### Parcel / weight

- Per-parcel `weight` and the shipment-level `weight` are in **grams, rounded
  up to the nearest 10 g** (`_round_grams`: `ceil(g/10)*10`). META divides by
  10 before handing to the downstream SOAP BU-API (10 g units).
- `dimensions` (length/width/height, integer cm) sent only when the package
  `has_dimensions`.
- `numberOfParcels` = parcel count; one `parcel[]` entry per package.
- `senderParcelRefs` from `pkg.reference_number` unless it equals the parcel id.

### COD (`parcel.cod`)

`amount{amount,currency}`, `collectType` (default `s0` cash), plus
`purpose/bankCode/bankName/bankAccountNumber/bankAccountName/iban/bic` each
sourced from the per-shipment option then the connection config. Setting COD
also stamps `mpsCompleteDelivery="s2"`.

| `CodCollectType` | Wire |
|---|---|
| CASH | `s0` |
| CROSSED_CHEQUE | `s1` |
| CREDIT_CARD | `s2` |
| DEFAULT | `s9` |

### Customs (`international` block)

`has_customs` is true when `customs.is_defined` AND shipper/recipient countries
differ AND (not intra-EU OR the service is `dpd_meta_international_express`
`302`). Intra-EU cross-border needs no customs data per DPD. EU set in
`EU_MEMBER_STATES`.

```
karrio CustomsInfo            META international field
──────────────────            ───────────────────────
content_type=="documents"  ─► parcelType "D" else "P"
duty.declared_value / value ─► customsAmount / customsAmountEx {amount,currency}
incoterm (Incoterm map)    ─► customsTerms (default s01 DAP-not-cleared)
                              customsPaper="A" (COMMERCIAL_INVOICE)
                              clearanceStatus="N"
value ≥150 / ≥22 / else     ─► customsHighLowValue H / M / L
invoice / reference / "N/A" ─► customsInvoice (max 35)
invoice_date               ─► customsInvoiceDates[]
len(commodities)           ─► numberOfArticles
content_type               ─► exportReason (CustomsContentType map; default s01 SALE)
content_description        ─► shipmentContent
recipient                  ─► importer{address,contact,vatNumber,eori}
exporter (duty.paid_by)    ─► exporter{address,contact,eori}
commodities[i]             ─► interInvoiceLines[i] {invoicePosition, quantityOfItems,
                              content, amountOfPosition, manufacturedCountry,
                              netWeight/grossWeight (grams), customerProductCode=sku,
                              productDescription, import/exportTarifCode=hs_code,
                              parcelRank="1"}
```

Incoterm → DPD `CustomsTerms`: `DAP→s06`, `DDP→s03` (duties+taxes),
`DDU→s01` (DAP not cleared), `EXW→s05`; CFR/CIF/CIP/CPT→DAP, FCA/FOB/FAS→EXW.
Export reason: sale/merchandise/sample/documents/other→`s01`, gift→`s03`,
return_merchandise/repair→`s02`.

### Shipment response → `ShipmentDetails`

```
ShipmentResponseType          ShipmentDetails
────────────────────          ───────────────
parcelIds[0]          ──►      tracking_number
shipmentId            ──►      shipment_identifier
label.base64Data      ──►      docs.label
qrcode.base64Data     ──►      docs.extra_documents[] (category qr_code)
parcelBarcodes[]      ──►      meta.parcel_barcodes
networkShipmentId     ──►      meta.network_shipment_id
networkParcelIds      ──►      meta.network_parcel_ids
parcelIds             ──►      meta.tracking_numbers + meta.tracking_url
```

`label_type` echoes the requested `LabelPrintFormat` (default `PDF`).

### Pickup (`/pickupscheduling`)

`pickup{date, fromTime(HHMM, default 0900), toTime(HHMM, default 1700)}`,
`pickupAddress`, `pickupContact` (phone gated like shipments),
`shipmentNumbers`/`parcelNumbers` from the request,
`pickupWeight` = `max(total grams, 1000)`, `comment` = instruction. Response
`scheduledPickupResponse[]`: the first entry with a `pickupreference` becomes
`confirmation_number`; entries without one but with `statusDescription` become
error `Message`s.

## Depot resolution & `[DEPOT]` placeholder

DPD requires an origin **sendingDepot**. Resolution order:

1. **Connection override** — `connection_config.sending_depot`. Shipments need
   the **7-digit GeoRouting code** (`{bucode}{depot}`); pickups need the bare
   **4-digit depot** (`configured_depot(..., geo_routing=)`).
2. **Per-request resolution** — when no override, `resolve_shipper_depot` on
   (default), and origin is **DE**: the mapper stamps `sendingDepot="[DEPOT]"`
   and sets `ctx.resolve_depot=True`. The proxy then runs LoginService +
   DepotDataService for the sender/pickup postal code and `inject_sending_depot`
   substitutes the placeholder (7-digit for shipments, 4-digit for pickups).
   If nothing resolves, the placeholder is **dropped** rather than sending a
   bogus value. Resolved depots are cached 24h per country+zip.

This is the reseller/brokerage case: the DPD account belongs to the broker, so
the customer's depot isn't known from credentials and must be derived per
shipment.

## Error parsing

`parse_error_response` normalizes dict/list responses and recognizes three
shapes (first match wins per item):

| Detect | Source | Emitted `code` / `message` |
|---|---|---|
| `errorCode` / `errorMessage` | META standard error (`ErrorResponseType`) | `errorCode` / `Error Code {code}: {message}`; `details` carries `errorOrigin` + `debugList[]` |
| `detail` / `http_status` | `lib.error_decoder` HTTP failure | `http_status` / `detail` or `HTTP {status}: {message}` |
| `errors` / `message` | META validation error | `code` or `VALIDATION_ERROR` |

`parse_soap_faults` handles public-WS SOAP faults: prefers
`<detail>` faults (`authenticationFault`/`dataFault`/`systemFault` with
`errorCode`+`errorMessage`), falls back to the generic `<Fault>`
`faultcode`/`faultstring`. Login failures short-circuit `get_locations` to a
list of `Message`s (no depot string to parse). LOGIN_5 and LOGIN_6 are treated
as expired public-WS auth-token signals during depot lookup, so the proxy
invalidates the SOAP auth cache and retries once.

## Tracking Push (webhook)

`dpd_meta`'s only tracking path. DPD's **Tracking Push Service** (DE) pushes one
scan event per call to a subscriber URL as **HTTP GET query parameters** — there
is no registration API; the URL is configured once per DPD account in the DPD
customer center. Source: *Tracking Push Service — Schnelleinstieg (04/2023)*.

**Reception.** Carrier-level inbound endpoint (one static URL per integration,
not per connection): `GET /v1/connections/webhook/dpd_meta/events`. The
parcel — and through it the tracker, connection and org — is resolved from the
globally-unique parcel number (`pnr`), so no `connection_pk` is in the URL. The
hook (`providers/dpd_meta/hooks/event.py`) parses with a stub gateway; core
(`karrio/server/providers/webhooks.py::process`) does the tracker match + update.

**Query parameters** (the wire payload): `pushid` (unique record id, echoed in
the ack), `pnr` (parcel no. = our `tracking_number`), `status` (code, mapped
below), `statusdate` (`ddMMyyyyHHmmss`), `depot`, `ref` (MPSEXPDATA ref —
configured as MPSCREF1), `receiver`, `services`, `pod`, `weight`.

**Status mapping** (`units.PushTrackingStatus`):

| DPD `status` | Unified |
|---|---|
| `start_order` | `pending` |
| `pickup_driver` | `picked_up` |
| `pickup_depot`, `delivery_depot`, `delivery_nab` | `in_transit` |
| `delivery_carload` | `out_for_delivery` |
| `delivery_notification` | `on_hold` |
| `delivery_customer`, `pickup_by_consignee` | `delivered` |
| `delivery_shop` | `ready_for_pickup` |
| `error_pickup` | `delivery_failed` |
| `error_return`, `no_pickup_by_consignee` | `return_to_sender` |

**Acknowledgment (mandatory).** The endpoint returns
`<push><pushid>{pushid}</pushid><status>OK</status></push>` as
`application/xml` (the `WebhookEventDetails.response`/`response_format` seam). A
response that does **not** echo the `pushid` is treated by DPD as a failure and
buffered/retried for 48h — so the ack is returned even when no local tracker
matches, and a malformed `statusdate` is parsed `failsafe` rather than 500ing.

**Robustness rules** (why the hook/serializer look the way they do):
- *Unknown / missing `status`* → emit `status=None` (record the event, don't
  overwrite the stored status — never downgrade e.g. a delivered tracker).
- *Ambiguous match* — `tracking_number` is not unique; if `(tracking_number,
  carrier)` matches >1 tracker the update is a no-op (logged), never `.first()`.
- *Auth* — DPD push carries no signature/secret, so the endpoint is public and
  update-existing only (worst case: a status change on a parcel whose number is
  already known). Controls, in order of authority:
  1. **Ingress allow-list (authoritative)** — restrict the route's source to
     DPD's published IP (`213.95.42.108`) at the k8s NetworkPolicy / nginx layer,
     where the peer address is trustworthy.
  2. **Shared-secret token (app, defense-in-depth)** — `WEBHOOK_CARRIER_TOKENS`
     ({carrier: secret}); when set, the request must present it as `?token=` or
     `X-Webhook-Token` (constant-time compared). ⚠️ Whether DPD preserves an
     existing query string when it appends `?pushid=…` is unconfirmed — verify
     before relying on a query token; the header form is unaffected.
  3. **App source-IP allowlist (defense-in-depth)** — `WEBHOOK_CARRIER_IP_ALLOWLIST`.
     The client IP is the real TCP peer (`REMOTE_ADDR`) unless
     `WEBHOOK_TRUSTED_PROXY_COUNT > 0`, in which case the n-th X-Forwarded-For
     entry **from the right** is used; the left-most (client-supplied) value is
     never trusted. Set the proxy count to match the ingress depth, else a
     configured allowlist fails closed.

  With neither token nor allowlist set the endpoint logs a warning and stays open
  (update-existing-only) — configure at least the ingress control in production.

**Downstream.** `update_tracker` → `post_save(Tracking)` → bridge track-hub
broadcast + outbound webhooks (the same path the pull flow uses).

## References

- **Vendor docs** (`vendor/`):
  - `METAAPI_CUSTOMER_DOCUMENTATION_1_2.pdf` — META-API customer documentation
  - `openapi_metaapi_shipping.yaml` / `meta-api-docs.json` — META shipping OpenAPI
  - `dpd-api.developer.guidelines-A4-20250115.pdf` — public-WS base URLs, dev guidelines
  - `LoginService_V2_0_C0.pdf`, `DepotDataService_V1_0.pdf` — SOAP services
  - DPD Product & Service List, April 2026 — SoCode source of truth
- **Live docs endpoint** — `{server_url}/meta-api-docs`.
- **Generated schemas** — `karrio/schemas/dpd_meta/*.py`. JSON request/response
  modules generated by `kcli codegen generate ... --no-nice-property-names`
  (camelCase preserved); the SOAP `webapi.py` by `generateDS` from
  `schemas/webapi.xsd`. DPD WSDLs are `elementFormDefault="unqualified"`
  (operation elements carry the service namespace prefix, child fields do not).
  Regenerate with `./bin/run-generate-on modules/connectors/dpd_meta` — never
  hand-edit.
