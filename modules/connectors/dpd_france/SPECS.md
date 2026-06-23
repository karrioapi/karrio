# DPD France integration — specification

Reference for the `dpd_france` connector. DPD France does **not** use the
DPD-group "web-connect" SOAP suite that the sibling `dpd` connector targets;
it integrates the **cargoNET** platform's two **SOAP 1.1 / XML** ASMX
web-services: `EPrintWebservice` (shipment creation, cancellation, return,
pickup, GeoLabel printing) and `Webtrace_Service` (tracking). Both expose the
`http://www.cargonet.software` namespace. The connector wires shipment
create/cancel/return, pickup schedule/cancel, tracking, and a **CSV-driven
static rate sheet** (via karrio's universal rating mixin) — cargoNET has no
live rate endpoint.

The **vendor source of truth** is the two PDFs under `vendor/`
(`DPD France Shipping WebService - GeoLabel.pdf` v1.9a 02/2026 and
`DPD France Tracking WebService.pdf` v5.0 10/2025) plus the WSDL-extracted
XSDs under `schemas/*.xsd`. The Python types under
`karrio/schemas/dpd_france/*.py` are **generated** from those XSDs with
`generateDS` — never hand-edit (see [References](#references)). The connector
is `status="beta"` pending live API verification.

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Data flow](#data-flow)
3. [Endpoints](#endpoints)
4. [Authentication](#authentication)
5. [Supported operations](#supported-operations)
6. [Services](#services)
7. [Options & config](#options--config)
8. [Data mapping](#data-mapping)
9. [Multi-piece (Pattern B)](#multi-piece-pattern-b)
10. [Tracking](#tracking)
11. [Error parsing](#error-parsing)
12. [References](#references)

---

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio ShipmentRequest / ShipmentCancelRequest /
│   (karrio core)         │   PickupRequest / PickupCancelRequest /
│                         │   TrackingRequest / RateRequest
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  providers/dpd_france   │   Pure data transforms.
│   shipment/create.py    │   Unified model → typed cargoNET SOAP body,
│   shipment/cancel.py    │   typed cargoNET response → unified model.
│   return_shipment.py    │   No HTTP, no side effects.
│   pickup/create.py      │
│   pickup/cancel.py      │
│   tracking.py           │
│   error.py              │
│   units.py              │   ShippingService, ShippingOption, LabelType,
│   utils.py (Settings)   │   TrackingStatus, ConnectionConfig; CSV loader.
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  mappers/dpd_france     │   HTTP transport only.
│   proxy.py              │   - SOAP envelope POST (text/xml + SOAPAction)
│   settings.py           │   - per-op SOAPAction headers
│   mapper.py             │   - concurrent fan-out (create/return/tracking)
│                         │   rate.py → karrio universal RatingMixin
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  cargoNET SOAP services │
│  ─────────────────────  │
│  EPrintWebservice .asmx │   CreateShipmentWithLabelsBc, TerminateShipment,
│                         │   CreateReverseInverseShipmentWithLabelsBc,
│                         │   CreateCollectionRequestBc,
│                         │   TerminateCollectionRequestBc
│  Webtrace_Service .asmx │   GetShipmentTrace
└─────────────────────────┘
```

**Key architectural choices:**

- **No live rate API.** cargoNET exposes no carrier rate endpoint; rating is
  served by karrio's `universal.providers.rating` over a static rate sheet
  built from `karrio/providers/dpd_france/services.csv`. `Settings` subclasses
  `RatingMixinSettings`, the proxy subclasses `RatingMixinProxy`, and
  `mapper.py` delegates `create_rate_request` / `parse_rate_response` to the
  universal provider.
- **No token grant.** Unlike the sibling `dpd` connector (which does a
  LoginService `getAuth` token dance), cargoNET authenticates **per call**
  via a `UserCredentials` SOAP header (`userid` + `password`) baked into
  every envelope. There is no token cache.
- **SOAP envelopes built by hand** with `lib.Envelope` / `lib.Header` /
  `lib.Body` + `lib.envelope_serializer`, with explicit namespace prefixes
  (`soapenv` for the envelope, `imt` for the cargoNET body/header).
- **Two distinct namespaces.** The shipping service uses
  `http://www.cargonet.software` (**no trailing slash**); the tracking
  service uses `http://www.cargonet.software/` (**with trailing slash**).
  Both are verified against the extracted WSDLs; the difference is real and
  flows into the SOAPAction strings.
- **Multi-piece via Pattern B** (one parallel call per parcel) — cargoNET's
  `CreateMultiShipmentBc` op returns no labels and excludes Predict / Relais
  / Retour services, so it is not used (see [Multi-piece](#multi-piece-pattern-b)).
- **Generated schemas** — `karrio/schemas/dpd_france/*.py` is generated from
  the XSDs with `generateDS --no-namespace-defs` via the connector's
  `generate` script.

Plugin metadata (`karrio/plugins/dpd_france/__init__.py`): `id="dpd_france"`,
`label="DPD France"`, `status="beta"`, `is_hub=False`,
`website="https://www.dpd.fr"`.

## Data flow

### Shipment creation (per-parcel fan-out, single-leg)

```
ShipmentRequest                                    cargoNET EPrintWebservice
     │                                                       │
     ├─► shipment_request()                                  │
     │     to_address(shipper / recipient)                   │
     │     to_packages(parcels)                              │
     │     map label_type → LabelType (default "PDF")        │
     │     one Envelope per package (Pattern B)              │
     │                                                       │
     ├─► lib.Envelope{                                       │
     │     Header: UserCredentials(userid, password),        │
     │     Body: CreateShipmentWithLabelsBc{                 │
     │             StdShipmentLabelRequest } } → XML         │
     │                                                       │
     │   proxy.create_shipment:                              │
     │     lib.run_concurently(_send, [envelopes])           │
     │     ─── POST eprintwebservice.asmx ──────────────────►│
     │         SOAPAction: …/CreateShipmentWithLabelsBc      │  validate
     │                                                       │  label gen
     │   ◄── ShipmentBc{ Shipment{ BarCode, BarcodeId } },   │
     │       Label{ label (bytes), type_ } ──────────────────│
     │                                                       │
     ├─► _extract_details (per response):                    │
     │     Shipment.BarCode    → tracking_number             │
     │     Shipment.BarcodeId  → shipment_identifier         │
     │     Label.label (b64)   → docs.label                  │
     │     Label.type_         → label_type (mapped)         │
     │                                                       │
     ├─► lib.to_multi_piece_shipment(package_shipments)      │
     ▼                                                       ▼
ShipmentDetails                          (N HTTP calls, one per parcel)
```

### Tracking (per-number concurrent fan-out)

```
TrackingRequest                                    cargoNET Webtrace_Service
     │                                                       │
     ├─► tracking_request()                                  │
     │     one (number, Envelope) per tracking number        │
     │     GetShipmentTrace{ ShipmentDetailRequest{          │
     │       Customer, Language, ShipmentNumber } }          │
     │                                                       │
     │   proxy.get_tracking:                                 │
     │     lib.run_concurently(_fetch, [(num, xml)])         │
     │     ─── POST Webtrace_Service.asmx ──────────────────►│  (per number)
     │         SOAPAction: …/GetShipmentTrace                │
     │                                                       │
     │   ◄── ShipmentTrace{ ShipmentNumber,                  │
     │         Traces.clsTrace[] } ──────────────────────────│
     │                                                       │
     ├─► _extract_details (per trace):                       │
     │     clsTrace[] → events[] (date/time/code/desc/loc)   │
     │     last event StatusNumber → TrackingStatus          │
     │     status == "delivered" → delivered                 │
     ▼                                                       ▼
list[TrackingDetails]                    (1 HTTP call per tracking number)
```

## Endpoints

Test mode (`test_mode=True`) and production are selected per service. The
**production shipping URL carries a `dpd-` path prefix** that the test URL
lacks; the **production tracking URL uses a different host** (`webtrace.dpd.fr`).

| Service | Test (`test_mode=True`) | Production |
|---|---|---|
| Shipping (`server_url`) | `https://e-station-testenv.cargonet.software/eprintwebservice/eprintwebservice.asmx` | `https://e-station.cargonet.software/dpd-eprintwebservice/eprintwebservice.asmx` |
| Tracking (`tracking_url`) | `https://e-station-testenv.cargonet.software/trace-service/Webtrace_Service.asmx` | `https://webtrace.dpd.fr/trace-service/Webtrace_Service.asmx` |

Every call is a SOAP 1.1 POST with `Content-Type: text/xml; charset=utf-8`
plus the matching `SOAPAction` header (`<targetNamespace>/<OperationName>`):

| Purpose | URL | SOAPAction |
|---|---|---|
| Create shipment | `server_url` | `http://www.cargonet.software/CreateShipmentWithLabelsBc` |
| Cancel shipment | `server_url` | `http://www.cargonet.software/TerminateShipment` |
| Return shipment | `server_url` | `http://www.cargonet.software/CreateReverseInverseShipmentWithLabelsBc` |
| Schedule pickup | `server_url` | `http://www.cargonet.software/CreateCollectionRequestBc` |
| Cancel pickup | `server_url` | `http://www.cargonet.software/TerminateCollectionRequestBc` |
| Tracking | `tracking_url` | `http://www.cargonet.software/GetShipmentTrace` |
| Rating | — | (no HTTP — static CSV rate sheet via universal RatingMixin) |

Note the shipping SOAPActions have **no double slash** (namespace lacks a
trailing slash); the tracking SOAPAction is built from the trailing-slash
tracking namespace, so the proxy concatenates `tracking_namespace +
"GetShipmentTrace"` (no extra `/`).

## Authentication

Per-call SOAP-header credentials — **no token grant, no caching**. Every
envelope carries:

```xml
<soapenv:Header>
  <imt:UserCredentials>
    <imt:userid>...</imt:userid>
    <imt:password>...</imt:password>
  </imt:UserCredentials>
</soapenv:Header>
```

Credentials are issued by DPD France sales. The calling server's IP must be
**whitelisted** by cargoNET; calls from non-whitelisted IPs return a SOAP
fault with error code `IpPermissionDenied`. Request whitelisting when
obtaining credentials (vendor contact:
`support.webservices@cargonet-software.fr`, `+33 3 88 79 79 50`).

### Connection settings (`mappers/dpd_france/settings.py`)

| Field | Required | Default | Notes |
|---|---|---|---|
| `userid` | yes | — | cargoNET user id (SOAP header) |
| `password` | yes | — | account password (marked `sensitive`) |
| `customer_center_number` | no | `None` | DPD France depot/centre number; sent on every request |
| `customer_number` | no | `None` | DPD France customer account number; sent on every request |
| `language` | no | `"EN"` | sent as `Language` on tracking requests |
| `customer_country_code` | no | `"250"` | ISO numeric for France — DPD France is locked to `250`; exposed with a default for future flexibility |
| `account_country_code` | no | `"FR"` | |
| `test_mode` | no | `False` | selects sandbox base URLs |
| `services` | no | CSV defaults | rate-sheet service levels (universal rating) |
| `config` | no | `{}` | parsed into `ConnectionConfig` |

`shipping_services` returns the configured `services` if any, else
`DEFAULT_SERVICES` (loaded from `services.csv`).

## Supported operations

| Operation | Wired? | cargoNET op | Notes |
|---|---|---|---|
| Rate | ✅ | — | Static CSV rate sheet via universal `RatingMixin`; no carrier rate API |
| Shipment create | ✅ | `CreateShipmentWithLabelsBc` | per-parcel fan-out; returns GeoLabel + barcodes |
| Shipment cancel | ✅ | `TerminateShipment` | by `BarcodeId`; only valid **before** physical handover (Shipping PDF §8.14) |
| Return shipment | ✅ | `CreateReverseInverseShipmentWithLabelsBc` | reverse-inverse flow; reuses create's response parser |
| Pickup schedule | ✅ | `CreateCollectionRequestBc` | returns a confirmation number |
| Pickup cancel | ✅ | `TerminateCollectionRequestBc` | by confirmation number (barcode `BIC_3`) |
| Tracking | ✅ | `GetShipmentTrace` | one call per tracking number, run concurrently |
| Pickup at customer site | ❌ | `CreatePickupAtCustomerBc` | deferred (per README) |
| Multi-shipment (single op) | ❌ | `CreateMultiShipmentBc` | not used — no labels, excludes Predict/Relais/Retour |

## Services

cargoNET DPD France products are mapped via `ShippingService` (a
`lib.StrEnum` whose **value is the cargoNET product display name**). Per
Shipping PDF §1:

| karrio service code | cargoNET product name |
|---|---|
| `dpd_france_classic` | `DPD Classic` |
| `dpd_france_predict` | `DPD Predict` |
| `dpd_france_medical` | `DPD Medical` |
| `dpd_france_relais_pickup_consigne` | `DPD Relais Pickup & Consigne` |
| `dpd_france_reverse_pickup` | `DPD Reverse at Pickup shop` |
| `dpd_france_secure` | `DPD Secure` |

### Rate sheet (`services.csv`)

The universal rating provider consumes `services.csv`. The shipped matrix
covers `dpd_france_classic` and `dpd_france_predict` for both a `France`
(`FR`) zone and an `EU` zone (`BE,DE,ES,IT,LU,NL,PT,AT,IE`), and
`dpd_france_medical` / `dpd_france_relais_pickup_consigne` /
`dpd_france_reverse_pickup` / `dpd_france_secure` for `FR` only. All sample
rates are `0.0` placeholders; currency `EUR`; weight bands run `0.01–30.0`
kg in `KG`; `transit_days` taken from the low end of a `m-n` range. The CSV
loader (`load_services_from_csv`) groups rows by `ShippingService.map(code)
.name_or_key` into `models.ServiceLevel` with per-row `ServiceZone` entries,
and falls back to a single `DPD Classic` service level if the CSV is missing.

## Options & config

### `ShippingOption` (per Shipping PDF §10 STDSERVICES)

These option enums are **defined** in `units.py` and surfaced through
`shipping_options_initializer`, but the current `shipment/create.py`
`StdShipmentLabelRequest` does **not** yet emit them onto the wire — the
create payload carries only addresses, weight, reference, and label type.
The option catalog is in place for when the STDSERVICES block is wired:

| karrio option | Wire key | Type |
|---|---|---|
| `dpd_france_extra_insurance` | `extra_insurance` | float |
| `dpd_france_predict_contact` | `predict_contact` | str |
| `dpd_france_parcelshop` | `parcelshop` | str |
| `dpd_france_autoconsolidation` | `autoconsolidation` | bool |

### `LabelType` (cargoNET eLabelType — Shipping PDF §11.6)

`Default`, `PDF`, `PDF_A6`, `EPL`, `ZPL`, `ZPL300`, `ZPL_A6`, `ZPL300_A6`.
The request defaults to `"PDF"` (`payload.label_type` mapped through
`LabelType`, falling back to `"PDF"`). On the response, a `Default` label
type is reported back to karrio as `"PNG"`; any other value maps through
`LabelType`.

### `ConnectionConfig`

| Key | Type | Default |
|---|---|---|
| `shipping_options` | list | — |
| `shipping_services` | list | — |
| `label_type` | str | `"PDF"` |

## Data mapping

### Address — karrio `Address` → cargoNET `Address`

The same `dpd_france.Address` shape is used for shipper, recipient, and the
pickup shipper. Only a reduced field set is populated:

```
karrio Address                       cargoNET Address
─────────────────                    ────────────────
country_code            ───►         countryPrefix
postal_code             ───►         zipCode
city                    ───►         city
street                  ───►         street   (truncated to 35 chars)
company_name | person_name ──►       name
phone_number            ───►         phoneNumber
```

`street` is hard-truncated to 35 characters (`(shipper.street or "")[:35]`).
`name` prefers `company_name`, falling back to `person_name`.

### Shipment request — `StdShipmentLabelRequest`

```
settings.customer_country_code   ───► customer_countrycode  (always "250")
settings.customer_center_number  ───► customer_centernumber
settings.customer_number         ───► customer_number
shipper  (mapped Address)        ───► shipperaddress
recipient (mapped Address)       ───► receiveraddress
package.weight.KG                ───► weight        (always kg)
payload.reference                ───► referencenumber
label_type                       ───► labelType.type_
```

### Return shipment — `ReverseShipmentLabelRequest`

Same field set as the create request, via
`CreateReverseInverseShipmentWithLabelsBc`. Per Shipping PDF §8.5 the
reverse-inverse op flips the direction: the recipient is the original
shipper (the return destination) and the shipper is the customer returning
the parcel. The connector maps `payload.shipper` → `shipperaddress` and
`payload.recipient` → `receiveraddress` directly (the caller is responsible
for supplying them in the reverse orientation). The response is parsed by
`create.parse_shipment_response`.

### Pickup — `CollectionRequestRequest`

```
address (mapped Address)         ───► shipperaddress
parcels_count | len(parcels) | 1 ───► parcel_count
payload.reference                ───► referencenumber
lib.fdate(payload.pickup_date)   ───► pick_date
payload.ready_time               ───► time_from
payload.closing_time             ───► time_to
payload.instruction              ───► pick_remark
```

Pickup cancel sends the confirmation number as a barcode with identifier
`BcIdentifier.BIC_3`.

### Identifiers returned on shipment create

```
ShipmentBc.Shipment
  ├─ BarCode    ───►  tracking_number      (customer-facing parcel barcode)
  └─ BarcodeId  ───►  shipment_identifier  (cargoNET internal handle;
                       the value TerminateShipment cancels by)
```

For multi-piece, `lib.to_multi_piece_shipment` promotes the first parcel's
values to the primary `tracking_number` / `shipment_identifier` and bundles
the rest (see below).

## Multi-piece (Pattern B)

cargoNET's single-op `CreateMultiShipmentBc` returns **no labels** (there is
no `WithLabels` variant in the WSDL) and **excludes** Predict / Relais /
Retour services per Shipping PDF §8.3. The connector therefore implements
multi-piece as **Pattern B**: issue N parallel `CreateShipmentWithLabelsBc`
calls (one per parcel) via `lib.run_concurently`, then aggregate the N
responses with `lib.to_multi_piece_shipment`. Single-parcel requests are a
one-element list and traverse the identical code path. The same pattern
applies to return shipments. Each response is indexed `1..N`; responses
whose `_extract_details` yields `None` (no `ShipmentBc`) are dropped before
aggregation.

## Tracking

`GetShipmentTrace` is called once per tracking number (`tracking_request`
builds one `(number, Envelope)` pair per number; `proxy.get_tracking` runs
them through `lib.run_concurently`, preserving the queried number alongside
each response).

`_iter_traces` handles cargoNET's two response shapes: a batch nests
`ShipmentTrace` nodes; a single result wraps the trace under
`GetShipmentTraceResult` (parsed with `lib.to_object`). Per trace,
`Traces.clsTrace[]` becomes the event list **in document order** (no
reversal). Per event:

```
clsTrace event                       TrackingEvent
──────────────                       ─────────────
ScanDate           ───► lib.fdate    date
ScanTime           ─► lib.flocaltime time
StatusNumber       ───► str(...)     code
StatusDescription  ───►              description
CenterName         ───►              location
```

The overall `status` is derived from the **last** event's `StatusNumber`
mapped through `TrackingStatus`; `delivered` is `True` when that status
resolves to `"delivered"`. `tracking_number` is `trace.ShipmentNumber`.

### Status mapping (`TrackingStatus`)

The Tracking PDF §8.8 documents `StatusNumber` only as `int` without
enumerating values, so the current map keys are the karrio status names
themselves (identity placeholders) pending live samples:

| karrio status | cargoNET key |
|---|---|
| `on_hold` | `on_hold` |
| `delivered` | `delivered` |
| `in_transit` | `in_transit` |
| `delivery_failed` | `delivery_failed` |
| `delivery_delayed` | `delivery_delayed` |
| `out_for_delivery` | `out_for_delivery` |
| `ready_for_pickup` | `ready_for_pickup` |

These mappings must be refined to real numeric `StatusNumber` codes once
live response samples are captured.

## Error parsing

cargoNET returns access / validation errors as a top-level
`<Error><ErrorId/><ErrorMessage/></Error>` document.
`error.parse_error_response` finds every `Error` element (or treats the root
itself as one if its tag is `Error`) and emits one `models.Message` per
error:

```
Response                  ┌────────────────────────────────┐
   │                      │ error.parse_error_response       │
   ├─► find Error nodes ──► │   code    ← Error/ErrorId      │
   │   (or root == Error) │   message ← Error/ErrorMessage   │
   │                      │   details ← **kwargs             │
   ▼                      └───────────────┬─────────────────┘
   {ErrorId, ErrorMessage}                ▼
                                    list[Message]
```

Extra kwargs (e.g. `tracking_number=...` from the tracking parser) are
attached to `Message.details`. Cancel and pickup-cancel treat an empty error
list as success (an empty/`<Error>`-free body means the op succeeded — see
the `TerminateShipment` caveat below). Per-operation error patterns beyond
the top-level `Error` shape will be added once observed in live responses.

### `TerminateShipment` caveat (Shipping PDF §8.14)

`TerminateShipment` is only callable **before the parcel is physically
shipped** (before pickup/handover); cargoNET rejects it once the shipment
enters the network. A response with no `<Error>` element is treated as
success — the op otherwise returns an empty body.

## References

- **Vendor PDFs (authoritative)** — `vendor/`:
  - `DPD France Shipping WebService - GeoLabel.pdf` — EPrintWebservice
    (shipment create / cancel / return / pickup, GeoLabel printing), v1.9a 02/2026.
  - `DPD France Tracking WebService.pdf` — Webtrace_Service (status / events), v5.0 10/2025.
  - `vendor/README.md` — endpoints, SOAPAction strings, namespace notes,
    IP-whitelisting, credential contacts.
- **Vendor XSDs** — `schemas/*.xsd` (extracted from cargoNET-supplied WSDLs,
  with `s:` → `xs:` prefix normalization so generateDS accepts them):
  - `EPrintWebservice.xsd` — shipping / pickup / return ops and types.
  - `Webtrace_Service.xsd` — `GetShipmentTrace` / `ShipmentTrace` / `clsTrace`.
  - `error_response.xsd` — top-level `Error` document.
- **Generated Python types** — `karrio/schemas/dpd_france/{eprintwebservice,
  webtraceservice,error}.py`, produced by `generateDS --no-namespace-defs`
  from the XSDs (see the connector's `generate` script). **Do not
  hand-edit**; regenerate with `./bin/run-generate-on modules/connectors/dpd_france`.
- **Rate sheet** — `karrio/providers/dpd_france/services.csv` (zone/weight
  matrix consumed by `load_services_from_csv`). Rates are `0.0` placeholders;
  replace per account.
