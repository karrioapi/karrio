# DPD integration — specification

Reference for the DPD connector. DPD exposes a **SOAP 1.1 / XML** web-service
suite (the "DPD web-connect" / Login + Shipment + ParcelLifeCycle services).
This connector wires **shipment creation**, **tracking**, and a **CSV-driven
static rate sheet** (via karrio's universal rating mixin). It targets the
**Benelux** clusters — `wsshipper.dpd.be` and `wsshipper.dpd.nl` — selected by
the account country code.

The **vendor source of truth** is the WSDL/XSD set under `schemas/*.xsd`
(`Authentication20`, `LoginServiceV21`, `ShipmentServiceV33`,
`ParcelLifecycleServiceV20`, plus `EndOfDayServiceV10` and
`ParcelShopFinderServiceV50`, which are vendored but not yet wired). The Python
types under `karrio/schemas/dpd/*.py` are **generated** from those XSDs with
`generateDS` — never hand-edit (see [References](#references)).

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Data flow](#data-flow)
3. [Endpoints](#endpoints)
4. [Authentication](#authentication)
5. [Supported operations](#supported-operations)
6. [Services](#services)
7. [Options](#options)
8. [Data mapping](#data-mapping)
9. [International / customs](#international--customs)
10. [Tracking](#tracking)
11. [Error parsing](#error-parsing)
12. [References](#references)

---

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio ShipmentRequest / TrackingRequest /
│   (karrio core)         │   RateRequest / CustomsInfo
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  providers/dpd          │   Pure data transforms.
│   shipment/create.py    │   Unified model → typed DPD SOAP body,
│   tracking.py           │   typed DPD response → unified model.
│   error.py              │   No HTTP, no side effects.
│   units.py              │   ShippingService, ShippingOption, Incoterm,
│   utils.py (Settings)   │   CustomsContentType, TrackingStatus,
│                         │   TrackingIncidentReason; CSV service loader.
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  mappers/dpd            │   HTTP transport only.
│   proxy.py              │   - SOAP envelope POST (text/xml + SOAPAction)
│   settings.py           │   - token caching (LoginService getAuth)
│   mapper.py             │   - [AUTH_TOKEN] placeholder substitution
│                         │   - concurrent tracking fan-out
│                         │   rate.py → karrio universal RatingMixin
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  DPD SOAP services      │
│  ─────────────────────  │
│  LoginService V2.1      │   getAuth → authToken (cached)
│  ShipmentService V3.3   │   storeOrders → labels + parcel numbers
│  ParcelLifeCycle V2.0   │   getTrackingData → status events
│  (EndOfDay V1.0,        │   vendored XSDs, NOT wired
│   ParcelShopFinder V5.0)│
└─────────────────────────┘
```

**Key architectural choices:**

- **No live rate API.** DPD's connector has no carrier rate endpoint; rating is
  served by karrio's `universal.mappers.rating_proxy.RatingMixin` over a static
  rate sheet built from `karrio/providers/dpd/services.csv`. `Settings`
  subclasses `RatingMixinSettings`, the proxy subclasses `RatingMixinProxy`, and
  `mapper.py` delegates `create_rate_request` / `parse_rate_response` to the
  universal provider.
- **Token-then-call** for every shipment / tracking call. `proxy.authenticate()`
  hits LoginService once, caches the token per connection, then substitutes the
  `[AUTH_TOKEN]` placeholder baked into the serialized SOAP body.
- **SOAP envelopes built by hand** with `lib.Envelope` / `lib.Header` /
  `lib.Body` + `lib.envelope_serializer`, with explicit namespace prefixes per
  service. The auth header (`Authentication/2.0`) is a separate XSD from the
  service body XSD.
- **Generated schemas** — `karrio/schemas/dpd/*.py` is generated from the XSDs
  with `generateDS` via the connector's `generate` script.

Plugin metadata (`karrio/plugins/dpd/__init__.py`): `id="dpd"`, `label="DPD"`,
`status="beta"`, `is_hub=False`, `has_intl_accounts=True`.

## Data flow

### Shipment creation (auth + storeOrders)

```
ShipmentRequest                                    DPD SOAP
     │                                                │
     ├─► shipment_request()                           │
     │     to_address(shipper/recipient)              │
     │     to_packages(parcels)                       │
     │     map service → product code (CL/E10/…)      │
     │     to_shipping_options()                      │
     │     to_customs_info()  (when intl)             │
     │                                                │
     ├─► lib.Envelope{ Header: authentication,        │
     │                 Body: storeOrders } → XML      │
     │     (authToken="[AUTH_TOKEN]" placeholder)     │
     │                                                │
     │   proxy.create_shipment:                       │
     │     1. authenticate() ── POST LoginService ───►│
     │        ◄── return.authToken (cached) ──────────│
     │     2. body.replace("[AUTH_TOKEN]", token)     │
     │     ─── POST ShipmentService/V3_3 ────────────►│
     │         SOAPAction: …/storeOrders              │  validate
     │                                                │  label gen
     │   ◄── StoreOrdersResponseDto33{                │
     │         orderResult.parcellabelsPDF,           │
     │         shipmentResponses[].mpsId,             │
     │         …parcelInformation[].parcelLabelNumber}│
     │                                                │
     ├─► _extract_details:                            │
     │     parcelLabelNumber → tracking_number        │
     │     mpsId             → shipment_identifier    │
     │     parcellabelsPDF   → b64 docs.label         │
     ▼                                                ▼
ShipmentDetails                              (single create call)
```

### Tracking (auth + concurrent getTrackingData)

```
TrackingRequest                                    DPD SOAP
     │                                                │
     ├─► tracking_request()                           │
     │     one Envelope per tracking number,          │
     │     getTrackingData{ parcelLabelNumber }       │
     │                                                │
     │   proxy.get_tracking:                           │
     │     authenticate() once (shared token)          │
     │     lib.run_concurently over each envelope:     │
     │       body.replace("[AUTH_TOKEN]", token)       │
     │     ─── POST ParcelLifeCycleService/V2_0 ──────►│  (per number)
     │         SOAPAction: …/getTrackingData          │
     │                                                │
     │   ◄── trackingresult{ statusInfo[] } ──────────│
     │                                                │
     ├─► _extract_details (per number):               │
     │     statusInfo[] reversed → events[]           │
     │     last status → TrackingStatus               │
     │     status "Delivered" present → delivered     │
     ▼                                                ▼
list[TrackingDetails]                  (1 HTTP call per tracking number)
```

## Endpoints

Test mode and production are selected by `account_country_code`:

| Country | Test (`test_mode=True`) | Production |
|---|---|---|
| `BE` (default) | `https://shipperadmintest.dpd.be/PublicApi` | `https://wsshipper.dpd.be` |
| `NL` | `https://shipperadmintest.dpd.nl/PublicApi` | `https://wsshipper.dpd.nl` |

All calls are SOAP POSTs under that base:

| Purpose | Method | Path (under `server_url`) | SOAPAction |
|---|---|---|---|
| Authenticate | POST | `/soap/services/LoginService/V2_1` | `…/LoginService/2.1/getAuth` |
| Create shipment | POST | `/soap/services/ShipmentService/V3_3` | `…/ShipmentService/3.3/storeOrders` |
| Tracking | POST | `/soap/services/ParcelLifeCycleService/V2_0` | `…/ParcelLifeCycleService/2.0/getTrackingData` |
| Rating | — | (no HTTP — static CSV rate sheet via universal RatingMixin) | — |

Every call sends `Content-Type: text/xml;charset=UTF-8` plus the matching
`SOAPAction` header. The auth call uses `max_retries=2`.

The end-customer **tracking link** (`Settings.tracking_url`) is
`https://www.dpdgroup.com/{country}/mydpd/my-parcels/track?lang={lang}&parcelNumber={}`,
where `country` is the lowercased account country and `lang` is the first
segment of `message_language` (e.g. `en` from `en_EN`).

## Authentication

`LoginService` `getAuth` token grant. The proxy posts `delisId` + `password` +
`messageLanguage`, reads `return.authToken` / `return.authTokenExpires`
(`%Y-%m-%dT%H:%M:%S.%f`) / `return.depot`, and caches the token via
`connection_cache.thread_safe` keyed by `dpd|<delis_id>|<password>`, refreshing
when within `buffer_minutes=30` of expiry.

Subsequent shipment / tracking SOAP bodies are built with the literal
placeholder `authToken="[AUTH_TOKEN]"` in the `authentication` SOAP header; the
proxy does a string `.replace("[AUTH_TOKEN]", token)` on the serialized request
just before sending. Auth failures surface as `ParsedMessagesError` (the auth
flow raises rather than returning an empty token).

```
delis_id + password                      ┌──────────────────┐
       │                                 │ connection_cache │
       ▼                                 │  thread_safe     │
┌──────────────┐    miss / expired       │                  │
│ authenticate │◄────────────────────────│ key:             │
│              │                         │  dpd|<delis_id>| │
│              │    cache hit            │  <password>      │
│              │────────────────────────►│  buffer 30 min   │
└──────┬───────┘                         └──────────────────┘
       │ POST LoginService/V2_1 getAuth
       ▼
   return.authToken ──► substituted into [AUTH_TOKEN] of each SOAP body
```

### Connection settings (`mappers/dpd/settings.py`)

| Field | Required | Default | Notes |
|---|---|---|---|
| `delis_id` | yes | — | DPD DELIS customer id |
| `password` | yes | — | account password |
| `depot` | no | `None` | sending depot; sent as `generalShipmentData.sendingDepot` |
| `message_language` | no | `"en_EN"` | sent on getAuth + auth header; drives tracking-link `lang` |
| `account_country_code` | no | `"BE"` | selects `.be` vs `.nl` server URL and default service set |
| `test_mode` | no | `False` | selects sandbox base URL |
| `services` | no | CSV defaults | rate-sheet service levels (universal rating) |

`shipping_services` returns the configured `services` if any, else
`DEFAULT_NL_SERVICES` for `NL`, else `DEFAULT_SERVICES` (loaded from
`services.csv`).

## Supported operations

| Operation | Wired? | Notes |
|---|---|---|
| Rate | ✅ | Static CSV rate sheet via universal `RatingMixin` — no carrier rate API |
| Shipment create | ✅ | `storeOrders`; single create call returns label PDF + parcel numbers |
| Shipment cancel | ❌ | No `cancel.py`; no void operation wired |
| Tracking | ✅ | `getTrackingData`, one call per tracking number, run concurrently |
| Pickup | ❌ | Not wired |
| End-of-day manifest | ❌ | `EndOfDayServiceV10.xsd` vendored but not wired |
| ParcelShop finder | ❌ | `ParcelShopFinderServiceV50.xsd` vendored but not wired |

Multi-piece shipments are supported: each parcel becomes a `parcels[]` entry on
a single `order`. `_extract_details` flattens `parcelInformation` across
`shipmentResponses`, surfaces the **first** parcel number / `mpsId` as the
primary `tracking_number` / `shipment_identifier`, and lists all of them in
`meta.tracking_numbers` / `meta.shipment_identifiers`.

## Services

DPD products map onto the `product` field of `generalShipmentData`. The wire
code is `ShippingService.map(payload.service).value_or_key`.

| karrio service code | Wire `product` |
|---|---|
| `dpd_cl` | `CL` |
| `dpd_express_10h` | `E10` |
| `dpd_express_12h` | `E12` |
| `dpd_express_18h_guarantee` | `E18` |
| `dpd_express_b2b_predict` | `B2B MSG option` |
| `dpd_home_europe` | `CL` (alias) |
| `dpd_shop_europe` | `CL` (alias) |
| `dpd_express_europe` | `CL` (alias) |
| `dpd_express_guarantee` | `CL` (alias) |
| `dpd_express_international` | `CL` (alias) |

The rate-sheet zone/weight matrix (`services.csv`) ships `CL` across BE/DE and
EU zones 1A–1G, plus `E10`/`E12`/`E18`/`B2B MSG option` for BE/DE. All sample
rates are `0.0` placeholders; weight cap is `31.5` kg, max length `175` cm. The
CSV loader groups rows by service into `models.ServiceLevel` with `ServiceZone`
entries (per-country `country_codes`, weight band, `transit_days` taken from the
low end of a `m-n` range).

## Options

`ShippingOption` (the active, non-commented entries) feed
`productAndServiceData`. The first `OptionEnum` positional arg is the wire key.

| karrio option | Wire field | Type | Notes |
|---|---|---|---|
| `dpd_order_type` | `orderType` | str | defaults to `"consignment"` when unset |
| `dpd_saturday_delivery` / `saturday_delivery` | `saturdayDelivery` | bool | `category=DELIVERY_OPTIONS`; `saturday_delivery` is the unified alias |
| `dpd_ex_works_delivery` | `exWorksDelivery` | bool | `category=DELIVERY_OPTIONS` |
| `dpd_tyres` | `tyres` | bool | |
| `dpd_parcel_shop_delivery` | `parcelShopDelivery` | str | `category=PUDO`; parcel-shop id (see below) |

Several options are scaffolded but **commented out** in `units.py`
(`dpd_guarantee`, `dpd_personal_delivery`, `dpd_pickup`, `dpd_predict`,
`dpd_personal_delivery_notification`, `dpd_proactive_notification`,
`dpd_delivery`, `dpd_invoice_address`, `dpd_country_specific_service`). The
corresponding `productAndServiceData` fields (`guarantee`, `personalDelivery`,
`pickup`, `predict`, …) are always sent as `None`.

### ParcelShop delivery + notification

When `dpd_parcel_shop_delivery` is set, `parcelShopDelivery` carries
`parcelShopId` plus an optional `parcelShopNotification`:

- A notification block is emitted only if any of `email_notification_to`,
  `recipient.email`, or `recipient.phone_number` is present.
- `channel` is `"3"` when neither `email_notification_to` nor `recipient.email`
  is present (i.e. falling back to phone), otherwise `"1"`.
- `value` is `email_notification_to` → `recipient.email` → `recipient.phone_number`.
- `language` is hardcoded `"EN"`.

`PackagingType` collapses every unified packaging preset onto the single DPD
code `PACKAGE`.

## Data mapping

### Address — karrio `Address` → DPD `address`

The same `dpd.address` shape is used for `sender`, `recipient`, and the customs
`commercialInvoiceConsignee` / `commercialInvoiceConsignor`.

```
karrio Address                       DPD address
─────────────────                    ───────────
person_name (or company_name) ──►    name1
company_name                  ──►    name2
address_line1                 ──►    street
street_number                 ──►    houseNo
address_line2                 ──►    street2
state_code                    ──►    state
country_code                  ──►    country
postal_code                   ──►    zipCode
city                          ──►    city
residential                   ──►    type_ ("P" residential, else "B")
person_name                   ──►    contact
phone_number                  ──►    phone
email                         ──►    email
tax_id (recipient)            ──►    vatNumber
```

Unused address fields are explicitly sent as `None` (`gln`, `customerNumber`,
`fax`, `comment`, `iaccount`, `eoriNumber`, `idDocType`, `idDocNumber`,
`webSite`, `referenceNumber`, `destinationCountryRegistration`).

### Parcel — karrio package → DPD `parcels`

```
karrio package                       DPD parcels[i]
──────────────                       ──────────────
parcel.reference_number       ──►    customerReferenceNumber1
volume.m3                     ──►    volume
weight.KG                     ──►    weight
parcel.content                ──►    content
```

`weight` is always sent in **kg** (`pkg.weight.KG`); customs commodity weights
are converted to KG via `to_customs_info(..., weight_unit="KG")`.

### Shipment-level references / print options

```
payload.reference            ──►    generalShipmentData.mpsCustomerReferenceNumber1
settings.depot               ──►    generalShipmentData.sendingDepot
service code                 ──►    generalShipmentData.product
label_type (default "PDF")   ──►    printOptions.printerLanguage (via LabelType)
"A6"                         ──►    printOptions.paperFormat (hardcoded)
```

## International / customs

`is_intl` is `True` when shipper and recipient country codes differ. The
per-parcel `international` block is emitted only when `is_intl`; domestic
parcels send `international=None`.

```
karrio CustomsInfo                   DPD international
──────────────────                   ─────────────────
duty.declared_value / declared_value ─► customsAmount, customsAmountEx
duty.currency / options.currency   ──► customsCurrency, customsCurrencyEx
incoterm → CustomsContentType      ──► exportReason   (01 sale / 02 return / 03 gift)
incoterm → Incoterm                ──► customsTerms    (defaults "DAP")
content_description                ──► customsContent
invoice                            ──► customsInvoice
invoice_date (%Y-%m-%d → %Y%m%d)   ──► customsInvoiceDate
duty_billing_address               ──► commercialInvoiceConsignee (+ VAT/EORI)
shipper                            ──► commercialInvoiceConsignor
commodities[]                      ──► commercialInvoiceLine[]
```

Fixed wire constants on the `international` block:

| Field | Value | Meaning |
|---|---|---|
| `parcelType` | `False` | |
| `clearanceCleared` | `"N"` | |
| `prealertStatus` | `"S03"` | |
| `customsPaper` | `"A"` | |

### Incoterm — `customsTerms`

| karrio incoterm | DPD `customsTerms` |
|---|---|
| `DAP` | `06` |
| `DAP_enhanced` | `07` |

`Incoterm.map(...).value or "DAP"` — falls back to the literal string `"DAP"`
when the incoterm doesn't map to a DPD code.

### Export reason — `CustomsContentType` (`exportReason`)

| karrio content type | DPD code |
|---|---|
| `sale` | `01` |
| `return_replacement` | `02` |
| `gift` | `03` |
| `sample` (alias) | `01` |
| `merchandise` (alias) | `01` |
| `return_merchandise` (alias) | `02` |

### Commercial invoice line — `commercialInvoiceLine[]`

One `internationalLine` per commodity, sourced from `pkg.items` if present, else
`customs.commodities`:

```
hs_code (or sku)     ──► customsTarif, receiverCustomsTarif
sku                  ──► productCode
title (or description) ─► content
weight → KG          ──► grossWeight
enumerate index (1-based) ─► itemsNumber
value_amount         ──► amountLine
origin_country       ──► customsOrigin
```

Consignee VAT / EORI come from `customs.options.vatNumber` /
`customs.options.eoriNumber` (falling back to the duty-billing-address tax id);
consignor VAT is `shipper.tax_id`.

## Tracking

`getTrackingData` is called once per tracking number (the request builder
produces one envelope per number; `proxy.get_tracking` runs them through
`lib.run_concurently`). Responses with a `trackingresult` element become
tracking details; those without become error messages (carrying the queried
`tracking_number` in `details`).

`statusInfo[]` events are **reversed** before mapping (the API returns them
newest-first; karrio emits oldest-first). Per event: `code` ← `status`,
`location` ← `location.content`, `date`/`time`/`timestamp` parsed from
`date.content` with format `%m/%d/%Y %H:%M:%S %p`, `description` joins the
`description.content[]` children comma-separated. `delivered` is `True` when any
event has `status == "Delivered"`. The overall `status` is derived from the
**first** (newest) event's status, defaulting to `in_transit`.

### Status mapping (`TrackingStatus`)

| karrio status | DPD `status` values |
|---|---|
| `delivered` | `Delivered` |
| `in_transit` | `in_transit` (also the default fallback) |
| `ready_for_pickup` | `ParcelShop` |
| `delivery_failed` | `DeliveryFailure` |
| `out_for_delivery` | `Courier`, `ReturningFromDelivery` |

### Incident reason mapping (`TrackingIncidentReason`)

Each event also resolves a normalized `reason` from its `status` code. The
mapping covers carrier-caused (`DMG`/`DAMAGED`, `MISROUTED`,
`ADDRESS_NOT_FOUND`, `LOST`, `VEHICLE_ISSUE`), consignee-caused (`REFUSED`/
`REJECTED`, `BUSINESS_CLOSED`, `NOT_AVAILABLE`, `NOT_HOME`/`RECIPIENT_ABSENT`,
`INCORRECT_ADDRESS`/`WRONG_ADDRESS`, `ACCESS_RESTRICTED`), customs
(`CUSTOMS_DELAY`/`CUSTOMS_HOLD`, `CUSTOMS_DOCS`, `DUTIES_UNPAID`), and
weather/force-majeure (`WEATHER`, `NATURAL_DISASTER`) buckets, with `unknown` as
the empty fallback. These are normalized labels, not necessarily literal DPD
exception codes.

## Error parsing

`error.parse_error_response` walks the SOAP response for two shapes and returns
one `models.Message` per error:

1. **`detail` blocks** (e.g. `authenticationFault`) — read `errorCode` /
   `errorMessage` from each child of every `<detail>`.
2. **SOAP `Fault`** (when no `detail` present) — read `faultcode` /
   `faultstring`.

```
SOAP Response                  ┌──────────────────────────────┐
   │                           │ error.parse_error_response     │
   ├─► <detail> children? ───► │   code  ← errorCode            │
   │                           │   msg   ← errorMessage         │
   ├─► else <Fault>? ────────► │   code  ← faultcode            │
   │                           │   msg   ← faultstring          │
   ▼                           └──────────────┬───────────────┘
   {code, message}                            ▼
                                       list[Message]
```

Extra kwargs (e.g. `tracking_number=...` from the tracking parser) are attached
to `Message.details`. During authentication, any parsed message raises
`errors.ParsedMessagesError` so a bad login never silently yields a blank token.

A real DPD auth fault looks like:

```xml
<soap:Fault>
  <faultcode>soap:Server</faultcode>
  <faultstring>Fault occured</faultstring>
  <detail>
    <ns:authenticationFault xmlns:ns="http://dpd.com/common/service/types/Authentication/2.0">
      <errorCode>DELICOM_ERR_AUTHENTICATION</errorCode>
      <errorMessage>Authentication failure, check delisId and password.</errorMessage>
    </ns:authenticationFault>
  </detail>
</soap:Fault>
```

→ parsed (detail branch) as `code=DELICOM_ERR_AUTHENTICATION`,
`message="Authentication failure, check delisId and password."`.

## References

- **Vendor XSDs (authoritative)** — `schemas/*.xsd`:
  - `LoginServiceV21.xsd` — `getAuth` / `GetAuthResponseDto`
  - `Authentication20.xsd` — the `authentication` SOAP header
  - `ShipmentServiceV33.xsd` — `storeOrders` / `StoreOrdersResponseDto33`
  - `ParcelLifecycleServiceV20.xsd` — `getTrackingData` / `StatusInfo`
  - `EndOfDayServiceV10.xsd`, `ParcelShopFinderServiceV50.xsd` — vendored, not
    wired
- **Generated Python types** — `karrio/schemas/dpd/*.py`, produced by
  `generateDS --no-namespace-defs` from the XSDs (see the connector's `generate`
  script). **Do not hand-edit**; regenerate with
  `./bin/run-generate-on modules/connectors/dpd`.
- **Rate sheet** — `karrio/providers/dpd/services.csv` (zone/weight matrix
  consumed by `load_services_from_csv`). Rates are placeholders; replace per
  account.
- **Service / option display names (i18n)** — `karrio/providers/dpd/i18n.py`.
