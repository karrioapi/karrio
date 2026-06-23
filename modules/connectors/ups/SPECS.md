# UPS integration — specification

Reference for the UPS connector. UPS is a **direct carrier** (not a hub)
exposed through UPS's JSON REST API ("UPS Developer Kit" / RESTful APIs),
authenticated with OAuth 2.0 `client_credentials`. The connector wires
rating, shipment create / cancel / return, tracking, pickup
create / cancel, and paperless-documents upload.

The **vendor source of truth** is the set of OpenAPI YAMLs and Postman
collections kept under `vendors/` (`Rating.yaml`, `Shipping.yaml`,
`Tracking.yaml`, `Pickup.yaml`, `Paperless.yaml`,
`AddressValidation.yaml`, plus the `UPS *.postman_collection.json`
files and the `Tracking-*.html` code appendices). The connector's typed
schemas under `karrio/schemas/ups/*.py` are generated from JSON samples
in `schemas/` — never hand-edit them (see [References](#references)).

The plugin advertises itself as `production-ready`, `has_intl_accounts=True`.

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Data flow](#data-flow)
3. [Endpoints](#endpoints)
4. [Authentication](#authentication)
5. [Supported operations](#supported-operations)
6. [Services](#services)
7. [Service zones & rate-response service resolution](#service-zones--rate-response-service-resolution)
8. [Options](#options)
9. [Data mapping](#data-mapping)
10. [Delivery confirmation (signature) matrix](#delivery-confirmation-signature-matrix)
11. [Customs / international forms](#customs--international-forms)
12. [Label handling](#label-handling)
13. [Tracking status mapping](#tracking-status-mapping)
14. [Pickup](#pickup)
15. [Error parsing](#error-parsing)
16. [Carrier-specific invariants / gotchas](#carrier-specific-invariants--gotchas)
17. [References](#references)

---

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio RateRequest / ShipmentRequest /
│   (karrio core)         │   TrackingRequest / PickupRequest /
└───────────┬─────────────┘   DocumentUploadRequest
            │
            ▼
┌─────────────────────────┐
│  providers/ups          │   Pure data transforms.
│   rate.py               │   Unified model → typed UPS request,
│   shipment/create.py    │   typed UPS response → unified model.
│   shipment/cancel.py    │   No HTTP, no side effects.
│   shipment/return_shipment.py
│   tracking.py           │
│   pickup/create.py      │
│   pickup/cancel.py      │
│   document.py           │
│   error.py              │
│   units.py              │   ServiceCode, ServiceZone, ShippingService,
│                         │   ShippingOption, PackagingType, ReturnServiceCode,
│                         │   TrackingStatus, SurchargeType, UploadDocumentType, ...
│   utils.py              │   Settings: server_url, default_currency, authorization
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  mappers/ups/proxy.py   │   HTTP transport only.
│   - get_token           │   - OAuth token caching (thread-safe)
│   - get_rates           │   - Bearer auth on every call
│   - create_shipment     │   - Concurrent multi-number tracking
│   - cancel_shipment     │   - content-Type application/json (calls)
│   - create_return_shipment    application/x-www-form-urlencoded (token)
│   - get_tracking        │
│   - schedule_pickup     │
│   - cancel_pickup       │
│   - upload_document     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  UPS REST APIs          │
│  ─────────────────────  │
│  OAuth (security/v1)    │   client_credentials token
│  Rating  v2409          │   Shop (multi-service) + time-in-transit
│  Shipping v2409         │   ship / void / pickup-void
│  Track   v1             │   per-tracking-number details
│  Pickup  v2409          │   on-call (one-time) pickup creation
│  Paperless v1           │   customs document upload
└─────────────────────────┘
```

**Key architectural choices:**

- **Single-call shipment creation** — one `POST /api/shipments/v2409/ship`
  returns the label(s), shipment id, and any auxiliary documents
  (commercial invoice, COD turn-in page, high-value report, control-log
  receipt, shipping receipt, dangerous-goods paper). No second call.
- **OAuth2 `client_credentials`** with a per-connection cached access
  token, refreshed 30 minutes before expiry via the SDK's
  `connection_cache.thread_safe(...)` helper.
- **Static service catalog** — UPS does not expose a per-account product
  catalog through these APIs. `units.py` carries the full service
  enumeration (`ServiceCode`, `ShippingService`, plus the CSV-driven
  `DEFAULT_SERVICES` service levels in `services.csv`).
- **Returns reuse the ship endpoint** — `return_shipment` is a thin
  wrapper that forces `ups_return_service` on and calls
  `shipment.create`.
- **Generated schemas** — `karrio/schemas/ups/*.py` is generated from the
  JSON samples in `schemas/` with `--no-nice-property-names`
  `--append-type-suffix` (preserves UPS's PascalCase / camelCase field
  names). Don't hand-edit; regenerate with
  `./bin/run-generate-on modules/connectors/ups`.

## Data flow

### Rate (one HTTP call)

```
RateRequest                                  UPS Rating v2409
     │                                              │
     ├─► rate_request()                             │
     │     to_address() shipper/recipient/return    │
     │     to_packages() + presets                  │
     │     to_shipping_options(initializer)         │
     │     map service → ServiceCode (or default    │
     │                    ups_standard "11")         │
     │     ctx = {origin: EU|<country_code>}         │
     │                                              │
     │   ─ POST /api/rating/v2409/Shop              │
     │       ?additionalinfo=timeintransit ────────►│
     │                                              │  rate + ETA
     │   ◄─ RateResponse.RatedShipment[] ───────────│
     │                                              │
     ├─► _extract_details per RatedShipment:        │
     │     prefer NegotiatedRateCharges over         │
     │       published; total = TotalChargesWithTaxes│
     │       / TotalCharges / TotalCharge /          │
     │       TransportationCharges (first present)   │
     │     itemized → SurchargeType.map(Code|Type)   │
     │     service = ServiceZone.find(Code, origin)  │
     │     transit_days = TimeInTransit…BusinessDays  │
     ▼                                              ▼
list[RateDetails]                            (no further call)
```

### Shipment create (one HTTP call)

```
ShipmentRequest                              UPS Shipping v2409
     │                                              │
     ├─► shipment_request()                         │
     │     Shipper / ShipTo / ShipFrom              │
     │     PaymentInformation.ShipmentCharge[]      │
     │        "01" transportation, "02" duty        │
     │     Service ← ServiceCode.map(payload.service)│
     │     ShipmentServiceOptions ← options          │
     │     InternationalForms (if customs)           │
     │     Package[] (1 per parcel)                  │
     │     LabelSpecification (PDF/ZPL, stock size)  │
     │     ctx = {label{h,w,type}, return_service}   │
     │                                              │
     │   ─ POST /api/shipments/v2409/ship ─────────►│
     │                                              │  validate
     │   ◄─ ShipmentResponse.ShipmentResults ───────│  label gen
     │                                              │
     ├─► _extract_shipment:                          │
     │     ShipmentIdentificationNumber              │
     │       → tracking_number + shipment_identifier │
     │     PackageResults[].TrackingNumber           │
     │       → meta.tracking_numbers[]               │
     │     ShippingLabel.GraphicImage → docs.label   │
     │       (PDF: image_to_pdf rotate -90; bundle)  │
     │     Form/COD/HighValue/ControlLog/Receipt/DG  │
     │       → docs.invoice / extra_documents        │
     ▼                                              ▼
ShipmentDetails                              (no further call)
```

### Tracking (concurrent, one call per number)

```
TrackingRequest                              UPS Track v1
     │   tracking_numbers[]                         │
     ├─► run_concurently(fetch_tracking, numbers)   │
     │     per number:                              │
     │       GET /api/track/v1/details/{num}        │
     │         ?locale=<cfg>&returnSignature=true ─►│
     │       headers: transId (uuid),                │
     │                transactionSrc                 │
     │                (karrio-test|karrio-prod)      │
     │   ◄─ trackResponse.shipment[0] ──────────────│
     │                                              │
     ├─► drop empty bodies; keep packages that       │
     │     carry a `package` array                   │
     ├─► _extract_details per package:               │
     │     status ← TrackingStatus.find(activity      │
     │              .status.type), fallback type/code │
     │     events[], images (signature/photo),        │
     │     TrackingInfo (origin/dest/weight/signed_by)│
     ▼                                              ▼
list[TrackingDetails]                        (+ warnings as Message)
```

### Pickup create / cancel

```
PickupRequest                                UPS Pickup v2409
     │  pickup_type must be one_time (else FieldError)
     ├─► pickup_request()                            │
     │     PickupServiceCode ← option or              │
     │       default_pickup_service_code(country)     │
     │     PickupAddress, PickupDateInfo, TotalWeight │
     │   ─ POST /api/pickupcreation/v2409/pickup ───►│
     │   ◄─ PickupCreationResponse{PRN, RateResult} ─│
     ▼     confirmation_number ← PRN                  ▼

PickupCancelRequest                          UPS Shipping v2409
     ├─► prn = confirmation_number, cancel_by="02"    │
     │   ─ DELETE /api/shipments/v2409/pickup/02 ────►│
     │       header Prn: <prn>                         │
     │   ◄─ PickupCancelResponse.Response.ResponseStatus.Code == "1"
     ▼                                                 ▼
ConfirmationDetails
```

## Endpoints

Test mode: `https://wwwcie.ups.com` (CIE). Prod: `https://onlinetools.ups.com`.
(`Settings.server_url`, switched by `test_mode`.)

| Purpose | Method | Path |
|---|---|---|
| OAuth token | POST | `/security/v1/oauth/token` |
| Rate (Shop) | POST | `/api/rating/v2409/Shop?additionalinfo=timeintransit` |
| Create shipment | POST | `/api/shipments/v2409/ship` |
| Create return shipment | POST | `/api/shipments/v2409/ship` (same endpoint, return service forced) |
| Void / cancel shipment | DELETE | `/api/shipments/v2409/void/cancel/{shipmentIdentificationNumber}` |
| Tracking | GET | `/api/track/v1/details/{trackingNumber}?locale={locale}&returnSignature=true` |
| Schedule pickup | POST | `/api/pickupcreation/v2409/pickup` |
| Cancel pickup | DELETE | `/api/shipments/v2409/pickup/{cancel_by}` (header `Prn`) |
| Upload paperless document | POST | `/api/paperlessdocuments/v1/upload` (header `ShipperNumber`) |

`content-Type` is `application/json` on every API call except the OAuth
token call, which uses `application/x-www-form-urlencoded`.

## Authentication

OAuth2 `client_credentials` grant. The Basic-auth header is
`base64(client_id:client_secret)` (`Settings.authorization`). The
token call posts `grant_type=client_credentials`, optionally adding an
`x-merchant-id` header when `ConnectionConfig.merchant_id` is set.

`client_id` / `client_secret` resolve via `connection_client_id` /
`connection_client_secret`: the per-connection value when present, otherwise the
platform-wide system credential (`UPS_CLIENT_ID` / `UPS_SANDBOX_CLIENT_ID`,
mode-aware). So merchants can connect with only an account number when ops has
configured a UPS app.

```
get_token()                                       ┌──────────────────────┐
   │  cache_key (empty parts dropped):            │ connection_cache     │
   │   ups|<client_id>|<client_secret>|<merchant> │  .thread_safe(...)   │
   ▼                                              │  buffer_minutes=30   │
┌──────────────┐  miss / within 30 min            │  token_field:        │
│ fetch_token  │◄─────────────────────────────────│   access_token       │
│              │                                  │  expiry_field: expiry│
│  POST        │  cache hit                        │                      │
│  /security/  │─────────────────────────────────►│ (versioned key)      │
│  v1/oauth/   │                                  └──────────────────────┘
│  token       │
└──────┬───────┘
       │  Authorization: Basic b64(cid:secret)
       │  content-Type: application/x-www-form-urlencoded
       │  [x-merchant-id: <merchant_id>]   (optional)
       │  body: grant_type=client_credentials
       ▼
   response: { access_token, issued_at(ms), expires_in(s), ... }
   expiry = epoch(issued_at/1000) + expires_in   (stored as "expiry")
```

`merchant_id` is part of the cache key because the token is fetched with the
optional `x-merchant-id` header. Under platform-wide system credentials many
connections share one `client_id` / `client_secret`; keying on credentials
alone would let connections with different merchant ids reuse each other's
merchant-scoped token. Empty key parts are dropped, so a connection with no
`merchant_id` keeps the `ups|<client_id>|<client_secret>` key.

Expiry is computed from `issued_at` (epoch **milliseconds**) plus
`expires_in` (seconds) and stamped onto the cached payload as `expiry`.
Every rate / ship / cancel / track / pickup / document call carries
`Authorization: Bearer <access_token>`. If the token response carries
errors, `errors.ParsedMessagesError` is raised before any business call.

Connection settings (`mappers/ups/settings.py`):

| Field | Notes |
|---|---|
| `client_id` | OAuth client id — optional; falls back to system config when unset |
| `client_secret` | OAuth client secret — optional; falls back to system config when unset |
| `account_number` | UPS shipper number; used as `ShipperNumber` / `AccountNumber` |
| `account_country_code` | drives `default_currency` and pickup `AccountCountryCode` |
| `test_mode` | switches `server_url` and tracking `transactionSrc` |
| `metadata` / `config` | `config` feeds `ConnectionConfig` |

`default_currency` returns the country currency for `US / CA / FR / AU`
(`SUPPORTED_COUNTRY_CURRENCY`), else `"USD"`.

### ConnectionConfig

| Config key | Type | Purpose |
|---|---|---|
| `cost_center` | str | Shipment `CostCenter` (+ enables `CostCenterBarcodeIndicator`) |
| `merchant_id` | str | sent as `x-merchant-id` on the OAuth token call |
| `enforce_zpl` | bool | force label `Code=ZPL`; on PDF requests, attempt `zpl_to_pdf` and keep the original ZPL as `zpl_label` |
| `label_type` | `LabelType` | default label format when the request omits `label_type` |
| `locale` | str | tracking `locale` query param (default `en_US`) — read via `connection_config.locale` |
| `shipping_options` | list | option allowlist surfaced to the picker |
| `shipping_services` | list | service allowlist surfaced to the picker |

## Supported operations

| Operation | Mapper method | Provider |
|---|---|---|
| Rate | `create_rate_request` / `parse_rate_response` | `rate.py` |
| Ship | `create_shipment_request` / `parse_shipment_response` | `shipment/create.py` |
| Return ship | `create_return_shipment_request` / `parse_return_shipment_response` | `shipment/return_shipment.py` |
| Cancel ship | `create_cancel_shipment_request` / `parse_cancel_shipment_response` | `shipment/cancel.py` |
| Track | `create_tracking_request` / `parse_tracking_response` | `tracking.py` |
| Pickup | `create_pickup_request` / `parse_pickup_response` | `pickup/create.py` |
| Cancel pickup | `create_cancel_pickup_request` / `parse_cancel_pickup_response` | `pickup/cancel.py` |
| Document upload | `create_document_upload_request` / `parse_document_upload_response` | `document.py` |

No rate-confirm / manifest / address-validation operations are wired
(an `AddressValidation.yaml` vendor spec is present but not implemented).

## Services

UPS services carry two parallel representations: a **wire `ServiceCode`**
(2-digit string sent on the request) and a **display `ShippingService`**
(human-readable name). On a ship request the service comes from
`ServiceCode.map(payload.service)`; on a rate response the returned code
is resolved back to a display name via `ServiceZone.find(code, origin)`
(see next section).

### Base service codes (`ServiceCode`)

| Wire code | Service key | Display name |
|---|---|---|
| `01` | `ups_next_day_air` | UPS Next Day Air |
| `02` | `ups_2nd_day_air` | UPS 2nd Day Air |
| `03` | `ups_ground` | UPS Ground |
| `07` | `ups_express` / `ups_worldwide_express` | UPS Worldwide Express |
| `08` | `ups_worldwide_expedited` | UPS Worldwide Expedited |
| `11` | `ups_standard` | UPS Standard |
| `12` | `ups_3_day_select` | UPS 3 Day Select |
| `13` | `ups_next_day_air_saver` | UPS Next Day Air Saver |
| `14` | `ups_next_day_air_early` | UPS Next Day Air Early |
| `17` | `ups_worldwide_economy_ddu` | UPS Worldwide Economy DDU |
| `54` | `ups_worldwide_express_plus` | UPS Worldwide Express Plus |
| `59` | `ups_2nd_day_air_am` | UPS 2nd Day Air A.M. |
| `65` | `ups_worldwide_saver` | UPS Worldwide Saver |
| `70` | `ups_access_point_economy` | UPS Access Point Economy |
| `71` | `ups_worldwide_express_freight_midday` | UPS Worldwide Express Freight Midday |
| `72` | `ups_worldwide_economy_ddp` | UPS Worldwide Economy DDP |
| `74` | `ups_express_12_00_de` | UPS Express 12:00 DE |
| `82`–`86` | `ups_today_*_pl` | UPS Today (Poland domestic) |
| `96` | `ups_worldwide_express_freight` | UPS Worldwide Express Freight |

The `ups_*_ca / _eu / _mx / _pl / _pr` members are **zone-specific
aliases** that resolve to a base code (e.g. `ups_express_ca → "01"`,
`ups_expedited_eu → "08"`). They exist so a caller can request a
zone-named service and so rate responses can round-trip back to the
canonical service name.

`services.csv` additionally drives `DEFAULT_SERVICES`
(`models.ServiceLevel`) with per-service weight/dimension limits,
transit days, currency, domicile/international flags and `ServiceZone`
country lists. CSV columns:
`service_code, service_name, carrier_service_code, features, zone_label,
country_codes, min_weight, max_weight, max_length, max_width, max_height,
currency, weight_unit, dimension_unit, transit_days, domicile,
international`.

## Service zones & rate-response service resolution

A rate response only returns the 2-digit `Service.Code`, not the
display name. The same code means different products in different
origin zones (e.g. `01` is *Next Day Air* in `US` but *Express* in
`CA`). `rate_request` stamps `ctx["origin"]` = `"EU"` (when the shipper
country is an EU member) else the shipper country code; `ServiceZone.find`
then matches `(code, origin)` to the right `ShippingService`.

```
RatedShipment.Service.Code  +  ctx.origin
        │
        ▼  ServiceZone.find(code, origin)
   match (value[0]==code, value[1]==origin)
        │
        ├─ zone alias for a base code?  ─► canonical base name
        │     (via _ZONE_ALIAS_TO_BASE, built from ServiceCode at import)
        │
        └─ no zone match ─► ServiceCode.map(code)
        ▼
   ShippingService.map(name)   → service / meta.service_name
```

`_ZONE_ALIAS_TO_BASE` is computed at import (`_build_zone_alias_map`):
the first `ServiceCode` member for each wire value is treated as the
"base", and any `ServiceZone` member whose code resolves to a different
base name is recorded as an alias → base, so rate selection can match
"ups_standard" regardless of the origin zone.

`ServiceZone` also lists **JTL-composite variants** (return / saturday /
access-point combinations such as `ups_worldwide_express_return`,
`ups_expedited_door`, `ups_expedited_access_point`) mapped to their base
UPS code + `US`, so those display names round-trip through
`ShippingService.map`.

## Options

Options are `lib.OptionEnum`s on `ShippingOption`; the **first positional
arg is the UPS wire field name**. `shipping_options_initializer` derives
several aggregate flags before serialization:

- `pickup_options` — set when any of `hold_at_location`,
  `ups_epra_indicator`, `ups_access_point_pickup`,
  `ups_hold_for_pickup_indicator`, `ups_lift_gate_at_pickup_indicator`
  is present → emits shipment-indication `"01"` and `PickupOptions`.
- `delivery_options` — set for `ups_access_point_delivery`,
  `ups_lift_gate_at_delivery_indicator`,
  `ups_drop_off_at_ups_facility_indicator`,
  `ups_deliver_to_addressee_only_indicator` → emits indication `"02"`
  and `DeliveryOptions`.
- signature handling — resolves delivery-confirmation type + level (see
  the [signature matrix](#delivery-confirmation-signature-matrix)).
- dangerous goods — any DG flag (or `dangerous_good`) defaults
  `ups_restricted_articles` to `"Y"`.

### Selected option fields

| Option key | Wire field | Type / values | Notes |
|---|---|---|---|
| `ups_saturday_pickup_indicator` | `SaturdayPickupIndicator` | bool → `"Y"` | |
| `ups_saturday_delivery_indicator` | `SaturdayDeliveryIndicator` | bool → `"Y"` | unified `saturday_delivery` maps here |
| `ups_sunday_delivery_indicator` | `SundayDeliveryIndicator` | bool | |
| `ups_cod` | `COD` | float | unified `cash_on_delivery`; emits `CodType` (`CODFundsCode="0"`) |
| `ups_access_point_cod` | `AccessPointCOD` | float | emits currency + monetary value |
| `ups_deliver_to_addressee_only_indicator` | `DeliverToAddresseeOnlyIndicator` | bool | |
| `ups_direct_delivery_only_indicator` | `DirectDeliveryOnlyIndicator` | bool | |
| `ups_return_of_document_indicator` | `ReturnOfDocumentIndicator` | bool | |
| `ups_carbonneutral_indicator` | `UPScarbonneutralIndicator` | bool | |
| `ups_certificate_of_origin_indicator` | `CertificateOfOriginIndicator` | — | rate only |
| `ups_shipper_export_declaration_indicator` | `ShipperExportDeclarationIndicator` | bool | rate only |
| `ups_commercial_invoice_removal_indicator` | `CommercialInvoiceRemovalIndicator` | bool | |
| `ups_import_control` | `ImportControl` | enum `03/04/05` | |
| `ups_return_service` | `ReturnService` | `ReturnServiceCode` | enables return label |
| `ups_delivery_confirmation` | `DeliveryConfirmation.DCISType` | enum `1/2` | unified `signature_confirmation` triggers it |
| `ups_delivery_confirmation_level` | — | `P` / `S` | package vs shipment placement |
| `ups_inside_delivery` | `InsideDelivery` | enum `01/02/03` | |
| `ups_hold_for_pickup_indicator` | `HoldForPickupIndicator` | bool | unified `hold_at_location` |
| `ups_dropoff_at_ups_facility_indicator` | `DropoffAtUPSFacilityIndicator` | bool | |
| `ups_lift_gate_for_pickup_indicator` | `LiftGateForPickupIndicator` | bool | |
| `ups_lift_gate_for_delivery_indicator` | `LiftGateForDeliveryIndicator` | bool | |
| `ups_sdl_shipment_indicator` | `SDLShipmentIndicator` | bool | |
| `ups_item_disposal` | `ItemDisposal` / `ItemDisposalIndicator` | bool | |
| `ups_exchange_forward_indicator` | `ExchangeForwardIndicator` | bool | |
| `ups_epra_indicator` | `EPRAIndicator` / `EPRAReleaseCode` | bool | |
| `ups_negotiated_rates_indicator` | `NegotiatedRatesIndicator` | bool | **rate defaults to `"Y"`** unless explicitly `False`; ship always `"Y"` |
| `ups_frs_shipment_indicator` | `FRSShipmentIndicator` | bool | |
| `ups_rate_chart_indicator` | `RateChartIndicator` | bool | |
| `ups_user_level_discount_indicator` | `UserLevelDiscountIndicator` | bool | |
| `ups_tpfc_negotiated_rates_indicator` | `TPFCNegotiatedRatesIndicator` | bool | |
| `ups_access_point_pickup` | `01` | bool | PUDO category |
| `ups_access_point_delivery` | `02` | bool | PUDO category |

### Restricted-articles (dangerous goods)

`ups_restricted_articles` (unified `dangerous_good`) gates a
`RestrictedArticlesType` block aggregating the per-class flags:
`ups_alcoholic_beverages_indicator`, `ups_diagnostic_specimens_indicator`,
`ups_perishables_indicator`, `ups_plants_indicator`, `ups_seeds_indicator`,
`ups_special_exceptions_indicator` (also driven by `dangerous_good`),
`ups_tobacco_indicator`, `ups_ecigarettes_indicator`,
`ups_hemp_cbd_indicator`. (Rate request includes all of these; ship
request omits the e-cigarette / hemp-CBD pair.)

## Data mapping

### Address — karrio `Address` → UPS address (ship)

```
karrio Address                          UPS Shipper / ShipTo / ShipFrom
─────────────────                       ───────────────────────────────
company_name OR person_name  ───►       Name
person_name                  ───►       AttentionName
company_name                 ───►       CompanyDisplayableName
federal_tax_id / tax_id      ───►       TaxIdentificationNumber
phone_number (max 15)        ───►       Phone.Number (fallback "000-000-0000")
email                        ───►       EMailAddress
address_lines (each max 35)  ───►       Address.AddressLine[]
city                         ───►       Address.City
state_code                   ───►       Address.StateProvinceCode
postal_code                  ───►       Address.PostalCode
country_code                 ───►       Address.CountryCode
residential                  ───►       Address.ResidentialAddressIndicator ("Y")
```

`ShipFrom` is sourced from `payload.return_address or payload.shipper`.
`ShipperNumber` is `settings.account_number`.

### Parcel — karrio package → UPS `Package`

```
karrio Package                          UPS Package
──────────────                          ───────────
description (max 50)         ───►        Description
packaging_type               ───►        Packaging.Code (PackagingType enum)
length/width/height          ───►        Dimensions.{Length,Width,Height} (+ unit)
weight                       ───►        PackageWeight.Weight (+ WeightUnit KGS/LBS)
parcel.reference_number      ───►        ReferenceNumber.Value (US/US, PR/PR only)
```

Multi-piece: when `len(packages) > 1`, the per-package packaging code is
forced to `your_packaging` (`"02"`) on ship and `ups_unknown` (`"00"`)
on rate. Weight/dimension units come from
`COUNTRY_PREFERED_UNITS` (US → LB/IN) else the package's compatible
units.

### Packaging type (`PackagingType`)

| Unified | UPS code | | Unified | UPS code |
|---|---|---|---|---|
| `envelope` | `01` | | `pallet` | `30` |
| `pak` | `04` | | `small_box` | `2a` |
| `tube` | `03` | | `medium_box` | `2b` |
| `your_packaging` | `02` | | (large box) | `2c` |

(Full carrier list `00`–`67` in `units.py`, including USPS-shaped media
codes `56`–`67` for UPS Mail Innovations / SurePost.)

### Payment / billing — `PaymentInformation.ShipmentCharge[]`

Two charge entries are built: type `"01"` (transportation) and, when
customs is present, `"02"` (duty). Each maps `payment.paid_by` →
`BillShipper` (sender, defaults to `settings.account_number`) /
`BillReceiver` (recipient, with `ConsigneeBilledIndicator="Y"`) /
`BillThirdParty` (third_party).

#### Third-party billing via shipping options ("Billing" tab)

The JTL shipping-method flow never sets `payload.payment` (it always defaults
to `paid_by="sender"`), so a `THIRD_PARTY_BILLING` option group lets a method
configure recipient / third-party billing. When set these options **override**
the request-level payment / duty; otherwise they fall back to it.

| Option | Falls back to | UPS field (per `ShipmentCharge`) |
|---|---|---|
| `ups_bill_to` (enum sender/recipient/third_party) | `payment.paid_by` | selects `BillShipper` / `BillReceiver` / `BillThirdParty` on charge `Type 01` |
| `ups_billing_account_number` | `payment.account_number` | `Bill*.AccountNumber` |
| `ups_billing_postal_code` | — | `BillReceiver.Address.PostalCode` / `BillThirdParty.Address.PostalCode` |
| `ups_billing_country_code` | — | `BillThirdParty.Address.CountryCode` |
| `ups_bill_duties_to` (enum) | `customs.duty.paid_by` | same selection on charge `Type 02` (duty) |
| `ups_duties_account_number` | `customs.duty.account_number` | duty `Bill*.AccountNumber` |

For `third_party`, the payor address is built from the options' postal/country
(unless an explicit `payload.billing_address` / `customs.duty_billing_address`
is supplied, which wins).

### Reference number placement

- Domestic `US/US` and `PR/PR`: per-package `ReferenceNumber` from
  `package.reference_number`.
- All other lanes: shipment-level `ReferenceNumber` from
  `payload.reference`.

## Delivery confirmation (signature) matrix

UPS requires signature confirmation at **package** level for some
origin/destination pairs and **shipment** level for others, and not all
confirmation types are available on every lane. `units.py` encodes this:

- `DeliveryConfirmationLevel.get_level(origin, destination)` → `"P"`
  (package) for US→US/PR and CA→CA and PR→US/PR; `"S"` (shipment)
  otherwise.
- `DeliveryConfirmationAvailability.get_available_types/​get_preferred_type`
  → which `DCISType` codes are available (`1` signature required,
  `2` adult signature required) and the preferred one per lane.

The initializer validates the requested `ups_delivery_confirmation`
against availability and falls back to the preferred type; it then sets
the level so `rate.py` / `create.py` place the `DeliveryConfirmation`
block on the package (`P`) or `ShipmentServiceOptions` (`S`).

```
DCISType codes:  1 = signature required (DC-SR)
                 2 = adult signature required (DC-ASR)
```

## Customs / international forms

When `payload.customs` is present, `ShipmentServiceOptions.InternationalForms`
is built. `FormType` selection:

| Condition | `FormType` | Meaning |
|---|---|---|
| `paperless_trade` + `doc_references` present | `07` | reference uploaded documents (`UserCreatedForm[].DocumentID`) |
| `paperless_trade` (no refs) | `03` | UPS-generated commercial invoice |
| otherwise | `01` | traditional paper forms (includes `Contacts.SoldTo`) |

Per-commodity → `InternationalForms.Product[]`:

```
karrio Commodity                        UPS Product
────────────────                        ───────────
title / description (max 35) ───►        Description
quantity                     ───►        Unit.Number  (+ Unit "PCS")
value_amount                 ───►        Unit.Value
hs_code                      ───►        CommodityCode
sku                          ───►        PartNumber
origin_country (or shipper)  ───►        OriginCountryCode
weight (→ weight_unit)       ───►        ProductWeight.Weight
                                         NumberOfPackagesPerCommodity = "1"
                                         ExportType = "F"
```

Form-level: `InvoiceNumber` ← `customs.invoice`; `InvoiceDate` ←
`customs.invoice_date` (defaults today); `TermsOfShipment` ←
`Incoterm.map(...).name`; `ReasonForExport` ←
`CustomsContentType.map(content_type).value`; `CurrencyCode` ←
`customs.duty.currency or currency`; a fixed `DeclarationStatement`;
`InsuranceCharges` from `options.insurance`.

`Incoterm` (`StrEnum`) — `CFR, CIF, CIP, CPT, DAF, DDP, DDU, DEQ, DES,
EXW, FAS, FCA, FOB` (the enum **name** is sent as `TermsOfShipment`).

`CustomsContentType`: `sale=SALE`, `gift=GIFT`, `sample=SAMPLE`,
`repair=REPAIR`, `return_merchandise=RETURN`,
`inter_company_data=INTERCOMPANYDATA`, `other="Any other reason"`;
unified `documents→other`, `merchandise→sale`.

### Document upload (`/api/paperlessdocuments/v1/upload`)

`document.py` posts `UploadRequest` with one `UserCreatedForm` per file
(name, format, base64 file, `UserCreatedFormDocumentType`). The
`ShipperNumber` header comes from `options.ups_shipper_number` or
`settings.account_number`. Response `FormsHistoryDocumentID[].DocumentID`
becomes `DocumentDetails.doc_id` (also used as `file_name`), which the
caller feeds into `options.doc_references` so a subsequent ship request
references it via `FormType="07"`.

`UploadDocumentType` (unified → UPS):

| karrio | UPS code |
|---|---|
| `commercial_invoice` | `002` |
| `certificate_of_origin` | `003` |
| `pro_forma_invoice` | `008` (other document) |
| `packing_list` | `010` |
| `other` | `008` |

## Label handling

`LabelType` enum maps unified `PDF`/`ZPL` to `(format, width, height)`:
`PDF_6x4=("PNG",6,4)`, `PDF_8x4=("PNG",8,4)`, `ZPL_6x4=("ZPL",6,4)`.
The request label format comes from `payload.label_type` or
`ConnectionConfig.label_type`, defaulting to `PDF_6x4`.

- PDF labels: each package's `ShippingLabel.GraphicImage` is run through
  `lib.image_to_pdf(..., rotate=-90, resize={height:1800,width:1200})`;
  multiple packages are bundled via `lib.bundle_base64`.
- ZPL labels: returned as-is.
- `enforce_zpl` config forces `LabelImageFormat.Code="ZPL"` on the
  request; if the request label type was PDF, the connector attempts
  `lib.zpl_to_pdf(...)` and keeps the original ZPL as `docs.zpl_label`
  (falling back to the raw ZPL if conversion fails).

Auxiliary documents extracted into `docs.extra_documents`
(`ShippingDocumentCategory`): `Form.Image` → `docs.invoice`;
`CODTurnInPage` (cod_document), `HighValueReport` (high_value_report),
`ControlLogReceipt[]` (control_log_receipt), `PackageResults[].ShippingReceipt`
(shipping_receipt), `DGPaperImage[]` (dangerous_goods_paper).

## Tracking status mapping

`tracking.py` resolves status from the latest activity's `status.type`
(falling back to `status.code`), via `TrackingStatus.find`. UPS codes
are short alpha tokens (`status.type` = `D`/`I`/`M`/`X`/...; plus
finer-grained codes).

| karrio status | UPS codes |
|---|---|
| `pending` | `M`, `MV`, `MP`, `XD`, `OA`, `DD` |
| `picked_up` | `OR`, `PU`, `OC`, `OG` |
| `in_transit` | `I`, `DP`, `AA`, `AR`, `AF`, `AL`, `DS`, `IH`, `AP` |
| `out_for_delivery` | `OT`, `OD`, `OF`, `DL` |
| `delivered` | `D`, `FS`, `KB`, `F4` |
| `on_hold` | `X`, `EX`, `HX`, `HD`, `HI`, `HS`, `HU`, `NH` |
| `delivery_failed` | `RF`, `UR`, `UF`, `CC` |
| `cancelled` | `VD`, `CA`, `CN`, `CV` |
| `ready_for_pickup` | `RP`, `UU`, `AC`, `WC` |
| `delivery_delayed` | `DY`, `DE`, `SD` |
| `return_to_sender` | `RS`, `RT`, `RH`, `RU` |
| `unknown` | (fallback) |

`delivered` is also asserted when any activity has `status.type == "D"`.
Per-event `reason` is mapped via `TrackingIncidentReason` (carrier /
consignee / customs / weather buckets). `TrackingInfo` carries
origin/destination country + postal code (from `packageAddress[].type ==
ORIGIN|DESTINATION`), `signed_by` (`deliveryInformation.receivedBy`),
service description, pickup date, and package weight. Signature /
delivery photos populate `Images` (the `returnSignature=true` query
param enables them).

## Pickup

UPS supports **only on-call (one-time)** pickups via API; any other
`pickup_type` raises `lib.exceptions.FieldError`. `PickupServiceCode`
defaults via `default_pickup_service_code(origin, dest)`:

| Origin region | Same-region dest | Cross-region dest |
|---|---|---|
| EU country (incl. GB/CH/NO) | `011` | `007` |
| `CA` | `011` (CA→CA) | `007` |
| `MX` | `011` | `011` |
| `US` (default) | `003` (dest == origin) | `007` |

`PaymentMethod` is `"01"` when an account number is set, else `"00"`;
`OverweightIndicator="Y"` when weight > 70 LB. Cancel is by PRN
(`cancel_by="02"`, PRN passed in the `Prn` header).

## Error parsing

`error.parse_error_response` normalizes the several error/warning shapes
UPS returns into `list[models.Message]`:

```
response(s)                 ┌─────────────────────────────────────┐
   │                        │ parse_error_response                 │
   ├─ response.errors[] ──► │  → errors (level "error")            │
   │                        │                                      │
   ├─ trackResponse         │                                      │
   │   .shipment[0]         │                                      │
   │   .warnings[]    ────► │  → warnings (level "warning")        │
   │                        │                                      │
   ├─ UploadResponse        │                                      │
   │   .FormsHistory        │                                      │
   │   DocumentID.warnings  │  → warnings                          │
   │                        │                                      │
   └─ Fault.detail.Errors   │  → errors (PrimaryErrorCode)         │
      .ErrorDetail          └──────────────────┬──────────────────┘
      .PrimaryErrorCode                        ▼
                                       list[Message]
                            code  ← code|Code
                            message ← message|Description
```

The OAuth token path runs the same parser on the token response and
raises `ParsedMessagesError` if any error is present.

## Carrier-specific invariants / gotchas

- **API versions are pinned in the path**: rating / shipping / pickup use
  `v2409`; tracking uses `v1`; paperless documents use `v1`; OAuth uses
  `security/v1`. The shipping request body also sets `SubVersion`
  (`"v2409"` on ship, `"2409"` on rate/pickup) and the rate
  `RequestOption` is `"Shoptimeintransit"`.
- **`issued_at` is epoch milliseconds**, not seconds — divided by 1000
  before computing expiry. Getting this wrong over- or under-states the
  token lifetime by 1000×.
- **Rate `NegotiatedRatesIndicator` defaults ON** (`"Y"`) unless the
  caller explicitly sets it `False`; shipment always sends `"Y"`. So
  negotiated (account) rates are returned by default.
- **Total-charge fallback chain** on rate: `TotalChargesWithTaxes` →
  `TotalCharges` → `TotalCharge` → `TransportationCharges`, applied to
  the negotiated block when present, else the published block.
- **Phone fallback `"000-000-0000"`** is injected when an address has no
  phone, because UPS rejects missing phone numbers; addresses are also
  truncated (lines max 35, phone max 15, descriptions max 50).
- **Reference-number placement is lane-dependent** (per-package for
  US/US & PR/PR, shipment-level elsewhere) — UPS rejects the wrong
  placement.
- **`COD.CODFundsCode` is hardcoded `"0"`** (marked `TODO: find
  reference` in both rate and ship).
- **Service `Description` fields carry mislabeled hints** in the rate
  request (e.g. `ShipmentTotalWeight.UnitOfMeasurement.Description =
  "Dimension"`) — these are cosmetic and ignored by UPS.
- **Returns** reuse `/ship`; the wrapper defaults `ups_return_service`
  to `ups_return_3_attempt` (`"5"`) when none is supplied. The response
  surfaces `return_shipment` with `MIDualReturnShipmentKey`, `LabelURL`,
  `ReceiptURL` (+ local-language variants) in `meta`.
- **Tracking is fan-out + concurrent** (`lib.run_concurently`), one GET
  per tracking number; empty response bodies are filtered out, and
  per-number `transId` is a fresh UUID with `transactionSrc`
  `karrio-test` / `karrio-prod` keyed off `test_mode`.
- **`document.py` sets `carrier_name=settings.carrier_id`** on the upload
  details (uses `carrier_id` for both name and id fields).
- **Schemas are generated** with `--no-nice-property-names` so UPS's
  PascalCase (shipping/rating) and camelCase (tracking) field names are
  preserved verbatim — type names get a `Type` suffix
  (`--append-type-suffix`). kcli structurally collapses identically
  shaped objects, hence the reused type names in the schema modules
  (e.g. `CustomerClassificationType`, `LabelImageFormatType`,
  `AlternateDeliveryAddressAddressType`, `InvoiceLineTotalType` appear
  in many unrelated positions).

## References

- **Vendor OpenAPI specs** — `vendors/Rating.yaml`, `vendors/Shipping.yaml`,
  `vendors/Tracking.yaml`, `vendors/Pickup.yaml`, `vendors/Paperless.yaml`,
  `vendors/AddressValidation.yaml`.
- **Vendor Postman collections** — `vendors/UPS *.postman_collection.json`
  (Rating, Shipping, Tracking, Pickup, Paperless Documents, Address
  Validation).
- **Tracking code appendices** — `vendors/Tracking-status-description-codes.html`,
  `Tracking-package-activity-types.html`, `Tracking-package-exceptions.html`,
  `Tracking-movement-scans.html`, `Tracking-manifest-codes.html`,
  `Tracking-delivery-codes.html`, `Tracking-mail-innovation.html`,
  `Tracking-updates.html`.
- **Surcharge appendix** — UPS Rating appendix referenced inline in
  `units.py`: <https://developer.ups.com/api/reference/rating/appendix?loc=en_US>.
- **Generated schema provenance** — `karrio/schemas/ups/*.py` is generated
  from `schemas/*.json` via the `generate` script. Regenerate with
  `./bin/run-generate-on modules/connectors/ups` — never hand-edit the
  generated modules.
