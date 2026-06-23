# Purolator integration — specification

Reference for the Purolator connector. Purolator is a Canadian courier;
its web services are **SOAP 1.1 over HTTPS** (each operation is an
`.asmx` endpoint with a distinct `soapaction` header and a typed
XML body). This connector wires rating, shipment create/void, tracking,
pickup schedule/modify/cancel, address validation, and returns.

The **vendor source of truth** is the set of WSDL/XSD contracts under
`schemas/*.xsd` (E-Ship Web Services — "EWS"/"PWS"). The Python typed
modules under `karrio/schemas/purolator/*.py` are generated from those
XSDs with `generateDS` (see `generate`); never hand-edit them.

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Data flow](#data-flow)
3. [Endpoints](#endpoints)
4. [Authentication](#authentication)
5. [Supported operations](#supported-operations)
6. [SOAP envelope shaping](#soap-envelope-shaping)
7. [Services](#services)
8. [Options](#options)
9. [Packaging & measurement](#packaging--measurement)
10. [Data mapping](#data-mapping)
11. [Tracking](#tracking)
12. [Error parsing](#error-parsing)
13. [References](#references)

---

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio RateRequest / ShipmentRequest /
│   (karrio core)         │   TrackingRequest / PickupRequest /
│                         │   AddressValidationRequest
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  providers/purolator    │   Pure data transforms.
│   rate.py               │   Unified model → typed Purolator request,
│   shipment/create.py    │   typed Purolator response → unified model.
│   shipment/cancel.py    │   No HTTP, no side effects.
│   shipment/documents.py │
│   shipment/return_*.py  │
│   tracking.py           │
│   address.py            │
│   pickup/{create,update,│
│     cancel,validate}.py │
│   error.py              │
│   units.py              │   ShippingService, ShippingOption,
│   utils.py              │   PackagingType, PaymentType, TrackingStatus,
│                         │   TrackingIncidentReason, serializer
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  mappers/purolator      │   HTTP transport only.
│   proxy.py              │   - one POST per .asmx operation
│   settings.py           │   - SOAP 1.1, Content-Type text/xml
│                         │   - HTTP Basic auth header
│                         │   - Pipeline chaining (label, pickup)
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Purolator Web Services │  SOAP .asmx endpoints
│  ─────────────────────  │
│  EWS V2 Estimating      │  GetFullEstimate
│  EWS V2 Shipping        │  CreateShipment / VoidShipment
│  EWS V1 ShippingDocs    │  GetDocuments (label PDF/ZPL)
│  EWS V2 ServiceAvail.   │  ValidateCityPostalCodeZip
│  EWS V1 PickUp          │  Validate / Schedule / Modify / Void PickUp
│  PWS V1 Tracking        │  TrackPackagesByPin
└─────────────────────────┘
```

**Key architectural choices:**

- **One SOAP call per operation**; the two multi-step flows
  (shipment create, pickup) are orchestrated as a `lib.Pipeline` in the
  provider and dispatched leg-by-leg by the proxy.
- **Two-call shipment creation**: `CreateShipment` returns the
  `ShipmentPIN` but not the label artifact. A second call to
  `GetDocuments` (Shipping Documents service) fetches the label by PIN.
- **No OAuth / token cache** — every call carries a static HTTP Basic
  `Authorization` header derived from `username:password`. A
  `user_token` is sent inside every `RequestContext` element.
- **Generated schemas** — `karrio/schemas/purolator/*.py` is generated
  from `schemas/*.xsd` via `generateDS`. Regenerate with
  `./bin/run-generate-on modules/connectors/purolator`.
- **Freight services** (`Freight*.xsd` → `freight_*` schema modules) are
  generated but **not wired** into any provider; only the parcel
  services above are mapped.

## Data flow

### Rate (one HTTP call)

```
RateRequest                              Purolator EWS Estimating
     │                                            │
     ├─► rate_request                             │
     │     to_address(shipper/recipient)          │
     │     to_packages()                          │
     │     to_services()  (default if none)       │
     │     to_shipping_options()                  │
     │     build GetFullEstimateRequest envelope  │
     │                                            │
     │   ─── POST .../EstimatingService.asmx ────►│
     │       soapaction GetFullEstimate           │
     │                                            │
     │   ◄── GetFullEstimateResponse{             │
     │         ShipmentEstimate[] } ──────────────│
     │                                            │
     ├─► parse_rate_response                       │
     │     one RateDetails per ShipmentEstimate    │
     │     charges = BasePrice + Taxes +           │
     │               Surcharges + OptionPrices     │
     ▼                                            ▼
list[RateDetails]
```

### Shipment create (two HTTP calls, pipelined)

```
ShipmentRequest                                       Purolator EWS
     │                                                       │
     ├─► shipment_request → Pipeline(create, document)       │
     │                                                       │
     │   leg "create":                                       │
     │     _shipment_request → CreateShipmentRequest         │
     │   ─── POST .../ShippingService.asmx ─────────────────►│
     │       soapaction CreateShipment                       │
     │   ◄── CreateShipmentResponse{ ShipmentPIN } ──────────│
     │                                                       │
     │   leg "document" (_get_shipment_label):               │
     │     skip if create leg returned errors / no PIN       │
     │     GetDocumentsRequest keyed by PIN                  │
     │   ─── POST .../ShippingDocumentsService.asmx ────────►│
     │       soapaction GetDocuments                         │
     │   ◄── GetDocumentsResponse{ DocumentDetail[] } ───────│
     │                                                       │
     ├─► proxy bundles both XML responses (XP.bundle_xml)    │
     ├─► parse_shipment_response                              │
     │     PIN.Value → tracking_number + shipment_identifier  │
     │     DocumentDetail[DocumentType~BillOfLading].Data     │
     │        → docs.label                                    │
     │     DocumentDetail[DocumentType~Invoice].Data          │
     │        → docs.invoice (if present)                     │
     ▼                                                       ▼
ShipmentDetails
```

If the create leg returns errors or no `ShipmentPIN`, the document leg
is skipped (`job.data = None`, fallback `""`) so a failed label POST
isn't fired with an empty PIN.

### Pickup schedule (two HTTP calls, pipelined)

```
PickupRequest → Pipeline(validate, schedule)         Purolator EWS PickUp
     │                                                       │
     │   leg "validate": ValidatePickUpRequest               │
     │   ─── POST .../PickUpService.asmx (ValidatePickUp) ──►│
     │   ◄── validation result ──────────────────────────────│
     │   leg "schedule": fired only if validate had 0 errors │
     │   ─── POST .../PickUpService.asmx (SchedulePickUp) ──►│
     │   ◄── SchedulePickUpResponse{ PickUpConfirmationNumber}│
     ▼                                                       ▼
PickupDetails(confirmation_number)
```

Pickup modify uses the same validate→modify pipeline against
`ModifyPickUp`. Pickup cancel is a single `VoidPickUp` call.

## Endpoints

Test mode: `https://devwebservices.purolator.com`.
Prod: `https://webservices.purolator.com`.
All operations are `POST` with `Content-Type: text/xml; charset=utf-8`
and a distinct `soapaction` header.

| Purpose | Path | soapaction |
|---|---|---|
| Rate (full estimate) | `/EWS/V2/Estimating/EstimatingService.asmx` | `http://purolator.com/pws/service/v2/GetFullEstimate` |
| Create shipment | `/EWS/V2/Shipping/ShippingService.asmx` | `http://purolator.com/pws/service/v2/CreateShipment` |
| Void (cancel) shipment | `/EWS/V2/Shipping/ShippingService.asmx` | `http://purolator.com/pws/service/v2/VoidShipment` |
| Get documents (label) | `/EWS/V1/ShippingDocuments/ShippingDocumentsService.asmx` | `http://purolator.com/pws/service/v1/GetDocuments` |
| Address validation | `/EWS/V2/ServiceAvailability/ServiceAvailabilityService.asmx` | `http://purolator.com/pws/service/v2/ValidateCityPostalCodeZip` |
| Validate pickup | `/EWS/V1/PickUp/PickUpService.asmx` | `http://purolator.com/pws/service/v1/ValidatePickUp` |
| Schedule pickup | `/EWS/V1/PickUp/PickUpService.asmx` | `http://purolator.com/pws/service/v1/SchedulePickUp` |
| Modify pickup | `/EWS/V1/PickUp/PickUpService.asmx` | `http://purolator.com/pws/service/v1/ModifyPickUp` |
| Void (cancel) pickup | `/EWS/V1/PickUp/PickUpService.asmx` | `http://purolator.com/pws/service/v1/VoidPickUp` |
| Tracking | `/PWS/V1/Tracking/TrackingService.asmx` | `http://purolator.com/pws/service/v1/TrackPackagesByPin` |

Note the path-version vs datatype-version split: the shipping/estimating
endpoints are mounted under `/EWS/V2/...` but the `RequestContext.Version`
carried in the body is the **service contract** version, which differs per
operation (rate `2.1`, create `2.1`, void `2.0`, documents `1.3`,
address `2.1`, pickup `1.2`, tracking `1.2`).

## Authentication

HTTP Basic only. `Settings.authorization` is
`base64(username + ":" + password)`, sent as
`Authorization: Basic <b64>` on every request. There is no token
exchange and no caching.

```
settings.username  ┐
settings.password  ┴─► base64("user:pass") ─► Authorization: Basic <b64>
```

Connection settings (`mappers/purolator/settings.py`):

| Field | Required | Notes |
|---|---|---|
| `username` | yes | API key / web-services username |
| `password` | yes | API key password (marked sensitive in commented attr) |
| `account_number` | yes | Purolator billing account; default payer / billing account |
| `user_token` | no | echoed into every `RequestContext.UserToken` |
| `language` | no | `LanguageEnum` (`en` / `fr`), default `en` → `RequestContext.Language` |
| `account_country_code` | no | default `CA` |
| `test_mode` | no | selects dev vs prod `server_url` |

## Supported operations

| Operation | Mapper method | Provider |
|---|---|---|
| Rate | `create_rate_request` / `parse_rate_response` | `rate.py` (`GetFullEstimate`) |
| Shipment create | `create_shipment_request` / `parse_shipment_response` | `shipment/create.py` + `shipment/documents.py` |
| Shipment cancel | `create_cancel_shipment_request` / `parse_cancel_shipment_response` | `shipment/cancel.py` (`VoidShipment`) |
| Return shipment | `create_return_shipment_request` / `parse_return_shipment_response` | `shipment/return_shipment.py` |
| Tracking | `create_tracking_request` / `parse_tracking_response` | `tracking.py` (`TrackPackagesByPin`) |
| Pickup schedule | `create_pickup_request` / `parse_pickup_response` | `pickup/create.py` |
| Pickup update | `create_pickup_update_request` / `parse_pickup_update_response` | `pickup/update.py` |
| Pickup cancel | `create_cancel_pickup_request` / `parse_cancel_pickup_response` | `pickup/cancel.py` |
| Address validation | `create_address_validation_request` / `parse_address_validation_response` | `address.py` (`ValidateCityPostalCodeZip`) |

Plugin metadata (`karrio/plugins/purolator/__init__.py`): id `purolator`,
label `Purolator`, status `production-ready`, account country `CA`.

### Returns

`return_shipment_request` is a thin wrapper over `shipment_request`: it
forces `purolator_return_services=True` into `options` and re-runs the
standard create + GetDocuments pipeline. The response parser delegates
to `parse_shipment_response`.

## SOAP envelope shaping

SOAP namespacing is applied by hand because the typed bodies have no
namespace knowledge. Two serializers exist:

- **`standard_request_serializer(envelope, version="v2")`** — used by
  rate, create, void, address, and (with `version="v1"`) pickup. Sets
  the `soap` prefix on `Envelope/Header/Body`, then walks every
  `Header`/`Body` child and applies the
  `xmlns:vN="http://purolator.com/pws/datatypes/vN"` prefix. The
  `version` argument (`v1`/`v2`) selects the datatype namespace.
- **`shipment/documents.py:_request_serializer`** — a `v1`-pinned variant
  for the GetDocuments call (single Header/Body child).
- **Tracking** builds its envelope directly with
  `lib.envelope_serializer`, pinning `RequestContext` /
  `TrackPackagesByPinRequest` to the `v1` prefix.

`RequestContext` (header) carries `Version`, `Language`, `GroupID` (always
`""`), `RequestReference`, and `UserToken` on every operation.

## Services

`ShippingService` (`units.py`) maps karrio service codes → Purolator
`ServiceID` wire strings. The wire strings embed packaging and
time-window in the ID (e.g. `PurolatorExpressBox10:30AM`,
`PurolatorExpressU.S.9AM`). Selected entries (full list in `units.py`,
67 entries):

| karrio code | wire `ServiceID` |
|---|---|
| `purolator_express` | `PurolatorExpress` |
| `purolator_express_9_am` | `PurolatorExpress9AM` |
| `purolator_express_10_30_am` | `PurolatorExpress10:30AM` |
| `purolator_express_12_pm` | `PurolatorExpress12PM` |
| `purolator_express_evening` | `PurolatorExpressEvening` |
| `purolator_ground` | `PurolatorGround` |
| `purolator_ground_9_am` | `PurolatorGround9AM` |
| `purolator_quick_ship` | `PurolatorQuickShip` |
| `purolator_express_us` | `PurolatorExpressU.S.` |
| `purolator_ground_us` | `PurolatorGroundU.S.` |
| `purolator_express_international` | `PurolatorExpressInternational` |
| ... | (Envelope / Pack / Box and 9AM/10:30AM/12:00/Evening variants for CA, U.S., and International lanes) |

### Default service selection

`shipping_services_initializer` injects a default service when the caller
supplies none:

| Lane | Default |
|---|---|
| Domestic (`shipper.country == recipient.country`) | `purolator_express` |
| Recipient `US` | `purolator_express_us` |
| Other international | `purolator_express_international` |

`is_international` is simply `shipper.country_code != recipient.country_code`.

### Service catalog (`DEFAULT_SERVICES`)

`load_services_from_csv()` reads `providers/purolator/services.csv` at
import and projects it into `models.ServiceLevel` rows (the static rate
sheet shown in the dashboard). CSV columns:
`service_code, service_name, zone_label, country_codes, min_weight,
max_weight, max_length, max_width, max_height, rate, currency,
transit_days, domicile, international`. Weights/dims are `KG`/`CM`,
currency defaults `CAD`; rows are grouped by mapped karrio code with one
`ServiceZone` per CSV row. The CSV is data only — it does not affect live
`GetFullEstimate` pricing.

## Options

`ShippingOption` (`units.py`). The `OptionEnum` first positional arg is
the Purolator option `ID` (the `OptionIDValuePair.ID` on the wire).

| karrio option | wire `ID` | meta category |
|---|---|---|
| `purolator_dangerous_goods` | `Dangerous Goods` | `DANGEROUS_GOOD` |
| `purolator_chain_of_signature` | `Chain of Signature` | `SIGNATURE` |
| `purolator_express_cheque` | `ExpressCheque` | `COD` |
| `purolator_hold_for_pickup` | `Hold For Pickup` | `PUDO` |
| `purolator_return_services` | `Return Services` | `RETURN` |
| `purolator_saturday_service` | `Saturday Service` | `DELIVERY_OPTIONS` |
| `purolator_origin_signature_not_required` | `Origin Signature Not Required (OSNR)` | `SIGNATURE` |
| `purolator_adult_signature_required` | `Adult Signature Required (ASR)` | `SIGNATURE` |
| `purolator_special_handling` | `Special Handling` | — |
| `purolator_show_alternative_services` | `Show Alternate Services` (bool) | karrio-internal, not sent as an option |

Unified alias: `saturday_delivery` → `purolator_saturday_service`.

### `purolator_show_alternative_services`

A karrio-internal flag (in `NON_OFFICIAL_SERVICES`, filtered out of the
on-wire option list). `shipping_options_initializer` defaults it to
`True` whenever no specific service was requested, so the rate call asks
Purolator to return alternate services. It is surfaced on the rate
request as `GetFullEstimateRequest.ShowAlternativeServicesIndicator`.

### Option serialization

Options are emitted as `OptionIDValuePair{ID: option.code, Value:
lib.to_money(option.state)}`. On the **rate** call they ride per-piece
(`Piece.Options`); on the **create** call they ride at package level
(`PackageInformation.OptionsInformation`). Both are omitted when no
options are present.

## Packaging & measurement

`PackagingType` maps unified packaging → Purolator label packaging
(`Envelope`, `Pack`, `Box`, `Customer Packaging`):

| unified | wire |
|---|---|
| `envelope` | `Envelope` |
| `pak` | `Pack` |
| `tube` / `pallet` / `small_box` / `medium_box` / `large_box` / `your_packaging` | `Customer Packaging` |

`PackagePresets` (dims in `IN`, weight in `LB`):
`purolator_express_envelope` (12.5×16×1.5, 1 lb),
`purolator_express_pack` (12.5×16×1.0, 3 lb),
`purolator_express_box` (18×12×3.5, 7 lb).

`MeasurementOptions = MeasurementOptionsType(min_kg=0.45, min_lb=1)` —
weights below the floor are rounded up.

`LabelType` / `PrintType`: `PDF → Regular`, `ZPL → Thermal`. The
`PrinterType` on the create request and the `OutputType` on GetDocuments
both derive from `payload.label_type` (default `PDF`).

## Data mapping

### Address — karrio `Address` → Purolator `Address`

```
karrio Address                          Purolator Address
─────────────────                       ─────────────────
person_name        ───►                 Name
company_name       ───►                 Company
street_number      ───►                 StreetNumber
address_line1      ───►                 StreetName
address_line2      ───►                 StreetAddress2
city               ───►                 City
state_code         ───►                 Province
country_code       ───►                 Country
postal_code        ───►                 PostalCode
phone_number       ───► (units.Phone)   PhoneNumber{CountryCode, AreaCode, Phone}
federal_tax_id /                        TaxNumber  (Sender/Receiver only)
  state_tax_id
```

`Department`, `StreetSuffix`, `StreetType`, `StreetDirection`, `Suite`,
`Floor`, `StreetAddress3`, `FaxNumber`, phone `Extension` are always sent
as `None`. Phone numbers are split via `units.Phone` into
`CountryCode`/`AreaCode`/`Phone`, each falling back to `"0"`; create.py
defaults a missing number to `"000 000 0000"`.

### Payment — `PaymentType` / `DutyPaymentType`

| karrio `paid_by` | `PaymentType` (transport) | `DutyPaymentType` (duties) |
|---|---|---|
| `sender` | `Sender` | `Sender` |
| `recipient` | `Receiver` | `Receiver` |
| `third_party` | `ThirdParty` | `Buyer` |
| `credit_card` | `CreditCard` | — |

On **create**: `PaymentInformation` is only emitted when
`payload.payment` is present; `RegisteredAccountNumber` and
`BillingAccountNumber` fall back to `settings.account_number`. On
**rate**, payment is hardcoded to `PaymentType.SENDER` against
`settings.account_number`.

### International / customs (create) — `InternationalInformation`

Sent only when `is_international`. Built from `lib.to_customs_info`:

```
karrio CustomsInfo                  Purolator InternationalInformation
──────────────────                  ──────────────────────────────────
packages.is_document    ───►        DocumentsOnlyIndicator
commodities[i]          ───►        ContentDetails.ContentDetail[i] {
  title/description (≤25) ─►          Description
  hs_code (or "0000")   ───►          HarmonizedCode
  origin_country (or shipper) ►       CountryOfManufacture
  sku (or "0000")       ───►          ProductCode
  value_amount          ───►          UnitValue
  quantity              ───►          Quantity
                                    }
duty.paid_by            ───►        DutyInformation.BillDutiesToParty (default Sender)
                                    DutyInformation.BusinessRelationship = NotRelated
duty.currency / options.currency ► DutyInformation.Currency
                                    ImportExportType = "Permanent"
                                    CustomsInvoiceDocumentIndicator = True
```

`ContentDetails` is omitted for documents-only shipments. On the **rate**
call `InternationalInformation` is sent as a near-empty shell carrying
only `DocumentsOnlyIndicator`.

### Notification / reference (create)

- `NotificationInformation.ConfirmationEmailAddress` is sent when
  `options.email_notification` is on and either
  `options.email_notification_to` or `recipient.email` is present.
- `TrackingReferenceInformation.Reference1` echoes `payload.reference`
  when non-empty (rate uses the same field).
- `PickupInformation.PickupType` is hardcoded `DropOff`.

### Label / document extraction (create response)

`GetDocumentsResponse.DocumentDetail[]`:

| DocumentType contains | → unified |
|---|---|
| `BillOfLading` | `docs.label` (`.Data`, base64) |
| `Invoice` | `docs.invoice` (`.Data`) if present |

Document type string is composed in `documents.py` as
`{Domestic|International}BillOfLading{Thermal?}` — `Thermal` suffix when
label type is ZPL. (CustomsInvoice request is stubbed out with a
`TODO: Find what is missing to get customs invoice.`)

### Identifiers

`ShipmentPIN.Value` is the single Purolator identifier; the connector
sets **both** `tracking_number` and `shipment_identifier` to it.
`VoidShipment` and `TrackPackagesByPin` both key on this PIN
(`shipment_identifier` is passed to void).

### Address validation

`ValidateCityPostalCodeZipRequest.Addresses.ShortAddress[]` from
`payload.address` (`City`/`Province`/`Country`/`PostalCode`). Response:
first `SuggestedAddresses.SuggestedAddress.Address` →
`AddressValidationDetails.complete_address`. `success` is true when there
are zero parsed errors.

## Tracking

`TrackPackagesByPinRequest.PINs.PIN[]` from `payload.tracking_numbers`.
Each response `TrackingInformation` node → one `TrackingDetails`:

- `tracking_number` = `PIN.Value`.
- `delivered` = any scan with `ScanType == "Delivery"`.
- `status` derived from the **most recent** scan (`Scans.Scan[0]`).
- One `TrackingEvent` per scan: `date` (`ScanDate`), `time`
  (`ScanTime`, `%H%M%S`), `description`, `location` (`Depot.Name`),
  `code` (`ScanType`), `timestamp` (ISO), plus per-event `status` and
  `reason`.

### Status mapping (`TrackingStatus`)

| karrio | Purolator `ScanType` |
|---|---|
| `delivered` | `Delivery` |
| `delivery_failed` | `Undeliverable` |
| `out_for_delivery` | `OnDelivery` |
| `in_transit` | (default fallback; empty match set) |

### Incident reason mapping (`TrackingIncidentReason`)

Per-event `reason` is matched against `ScanType` **or** `Description`
against a curated keyword table (`units.py`). Buckets:

- Carrier: `carrier_damaged_parcel`, `carrier_sorting_error`,
  `carrier_address_not_found`, `carrier_parcel_lost`,
  `carrier_not_enough_time`, `carrier_vehicle_issue`.
- Consignee: `consignee_refused`, `consignee_business_closed`,
  `consignee_not_available`, `consignee_not_home`,
  `consignee_incorrect_address`, `consignee_access_restricted`.
- Customs: `customs_delay`, `customs_documentation`,
  `customs_duties_unpaid`.
- Force majeure: `weather_delay`, `natural_disaster`.
- Delivery exceptions: `delivery_exception_hold`,
  `delivery_exception_undeliverable`.
- `unknown` (empty match set).

(Keyword lists such as `["Refused", "Delivery Refused", "Recipient
Refused"]` are heuristic — they match Purolator's free-text scan
descriptions, not a documented exception-code enum.)

## Error parsing

`error.parse_error_response` collects two shapes from the response XML
and concatenates them:

1. **Purolator `Error` elements** — any node with local-name `Error` is
   built into the generated `Error` type → `Message` with
   `code = Error.Code`, `message = Error.Description`, and
   `details = {AdditionalInformation}` when present.
2. **SOAP `Fault` elements** — `karrio.core.utils.soap.extract_fault`
   maps each `Fault` → `Message` with `code = faultcode`,
   `message = faultstring`.

```
Response XML
   │
   ├─► .//Error  ─► Error.build ─► Message{code=Code, message=Description,
   │                                       details={AdditionalInformation}?}
   │
   └─► .//Fault  ─► extract_fault ─► Message{code=faultcode,
                                             message=faultstring}
                         │
                         ▼
                   list[Message]
```

Success of each operation is gated on the **presence of the success
payload** (e.g. `ShipmentPIN.Value`, `PickUpConfirmationNumber`,
`VoidShipmentResponse.ShipmentVoided`) AND zero parsed errors, rather
than an HTTP status code — SOAP faults arrive with 2xx/5xx bodies.

## References

- **WSDL/XSD contracts (source of truth)** — `schemas/*.xsd`:
  - `EstimateService.xsd` → `estimate_service_2_1_2.py` (rate)
  - `ShippingService.xsd` → `shipping_service_2_1_3.py` (create / void)
  - `ShippingDocumentsService.xsd` → `shipping_documents_service_1_3_0.py` (labels)
  - `ServiceAvailabilityService.xsd` → `service_availability_service_2_0_2.py` (address validation)
  - `PickupService.xsd` → `pickup_service_1_2_1.py` (pickup)
  - `TrackingService.xsd` → `tracking_service_1_2_2.py` (tracking)
  - `LocatorService.xsd`, `ReturnsManagementService.xsd`,
    `Freight*.xsd`, `DataTypes.xsd`, `ArrayOfstring.xsd`,
    `Validation*.xsd` — generated but not all wired.
- **Generated Python types** — `karrio/schemas/purolator/*.py`. Do not
  hand-edit; regenerate with
  `./bin/run-generate-on modules/connectors/purolator` (drives the
  `generate` script → `generateDS --no-namespace-defs`).
- **Static service catalog** — `karrio/providers/purolator/services.csv`.
- **Service / option display names (i18n)** —
  `karrio/providers/purolator/i18n.py`
  (`SERVICE_NAME_TRANSLATIONS`, `OPTION_NAME_TRANSLATIONS`).
- **Vendor site** — <https://www.purolator.com> (Purolator E-Ship Web
  Services / Developer portal for the EWS/PWS endpoints above).
