# MyDHL Express integration — specification

Reference for the `mydhl` connector. It integrates **DHL Express's MyDHL
API** — a modern **JSON REST** API (vendor OpenAPI title *"DHL Express
APIs (MyDHL API)"*, version `3.1.1`). The connector supports rating,
shipment creation, return shipments, tracking (with proof-of-delivery
image fetch), one-time pickup schedule/update/cancel, address
validation, and paperless-trade (PLT) document upload.

The **vendor source of truth** is the OpenAPI spec kept verbatim at
`vendors/dpdhl-express-api-3.1.1_swagger.yaml`. Generated typed schema
modules under `karrio/schemas/mydhl/*.py` are produced from the per-
operation sample JSON in `schemas/*.json` (see
[References](#references)). The DHL event-status code list used for
tracking is captured in `vendors/status_1.csv`.

> **Maturity note:** the plugin METADATA declares
> `status="in-development"`. `proxy.py` and `address.py` still carry the
> connector-scaffold "IMPLEMENTATION INSTRUCTIONS" comment banners even
> though the code beneath them is wired and functional. There is **no
> shipment-cancel/void operation** implemented (cancel exists only for
> pickups). The cancel schemas (`shipment_cancel_*`) are generated but
> unused.

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Data flow](#data-flow)
3. [Endpoints](#endpoints)
4. [Authentication](#authentication)
5. [Supported operations](#supported-operations)
6. [Services](#services)
7. [Options (value-added services)](#options-value-added-services)
8. [Packaging types](#packaging-types)
9. [Data mapping](#data-mapping)
10. [Carrier-specific invariants / gotchas](#carrier-specific-invariants--gotchas)
11. [Tracking](#tracking)
12. [Error parsing](#error-parsing)
13. [Service catalog (services.csv)](#service-catalog-servicescsv)
14. [References](#references)

---

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio RateRequest / ShipmentRequest /
│   (karrio core)         │   TrackingRequest / PickupRequest /
│                         │   PickupUpdateRequest / PickupCancelRequest /
│                         │   AddressValidationRequest / DocumentUploadRequest
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  providers/mydhl        │   Pure data transforms.
│   rate.py               │   Unified model → typed MyDHL request,
│   shipment/create.py    │   typed MyDHL response → unified model.
│   shipment/return_*.py  │   No HTTP, no side effects.
│   tracking.py           │
│   pickup/create.py      │
│   pickup/update.py      │
│   pickup/cancel.py      │
│   address.py            │
│   document.py           │
│   error.py              │
│   units.py              │   ShippingService, ShippingOption,
│   utils.py              │   PackagingType, TrackingStatus,
│   i18n.py               │   TrackingIncidentReason, Settings,
│                         │   ConnectionConfig, get_proof_of_delivery()
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  mappers/mydhl/proxy.py │   HTTP transport only.
│   - get_rates           │   - Basic Auth header
│   - create_shipment     │   - Content-Type: application/json
│   - create_return_*     │   - shipment create chains a 2nd
│   - get_tracking        │     PATCH for paperless upload
│   - schedule_pickup     │
│   - modify_pickup       │
│   - cancel_pickup       │
│   - validate_address    │
│   - upload_document     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  DHL Express MyDHL API  │   JSON REST, base /mydhlapi (prod)
│  (express.api.dhl.com)  │   or /mydhlapi/test (sandbox)
└─────────────────────────┘
```

**Key architectural choices:**

- **Single endpoint family.** All operations hit the one MyDHL base URL
  (`https://express.api.dhl.com/mydhlapi[/test]`). There is no separate
  rating/tracking host — paths differ, host does not.
- **HTTP Basic Auth** (`base64(username:password)`), no token caching.
  The OAuth `client_credentials` scaffold in `utils.py` is commented out
  and unused.
- **Shipment create is single-call** for the label, with an **optional
  second PATCH** to `/shipments/{trackingNumber}/upload-image` when
  paperless trade applies. The proxy runs both legs and merges the
  paperless result into the deserialization context.
- **Static service catalog.** `units.ShippingService` is the union of
  DHL Express global product codes from the OpenAPI reference data.
  `DEFAULT_SERVICES` (service-level metadata exposed to the picker) is
  loaded at import time from `services.csv`.
- **Generated schemas** — `karrio/schemas/mydhl/*.py` is generated from
  `schemas/*.json`. Regenerate with
  `./bin/run-generate-on modules/connectors/mydhl` — never hand-edit.

## Data flow

### Rate (one HTTP call)

```
RateRequest                              MyDHL /rates
     │                                        │
     ├─► to_address(shipper / recipient)      │
     │   to_packages(parcels)                 │
     │   to_services → productCode (optional) │
     │   is_international = shipper.cc != recipient.cc
     │   is_dutiable = international AND not all docs
     │                                        │
     ├─► RateRequestType (typed)              │
     │     customerDetails{shipper,receiver}  │
     │     accounts[{typeCode:"shipper"}]     │
     │     unitOfMeasurement metric/imperial  │
     │     isCustomsDeclarable                │
     │     packages[{weight,dimensions}]      │
     │                                        │
     │   ─── POST /rates ────────────────────►│
     │   ◄── { products[] } ───────────────────│
     │                                        │
     ├─► one RateDetails per product that     │
     │   carries totalPrice[]                 │
     ▼                                        ▼
list[RateDetails]                        (no further call)
```

### Shipment create (label, + optional paperless PATCH)

```
ShipmentRequest                                   MyDHL APIs
     │                                                │
     ├─► to_address / to_packages / to_customs_info   │
     │   service_code = ShippingService.map(service)  │
     │   is_international = shipper.cc != recipient.cc │
     │   is_paperless = international AND doc_files w/  │
     │     doc_type ∈ {commercial_invoice, invoice,    │
     │                 proforma, certificate_of_origin}│
     │                                                │
     ├─► ShipmentRequestType (typed) →  payload.shipment
     │   paperless dict (documentImages[]) → payload.paperless
     │                                                │
     │   ─── POST /shipments ─────────────────────────►│
     │   ◄── { shipmentTrackingNumber, documents[],    │
     │         packages[], shipmentCharges[] } ────────│
     │                                                │
     ├─► if is_paperless and tracking_number:         │
     │     PATCH /shipments/{tn}/upload-image ─────────►│  (on_ok → {ok:True})
     │   ◄── 200 ──────────────────────────────────────│
     │                                                │
     ├─► _extract_details: label from documents[0] or  │
     │     bundle_base64 of multiple; tracking_number  │
     │     = shipmentTrackingNumber; selected_rate from│
     │     shipmentCharges[0]                          │
     ▼                                                ▼
ShipmentDetails                              (1 or 2 calls)
```

Return shipments (`create_return_shipment_request` →
`return_shipment.py`) reuse the exact same `shipment_request` path with
`options.mydhl_return_to_seller = True` forced on, and the proxy's
`create_return_shipment` delegates to `create_shipment`.

### Tracking (one HTTP call, + optional POD fetch)

```
TrackingRequest                          MyDHL /tracking
     │                                        │
     ├─► query: shipmentTrackingNumber={n}&…  │
     │   ─── GET /tracking?<qs> ─────────────►│
     │   ◄── { shipments[] } ──────────────────│
     │                                        │
     ├─► per shipment: status from events[0]  │
     │     .typeCode via TrackingStatus       │
     │   if delivered → get_proof_of_delivery │
     │     GET /shipments/{tn}/proof-of-delivery
     │     (bundles document contents → PDF)  │
     ▼                                        ▼
list[TrackingDetails]                    (1 + N POD calls)
```

### Pickup (schedule / update / cancel)

```
schedule_pickup   POST   /pickups               → dispatchConfirmationNumbers[]
modify_pickup     PATCH  /pickups               (body carries dispatchConfirmationNumber)
cancel_pickup     DELETE /pickups/{confirmationNumber}
```

## Endpoints

Base URL: `https://express.api.dhl.com/mydhlapi` (prod) or
`https://express.api.dhl.com/mydhlapi/test` (test mode). Selected by
`Settings.test_mode`. (The OpenAPI also lists a mock host
`https://api-mock.dhl.com/mydhlapi`, not used by the connector.)

| Purpose | Method | Path |
|---|---|---|
| Rate quote | POST | `/rates` |
| Create shipment | POST | `/shipments` |
| Paperless upload (PLT) | PATCH | `/shipments/{trackingNumber}/upload-image` |
| Proof of delivery image | GET | `/shipments/{trackingNumber}/proof-of-delivery` |
| Tracking | GET | `/tracking?shipmentTrackingNumber={n}[&shipmentTrackingNumber=…]` |
| Schedule pickup | POST | `/pickups` |
| Modify pickup | PATCH | `/pickups` |
| Cancel pickup | DELETE | `/pickups/{confirmationNumber}` |
| Address validation | GET | `/address-validate?type=…&countryCode=…&postalCode=…&cityName=…` |

`Content-Type: application/json` is sent on every body-carrying request
(POST/PATCH). GET/DELETE carry only the `Authorization` header.

## Authentication

**HTTP Basic Auth.** Credentials are `username` + `password` on the
connection settings, plus an `account_number` that is echoed in request
bodies (`accounts: [{typeCode: "shipper", number: <account_number>}]`)
but is not part of the auth header.

```
Settings.authorization = base64(f"{username}:{password}")

every request →  Authorization: Basic <authorization>
```

There is no token exchange, no refresh, no cache. The commented-out
`access_token` / `login()` OAuth scaffold in `utils.py` is dead and not
referenced anywhere.

`Settings` fields (`mappers/mydhl/settings.py`):

| Field | Required | Notes |
|---|---|---|
| `username` | yes | Basic Auth user |
| `password` | yes | Basic Auth password (intended `sensitive`; metadata line is commented out) |
| `account_number` | no | DHL Express account; sent in `accounts[].number` |
| `account_country_code` | no | generic karrio field |
| `test_mode` | no | toggles `/mydhlapi/test` vs `/mydhlapi` |
| `config` | no | projects to `ConnectionConfig` |

### ConnectionConfig

| Key | Type | Default | Use |
|---|---|---|---|
| `shipping_options` | list | — | restrict offered options |
| `shipping_services` | list | — | restrict offered services |
| `label_type` | str | `PDF` | label encoding preference |

## Supported operations

| Operation | Mapper method | Provider | Status |
|---|---|---|---|
| Rate | `create_rate_request` / `parse_rate_response` | `rate.py` | wired |
| Shipment create | `create_shipment_request` / `parse_shipment_response` | `shipment/create.py` | wired |
| Return shipment | `create_return_shipment_request` / `parse_return_shipment_response` | `shipment/return_shipment.py` | wired (delegates to create) |
| Shipment cancel/void | — | — | **not implemented** |
| Tracking | `create_tracking_request` / `parse_tracking_response` | `tracking.py` | wired (+ POD image when delivered) |
| Pickup schedule | `create_pickup_request` / `parse_pickup_response` | `pickup/create.py` | wired (one-time only) |
| Pickup update | `create_pickup_update_request` / `parse_pickup_update_response` | `pickup/update.py` | wired |
| Pickup cancel | `create_cancel_pickup_request` / `parse_cancel_pickup_response` | `pickup/cancel.py` | wired |
| Address validation | `create_address_validation_request` / `parse_address_validation_response` | `address.py` | wired |
| Document upload (PLT) | `create_document_upload_request` / `parse_document_upload_response` | `document.py` | wired |

## Services

`units.ShippingService` maps karrio service codes to DHL Express
**global product codes** (`productCode`, 1–2 chars). Sent as
`productCode` (and `localProductCode` on shipment create).

### International Express

| karrio service | productCode |
|---|---|
| `mydhl_express_worldwide` | `P` |
| `mydhl_express_12_00` | `T` |
| `mydhl_express_9_00` | `Y` |
| `mydhl_express_10_30` | `K` |
| `mydhl_express_easy` | `8` |
| `mydhl_medical_express` | `Q` |
| `mydhl_jetline` | `J` |
| `mydhl_sprintline` | `R` |
| `mydhl_globalmail` | `G` |
| `mydhl_globalmail_business` | `M` |

### Domestic Express

| karrio service | productCode |
|---|---|
| `mydhl_express_domestic` | `N` |
| `mydhl_express_domestic_12_00` | `1` |
| `mydhl_express_domestic_10_30` | `O` |
| `mydhl_express_domestic_9_00` | `I` |
| `mydhl_medical_express_domestic` | `C` |
| `mydhl_same_day` | `S` |

### Economy / Freight

| karrio service | productCode |
|---|---|
| `mydhl_economy_select` | `W` |
| `mydhl_europack` | `H` |
| `mydhl_breakbulk_express` | `E` |
| `mydhl_express_freight` | `F` |

### Document / Envelope / B2C

| karrio service | productCode |
|---|---|
| `mydhl_express_worldwide_doc` | `D` |
| `mydhl_express_envelope` | `X` |
| `mydhl_express_worldwide_b2c` | `7` |
| `mydhl_express_easy_b2c` | `6` |

When the caller doesn't supply a service, the rate request leaves
`productCode` unset (DHL returns the full eligible product list). On
shipment create, `ShippingService.map(payload.service).value_or_key`
falls back to the raw string when the service is unknown.

## Options (value-added services)

`units.ShippingOption` maps option keys to DHL **serviceCode** values.
Each option carries an optional `meta.category` tag used by the UI to
group the value-added service (e.g. `DELIVERY_OPTIONS`, `SIGNATURE`,
`PUDO`, `DANGEROUS_GOOD`, `PAPERLESS`, `NOTIFICATION`, `INSURANCE`,
`RETURN`). Selected highlights:

| Option | serviceCode | category |
|---|---|---|
| `mydhl_saturday_delivery` | `AA` | DELIVERY_OPTIONS |
| `mydhl_hold_for_collection` | `LX` | PUDO |
| `mydhl_neutral_delivery` | `NN` | DELIVERY_OPTIONS |
| `mydhl_residential_delivery` | `TK` | DELIVERY_OPTIONS |
| `mydhl_scheduled_delivery` | `TT` | DELIVERY_OPTIONS |
| `mydhl_collect_from_service_point` | `TV` | PUDO |
| `mydhl_verified_delivery` | `TF` | SIGNATURE |
| `mydhl_direct_signature` | `SF` | SIGNATURE |
| `mydhl_signature_release` | `SX` | SIGNATURE |
| `mydhl_duty_tax_paid` | `DD` | — |
| `mydhl_receiver_paid` | `DE` | — |
| `mydhl_import_billing` | `DT` | — |
| `mydhl_duty_tax_importer` | `DU` | — |
| `mydhl_shipment_insurance` | `II` (float) | INSURANCE |
| `mydhl_dangerous_goods` | `HE` | DANGEROUS_GOOD |
| `mydhl_dry_ice` | `HC` | DANGEROUS_GOOD |
| `mydhl_lithium_ion_pi966_section_ii` | `HD` | DANGEROUS_GOOD |
| `mydhl_lithium_ion_pi967_section_ii` | `HV` | DANGEROUS_GOOD |
| `mydhl_lithium_metal_pi969_section_ii` | `HM` | DANGEROUS_GOOD |
| `mydhl_lithium_metal_pi970_section_ii` | `HW` | DANGEROUS_GOOD |
| `mydhl_excepted_quantities` | `HH` | DANGEROUS_GOOD |
| `mydhl_consumer_commodities` | `HK` | DANGEROUS_GOOD |
| `mydhl_magnetized_material` | `HX` | DANGEROUS_GOOD |
| `mydhl_not_restricted_dangerous_goods` | `HU` | DANGEROUS_GOOD |
| `mydhl_active_data_logger` | `HT` | DANGEROUS_GOOD |
| `mydhl_gogreen_climate_neutral` | `EE` | — |
| `mydhl_gogreen_plus_carbon_reduced` | `FE` | — |
| `mydhl_verbal_notification` | `JA` | NOTIFICATION |
| `mydhl_verbal_notification_alternative` | `JD` | NOTIFICATION |
| `mydhl_broker_notification` | `WG` | NOTIFICATION |
| `mydhl_paperless_trade` | `WY` | PAPERLESS |
| `mydhl_export_declaration` | `WO` | PAPERLESS |
| `mydhl_return_to_seller` | `PH` | RETURN |
| `mydhl_return_to_origin` | `PR` | RETURN |
| `mydhl_courier_time_window` | `JY` | DELIVERY_OPTIONS |
| `mydhl_remote_area_delivery` | `OO` | DELIVERY_OPTIONS |

Additional codes exist for special handling (`CR`, `CG`, `LG`, `LU`,
`QA`, `YC`), clearance (`WD`, `WF`, `WK`, `WL`, `WM`, `WB`, `WE`, `WH`,
`WI`, `WJ`, `WS`, `WT`), data/label (`PD`, `PZ`, `PQ`, `PP`), surcharges
(`FF`, `MA`, `GG`), import/export taxes (`XB`, `XX`, `XE`, `XJ`, `XK`),
data staging (`PT`/`PU`/`PV`/`PW`), and other DHL services (`PA`, `PJ`,
`PK`, `PL`, `PM`, `PO`, `30`). See `units.py` for the full list.

### Unified-option aliases

karrio's standard options resolve to MyDHL codes:

| Unified option | → MyDHL option | serviceCode |
|---|---|---|
| `insurance` | `mydhl_shipment_insurance` | `II` |
| `signature_confirmation` | `mydhl_direct_signature` | `SF` |
| `hold_for_pickup` | `mydhl_hold_for_collection` | `LX` |
| `hold_at_location` | `mydhl_hold_for_collection` | `LX` |
| `saturday_delivery` | `mydhl_saturday_delivery` | `AA` |
| `dangerous_goods` | `mydhl_dangerous_goods` | `HE` |
| `email_notification` | `mydhl_verbal_notification` | `JA` |
| `dry_ice` | `mydhl_dry_ice` | `HC` |

> **Note:** although the option enum is fully populated, the current
> `shipment_request` builder does **not** serialize `valueAddedServices`
> onto the wire payload. Options drive only `currency` / `declared_value`
> / `doc_files` (paperless) selection in `create.py`. Value-added
> service codes are defined and surfaced for the picker but are not yet
> attached to the shipment `content`.

`doc_files` is a special option (`lib.to_dict`, category `PAPERLESS`)
carrying the paperless-trade document list (see
[Paperless trade](#paperless-trade-plt)).

## Packaging types

`units.PackagingType` maps to DHL `typeCode`:

| karrio packaging | typeCode | DHL name |
|---|---|---|
| `mydhl_flyer` / `pak` | `FLY` | DHL Flyer |
| `mydhl_box_2` / `tube` | `2BC` | Box 2 |
| `mydhl_box_3` / `small_box` | `3BX` | Box 3 |
| `mydhl_box_4` | `4BX` | Box 4 |
| `mydhl_box_5` / `medium_box` | `5BX` | Box 5 |
| `mydhl_box_6` | `6BX` | Box 6 |
| `mydhl_box_7` | `7BX` | Box 7 |
| `mydhl_box_8` / `large_box` | `8BX` | Box 8 |
| `mydhl_express_envelope` / `envelope` | `3` | Express Envelope |
| `mydhl_jumbo_box` | `JB` | Jumbo Box |
| `mydhl_jumbo_box_junior` | `JJ` | Jumbo Box Junior |
| `mydhl_customer_packaging` / `your_packaging` | `YP` | Customer packaging |

## Data mapping

### Address — karrio `Address` → MyDHL `postalAddress` + `contactInformation`

Shipment create / pickup use a nested `postalAddress` +
`contactInformation`; rate uses a flatter `ErDetailsType`.

```
karrio Address                     MyDHL postalAddress / contactInformation
─────────────────                  ─────────────────────────────────────────
postal_code        ───►            postalAddress.postalCode
city               ───►            postalAddress.cityName
country_code       ───►            postalAddress.countryCode
state_code         ───►            postalAddress.provinceCode
address_line1      ───►            postalAddress.addressLine1
address_line2      ───►            postalAddress.addressLine2
extra              ───►            postalAddress.addressLine3   (shipment only)
suburb             ───►            postalAddress.countyName
state_name         ───►            postalAddress.provinceName   (shipment/pickup)
country_name       ───►            postalAddress.countryName    (shipment only)
email              ───►            contactInformation.email
phone_number       ───►            contactInformation.phone (and mobilePhone)
company_name       ───►            contactInformation.companyName (falls back to person_name, then "N/A")
person_name        ───►            contactInformation.fullName
(derived)          ───►            typeCode = "business" if company_name else "private"
```

Defaults: on shipment create, `phone` falls back to `"0000000000"` when
the address has no phone, and `companyName` falls back to person name
then the literal `"N/A"`.

### Parcel — karrio `Package` → MyDHL `PackageType`

```
karrio Package                     MyDHL PackageType
─────────────                      ─────────────────
packaging_type     ───►            typeCode (via PackagingType.map; None if unset)
weight.value       ───►            weight
length/width/height ──►            dimensions{length,width,height} as int
                                   (omitted unless all three present on
                                    shipment create; any present on rate)
```

`unitOfMeasurement` is `metric` when the parcel weight unit is `KG`,
`imperial` when `LB`. (Rate uses the `MeasurementUnit` enum, shipment
derives the same string inline.)

### Customs — karrio `CustomsInfo` → MyDHL `content` + `exportDeclaration`

Customs is sent on shipment create only when `is_international` (shipper
country ≠ recipient country). `lib.to_customs_info` provides a default
single-commodity declaration (sku `"0000"`, qty 1, parcel weight,
description from package description or `"Goods"`) when the request
carries no explicit customs.

```
karrio CustomsInfo                 MyDHL content / exportDeclaration
──────────────────                 ─────────────────────────────────
(international flag)        ───►    content.isCustomsDeclarable = true
incoterm (default "DDU")   ───►    content.incoterm
declared value*            ───►    content.declaredValue
currency                   ───►    content.declaredValueCurrency
                                   content.unitOfMeasurement (metric/imperial)
commodities[i]             ───►    exportDeclaration.lineItems[i] {
   (1-based index)                   number
   description / title     ───►        description (max 75 chars)
   value_amount            ───►        price (int)
   quantity                ───►        quantity{value, unitOfMeasurement:"PCS"}
   hs_code                 ───►        commodityCodes[{typeCode:"outbound", value}]
   (content_type)          ───►        exportReasonType (see below)
   origin_country          ───►        manufacturerCountry (falls back to shipper.country_code)
   weight                  ───►        weight{netValue, grossValue}
                                     }
invoice number             ───►    exportDeclaration.invoice.number (default "INV-00000")
invoice date               ───►    exportDeclaration.invoice.date  (default today)
```

`*declared value` resolution order (international only):
`options.declared_value` → `customs.duty.declared_value` →
`customs.commodities.value_amount` → `packages.total_value` → `1.0`.

**Export reason** (`content_type` → `exportReasonType`):

| karrio content_type | exportReasonType |
|---|---|
| `merchandise`, `commercial_purpose_or_sale` | `permanent` |
| `sample` | `temporary` |
| `return_merchandise`, `return_for_repair` | `return` |
| (anything else) | `permanent` |

`units.py` also defines `ExportReasonType` (`permanent` / `temporary` /
`return`), `InvoiceType` (`commercial`/`proforma`/`returns`) and
`PartyRoleType` enums for reference.

### Rate response — MyDHL `products[]` → `RateDetails`

```
ProductType                        RateDetails
───────────                        ───────────
totalPrice[].price (first w/price) total_charge
totalPrice[].priceCurrency         currency (default "USD")
deliveryCapabilities.totalTransitDays  transit_days
totalPriceBreakdown[].priceBreakdown[] extra_charges[{typeCode, price, currency}]
productCode → ShippingService.map  service
productName                        meta.service_name
productCode                        meta.product_code
networkTypeCode                    meta.network_type_code
localProductCode                   meta.local_product_code
deliveryCapabilities.estimatedDeliveryDateAndTime  meta.estimated_delivery
```

Only products with a non-empty `totalPrice` array produce a rate. If the
response has a `status` key or no `products`, zero rates are returned.

### Shipment response — MyDHL → `ShipmentDetails`

```
ShipmentResponseType               ShipmentDetails
────────────────────               ───────────────
shipmentTrackingNumber             tracking_number AND shipment_identifier
documents[].content                docs.label (single content, or
  (or packages[].documents[])         bundle_base64 of multiple)
documents[0].imageFormat           label_type (default "PDF")
packages[].trackingNumber          meta.package_tracking_numbers[]
trackingUrl                        meta.tracking_url
shipmentCharges[0].price           selected_rate.total_charge
shipmentCharges[0].priceCurrency   selected_rate.currency
shipmentCharges[0].serviceBreakdown[] selected_rate.extra_charges
ctx.service → ShippingService.map  selected_rate.service
```

A response is treated as success only when it has **no `status`** and a
non-null `shipmentTrackingNumber`.

## Carrier-specific invariants / gotchas

- **No shipment void.** The connector cannot cancel/void a created
  shipment. `shipment_cancel_request.py` / `shipment_cancel_response.py`
  schemas are generated but no mapper/provider wires them. Only pickups
  can be cancelled.
- **`tracking_number == shipment_identifier`.** Both fields are set to
  the single `shipmentTrackingNumber`. There is no separate internal
  handle (unlike GLS's TrackID or ParcelOne's two-tier IDs).
  Per-package `trackingNumber`s land in
  `meta.package_tracking_numbers`.
- **Paperless trade is a chained second call**, not a separate mutation.
  `create_shipment` POSTs the label, reads `shipmentTrackingNumber` from
  the response, then PATCHes `/shipments/{tn}/upload-image` with the
  `documentImages` payload built in `create.py`. The PATCH uses
  `on_ok=lambda response: dict(ok=True)` so a 2xx with empty/non-JSON
  body still counts as success. Its outcome is folded into the
  deserialization `ctx` as `paperless_response` and both the shipment
  body and the paperless body are run through `error.parse_error_response`.
- **Paperless gating.** PLT fires only when `is_international` AND at
  least one `doc_files` entry has `doc_type ∈ {commercial_invoice,
  invoice, proforma, certificate_of_origin}` AND a `doc_file`. Otherwise
  `payload.paperless` is `None` and no second call is made.
- **`getRateEstimates=True`** is always sent on shipment create, so the
  response carries `shipmentCharges` that the parser surfaces as
  `selected_rate`.
- **Label template is hardcoded** to `ECOM26_84_001` with
  `printerDPI=300`; `encodingFormat` is the lowercased `label_type`
  (default `pdf`). `LabelFormat` supports `pdf`/`zpl`/`lp2`/`epl`;
  `LabelTemplate` lists the common DHL templates but only
  `ECOM26_84_001` is used.
- **Incoterm default is `DDU`** on international shipments when
  `customs.incoterm` is absent. (Domestic shipments send no incoterm.)
- **`unitOfMeasurement` strings differ by surface.** Rate/shipment use
  `metric`/`imperial`; pickups always send `"metric"`. Line-item
  quantity unit is the literal `"PCS"`.
- **Pickups are one-time only.** `pickup_request` raises
  `lib.exceptions.FieldError` if `pickup_type` is anything other than
  `one_time`/`None`, with a message pointing the user at DHL to set up
  recurring pickups. Pickup datetime is formatted as
  `%Y-%m-%dT%H:%M:%S GMT+00:00`. An empty parcel list defaults to a
  single 1.0-unit package.
- **Pickup location** defaults to `"reception"`;
  `locationType` is `"residence"` for residential addresses else
  `"business"`.
- **Pickup cancel takes the bare confirmation number.** The serializer
  returns `payload.confirmation_number` as a plain string; the proxy
  also tolerates a dict with `confirmationNumber`.
- **Address validation is a GET**, not a POST. `type` is hardcoded
  `"delivery"` and `strictValidation=True`. Only `countryCode`,
  `postalCode`, `cityName`, `countyName` query params are sent (truthy
  ones only).
- **Proof of delivery** is fetched opportunistically: when a tracked
  shipment's computed status is `delivered`, `get_proof_of_delivery`
  GETs `/shipments/{tn}/proof-of-delivery`, collects `documents[].content`,
  and bundles them into a single PDF (`signature_image`). Wrapped in
  `lib.failsafe` so a POD failure never breaks tracking.
- **`account_number` is always echoed** in `accounts[{typeCode:
  "shipper", number}]` on rate/shipment/pickup, but is not the auth
  credential.

## Tracking

`tracking_request` joins tracking numbers into a query string
(`shipmentTrackingNumber={n}&shipmentTrackingNumber={m}…`) and GETs
`/tracking`. The response `shipments[]` is parsed one `TrackingDetails`
per shipment. Events are assumed **most-recent-first**, so
`events[0].typeCode` drives the overall status.

### Status mapping — `units.TrackingStatus` (event `typeCode`)

| karrio status | DHL typeCodes |
|---|---|
| `pending` | `PU`, `PL`, `RW` |
| `on_hold` | `OH`, `HP`, `HN`, `HX` |
| `delivered` | `OK`, `DD`, `DL`, `PD` |
| `out_for_delivery` | `WC`, `OO` |
| `ready_for_pickup` | `HP`, `LX` |
| `delivery_failed` | `BA`, `BN`, `CA`, `CD`, `CM`, `CR`, `MS`, `NH`, `SS` |
| `delivery_delayed` | `AD`, `DY`, `HI`, `HO`, `HW`, `RD`, `SM`, `WX` |
| `in_transit` | `DF`, `AF`, `AR`, `CC`, `CD`, `CI`, `CR`, `CS`, `CU`, `DS`, `FD`, `HP`, `MC`, `OF`, `PA`, `PF`, `PO`, `RD`, `RR`, `RT`, `SA`, `SC`, `SS`, `TD`, `TP`, `TR`, `UD`, `WC` |

Some codes appear in multiple buckets (e.g. `HP`, `WC`, `RD`, `SS`,
`CD`, `CR`). The first matching status when iterating the enum wins, and
the latest event's `typeCode` is matched first; unmatched events fall
back to `in_transit`.

### Incident reasons — `units.TrackingIncidentReason`

Per-event `reason` is derived from `typeCode` (e.g. `RF`/`CR` →
`consignee_refused`, `CC`/`CI`/`CD`/`CM`/`CU` → `customs_delay`,
`WX`/`HW` → `weather_delay`, `UD` → `delivery_exception_undeliverable`).
See `units.py` for the full table.

### TrackingInfo fields

`carrier_tracking_link` is built from `Settings.tracking_url`
(`https://www.dhl.com/ca-en/home/tracking/tracking-parcel.html?submit=1&tracking-id={}`).
Origin/destination country + postal code, shipping date, signed-by,
weight + unit, piece count, and service (`productCode →
ShippingService`) are populated from the shipment object.

## Error parsing

`error.parse_error_response` handles the MyDHL RFC-7807-style problem
shape. A response (or each element of a list response) is treated as an
error when it carries any of `detail`, `message`, or `title`.

```
ErrorResponseType                  models.Message
─────────────────                  ──────────────
status            ───►             code (str)
detail / message / title (first)   message
instance                           details.instance
title                              details.title
additionalDetails                  details.additionalDetails
```

Success responses are recognized by the **absence of a `status` key**
(plus the presence of the operation's success key —
`shipmentTrackingNumber`, `products`, `dispatchConfirmationNumbers`,
`address`, etc.). On shipment create, errors from both the label
response and the paperless PATCH response are parsed and concatenated.

## Service catalog (services.csv)

`units.DEFAULT_SERVICES` is built at import time by
`load_services_from_csv()` from
`karrio/providers/mydhl/services.csv`. Each CSV row is a (service, zone)
tuple; rows are grouped by service code (mapped to the karrio service
name via `ShippingService.map`) and accumulated into
`models.ServiceLevel` objects with `models.ServiceZone` entries. Columns:

```
service_code, service_name, zone_label, country_codes, min_weight,
max_weight, max_length, max_width, max_height, rate, currency,
transit_days, domicile, international
```

Weight/dimension units default to `KG`/`CM`; `currency` defaults to
`EUR`. The file currently covers `P` (Express Worldwide) weight/zone
bands. If the file is missing, `DEFAULT_SERVICES` is an empty list.

## References

- **Vendor OpenAPI (authoritative)** —
  `vendors/dpdhl-express-api-3.1.1_swagger.yaml` (title *"DHL Express
  APIs (MyDHL API)"*, version `3.1.1`). Servers: mock
  `https://api-mock.dhl.com/mydhlapi`, test
  `https://express.api.dhl.com/mydhlapi/test`, prod
  `https://express.api.dhl.com/mydhlapi`.
- **DHL developer portal** —
  <https://developer.dhl.com/api-reference/mydhl-express> (linked from
  plugin METADATA `documentation`).
- **Tracking status codes** — `vendors/status_1.csv`.
- **Generated schemas** — `karrio/schemas/mydhl/*.py` are generated from
  the per-operation sample JSON under `schemas/*.json` via `kcli codegen`
  (see the `generate` script). Regenerate with
  `./bin/run-generate-on modules/connectors/mydhl` — **never hand-edit**
  the generated `*.py` modules. The schema set: `error_response`,
  `rate_request`/`rate_response`, `shipment_request`/`shipment_response`,
  `shipment_cancel_request`/`shipment_cancel_response` (generated but
  unused), `tracking_request`/`tracking_response`, `pickup_create_*`,
  `pickup_update_*`, `pickup_cancel_*`,
  `address_validation_request`/`address_validation_response`.
- **Tests** — `tests/mydhl/` (`test_rate`, `test_shipment`,
  `test_tracking`, `test_pickup`, `test_address`, `test_document`);
  gateway fixture in `tests/mydhl/fixture.py`.
</content>
</invoke>
