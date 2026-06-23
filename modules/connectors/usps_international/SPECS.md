# USPS International integration — specification

Reference for the `usps_international` connector. It targets the **modern
USPS APIs platform** (`api.usps.com`, OAuth2 + JSON REST, all `v3`
endpoints) and covers the cross-border lanes only: rate, label
(international-label), cancel, tracking, pickup, and SCAN-form manifest.

This connector is the **international sibling of the domestic `usps`
connector**. The two share the same OAuth platform, the same payment-token
flow, the same proxy shape, and most of the same `units.py` enums. They
differ in three ways that matter:

- **Label endpoint** — international posts to
  `/international-labels/v3/international-label`; domestic posts to
  `/labels/v3/label`.
- **Origin/destination guard** — `usps_international` *requires* US origin
  and a *non-US* destination; the domestic connector is US→US.
- **Customs** — international always builds a `customsForm` block (CN22/CN23
  content), plus a distinct `ShippingService` set
  (`*_INTERNATIONAL`, `GLOBAL_EXPRESS_GUARANTEED`) and `customsContentType`
  enum.

There is **no `vendor/` directory** in this connector — the source of truth
is the hand-written sample JSON under `schemas/*.json` from which
`karrio/schemas/usps_international/*.py` is generated.

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Data flow](#data-flow)
3. [Endpoints](#endpoints)
4. [Authentication](#authentication)
5. [Supported operations](#supported-operations)
6. [Services & options](#services--options)
7. [Data mapping](#data-mapping)
8. [Customs (CN22/CN23)](#customs-cn22cn23)
9. [Carrier-specific invariants / gotchas](#carrier-specific-invariants--gotchas)
10. [Error parsing](#error-parsing)
11. [References](#references)

---

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio RateRequest / ShipmentRequest /
│   (karrio core)         │   CustomsInfo / TrackingRequest /
└───────────┬─────────────┘   PickupRequest / ManifestRequest
            │
            ▼
┌─────────────────────────┐
│ providers/usps_international │  Pure data transforms.
│   rate.py               │  Unified model → typed USPS request,
│   shipment/create.py    │  typed USPS response → unified model.
│   shipment/cancel.py    │  No HTTP, no side effects.
│   shipment/return_shipment.py
│   tracking.py           │
│   pickup/{create,update,cancel}.py
│   manifest.py           │
│   error.py              │
│   units.py              │  ShippingService, ShippingOption,
│                         │  PackagingType, RateIndicator,
│                         │  CustomsContentType, LabelType,
│                         │  TrackingStatus, DEFAULT_SERVICES
│   utils.py              │  Settings, AccountType, ConnectionConfig,
│                         │  multipart-response parsing
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ mappers/usps_international/proxy.py │  HTTP transport only.
│   - authenticate (OAuth, cached)    │
│   - get_payment_token (cached)      │
│   - get_rates / create_shipment     │
│   - cancel_shipment / get_tracking  │
│   - schedule/modify/cancel_pickup   │
│   - create_manifest                 │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  USPS APIs (v3, JSON REST)          │
│  ─────────────────────────────────  │
│  OAuth2 v3            token          │
│  Payments v3          payment auth   │
│  International Prices via            │
│    Shipments v3 options/search       │
│  International Labels v3  label       │
│  Tracking v3          events         │
│  Pickup v3            carrier-pickup  │
│  Scan-Forms v3        SCAN form       │
└─────────────────────────┘
```

**Key architectural choices:**

- **Per-parcel fan-out.** `rate.py` and `shipment/create.py` build a list
  of one request per parcel and the proxy fires them via
  `lib.run_asynchronously`. The shipment parser aggregates N label
  responses into one `ShipmentDetails` via `lib.to_multi_piece_shipment`;
  the rate parser uses `lib.to_multi_piece_rates`.
- **Two-token auth.** Every shipping/cancel call carries both a Bearer
  `access_token` (OAuth2) **and** an `X-Payment-Authorization-Token`
  obtained from a second cached call to the Payments API.
- **Static service catalog.** Services are a fixed enum plus a CSV-driven
  `DEFAULT_SERVICES` (`service_levels`). There is no live per-account
  catalog fetch (unlike parcelone).
- **Generated schemas.** `karrio/schemas/usps_international/*.py` is
  generated from `schemas/*.json`. Regenerate with
  `./bin/run-generate-on modules/connectors/usps_international` — never
  hand-edit.

## Data flow

### Rate (per parcel)

```
RateRequest                                  USPS Shipments v3
   │                                               │
   ├─► guard: shipper US, recipient non-US         │
   ├─► map services → mail class                   │
   ├─► one RateRequestType per parcel              │
   │     pricingOptions[].priceType                │
   │     originZIPCode / foreignPostalCode         │
   │     destinationCountryCode                    │
   │                                               │
   │  ─── POST /shipments/v3/options/search ──────►│  (run_asynchronously
   │      (one call per parcel)                    │   per parcel)
   │                                               │
   │  ◄── pricingOptions[].shippingOptions[]       │
   │        .rateOptions[].rates[] ────────────────│
   │                                               │
   ├─► flatten rates, map productName → service    │
   │     filter by machinable_piece ctx            │
   ▼                                               ▼
list[RateDetails]                            (done)
```

### Shipment create (per parcel, two tokens)

```
ShipmentRequest                              USPS Payments + Int'l Labels
   │                                               │
   ├─► guard: shipper US, recipient non-US         │
   ├─► to_mail_class(service)                      │
   ├─► to_customs_info (weight_unit=LB)            │
   ├─► one LabelRequestType per parcel             │
   │     imageInfo / toAddress / fromAddress       │
   │     senderAddress / packageDescription        │
   │     customsForm                               │
   │                                               │
   │  ─── authenticate() ──────────────────────────►│ OAuth (cached)
   │  ─── get_payment_token() ─────────────────────►│ Payments (cached)
   │                                               │
   │  ─── POST /international-labels/v3/            │
   │        international-label ───────────────────►│
   │        Authorization: Bearer <token>          │
   │        X-Payment-Authorization-Token: <ptoken>│
   │                                               │
   │  ◄── { labelMetadata, labelImage } ───────────│
   │        (JSON or multipart — see invariants)   │
   │                                               │
   ├─► _extract_details:                            │
   │     labelMetadata.trackingNumber →            │
   │        tracking_number + shipment_identifier  │
   │     labelImage → docs.label                   │
   │     postage + extraServices + fees → rate     │
   ▼                                               ▼
ShipmentDetails (multi-piece)               (done)
```

### Cancel / tracking (per identifier)

```
ShipmentCancelRequest                        USPS Int'l Labels v3
   │  shipment_identifier + options.shipment_identifiers (de-duped set)
   │  ─── DELETE /international-labels/v3/international-label/{trackingNumber} ─►
   │  ◄── { status: "CANCELED" } ──────────────────────────────────────────────
   ▼  success = all responses CANCELED

TrackingRequest                              USPS Tracking v3
   │  ─── GET /tracking/v3/tracking/{trackingNumber}?expand=DETAIL ─►
   │  ◄── { trackingEvents[], status, mailClass, ... } ─────────────
   ▼  status mapped from status / statusCategory / eventType
```

## Endpoints

Test mode: `https://api-cat.usps.com`. Prod: `https://api.usps.com`.
Selected by `Settings.server_url` on `test_mode`.

| Purpose | Method | Path |
|---|---|---|
| OAuth token | POST | `/oauth2/v3/token` |
| Payment authorization token | POST | `/payments/v3/payment-authorization` |
| Rate (options search) | POST | `/shipments/v3/options/search` |
| Create international label | POST | `/international-labels/v3/international-label` |
| Cancel label | DELETE | `/international-labels/v3/international-label/{trackingNumber}` |
| Tracking | GET | `/tracking/v3/tracking/{trackingNumber}?expand=DETAIL` |
| Schedule pickup | POST | `/pickup/v3/carrier-pickup` |
| Modify pickup | POST | `/pickup/v3/carrier-pickup/{confirmationNumber}` |
| Cancel pickup | POST | `/pickup/v3/carrier-pickup/{confirmationNumber}` |
| Create manifest (SCAN form) | POST | `/scan-forms/v3/scan-form` |

All JSON bodies use `Content-Type: application/json`, except the OAuth
token call which uses `application/x-www-form-urlencoded`.

The return-shipment flow reuses the create-label endpoint —
`create_return_shipment` simply calls `create_shipment` (see
[return shipments](#return-shipments)).

`cancel_pickup` posts to the pickup-by-confirmation path and forces an
`{"ok": true}` body on HTTP success via `on_ok` (the live API returns an
empty body on cancel).

## Authentication

OAuth2 `client_credentials` grant. The `client_id` / `client_secret`
pair (from `Settings`) is sent in the form body — **not** as Basic Auth —
to `/oauth2/v3/token`, with an explicit `scope` covering every API the
connector touches:

```
addresses · international-prices · subscriptions · payments · pickup ·
tracking · labels · scan-forms · companies ·
service-delivery-standards · locations · international-labels ·
prices · shipments
```

### Token caching

Two independent caches, both via `Settings.connection_cache.thread_safe`
with a 30-minute refresh buffer:

```
access token                                  payment token
────────────                                  ─────────────
cache key:                                    cache key:
 access|usps_international|<cid>|<secret>       payment|usps_international|<cid>|<secret>

expiry: now + expires_in (from response)      expiry: now + 50 minutes (fixed)
token_field: (default access_token)           token_field: paymentAuthorizationToken
buffer_minutes: 30                            buffer_minutes: 30
```

The **payment token** is a second hop: `get_payment_token` first calls
`authenticate()` for a Bearer token, then POSTs to
`/payments/v3/payment-authorization` with two roles — `LABEL_OWNER` and
`PAYER` — each carrying `CRID`, `MID`, `accountType`, `accountNumber`
(and `manifestMID` for `LABEL_OWNER`) from `Settings`. The returned
`paymentAuthorizationToken` rides on shipping/cancel calls as the
`X-Payment-Authorization-Token` header.

### Settings fields

| Field | Purpose |
|---|---|
| `client_id` / `client_secret` | OAuth2 credentials |
| `account_number` | EPS / permit / meter account number (payment roles) |
| `account_type` | `AccountType` enum — `EPS` (default), `PERMIT`, `METER` |
| `manifest_MID` | Mailer ID used for the `LABEL_OWNER` role's `manifestMID` |
| `CRID` | Customer Registration ID (payment roles) |
| `MID` | Mailer ID (payment roles) |
| `account_country_code` | `"US"` (origin is always US) |

### Connection config (`ConnectionConfig`)

| Key | Type | Purpose |
|---|---|---|
| `permit_ZIP` | str | Permit ZIP |
| `permit_number` | str | Permit number |
| `shipping_options` | list | Default option overrides |
| `shipping_services` | list | Default service filter |
| `price_type` | enum | `RETAIL`/`COMMERCIAL`/`COMMERCIAL_BASE`/`COMMERCIAL_PLUS`/`CONTRACT` — default rate `priceType` when the request omits `usps_price_type` |

## Supported operations

| Operation | Wired | Notes |
|---|---|---|
| Rate | ✅ | `/shipments/v3/options/search`, per parcel |
| Shipment create | ✅ | International label, per parcel, multi-piece aggregation |
| Shipment cancel | ✅ | DELETE by tracking number; success = all `CANCELED` |
| Return shipment | ✅ | Wrapper over create with `usps_return_receipt=True` |
| Tracking | ✅ | Per tracking number, `expand=DETAIL` |
| Pickup schedule | ✅ | `one_time` only — daily/recurring rejected |
| Pickup update | ✅ | POST by confirmation number |
| Pickup cancel | ✅ | POST by confirmation number |
| Manifest (SCAN form) | ✅ | Form `5630`, PDF, `8.5x11LABEL` |

## Services & options

### Services — `ShippingService` (wire mail-class codes)

| Karrio service | Wire `mailClass` |
|---|---|
| `usps_first_class_package_international_service` | `FIRST-CLASS_PACKAGE_INTERNATIONAL_SERVICE` |
| `usps_priority_mail_international` | `PRIORITY_MAIL_INTERNATIONAL` |
| `usps_priority_mail_express_international` | `PRIORITY_MAIL_EXPRESS_INTERNATIONAL` |
| `usps_global_express_guaranteed` | `GLOBAL_EXPRESS_GUARANTEED` |
| `usps_all` | `ALL` |

`ShippingService.to_mail_class(product_code)` reduces a verbose product
code (e.g. a CSV/rate-response product name slug) back to one of the five
mail classes by substring match on the enum names. `to_product_code` /
`to_product_name` convert between USPS product-name strings and karrio
slugs. The default-service catalog (`DEFAULT_SERVICES`, exposed as
`service_levels`) is loaded from `services.csv` keyed by mail class, with
per-row weight/dimension limits and per-country `ServiceZone`s.

### Packaging — `PackagingType` (`rateIndicator`-style codes)

Carrier codes map to flat-rate / single-piece indicators; unified
packaging maps onto them:

| Unified | Wire code | Meaning |
|---|---|---|
| `envelope` | `E4` | Priority Mail Express Int'l Flat Rate Envelope |
| `pak` / `tube` | `SP` | Single Piece |
| `pallet` | `PL` | Large Flat Rate Box |
| `small_box` | `FS` | Small Flat Rate Box |
| `medium_box` | `FB` | Medium Flat Rate Box / Large Flat Rate Bag |
| `your_packaging` | `LE` | Single-piece parcel |

Carrier-only codes (no unified alias) include `E6`, `FA`, `FE`, `FP`,
`PA`, and the `ECOMPRO` family `EP`/`HA`/`HB`/`HE`/`HL`/`HP`/`HS`. The
full descriptive list lives in `RateIndicator`.

### Options — `ShippingOption` (wire extra-service codes & flags)

Numeric extra-service options (sent in `extraServices: [int]`):

| Option | Wire code | Category |
|---|---|---|
| `usps_hazardous_materials_class_7_radioactive_materials` | `813` | DANGEROUS_GOOD |
| `usps_hazardous_materials_class_9_unmarked_lithium_batteries` | `820` | DANGEROUS_GOOD |
| `usps_hazardous_materials_division_6_2_biological_materials` | `826` | DANGEROUS_GOOD |
| `usps_hazardous_materials` | `857` | DANGEROUS_GOOD |
| `usps_insurance_below_500` | `930` | INSURANCE |
| `usps_insurance_above_500` | `931` | INSURANCE |
| `usps_return_receipt` | `955` | RETURN |

Custom (non-extra-service) options — listed in `CUSTOM_OPTIONS`, mapped to
named request fields rather than `extraServices`:

| Option | Wire field | Type |
|---|---|---|
| `usps_mail_class` | `mailClass` | `ShippingService` |
| `usps_facility_id` | `facilityId` | str |
| `usps_machinable_piece` | `machinable` | bool |
| `usps_price_type` | `priceType` | `priceType` enum |
| `usps_hold_for_pickup` | `holdForPickup` | bool (PUDO) |
| `usps_carrier_release` | `carrierRelease` | bool |
| `usps_processing_category` | `processingCategory` | str |
| `usps_rate_indicator` | `rateIndicator` | `RateIndicator` |
| `usps_physical_signature_required` | `physicalSignatureRequired` | bool (SIGNATURE) |
| `usps_extra_services` | `extraServices` | list |
| `usps_shipping_filter` | `shippingFilter` | enum `["PRICE"]` |

Unified aliases: `insurance → usps_insurance_below_500`,
`hold_at_location → usps_hold_for_pickup`.

**Insurance routing** (`shipping_options_initializer`): a unified
`insurance` value > 500 is rewritten to `usps_insurance_above_500` (`931`);
otherwise `usps_insurance_below_500` (`930`). The split exists because USPS
prices international insurance in two tiers with distinct extra-service
codes.

## Data mapping

### Address — `ToAddressType` (recipient, non-US)

```
karrio recipient                         USPS ToAddressType
────────────────                         ──────────────────
address_line1          ───►              streetAddress
address_line2          ───►              secondaryAddress
city                   ───►              city
postal_code            ───►              postalCode
state_code             ───►              province
country_code           ───►              country + countryISOAlpha2Code
first_name|person_name ───►              firstName
last_name | " "        ───►              lastName  (single space fallback)
company_name           ───►              firm
phone_number           ───►              phone
```

### Address — `AddressType` (`fromAddress` + `senderAddress`, US)

```
karrio shipper                           USPS AddressType
──────────────                           ────────────────
address_line1          ───►              streetAddress
address_line2          ───►              secondaryAddress
city                   ───►              city
state_code             ───►              state          (US states only)
postal_code            ───►              ZIPCode / ZIPPlus4 (zip5 / zip4)
first_name|person_name ───►              firstName
last_name | " "        ───►              lastName
company_name           ───►              firm
phone_number           ───►              phone
email                  ───►              email
(constant)             ───►              ignoreBadAddress = True
```

`fromAddress` and `senderAddress` are populated from the same shipper.
`fromAddress.ZIPCode` uses `to_zip5`; `senderAddress.ZIPCode` uses
`to_zip4` falling back to the raw postal code.

### Package — `PackageDescriptionType`

```
karrio package                           USPS PackageDescriptionType
──────────────                           ───────────────────────────
weight.LB              ───►              weight (weightUOM = "lb")
length.IN / height.IN / width.IN ──►     length / height / width (dimensionsUOM = "in")
girth.value            ───►              girth
service mail class     ───►              mailClass
usps_rate_indicator    ───►              rateIndicator (default "DR")
usps_processing_category ──►             processingCategory (default "NON_MACHINABLE")
usps_destination_facility_type ──►       destinationEntryFacilityType (default "NONE")
hold_for_pickup_address ──►              destinationEntryFacilityAddress (when set)
total_value / declared_value /
  customs value / 1.0  ───►              packageOptions.packageValue
payload.reference      ───►              customerReference[].referenceNumber
extra-service options  ───►              extraServices: [int]  (codes not in CUSTOM_OPTIONS)
shipment_date | today  ───►              mailingDate
```

`extraServices` is taken verbatim from `usps_extra_services` if supplied,
otherwise computed as `lib.to_int(option.code)` for every non-custom
option — i.e. the wire code is read straight off the `OptionEnum`, not a
parallel dict.

### Rate response → `RateDetails`

```
rates[].rate / rateOption                RateDetails
─────────────────────────                ───────────
rate.productName|description|mailClass → service (via to_product_code)
rateOption.totalPrice    ───►            total_charge (USD)
rateOption.totalBasePrice ──►            extra_charges["Base Price"]
rateOption.extraServices[] ──►           extra_charges[name]
rate.mailClass / processingCategory /
  dimensionalWeight / rateIndicator /
  priceType / SKU / zone   ───►          meta.usps_*
```

The `machinable_piece` ctx value filters rates: a machinable request drops
non-machinable products and vice versa (substring `"machinable"` in the
service code).

### Tracking response → `TrackingDetails`

```
TrackingResponseType                     TrackingDetails
────────────────────                     ───────────────
trackingNumber         ───►              tracking_number
trackingEvents[]                          events[]:
  eventTimestamp ───►                       date / time / timestamp
  eventType      ───►                       description + per-event status
  eventCode      ───►                       code
  eventCity/ZIP/State/Country ──►           location (", "-joined)
expectedDeliveryTimeStamp ──►            estimated_delivery / info.expected_delivery
mailClass        ───►                    info.shipment_service
originCountry/ZIP, destinationCountryCode/ZIP → info.shipment_origin/destination_*
status / statusCategory ──►              status (TrackingStatus match)
```

`TrackingStatus` matches by case-insensitive substring against both
`status` and `statusCategory`, defaulting to `in_transit`:

| Karrio status | Match phrases |
|---|---|
| `on_hold` | `on hold` |
| `delivered` | `delivered` |
| `in_transit` | `in transit` (default) |
| `delivery_failed` | `delivery failed` |
| `delivery_delayed` | `delivery delayed` |
| `out_for_delivery` | `out for delivery` |
| `ready_for_pickup` | `ready for pickup` |

`delivered` is set when the resolved status equals `delivered`.

## Customs (CN22/CN23)

Every international label carries a `customsForm`. `to_customs_info` is
called with `weight_unit=LB` so commodity weights arrive in pounds.

```
karrio CustomsInfo                       USPS CustomsFormType
──────────────────                       ────────────────────
content_description    ───►              contentComments
content_type           ───►              customsContentType (CustomsContentType, default OTHER)
invoice                ───►              invoiceNumber
options.aes            ───►              AESITN
options.license_number ───►              licenseNumber
options.certificate_number (max 12) ──►  certificateNumber
usps_restriction_type  ───►              restrictionType
usps_restriction_comments ──►            restrictionComments
commodities[i]                            contents[i] (ContentType):
  description|title|"Item" (max 12) ──►     itemDescription
  quantity             ───►                 itemQuantity
  value_amount         ───►                 itemValue
  value_amount×quantity ──►                 itemTotalValue
  weight (lb)          ───►                 itemWeight (weightUOM="lb")
  weight×quantity      ───►                 itemTotalWeight
  hs_code              ───►                 HSTariffNumber
  origin_country       ───►                 countryofOrigin
  category             ───►                 itemCategory
```

`importersReference` / `exportersReference` are not populated.

### `customsContentType` — `CustomsContentType`

Wire enum values: `MERCHANDISE`, `GIFT`, `DOCUMENT`, `COMMERCIAL_SAMPLE`,
`RETURNED_GOODS`, `OTHER`, `HUMANITARIAN_DONATIONS`, `DANGEROUS_GOODS`,
`CREMATED_REMAINS`, `NON_NEGOTIABLE_DOCUMENT`, `MEDICAL_SUPPLIES`,
`PHARMACEUTICALS`.

Unified aliases: `documents → DOCUMENT`, `sample → COMMERCIAL_SAMPLE`,
`return_merchandise → RETURNED_GOODS`. Anything unmapped defaults to
`OTHER`.

## Carrier-specific invariants / gotchas

- **Origin must be US, destination must not be US.** Both `rate_request`
  and `shipment_request` raise `OriginNotServicedError` when the shipper
  is not `US`, and `DestinationNotServicedError` when the recipient *is*
  `US`. This is the hard line between this connector and domestic `usps`.

- **Two tokens per label.** A label POST/DELETE will fail without both the
  Bearer `access_token` and the `X-Payment-Authorization-Token`. The
  payment token has a fixed 50-minute lifetime (independent of the OAuth
  token's `expires_in`).

- **Multipart label responses.** The international-label response may come
  back as JSON *or* as a multipart body (label image part + metadata part).
  `provider_utils.parse_response` tries JSON first, then falls back to
  `normalize_multipart_response` + boundary splitting, returning a dict
  keyed by the multipart `name`s (JSON parts parsed, file parts kept as
  raw content). A parse failure yields
  `{error:{code:"SHIPPING_SDK_ERROR", message:"Failed to parse multipart response"}}`.

- **`lastName` single-space fallback.** Both addresses send `lastName=" "`
  (a single space) when no last name is present — USPS rejects an empty
  `lastName`, so a space is used as a placeholder.

- **`ignoreBadAddress=True`** is hardcoded on the US shipper addresses so a
  soft address-validation warning doesn't block the label.

- **Default package fields.** `rateIndicator` defaults to `"DR"`,
  `processingCategory` to `"NON_MACHINABLE"`, `destinationEntryFacilityType`
  to `"NONE"` when not supplied.

- **`packageValue` fallback chain**: `total_value` → `declared_value` →
  `customs.commodities.value_amount` → `1.0`. USPS rejects a missing/zero
  declared value on an international piece.

- **Truncation limits.** `itemDescription` is capped at 12 chars,
  `certificateNumber` at 12 chars (`lib.text(..., max=12)`). These are
  USPS field-length limits on the CN form.

- **`extraServices` wire codes come from `OptionEnum.code`.** The list is
  `lib.to_int(option.code)` over every option not in `CUSTOM_OPTIONS` —
  there is no parallel `{option: code}` dict to drift.

- **Pickups are `one_time` only.** `pickup_request` raises a `FieldError`
  for any `pickup_type` other than `one_time`/`None`, directing the caller
  to set up recurring pickups directly with USPS.

- **Manifest is SCAN form 5630.** `manifest_request` always sends
  `form="5630"`, `imageType="PDF"`, `labelType="8.5x11LABEL"`, builds the
  `fromAddress` by splitting `person_name` on the first space into
  first/last name, and lists the shipment tracking numbers under
  `shipment.trackingNumbers`.

- **Cancel de-dupes identifiers.** `shipment_cancel_request` collects
  `shipment_identifier` plus `options.shipment_identifiers` into a `set`,
  so a repeated tracking number is only cancelled once. Success requires
  *every* response to report `status == "CANCELED"`.

### Return shipments

`return_shipment.py` is a thin wrapper: it forces
`usps_return_receipt=True` onto the options and delegates to
`shipment.create.shipment_request`. The proxy's `create_return_shipment`
simply calls `create_shipment`, so returns hit the same
`/international-labels/v3/international-label` endpoint with the same
two-token auth.

## Error parsing

`error.parse_error_response` (provider) normalizes both single and list
responses. For each response containing an `"error"` key, it expands
`error.errors[]` if present, else treats `error` itself as one entry, and
maps each to a `models.Message`:

```
response.error                            models.Message
──────────────                            ──────────────
error.errors[].code | error.code   ───►   code
error.errors[].message | .detail   ───►   message
error.source                       ───►   details.source
(kwargs, e.g. tracking_number)     ───►   details.*
```

Two transport-level helpers in `utils.py` shape raw responses before they
reach the provider parser:

- **`parse_error_response`** (proxy `on_error`): reads the response body,
  tries JSON; on failure wraps the text body as
  `{error:{code:<http code>, message:<text>}}`.
- **`parse_response`**: the multipart-aware success parser described above;
  used by `create_shipment` so label bodies in either format normalize to
  a dict the shipment parser can read.

OAuth and payment-token failures raise `errors.ParsedMessagesError` early
(inside `authenticate` / `get_payment_token`) so a bad credential surfaces
before any shipping call.

## References

- **Vendor source of truth** — hand-written sample JSON under
  `schemas/*.json` (`error_response`, `label_request`, `label_response`,
  `rate_request`, `rate_response`, `pickup_request`/`response`,
  `pickup_update_request`/`response`, `scan_form_request`/`response`,
  `tracking_responses`). There is **no `vendor/` directory** for this
  connector.
- **USPS Developer Portal / APIs platform** — <https://developer.usps.com/>
  (OAuth2 v3, International Labels v3, Shipments v3, Tracking v3, Pickup
  v3, Scan-Forms v3, Payments v3).
- **Domestic sibling** — `karrio/modules/connectors/usps` shares the OAuth
  + payment-token flow and most `units.py` enums; differs by label
  endpoint (`/labels/v3/label`), US→US routing, and the absence of a
  `customsForm`.
- **Generated schemas** — `karrio/schemas/usps_international/*.py` is
  generated from `schemas/*.json` by `./generate` (kcli, run with
  `--no-nice-property-names`). Regenerate with
  `./bin/run-generate-on modules/connectors/usps_international` — never
  hand-edit. The first `find ... -exec rm` line in `generate` deletes the
  whole `karrio/schemas/usps_international` tree, so any module without a
  matching `schemas/*.json` sample disappears on regen.
