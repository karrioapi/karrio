# Chronopost integration — specification

Reference for the Chronopost connector. Chronopost is the French express
parcel arm of La Poste / DPDgroup. The integration speaks **SOAP 1.1 over
HTTP** to three separate CXF-hosted services (Quickcost, Shipping,
Tracking) on `https://ws.chronopost.fr`. Requests are hand-built SOAP
envelopes; responses are parsed as raw XML elements.

The **vendor source of truth** is the three WS-XSDs kept under
`schemas/` (`QuickcostServiceWS.xsd`, `ShippingServiceWS.xsd`,
`TrackingServiceWS.xsd`). Generated dataclasses under
`karrio/schemas/chronopost/*.py` are produced from those XSDs via
`generateDS`. Vendor API docs: <https://www.chrono-api.fr/docs/api/>.

This is a `status="beta"` connector (`karrio/plugins/chronopost/__init__.py`).

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Data flow](#data-flow)
3. [Endpoints](#endpoints)
4. [Authentication](#authentication)
5. [Supported operations](#supported-operations)
6. [Services](#services)
7. [Options](#options)
8. [Label types](#label-types)
9. [Data mapping](#data-mapping)
10. [Wire-shape invariants & quirks](#wire-shape-invariants--quirks)
11. [Tracking](#tracking)
12. [Error parsing](#error-parsing)
13. [References](#references)

---

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio RateRequest / ShipmentRequest /
│   (karrio core)         │   TrackingRequest / ShipmentCancelRequest
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  providers/chronopost   │   Pure data transforms. No HTTP, no side effects.
│   rate.py               │   Unified model → SOAP envelope (lib.Envelope),
│   shipment/create.py    │   XML element → unified model.
│   shipment/cancel.py    │
│   tracking.py           │   Each builder wraps a generated schema object
│   error.py              │   in lib.Envelope/lib.Body and serializes with
│   units.py              │   lib.envelope_serializer (per-service namespace).
│   utils.py              │
│   i18n.py               │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ mappers/chronopost/     │   HTTP transport only.
│   proxy.py              │   - POST text/xml; charset=utf-8
│   settings.py           │   - one URL path per SOAP service
│   mapper.py (generated) │   - tracking fans out concurrently
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────────────────────────┐
│  Chronopost SOAP services (ws.chronopost.fr) │
│  ───────────────────────────────────────────│
│  QuickcostServiceWS   calculateProducts      │   rating
│  ShippingServiceWS    shippingMultiParcelV5  │   label creation
│  TrackingServiceWS    trackSkybillV2         │   tracking
│                       cancelSkybill          │   cancellation
└─────────────────────────────────────────────┘
```

**Key architectural choices:**

- **Three distinct SOAP services**, each on its own URL path and its own
  XML namespace (`cxf.quickcost…`, `cxf.shipping…`, `cxf.tracking…`).
  Cancellation rides the **Tracking** service, not the Shipping service.
- **Single-parcel only.** `shipment_request` calls
  `lib.to_packages(...).single`; `numberOfParcel=1`, `bulkNumber=1`,
  `multiParcel="N"`. There is no multi-piece fan-out on shipment.
- **Tracking fans out per number.** One SOAP envelope per tracking
  number, dispatched concurrently via `lib.run_concurently`, then the
  responses are parsed as a list.
- **Static catalog from CSV.** Service levels are loaded at import time
  from `services.csv` (`DEFAULT_SERVICES = load_services_from_csv()`);
  there is no live product/catalog fetch.
- **Generated schemas** — `karrio/schemas/chronopost/*.py` is generated
  from the XSDs with `generateDS`. Don't hand-edit; regenerate via
  the `generate` script / `./bin/run-generate-on modules/connectors/chronopost`.

## Data flow

### Rate (one SOAP call)

```
RateRequest                              QuickcostServiceWS
     │                                          │
     ├─► rate_request                            │
     │     lib.to_address(shipper/recipient)     │
     │     lib.to_packages(...).single           │
     │     build calculateProducts{              │
     │       accountNumber, password,            │
     │       depCountryCode, arrCountryCode,     │
     │       depZipCode, arrZipCode, arrCity,    │
     │       type_="M", weight/H/L/W }           │
     │                                           │
     │   ── POST /quickcost-cxf/QuickcostServiceWS ─►│
     │                                           │
     │   ◄── return{ errorCode, productList[]{   │
     │          productCode, amountTTC,          │
     │          amountTVA } } ───────────────────│
     │                                           │
     ├─► parse_rate_response:                     │
     │     one RateDetails per productList        │
     │       where amount > 0.0                   │
     │     productCode → ShippingService          │
     │     amountTTC   → total_charge             │
     │     amountTVA   → extra_charges["TVA"]      │
     ▼                                           ▼
list[RateDetails]                          (no further call)
```

### Shipment create (one SOAP call)

```
ShipmentRequest                          ShippingServiceWS
     │                                          │
     ├─► shipment_request                        │
     │     lib.to_packages(...).single           │
     │       (required=["weight"])               │
     │     build shippingMultiParcelV5{          │
     │       headerValue (account/idEmit),       │
     │       shipperValue, customerValue,        │
     │       recipientValue, refValue,           │
     │       skybillValue (product, weight,      │
     │         COD, insurance, customs, date),   │
     │       skybillParamsValue (label mode),    │
     │       password, numberOfParcel=1,         │
     │       version="2.0", multiParcel="N" }    │
     │                                           │
     │   ── POST /shipping-cxf/ShippingServiceWS ──►│
     │                                           │
     │   ◄── return{ errorCode, errorMessage,    │
     │          resultMultiParcelValue{          │
     │            skybillNumber,                 │
     │            pdfEtiquette (base64 bytes) }} ─│
     │                                           │
     ├─► parse_shipment_response:                 │
     │     skybillNumber → tracking_number        │
     │                   → shipment_identifier    │
     │     pdfEtiquette  → b64 → docs.label        │
     │     tracking_url.format(skybillNumber)     │
     ▼                                           ▼
ShipmentDetails                            (no further call)
```

### Cancel (TrackingServiceWS)

`cancelSkybill{ accountNumber, password, language, skybillNumber }` is
POSTed to `/tracking-cxf/TrackingServiceWS`. `shipment_identifier`
(the skybill number from create) is the cancel key. Success is inferred
from the **absence of errors** (`success = len(errors) == 0`).

## Endpoints

Single host: `https://ws.chronopost.fr` (`Settings.server_url`). There is
no separate sandbox host in the connector — `test_mode` does not switch
the URL.

| Purpose | Service | Method | Path | SOAP operation |
|---|---|---|---|---|
| Rate | Quickcost | POST | `/quickcost-cxf/QuickcostServiceWS` | `calculateProducts` |
| Create shipment | Shipping | POST | `/shipping-cxf/ShippingServiceWS` | `shippingMultiParcelV5` |
| Cancel shipment | Tracking | POST | `/tracking-cxf/TrackingServiceWS` | `cancelSkybill` |
| Tracking | Tracking | POST | `/tracking-cxf/TrackingServiceWS` | `trackSkybillV2` |

All calls use `Content-Type: text/xml; charset=utf-8` and HTTP `POST`
(`proxy._send_request`). SOAP envelope namespaces per service:

| Service | Envelope namespace (`cxf`) |
|---|---|
| Quickcost | `http://cxf.quickcost.soap.chronopost.fr/` |
| Shipping | `http://cxf.shipping.soap.chronopost.fr/` |
| Tracking | `http://cxf.tracking.soap.chronopost.fr/` |

The customer-facing tracking link is
`https://www.chronopost.fr/tracking-no-cms/suivi-page?listeNumerosLT={skybillNumber}`
(`Settings.tracking_url`).

## Authentication

There is **no token exchange**. Credentials are passed inline in each
SOAP body / header:

- **`account_number`** + **`password`** — sent in the request body
  (`calculateProducts.accountNumber/password`,
  `shippingMultiParcelV5.password`, `cancelSkybill.accountNumber/password`)
  and in `headerValue` on shipment.
- **`id_emit`** — emitter id, default `"CHRFR"`; sent inside
  `headerValue` on shipment.
- **`language`** — `LanguageEnum` (`en_GB` | `fr_FR`, default `en_GB`);
  sent on tracking and cancel requests.
- **`account_country_code`** — default `"FR"` (settings only).

Settings live in `karrio/mappers/chronopost/settings.py` (attrs) backed
by `karrio/providers/chronopost/utils.py` (`Settings`). `header_value`
returns the generated `headerValue(accountNumber, idEmit)` object.

## Supported operations

| Operation | Wired | Notes |
|---|---|---|
| Rate | yes | `calculateProducts`; products with `amount > 0` only |
| Shipment create | yes | single parcel; returns label (PDF/ZPL/…) |
| Shipment cancel | yes | via TrackingServiceWS `cancelSkybill` |
| Tracking | yes | per-number concurrent fan-out |
| Pickup | no | not implemented |
| Manifest / document upload | no | not implemented |

## Services

`provider_units.ShippingService` — karrio code → Chronopost
`productCode` (the wire value). On shipment the product code is
zero-padded to 2 digits (`product_code.zfill(2)`).

| karrio service code | wire `productCode` |
|---|---|
| `chronopost_retrait_bureau` | `0` |
| `chronopost_13` | `1` |
| `chronopost_10` | `2` |
| `chronopost_18` | `16` |
| `chronopost_relais` | `86` |
| `chronopost_express_international` | `17` |
| `chronopost_premium_international` | `37` |
| `chronopost_classic_international` | `44` |

`DEFAULT_SERVICES` (service levels with weight/dimension limits and zone
rates) is loaded from `services.csv`. Columns:
`service_code, service_name, zone_label, country_codes, min_weight,
max_weight, max_length, max_width, max_height, rate, currency,
transit_days, domicile, international`. The CSV `service_code` is the
wire code and is mapped back to the karrio name via
`ShippingService.map(...).name_or_key`. Rates in the CSV are placeholder
`0.0`; the real prices come from the live `calculateProducts` call.

Currently populated in `services.csv`: `chronopost_13`, `chronopost_18`,
`chronopost_relais`, `chronopost_express_international`,
`chronopost_classic_international`. (If the CSV is absent, a single
`chronopost_13` fallback ServiceLevel is returned.)

Service display names are localized in `i18n.py`
(`SERVICE_NAME_TRANSLATIONS`, `OPTION_NAME_TRANSLATIONS`).

## Options

`provider_units.ShippingOption` — karrio option → wire code. These map
onto the `skybillValue.service` delivery-option concept; all carry meta
`category="DELIVERY_OPTIONS", configurable=True, service_level=True`.

| karrio option | wire code |
|---|---|
| `chronopost_delivery_normal` | `0` |
| `chronopost_delivery_on_monday` | `1` |
| `chronopost_delivery_on_saturday` | `6` |
| `saturday_delivery` (unified) | `6` (alias of `chronopost_delivery_on_saturday`) |

`shipping_options_initializer` filters incoming options to keys present
in `ShippingOption`.

Standard karrio options consumed in `skybillValue` on create:

| karrio option | wire field | condition |
|---|---|---|
| `cash_on_delivery` | `codValue` | set when present |
| `currency` | `codCurrency` | sent when `cash_on_delivery` is set |
| `insurance` | `insuredValue` | set when present |
| `currency` | `insuredCurrency` | sent when `insurance` is set |
| `shipment_date` | `shipDate` | `lib.to_date(...)` else `now()` |

## Label types

`provider_units.LabelType` — selected via `payload.label_type` (default
`"PDF"`), emitted as `skybillParamsValue.mode`.

| karrio / code | wire value |
|---|---|
| `PDF` (unified) | `PDF` |
| `ZPL` (unified) | `ZPL300` |
| `PPR_LABEL` | `PPR` |
| `SPD_LABEL` | `SPD` |
| `Z2D_LABEL` | `Z2D` |
| `THE_LABEL` | `THE` |
| `XML_LABEL` | `XML` |
| `XML2D_LABEL` | `XML2D` |
| `THEPSG_LABEL` | `THEPSG` |
| `ZPLPSG_LABEL` | `ZPLPSG` |
| `ZPL300_LABEL` | `ZPL300` |

The label returned in `resultMultiParcelValue.pdfEtiquette` is raw bytes;
`create.py` base64-encodes it into `docs.label`.

## Data mapping

### Rate request — `calculateProducts`

```
karrio                          Chronopost calculateProducts
──────                          ─────────────────────────────
settings.account_number  ───►   accountNumber
settings.password        ───►   password
shipper.country_code     ───►   depCountryCode
shipper.postal_code      ───►   depZipCode
recipient.country_code   ───►   arrCountryCode
recipient.postal_code    ───►   arrZipCode
recipient.city           ───►   arrCity
(constant)               ───►   type = "M"
package.weight.KG        ───►   weight
package.height.CM        ───►   height
package.length.CM        ───►   length
package.width.CM         ───►   width
(none)                   ───►   shippingDate = None
```

### Shipment — address blocks

Three address blocks are sent. **`shipperValue`** ← `payload.shipper`;
**both `customerValue` and `recipientValue`** ← `payload.recipient`
(the recipient address is duplicated into the "customer" block).

```
karrio Address                 shipperValue / customerValue / recipientValue
──────────────                 ─────────────────────────────────────────────
street (line1)         ───►    {shipper,customer,recipient}Adress1
address_line2          ───►    …Adress2
city                   ───►    …City
person_name            ───►    …ContactName
country_code           ───►    …Country
country_name           ───►    …CountryName
email                  ───►    {shipper,customer,recipient}Email
phone_number           ───►    …MobilePhone
company_name           ───►    …Name   (and …Name2 — company duplicated)
(constant 0)           ───►    …PreAlert = 0
(constant "M")         ───►    shipperCivility / customerCivility
postal_code            ───►    …ZipCode
```

Note: `recipientValue` has no civility field; `customerValue.printAsSender`
is `None`.

### Shipment — `refValue`

| karrio | wire |
|---|---|
| `payload.reference` | `shipperRef` |
| (none) | `recipientRef`, `customerSkybillNumber`, `PCardTransactionNumber` = None |

### Shipment — `skybillValue`

```
karrio / source                         skybillValue field
───────────────                         ──────────────────
ShippingService(payload.service)  ───►  productCode  (zfill(2))
package.weight.KG                 ───►  weight
WeightUnit.KG ("KGM")             ───►  weightUnit
options.cash_on_delivery          ───►  codValue
options.currency (if COD set)     ───►  codCurrency
options.insurance                 ───►  insuredValue
options.currency (if insured)     ───►  insuredCurrency
customs.duty.currency /           ───►  customsCurrency  (only if customs)
  options.currency
customs.duty.declared_value /     ───►  customsValue     (only if customs)
  options.declared_value
CustomsContentType(content_type)  ───►  objectType (DOC | MAR; default MAR)
shipping_date                     ───►  shipDate ("%Y-%m-%dT%H:%M:%S")
(constant)                        ───►  evtCode = "DC"
(constant)                        ───►  service = "0"
(constant)                        ───►  shipHour = "10"
(constant)                        ───►  bulkNumber = 1
(none)                            ───►  masterSkybillNumber, skybillRank,
                                        latitude, longitude, port*, qualite,
                                        source = None
```

Top-level `shippingMultiParcelV5` constants: `modeRetour=1`,
`numberOfParcel=1`, `version="2.0"`, `multiParcel="N"`, `esdValue=None`.

### Customs content type

`provider_units.CustomsContentType` — `objectType`:

| karrio `content_type` | wire |
|---|---|
| `documents` / `document` | `DOC` |
| `merchandise` / `marchandise` | `MAR` |
| (default when none) | `MAR` |

### Shipment response

```
resultMultiParcelValue.skybillNumber  ───►  tracking_number
                                       ───►  shipment_identifier
resultMultiParcelValue.pdfEtiquette   ───►  base64 → docs.label
tracking_url.format(skybillNumber)    ───►  meta.carrier_tracking_link
```

## Wire-shape invariants & quirks

- **Recipient address is sent twice.** Both `customerValue` and
  `recipientValue` are populated from `payload.recipient`. Chronopost's
  model distinguishes "customer" (account holder of record) from
  "recipient"; the connector currently sends the same recipient data to
  both.
- **`productCode` is zero-padded to two digits** on shipment
  (`product_code.zfill(2)`) — e.g. service `1` → `"01"`, `2` → `"02"`.
  The rate response `productCode` is matched without padding via
  `ShippingService.map`.
- **`codCurrency` / `insuredCurrency` only ride when their value is
  present.** Each currency field is gated on the corresponding
  `*.state is not None` check so an empty COD/insurance doesn't emit a
  bare currency.
- **Customs fields only when `payload.customs` is present.**
  `customsCurrency` / `customsValue` are `None` otherwise.
- **Cancellation goes through TrackingServiceWS**, not the Shipping
  service — `cancel_shipment` POSTs `cancelSkybill` to
  `/tracking-cxf/TrackingServiceWS`.
- **Rate filtering:** only `productList` entries with `amount > 0.0` are
  surfaced as `RateDetails`. Chronopost returns the full product matrix
  with `0.0` for products not available on the lane.
- **TVA as an extra charge:** the rate parser exposes `amountTVA` as an
  `extra_charges` entry named `"TVA"` (only if `> 0`); `amountTTC`
  (tax-incl.) is the `total_charge`. Currency is hardcoded `"EUR"`.
- **Single host, no sandbox switch:** `test_mode` does not change the
  endpoint (`server_url` is constant `https://ws.chronopost.fr`).

## Tracking

`trackSkybillV2{ language, skybillNumber }` per tracking number, fanned
out concurrently. The response `return.listEventInfoComp` carries
`events[]` plus the `skybillNumber`.

```
listEventInfoComp.skybillNumber  ───►  tracking_number
events[i].code                   ───►  event.code
events[i].eventLabel             ───►  event.description
events[i].eventDate              ───►  event.date / time / timestamp
events[i].officeLabel            ───►  event.location
events[i].code matched against TrackingIncidentReason ─► event.reason
```

- **Delivered flag:** `delivered = True` when any event has `code == "D"`.
- **`TrackingInfo`:** `customer_name` ← delivery event's
  `infoCompList.name`; `shipment_destination_postal_code` ← delivery
  event's `zipCode`; `carrier_tracking_link` ← `tracking_url`.
- **Incident reasons** (`provider_units.TrackingIncidentReason`) map
  carrier exception codes to normalized karrio reasons. The lookup tests
  `event.code in reason.value`:

| normalized reason | matched codes |
|---|---|
| `carrier_damaged_parcel` | `DMG`, `DAMAGE`, `DAMAGED` |
| `carrier_sorting_error` | `MISROUTE`, `TRI` |
| `carrier_parcel_lost` | `LOST`, `PERDU` |
| `carrier_vehicle_issue` | `DELAY`, `RETARD` |
| `consignee_refused` | `REFUSED`, `REF`, `REFUSE` |
| `consignee_business_closed` | `CLOSED`, `FERME` |
| `consignee_not_home` | `NOTHOME`, `NH`, `ABSENT` |
| `consignee_incorrect_address` | `BADADDR`, `INCORRECT`, `ADRESSE` |
| `consignee_access_restricted` | `NOACCESS`, `ACCES` |
| `customs_delay` | `CUSTOMS`, `CUSTOMSHOLD`, `DOUANE` |
| `customs_documentation` | `CUSTOMSDOC`, `DOUANE_DOC` |
| `customs_duties_unpaid` | `CUSTOMS_UNPAID`, `TAXES` |
| `weather_delay` | `WEATHER`, `METEO` |
| `delivery_exception_hold` | `HOLD`, `ONHOLD`, `RETENU` |
| `delivery_exception_undeliverable` | `UNDELIVERABLE`, `NON_LIVRABLE` |
| `unknown` | (empty) |

> Note: the connector does not map Chronopost event codes to a unified
> tracking `status` enum — only the boolean `delivered` is derived (from
> code `D`) and per-event incident reasons are normalized.

> Note: the date format strings used by the tracking parser
> (`"%Y-%m%dT%H%:%M:%S"`) are malformed relative to the wire
> (`2022-06-19T13:47:53+02:00`), so `lib.fdate`/`flocaltime`/
> `fiso_timestamp` fall back to the raw value rather than reformatting.

## Error parsing

`error.parse_error_response` finds every `return` element (typed as
`resultMultiParcelExpeditionValue`) and emits a `Message` for each whose
`errorCode != 0`.

```
SOAP <return>                  karrio Message
─────────────                  ──────────────
errorCode  ───►                code     (only when != 0)
errorMessage ───►              message
```

`errorCode == 0` is success / no error. The same shape is shared across
all four operations (`<return><errorCode/><errorMessage/>…</return>`);
shipment and cancel both treat a non-zero `errorCode` as the failure
signal, and cancel infers success purely from `len(errors) == 0`.

Observed error examples from fixtures: rate `3 "invalid account or
password"`; shipment `33 "Invalid accesColis account number"`; cancel
`2 "the parcel doesn't match account or parcel information not found"`;
tracking `1 "System Error"`.

## References

- **Vendor API docs** — <https://www.chrono-api.fr/docs/api/>
- **Vendor site** — <https://www.chronopost.fr/en>
- **WS-XSD source of truth** — `schemas/QuickcostServiceWS.xsd`,
  `schemas/ShippingServiceWS.xsd`, `schemas/TrackingServiceWS.xsd`
- **Generated schemas** — `karrio/schemas/chronopost/{quickcostservice,
  shippingservice,trackingservice}.py` are generated from the XSDs with
  `generateDS` (see the `generate` script). Do **not** hand-edit;
  regenerate with `./bin/run-generate-on modules/connectors/chronopost`.
- **Service-level catalog** — `karrio/providers/chronopost/services.csv`.
- **Localization** — `karrio/providers/chronopost/i18n.py`.
