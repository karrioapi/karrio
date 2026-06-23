# FedEx integration — specification

Reference for the FedEx connector. FedEx is a **direct carrier**
(`is_hub=False`) integrated over FedEx's **JSON REST** developer platform.
The connector supports rating, shipment creation, return shipments, shipment
cancellation, tracking (with signature proof-of-delivery), pickup
schedule/update/cancel, and electronic trade document (ETD) upload, all behind
OAuth2 `client_credentials` authentication.

The **vendor source of truth** is the FedEx Developer Portal. The captured
OpenAPI/JSON specs the typed schemas are generated from live under
`vendor/` (`rate-api.json`, `ship-api.json`, `pickup-api.json`, `track.json`,
`upload-documents-api.json`) plus the HTML references
`vendor/ API-Reference-Guide.html` and `vendor/Tracking-Status-Codes.html`.

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Data flow](#data-flow)
3. [Endpoints](#endpoints)
4. [Authentication](#authentication)
5. [Supported operations](#supported-operations)
6. [Services](#services)
7. [Options](#options)
8. [Connection config](#connection-config)
9. [Data mapping](#data-mapping)
10. [Carrier-specific invariants / gotchas](#carrier-specific-invariants--gotchas)
11. [Tracking status mapping](#tracking-status-mapping)
12. [Error parsing](#error-parsing)
13. [References](#references)

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
│  providers/fedex        │   Pure data transforms.
│   rate.py               │   Unified model → typed FedEx request,
│   shipment/create.py    │   typed FedEx response → unified model.
│   shipment/cancel.py    │   No HTTP, no side effects.
│   shipment/return_…py   │
│   tracking.py           │
│   pickup/{create,        │
│     update,cancel}.py   │
│   document.py           │
│   error.py              │
│   units.py              │   ShippingService, ShippingOption,
│   utils.py              │   ConnectionConfig, TrackingStatus, …
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  mappers/fedex/proxy.py │   HTTP transport only.
│   - get_rates           │   - OAuth token caching (two token pools)
│   - get_tracking        │   - Bearer auth on every call
│   - create_shipment     │   - gzip-aware response decode
│   - cancel_shipment     │   - async fan-out for ETD upload
│   - schedule/modify/     │
│     cancel_pickup       │
│   - upload_document     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  FedEx REST APIs        │
│  ─────────────────────  │
│  OAuth   /oauth/token              client_credentials
│  Rate    /rate/v1/rates/quotes
│  Ship    /ship/v1/shipments        create + cancel + return
│  Track   /track/v1/trackingnumbers
│          /track/v1/trackingdocuments  (signature POD)
│  Pickup  /pickup/v1/pickups
│  ETD     documentapi…/documents/v1/etds/upload
└─────────────────────────┘
```

**Key architectural choices:**

- **Static catalog** — services and options are fixed enums in `units.py`
  (`is_hub=False`, no per-account discovery). A `services.csv` next to
  `units.py` seeds `DEFAULT_SERVICES` (`models.ServiceLevel` rows with weight/
  dimension limits and US-domestic zone metadata).
- **Two OAuth token pools** — Rate/Ship/Pickup/Document calls authenticate
  with the `api_key`/`secret_key` pair (`shipping_auth`); Tracking calls
  authenticate with the separate `track_api_key`/`track_secret_key` pair
  (`track_auth`). Each is cached under its own key. The token pool is selected
  by `request.ctx["auth_type"]` (defaults to `shipping_auth`); only
  `tracking_request` stamps `auth_type="track_auth"`.
- **Return shipments reuse the create path** — `return_shipment_request`
  forces `fedex_return_shipment=True` and delegates to `shipment_request`;
  the proxy's `create_return_shipment` just calls `create_shipment`. Same
  `/ship/v1/shipments` endpoint.
- **Generated schemas** — `karrio/schemas/fedex/*.py` is generated from
  `schemas/*.json` with `kcli codegen … --no-nice-property-names` (camelCase
  preserved). Don't hand-edit; regenerate with
  `./bin/run-generate-on modules/connectors/fedex`.

## Data flow

### Rate (one HTTP call)

```
RateRequest                                FedEx Rate API
   │                                            │
   ├─► rate_request                             │
   │     to_address(shipper/recipient)          │
   │     to_packages(); to_shipping_options()   │
   │     is_intl → customsClearanceDetail        │
   │     rateRequestType = LIST/ACCOUNT/PREFERRED│
   │                                            │
   │   ─── authenticate (shipping_auth) ────────►│ /oauth/token
   │   ─── POST /rate/v1/rates/quotes ──────────►│
   │   ◄── output.rateReplyDetails[] ────────────│
   │                                            │
   ├─► _extract_details per reply:              │
   │     pick PREFERRED_CURRENCY → ACCOUNT →     │
   │       ratedShipmentDetails[0]               │
   │     totalNetChargeWithDutiesAndTaxes        │
   │       (fallback totalNetCharge)             │
   │     transit_days = business days to         │
   │       operationalDetail.commitDate          │
   ▼                                            ▼
list[RateDetails]
```

### Shipment create (one HTTP call)

```
ShipmentRequest                            FedEx Ship API
   │                                            │
   ├─► shipment_request                         │
   │     shipper / recipients[] / origin        │
   │     shippingChargesPayment (paid_by)       │
   │     customsClearanceDetail (intl only)     │
   │     etdDetail (paperless trade)            │
   │     labelSpecification (PDF/ZPL + stock)   │
   │     requestedPackageLineItems[]            │
   │                                            │
   │   ─── authenticate (shipping_auth) ────────►│ /oauth/token
   │   ─── POST /ship/v1/shipments ─────────────►│
   │   ◄── output.transactionShipments[0] ───────│
   │                                            │
   ├─► _extract_details:                        │
   │     masterTrackingNumber → tracking_number  │
   │                          + shipment_identifier
   │     pieceResponses[].packageDocuments →     │
   │       label (bundle_base64; url fetched     │
   │       if no encodedLabel)                    │
   │     shipmentDocuments → invoice / extras    │
   ▼                                            ▼
ShipmentDetails
```

### Tracking (one HTTP call, batch of tracking numbers)

```
TrackingRequest                            FedEx Track API
   │                                            │
   ├─► tracking_request                         │
   │     includeDetailedScans = True            │
   │     trackingInfo[] per tracking number     │
   │     ctx{auth_type: "track_auth"}           │
   │                                            │
   │   ─── authenticate (track_auth) ───────────►│ /oauth/token
   │   ─── POST /track/v1/trackingnumbers ──────►│
   │   ◄── output.completeTrackResults[] ────────│
   │                                            │
   ├─► _extract_details per result:             │
   │     latestStatusDetail.code → TrackingStatus│
   │     scanEvents[] → TrackingEvent[]          │
   │     if delivered: fetch signature POD       │
   │       (POST /track/v1/trackingdocuments)    │
   ▼                                            ▼
list[TrackingDetails]
```

## Endpoints

Server base: `https://apis-sandbox.fedex.com` (test) / `https://apis.fedex.com`
(prod), selected by `Settings.test_mode`.

| Purpose | Method | Path |
|---|---|---|
| OAuth token | POST | `/oauth/token` |
| Rate quotes | POST | `/rate/v1/rates/quotes` |
| Create shipment | POST | `/ship/v1/shipments` |
| Create return shipment | POST | `/ship/v1/shipments` (same as create) |
| Cancel shipment | PUT | `/ship/v1/shipments/cancel` |
| Tracking | POST | `/track/v1/trackingnumbers` |
| Signature proof-of-delivery | POST | `/track/v1/trackingdocuments` |
| Schedule pickup | POST | `/pickup/v1/pickups` |
| Cancel pickup | PUT | `/pickup/v1/pickups/cancel` |
| ETD document upload | POST | `documentapitest.prod.fedex.com/sandbox/documents/v1/etds/upload` (test) / `documentapi.prod.fedex.com/documents/v1/etds/upload` (prod) |

Notes:

- **ETD upload uses a separate host** (`documentapi*.prod.fedex.com`), not the
  `apis*.fedex.com` base. It posts `multipart/form-data` (the request bodies are
  URL-encoded per document, fanned out asynchronously).
- **Pickup cancel is `PUT /pickup/v1/pickups/cancel`** in the code — not the
  `DELETE …/{code}` shown in the integration PRD. The code is authoritative.
- **Pickup modify** (`modify_pickup`) is not a single endpoint: the proxy
  cancels the existing pickup (`PUT …/cancel`) and, if a
  `pickupConfirmationCode` came back, re-schedules (`POST …/pickups`).
- Standard JSON calls send headers `x-locale: en_US`,
  `content-type: application/json`, `authorization: Bearer <token>`.

## Authentication

OAuth2 **`client_credentials`** grant. The token endpoint is
`POST /oauth/token` with `content-Type: application/x-www-form-urlencoded` and
body `grant_type=client_credentials&client_id=<key>&client_secret=<secret>`.

There are **two independent credential pools**, selected per request by
`request.ctx["auth_type"]`:

| `auth_type` | Required fields | Used for | Cache key |
|---|---|---|---|
| `shipping_auth` (default) | `api_key`, `secret_key`, `account_number` | Rate, Ship, Cancel, Pickup, Document | `fedex\|<api_key>\|<secret_key>` |
| `track_auth` | `track_api_key`, `track_secret_key` | Tracking | `fedex\|<track_api_key>\|<track_secret_key>` |

If any required value for the selected pool is missing, `authenticate` raises
before any HTTP call. Tokens are cached via
`settings.connection_cache.thread_safe(...)` with `buffer_minutes=30` (refreshed
when within 30 minutes of expiry); `expiry` is computed from the token's
`expires_in`. Token-fetch errors are parsed through `error.parse_error_response`
and raised as `errors.ParsedMessagesError`.

```
request.ctx.auth_type ──► pick pool ──► cache lookup (per pool key)
       │                                     │ hit (>30m left)
       │                                     ▼
       │                              return cached token
       │ miss / expiring
       ▼
  POST /oauth/token
  Content-Type: application/x-www-form-urlencoded
  grant_type=client_credentials&client_id=…&client_secret=…
       │
       ▼
  {access_token, expires_in} ──► store {…, expiry}
```

## Supported operations

| Operation | Mapper method | Provider | Proxy |
|---|---|---|---|
| Rate | `create_rate_request` / `parse_rate_response` | `rate.py` | `get_rates` |
| Shipment create | `create_shipment_request` / `parse_shipment_response` | `shipment/create.py` | `create_shipment` |
| Return shipment | `create_return_shipment_request` / `parse_return_shipment_response` | `shipment/return_shipment.py` → `create.py` | `create_return_shipment` → `create_shipment` |
| Shipment cancel | `create_cancel_shipment_request` / `parse_cancel_shipment_response` | `shipment/cancel.py` | `cancel_shipment` |
| Tracking | `create_tracking_request` / `parse_tracking_response` | `tracking.py` | `get_tracking` |
| Pickup schedule | `create_pickup_request` / `parse_pickup_response` | `pickup/create.py` | `schedule_pickup` |
| Pickup update | `create_pickup_update_request` / `parse_pickup_update_response` | `pickup/update.py` | `modify_pickup` |
| Pickup cancel | `create_cancel_pickup_request` / `parse_cancel_pickup_response` | `pickup/cancel.py` | `cancel_pickup` |
| Document upload (ETD) | `create_document_upload_request` / `parse_document_upload_response` | `document.py` | `upload_document` |

## Services

Static `ShippingService` enum (`units.py`) — unified key → FedEx `serviceType`
wire code. The full set:

| Unified key | FedEx `serviceType` |
|---|---|
| `fedex_international_priority_express` | `FEDEX_INTERNATIONAL_PRIORITY_EXPRESS` |
| `fedex_international_first` | `INTERNATIONAL_FIRST` |
| `fedex_international_priority` | `FEDEX_INTERNATIONAL_PRIORITY` |
| `fedex_international_economy` | `INTERNATIONAL_ECONOMY` |
| `fedex_ground` | `FEDEX_GROUND` |
| `fedex_cargo_mail` | `FEDEX_CARGO_MAIL` |
| `fedex_cargo_international_premium` | `FEDEX_CARGO_INTERNATIONAL_PREMIUM` |
| `fedex_first_overnight` | `FIRST_OVERNIGHT` |
| `fedex_first_overnight_freight` | `FIRST_OVERNIGHT_FREIGHT` |
| `fedex_1_day_freight` / `_2_day_freight` / `_3_day_freight` | `FEDEX_{1,2,3}_DAY_FREIGHT` |
| `fedex_international_priority_freight` | `INTERNATIONAL_PRIORITY_FREIGHT` |
| `fedex_international_economy_freight` | `INTERNATIONAL_ECONOMY_FREIGHT` |
| `fedex_cargo_airport_to_airport` | `FEDEX_CARGO_AIRPORT_TO_AIRPORT` |
| `fedex_international_priority_distribution` | `INTERNATIONAL_PRIORITY_DISTRIBUTION` |
| `fedex_ip_direct_distribution_freight` | `FEDEX_IP_DIRECT_DISTRIBUTION_FREIGHT` |
| `fedex_intl_ground_distribution` | `INTL_GROUND_DISTRIBUTION` |
| `fedex_ground_home_delivery` | `GROUND_HOME_DELIVERY` |
| `fedex_smart_post` | `SMART_POST` |
| `fedex_priority_overnight` | `PRIORITY_OVERNIGHT` |
| `fedex_standard_overnight` | `STANDARD_OVERNIGHT` |
| `fedex_2_day` / `fedex_2_day_am` | `FEDEX_2_DAY` / `FEDEX_2_DAY_AM` |
| `fedex_express_saver` | `FEDEX_EXPRESS_SAVER` |
| `fedex_same_day` / `fedex_same_day_city` | `SAME_DAY` / `SAME_DAY_CITY` |
| `fedex_one_day_freight` | `FEDEX_ONE_DAY_FREIGHT` |
| `fedex_international_economy_distribution` | `INTERNATIONAL_ECONOMY_DISTRIBUTION` |
| `fedex_international_connect_plus` | `FEDEX_INTERNATIONAL_CONNECT_PLUS` |
| `fedex_international_distribution_freight` | `INTERNATIONAL_DISTRIBUTION_FREIGHT` |
| `fedex_regional_economy` | `FEDEX_REGIONAL_ECONOMY` |
| `fedex_next_day_freight` | `FEDEX_NEXT_DAY_FREIGHT` |
| `fedex_next_day` / `_10am` / `_12pm` / `_end_of_day` | `FEDEX_NEXT_DAY` / `…_10AM` / `…_12PM` / `…_END_OF_DAY` |
| `fedex_distance_deferred` | `FEDEX_DISTANCE_DEFERRED` |

`DEFAULT_SERVICES` (from `services.csv`, 14 rows) is a separate `ServiceLevel`
catalog carrying weight/dimension limits, currency/units, US-domestic zone
labels and `domicile`/`international` flags — used for service-level display,
not request mapping.

## Options

`ShippingOption` (`units.py`) is built on `lib.OptionEnum` where the **first arg
is the FedEx wire code** (read off `option.code`; no parallel wire-code dict).
Options are routed to one of three request buckets by membership lists:

- **`RATING_OPTIONS`** → `rateRequestControlParameters.variableOptions`
  (comma-joined): `FREIGHT_GUARANTEE`, `SATURDAY_DELIVERY`,
  `SMART_POST_ALLOWED_INDICIA`, `SMART_POST_HUB_ID`.
- **`PACKAGE_OPTIONS`** → `requestedPackageLineItems[].packageSpecialServices.
  specialServiceTypes` (per package): `ALCOHOL`, `APPOINTMENT`, `BATTERY`,
  `COD`, `DANGEROUS_GOODS`, `DRY_ICE`, `PRIORITY_ALERT[_PLUS]`,
  `NON_STANDARD_CONTAINER`, `PIECE_COUNT_VERIFICATION`, `SIGNATURE_OPTION`,
  `EVENING`, `DATE_CERTAIN`, `SATURDAY_PICKUP`.
- **`SHIPMENT_OPTIONS`** → `requestedShipment.shipmentSpecialServices.
  specialServiceTypes` (shipment level): a large set incl. `BROKER_SELECT_OPTION`,
  `CALL_BEFORE_DELIVERY`, `CUSTOM_DELIVERY_WINDOW`, `HOLD_AT_LOCATION`,
  `INSIDE_DELIVERY`/`_PICKUP`, `LIFTGATE_*`, `LIMITED_ACCESS_*`,
  `ELECTRONIC_TRADE_DOCUMENTS`, `RETURN_SHIPMENT`, `RETURNS_CLEARANCE`,
  `SATURDAY_DELIVERY`, `EVENT_NOTIFICATION`, `FEDEX_ONE_RATE`, … (full list in
  `units.py`).

Unified-option aliases mapped to FedEx options:

| karrio standard option | FedEx option / wire code |
|---|---|
| `cash_on_delivery` | `fedex_cod` → `COD` |
| `dangerous_good` | `fedex_dangerous_goods` → `DANGEROUS_GOODS` |
| `notification` | `fedex_event_notification` → `EVENT_NOTIFICATION` |
| `saturday_delivery` | `fedex_saturday_delivery` → `SATURDAY_DELIVERY` |
| `paperless_trade` | `fedex_electronic_trade_documents` → `ELECTRONIC_TRADE_DOCUMENTS` |
| `insurance` | mapped to `customsClearanceDetail.insuranceCharge` (intl) |

Free-form / typed options used by the mappers: `doc_files`, `doc_references`
(paperless, `category=PAPERLESS`), `shipper_instructions`,
`recipient_instructions`, `fedex_signature_option` (→ `SignatureOptionType`),
`fedex_smart_post_hub_id`, `fedex_smart_post_allowed_indicia`,
`fedex_one_rate`, `fedex_return_shipment`. `shipping_options_initializer`
filters out `doc_files` / `doc_references` from the special-service buckets so
they never get sent as `specialServiceTypes`.

`SignatureOptionType`: `adult` → `ADULT`, `direct` → `DIRECT`,
`indirect` → `INDIRECT`, `no_signature_required` → `NO_SIGNATURE_REQUIRED`,
`service_default` → `SERVICE_DEFAULT` (default when unmapped).

## Connection config

`ConnectionConfig` (`units.py`) declared members:

| Config key | Type | Use |
|---|---|---|
| `label_type` | `LabelType` enum | default label format/stock |
| `smart_post_hub_id` | str | SmartPost hub id fallback (when not on the option) |
| `shipping_options` | list | allowed options (carrier-config filtering) |
| `shipping_services` | list | allowed services |
| `locale` | `en_US` / `fr_CA` | locale |

Soft-accessed config keys (read via the dynamic `connection_config` /
`Options` fallback, not declared enum members, resolve to `None`/empty when
unset): `rate_request_types` (overrides the default
`["LIST","ACCOUNT","PREFERRED"]`), `fedex_rate_sort_order` (default
`COMMITASCENDING`), `fedex_carrier_codes` (→ top-level `carrierCodes`).

## Data mapping

### Address — karrio `Address` → FedEx `AddressType` / `ResponsiblePartyAddressType`

```
karrio Address                  FedEx address
─────────────────               ─────────────
address_lines (1+2)   ───►      streetLines
city                  ───►      city
state_code            ───►      stateOrProvinceCode (via provider_utils.state_code)
postal_code           ───►      postalCode
country_code          ───►      countryCode
residential           ───►      residential
company_name          ───►      contact.companyName (max 35)
person_name/contact   ───►      contact.personName (max 35)
email                 ───►      contact.emailAddress
phone_number          ───►      contact.phoneNumber (max 15, trim; default "000-000-0000")
tax_id (has_tax_info) ───►      tins[].number
```

**`state_code` quirk**: for `CA` (Canada) addresses, a `QC` state code is
rewritten to `PQ` (FedEx's legacy Québec abbreviation). All other codes pass
through unchanged; `None` stays `None`.

### Packaging — `PackagingType` (unified → FedEx)

`envelope`→`FEDEX_ENVELOPE`, `pak`→`FEDEX_PAK`, `tube`→`FEDEX_TUBE`,
`pallet`→`YOUR_PACKAGING`, `small/medium/large/extra_large_box`→the matching
`FEDEX_*_BOX`; default `your_packaging`→`YOUR_PACKAGING`. `SubPackageType`
maps to FedEx `subPackagingType` (default `OTHER`). `PackagePresets` carries
FedEx box/envelope/pak dimensions (IN/LB).

**Dimensions are only sent when the resolved packaging type is
`YOUR_PACKAGING`** — FedEx rejects custom dimensions on its own branded
packaging. This guard lives in both `rate.py` and `shipment/create.py`.

### Labels — `LabelType` (`imageType`, `labelStockType`)

| Unified `label_type` | imageType | labelStockType |
|---|---|---|
| `PDF` / `PDF_4x6` | `PDF` | `STOCK_4X6` |
| `PDF_4x6_75` / `_4x8` / `_4x9` | `PDF` | `STOCK_4X6.75` / `STOCK_4X8` / `STOCK_4X9` |
| `ZPL` / `ZPL_4x6` | `ZPLII` | `STOCK_4X6` |
| `ZPL_4x6_75` / `_4x8` / `_4x9` | `ZPLII` | `STOCK_4X6.75` / `STOCK_4X8` / `STOCK_4X9` |

`labelSpecification` is fixed at `labelFormatType=COMMON2D`,
`labelOrder=SHIPPING_LABEL_FIRST`. Default `label_type` is `PDF_4x6`.

### Payment — `PaymentType`

`account`→`ACCOUNT`, `collect`→`COLLECT`, `recipient`→`RECIPIENT`,
`sender`→`SENDER`, `third_party`→`THIRD_PARTY`. Shipping charges and duties
each get their own payor/responsibleParty block; the billing address is
selected from `payment.paid_by` (sender/recipient/third_party) and the duty
billing address from `customs.duty.paid_by`. The payment account number falls
back to `settings.account_number` for sender-paid; otherwise the supplied
`payment.account_number`.

#### Third-party billing via shipping options ("Billing" tab)

The JTL shipping-method flow never sets `payload.payment` (it always defaults
to `paid_by="sender"`), so a `THIRD_PARTY_BILLING` option group is the seam to
configure recipient / third-party billing on the method. When set these options
**override** the request-level payment; otherwise they fall back to it. They are
deliberately kept out of `SHIPMENT_OPTIONS` / `PACKAGE_OPTIONS` so they never
leak into `specialServiceTypes`.

| Option | Falls back to | FedEx request field |
|---|---|---|
| `fedex_bill_to` (enum sender/recipient/third_party) | `payment.paid_by` | `shippingChargesPayment.paymentType` |
| `fedex_billing_account_number` | `payment.account_number` | `shippingChargesPayment.payor.responsibleParty.accountNumber.value` |
| `fedex_billing_postal_code` / `fedex_billing_country_code` | — | `…responsibleParty.address.postalCode` / `.countryCode` (third-party payor) |
| `fedex_bill_duties_to` (enum) | `customs.duty.paid_by` | `customsClearanceDetail.dutiesPayment.paymentType` |
| `fedex_duties_account_number` | `customs.duty.account_number` | `dutiesPayment.payor.responsibleParty.accountNumber.value` |

`billing_address` precedence: explicit `payload.billing_address` → options
postal/country (when `third_party`) → shipper/recipient selected by `bill_to`.

### Customs — `CustomsInfo` → `CustomsClearanceDetailType` (intl only)

`customsClearanceDetail` is emitted only when the shipment is international.
`is_intl` is `True` when shipper/recipient countries differ **or** both are
`IN` (India domestic still requires a customs block).

```
karrio CustomsInfo               FedEx CustomsClearanceDetailType
──────────────────               ────────────────────────────────
incoterm                ───►     commercialInvoice.termsOfSale (default DDU)
content_type            ───►     commercialInvoice.shipmentPurpose (PurposeType)
invoice                 ───►     commercialInvoice.customerReferences[INVOICE_NUMBER]
duty.paid_by            ───►     dutiesPayment.paymentType + payor
commodities[i]:                  commodities[i]:
  value_amount          ───►       unitPrice / customsValue (× quantity)
  quantity              ───►       quantity / numberOfPieces (quantityUnits "PCS")
  hs_code               ───►       harmonizedCode
  description/title     ───►       description (max 35) / name (max 35)
  origin_country        ───►       countryOfManufacture (fallback shipper country)
  weight                ───►       weight {units, value}
  sku                   ───►       partNumber
declared_value          ───►     totalCustomsValue
insurance               ───►     insuranceCharge
```

`Incoterm` enum supports `DDP/DDU/DAP/DAT/EXW/CPT/C_F(C&F)/CIP/CIF/FCA/FOB`.
`PurposeType`: `gift`→`GIFT`, `sample`→`SAMPLE`, `sold`→`SOLD`,
`not_sold`→`NOT_SOLD`, `personal_effects`→`PERSONAL_EFFECTS`,
`repair_and_return`→`REPAIR_AND_RETURN`; unified `documents`→`other` (None),
`merchandise`→`SOLD`, `return_merchandise`→`REPAIR_AND_RETURN`. The rate path
defaults `shipmentPurpose` to `sold`; the ship path defaults to `other`.

### Rate response — `RateReplyDetailType` → `RateDetails`

```
rateReplyDetails[i]                       RateDetails
───────────────────                       ───────────
serviceType        ───► ShippingService → service
ratedShipmentDetails: pick rateType        (PREFERRED_CURRENCY → ACCOUNT → [0])
  totalBaseCharge        ───► extra "Base Charge"
  totalDiscounts         ───► extra "Discounts"
  shipmentRateDetail.taxes[]      ───► extra charges
  shipmentRateDetail.surCharges[] ───► extra charges
  totalNetChargeWithDutiesAndTaxes ──► total_charge
    (fallback totalNetCharge)
  currency               ───► currency
operationalDetail.commitDate ──► estimated_delivery
  business-day count to commitDate ──► transit_days
meta: service_name, transit_time, rate_zone
```

### Document upload (ETD) — `DocumentUploadRequest` → `PaperlessRequestType[]`

One `PaperlessRequestType` per document, fanned out async. `workflowName` is
`ETDPreshipment` when `pre_shipment` option set, else `ETDPostshipment`.
`UploadDocumentType` maps `commercial_invoice`→`COMMERCIAL_INVOICE`,
`certificate_of_origin`→`CERTIFICATE_OF_ORIGIN`,
`pro_forma_invoice`→`PRO_FORMA_INVOICE`, `packing_list`/`other`→`OTHER`. The
response surfaces `output.meta.docId` as `DocumentDetails.doc_id`.

## Carrier-specific invariants / gotchas

- **gzip-aware response decode.** `provider_utils.parse_response` attempts
  `gzip.decompress` first and falls back to the raw bytes before `lib.decode`.
  FedEx may gzip responses; all Rate/Ship/Track/Pickup proxy calls use this
  decoder.
- **Two token pools, two cache keys.** Tracking must use `track_auth` (its
  own key/secret); everything else uses `shipping_auth` (which additionally
  requires `account_number`). Misconfigured track credentials fail only on
  tracking calls.
- **`state_code` Québec remap** — `QC` → `PQ` for Canadian addresses.
- **Dimensions only on `YOUR_PACKAGING`** — see Packaging mapping.
- **Phone defaults to `000-000-0000`** when absent (max 15 chars, trimmed).
  Person/company names truncate to 35 chars.
- **Master tracking number is both IDs** — `_extract_details` sets
  `tracking_number` and `shipment_identifier` to `masterTrackingNumber`.
  Cancel uses `payload.shipment_identifier` as `trackingNumber` with
  `deletionControl=DELETE_ALL_PACKAGES`.
- **Label content fetch** — a piece document is used directly when it carries
  `encodedLabel`; otherwise the connector fetches the document `url` and
  base64-encodes it. Multiple labels/invoices are bundled via
  `lib.bundle_base64`.
- **Document categorization** — `_get_doc_category` classifies extra documents
  by substring of `contentType` (`RETURN`, `CUSTOMS`, `CERTIFICATE_OF_ORIGIN`,
  `DANGEROUS`, `PACKING`, `RECEIPT`), defaulting to `other`. Primary labels and
  invoices are excluded from `extra_documents`.
- **Return shipment** — forced via `fedex_return_shipment=True`; sends
  `returnShipmentDetail.returnType=PRINT_RETURN_LABEL` and stamps
  `return_service="fedex_return_shipment"` into the response ctx so
  `ReturnShipment` is populated.
- **Paperless trade (ETD)** — when `fedex_electronic_trade_documents` is set,
  `etdDetail` is added. If neither `doc_files` nor `doc_references` is present,
  `attributes=["POST_SHIPMENT_UPLOAD_REQUESTED"]` (documents uploaded
  separately afterward); when `doc_files` are present they are attached inline
  with `requestedDocumentTypes=["COMMERCIAL_INVOICE"]`.
- **SmartPost** — `smartPostInfoDetail` is sent only when a hub id is resolved
  (`fedex_smart_post_hub_id` option or `smart_post_hub_id` config); on the ship
  path it additionally requires `serviceType == "SMART_POST"`. Default indicia
  `PARCEL_SELECT`.
- **COD** — sent as `shipmentCODDetail` with `codCollectionType="CASH"` and the
  `cash_on_delivery` amount; currency from option/default.
- **Email notifications** — `emailNotificationDetail` is added when
  `email_notification` is on, or when a recipient email / `email_notification_to`
  exists, with events `ON_DELIVERY`, `ON_EXCEPTION`, `ON_SHIPMENT`.
- **`pickupType=DROPOFF_AT_FEDEX_LOCATION`** is hardcoded on both rate and ship
  requests (this is the shipment's pickup type, distinct from the Pickup API).
- **Pickup type mapping** — unified `daily`/`recurring` → `REGULAR_STOP`,
  everything else → `ON_CALL`. Default carrier code `FDXE`. Ready/closing times
  are normalized to `HH:MM` (accepts `HH:MM` or `HH:MM:SS`);
  `readyDateTimestamp` is `"{pickup_date}T{ready_time}:00Z"`.
- **Signature proof-of-delivery** — on `delivered` tracking results the parser
  fetches a `SIGNATURE_PROOF_OF_DELIVERY` PNG via
  `POST /track/v1/trackingdocuments` and attaches it as `images.signature_image`.
  Failures are swallowed via `lib.failsafe`.

## Tracking status mapping

`TrackingStatus` (`units.py`) maps FedEx scan/status codes
(`latestStatusDetail.code` and per-event `eventType`) to unified statuses.
Unknown codes fall back to `in_transit` at the result level.

| Unified status | FedEx codes |
|---|---|
| `pending` | `OC`, `OX`, `EP`, `MD` |
| `picked_up` | `PU`, `PX`, `OF`, `AP` |
| `in_transit` | `IT`, `IX`, `AA`, `AC`, `AF`, `AR`, `AX`, `DP`, `EA`, `EO`, `FD`, `LO`, `Ow`, `PF`, `PL`, `PM`, `SF`, `TR` |
| `out_for_delivery` | `AD`, `ED`, `OD` |
| `delivered` | `DL` |
| `on_hold` | `CD`, `SE`, `HA` |
| `delivery_failed` | `DE` |
| `cancelled` | `CA`, `RD` |
| `ready_for_pickup` | `HL`, `HP` |
| `delivery_delayed` | `DY`, `DD`, `PY` |
| `return_to_sender` | `RS`, `RT` |
| `unknown` | (no codes — catch-all) |

`TrackingIncidentReason` additionally normalizes exception codes (refused,
business-closed, not-home, incorrect-address, customs delay, weather, etc.)
onto karrio incident reasons; see `units.py` for the full table. Each scan
event carries `code`/`status`/`reason` derived from `eventType`. Datetimes are
parsed with `["%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"]`.

## Error parsing

`error.parse_error_response` normalizes several FedEx error/alert shapes into
`list[Message]`. It accepts a single dict or a list and, per result, collects:

```
result.errors[]                                  ──► Message (level "error")
result.output.alerts[]                           ──► Message (level from alertType)
result.output.message (when alertType == "NOTE") ──► Message (level "info")
result.error  (+ trackingNumberInfo.trackingNumber)──► Message (with tracking_number)
```

`_get_level` maps `alertType`: missing → `error`; `NOTE` → `info`,
`WARNING` → `warning`, `ERROR` → `error` (case-insensitive). Token-auth
failures during `authenticate` are parsed the same way and raised as
`errors.ParsedMessagesError`. Tracking additionally runs error parsing over
each `result.trackResults` carrying the `trackingNumber` into the message
details.

## References

- **FedEx Developer Portal** — <https://developer.fedex.com>
  - API Reference Guide — `vendor/ API-Reference-Guide.html`
  - Tracking Status Codes — `vendor/Tracking-Status-Codes.html`
    (also <https://developer.fedex.com/api/en-us/guides/api-reference.html#trackingstatuscodes>)
- **Captured vendor specs** (schema source of truth) — `vendor/rate-api.json`,
  `vendor/ship-api.json`, `vendor/pickup-api.json`, `vendor/track.json`,
  `vendor/upload-documents-api.json`.
- **Generated schemas** — `karrio/schemas/fedex/*.py`, generated from
  `schemas/*.json` via the connector's `generate` script
  (`kcli codegen … --no-nice-property-names`). Regenerate with
  `./bin/run-generate-on modules/connectors/fedex` — never hand-edit.
