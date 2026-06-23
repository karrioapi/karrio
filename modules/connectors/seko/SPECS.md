# SEKO Logistics integration — specification

Reference for the SEKO Logistics connector. SEKO is a JSON/REST carrier
served from the **OmniParcel** API (`omniparcel.com`). The connector
wires rating, shipment create/cancel, tracking, and manifest. There is
no published vendor spec dir in this repo — the typed schema modules
under `karrio/schemas/seko/*.py` are generated from sample JSON captured
under `schemas/*.json` (see [References](#references)).

The connector is marked `production-ready` (`karrio/plugins/seko/__init__.py`,
`id="seko"`, label `"SEKO Logistics"`).

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio RateRequest / ShipmentRequest /
│   (karrio core)         │   ShipmentCancelRequest / TrackingRequest /
└───────────┬─────────────┘   ManifestRequest
            │
            ▼
┌─────────────────────────┐
│  providers/seko         │   Pure data transforms.
│   rate.py               │   Unified model → typed SEKO request,
│   shipment/create.py    │   typed SEKO response → unified model.
│   shipment/cancel.py    │   No HTTP, no side effects.
│   tracking.py           │
│   manifest.py           │
│   error.py              │
│   units.py              │   ShippingService, ShippingOption,
│   utils.py              │   CustomsOption, LabelType, PackagingType,
│                         │   TrackingStatus, TrackingIncidentReason,
│                         │   ConnectionConfig, Settings, parse_error_response
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  mappers/seko/proxy.py  │   HTTP transport only.
│   - get_rates           │   - One POST per operation
│   - create_shipment     │   - Header: access_key: <key>
│   - cancel_shipment     │   - Content-Type: application/json; charset=utf-8
│   - get_tracking        │   - JSON body via lib.to_json(request.serialize())
│   - create_manifest     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  SEKO OmniParcel API    │
│  ─────────────────────  │
│  /ratesqueryv1/...      │   available rates
│  /labels/printshipment  │   create label
│  /labels/delete         │   cancel
│  /labels/statusv2       │   tracking
│  /v2/publishmanifestv4  │   manifest
└─────────────────────────┘
```

**Key architectural choices:**

- **Single-call per operation.** Every operation is one POST. There is
  no token exchange — authentication is a static `access_key` header
  (the commented-out OAuth scaffolding in `utils.py` is unused).
- **No multi-piece fan-out.** One `ShippingRequestType` carries all
  packages in its `Packages[]` array; the response returns one or more
  `Consignments[]`. The connector surfaces `Consignments[0]` as the
  primary shipment and keeps every `ConsignmentId` / `TrackingUrl` in
  `meta`.
- **Static service catalog from CSV.** `units.py` loads
  `service_levels` from `services.csv` at import (`DEFAULT_SERVICES =
  load_services_from_csv()`) rather than fetching a live profile.
- **Generated schemas** — `karrio/schemas/seko/*.py` is generated from
  `schemas/*.json`. Regenerate with
  `./bin/run-generate-on modules/connectors/seko`; never hand-edit.

## Data flow

### Shipment create (one HTTP call)

```
ShipmentRequest                              SEKO OmniParcel
     │                                              │
     │  shipment_request()                          │
     ├─► lib.to_address(shipper/recipient/return)   │
     ├─► lib.to_packages(parcels)                   │
     ├─► lib.to_shipping_options(...)               │
     ├─► lib.to_customs_info(...)                   │
     ├─► map service → ShippingService.value        │
     ├─► resolve label_type/label_format            │
     │     from LabelType.map(payload.label_type)   │
     │                                              │
     ├─► ShippingRequestType (typed)                │
     │     ctx = {label_type, label_format, service}│
     │                                              │
     │   ─── POST /labels/printshipment ───────────►│
     │                                              │  validate
     │   ◄── { Consignments:[{Connote,             │  label gen
     │          ConsignmentId, TrackingUrl,         │  routing
     │          OutputFiles{<label_type>:[b64]},    │
     │          Cost}], CarrierName, ... } ─────────│
     │                                              │
     ├─► _extract_details (uses ctx):               │
     │     Connote          → tracking_number       │
     │     ConsignmentId    → shipment_identifier   │
     │     OutputFiles[label_type] → docs.label     │
     │       (bundled b64, label_format)            │
     │     Consignments[0].Cost → selected_rate     │
     │                                              │
     ▼                                              ▼
ShipmentDetails                               (no further call)
```

### Rating (one HTTP call)

```
RateRequest ─► rate_request() ─► RatingRequestType
            ─── POST /ratesqueryv1/availablerates ───►
            ◄── { Available:[{DeliveryType, Cost, Route,
                  QuoteId, CarrierName, ...}] }
            ─► one RateDetails per Available[] entry
               service ← ShippingService.map(DeliveryType)
               total_charge ← Cost; currency ← config.currency or "USD"
```

### Cancel (one HTTP call)

```
ShipmentCancelRequest ─► request body is a JSON array of IDs:
   options.shipment_identifiers or [payload.shipment_identifier]
            ─── POST /labels/delete ───►
            ◄── { "<id>": "<message>" , ... }   (map of id → status string)
   success  = any value contains "Deleted"
   errors   = any value that is a string and does NOT contain "Deleted"
```

### Tracking (one HTTP call)

```
TrackingRequest ─► request body is the raw tracking_numbers array
            ─── POST /labels/statusv2 ───►
            ◄── [ { ConsignmentNo, Status, Events:[{EventDT,
                  OmniCode, Code, Description, Location}], ... } ]
   one TrackingDetails per element that has any Events
   status ← OmniCode of the latest event (events reversed → [0]),
            mapped via TrackingStatus; default in_transit
```

## Endpoints

Base URL is environment-switched by `test_mode`:

- **Test:** `https://staging.omniparcel.com`
- **Prod:** `https://api.omniparcel.com`

| Purpose | Method | Path |
|---|---|---|
| Available rates | POST | `/ratesqueryv1/availablerates` |
| Create shipment / print label | POST | `/labels/printshipment` |
| Cancel / delete label | POST | `/labels/delete` |
| Tracking (status v2) | POST | `/labels/statusv2` |
| Publish manifest | POST | `/v2/publishmanifestv4` |

All five calls send `Content-Type: application/json; charset=utf-8` and
the `access_key` header, and parse transport errors through
`provider_utils.parse_error_response` (the `on_error` hook).

## Authentication

Static API-key header. There is no OAuth/token flow.

```
Settings.access_key  ───►  header  access_key: <access_key>
```

- `access_key` is the only required credential (`mappers/seko/settings.py`).
- It is sent verbatim on every request; the commented-out
  `access_token` / `login()` OAuth scaffolding in `utils.py` is dead and
  unused.
- `Settings.server_url` selects staging vs prod from `test_mode`.

## Supported operations

| Operation | Mapper method | Provider |
|---|---|---|
| Rate | `create_rate_request` / `parse_rate_response` | `rate.py` |
| Shipment create | `create_shipment_request` / `parse_shipment_response` | `shipment/create.py` |
| Shipment cancel | `create_cancel_shipment_request` / `parse_cancel_shipment_response` | `shipment/cancel.py` |
| Tracking | `create_tracking_request` / `parse_tracking_response` | `tracking.py` |
| Manifest | `create_manifest_request` / `parse_manifest_response` | `manifest.py` |

No pickup or document-upload operations are implemented. The plugin
metadata declares `is_hub=False`.

## Services & options

### Services — `ShippingService` (`units.py`)

The unified service key maps to the SEKO **`DeliveryType`** wire string.

| Karrio service key | Wire `DeliveryType` |
|---|---|
| `seko_ecommerce_standard_tracked` | `eCommerce Standard Tracked` |
| `seko_ecommerce_express_tracked` | `eCommerce Express Tracked` |
| `seko_domestic_express` | `Domestic Express` |
| `seko_domestic_standard` | `Domestic Standard` |
| `seko_domestic_large_parcel` | `Domestic Large Parcel` |

On create the value (`ShippingService.map(payload.service).value_or_key`)
is sent on `Service`; on rate parse the response `DeliveryType` is mapped
back to a key via `ShippingService.map(...)`.

### Service levels (CSV catalog)

`DEFAULT_SERVICES` is built from `services.csv` (32 rows) at import.
Each CSV row contributes a `ServiceZone` (rate, weight band, transit
days, country codes) to the matching `ServiceLevel`. CSV columns:
`service_code, service_name, zone_label, country_codes, min_weight,
max_weight, max_length, max_width, max_height, rate, currency,
transit_days, domicile, international`. Weight unit is `KG`, dimension
unit `CM`; `transit_days` parses the low end of a `"5-8"` range.

### Packaging — `PackagingType` (`StrEnum`)

Unified packaging keys map onto SEKO `Type` strings:

| Unified | SEKO `Type` |
|---|---|
| `envelope` | `Envelope` |
| `pak` | `Satchel` |
| `tube` | `Tube` |
| `pallet` | `Pallet` |
| `small_box` | `Box` |
| `medium_box` | `Carton` |
| `your_packaging` | `Custom` |

Other carrier-native values (`Bag`, `Container`, `Crate`, `Pail`) exist
on the enum. Rate uses `package.packaging_type or "your_packaging"`;
create maps the raw `packaging_type`.

### Label formats — `LabelType`

Each member is a `(format, wire_output_code)` pair. `format` is the
karrio doc format (`PDF`/`ZPL`/`PNG`); the second element is the wire
`Outputs[]` code and the key under `OutputFiles` in the response.

| Member | Format | Wire output code |
|---|---|---|
| `LABEL_PDF` | PDF | `LABEL_PDF` |
| `LABEL_PNG_100X150` | PNG | `LABEL_PNG_100X150` |
| `LABEL_PNG_100X175` | PNG | `LABEL_PNG_100X175` |
| `LABEL_PDF_100X175` | PDF | `LABEL_PDF_100X175` |
| `LABEL_PDF_100X150` | PDF | `LABEL_PDF_100X150` |
| `LABEL_ZPL_100X175` | ZPL | `LABEL_ZPL_100X175` |
| `LABEL_ZPL_100X150` | ZPL | `LABEL_ZPL_100X150` |

Unified aliases default the bare format to the 100×150 variant: `PDF →
LABEL_PDF_100X150`, `ZPL → LABEL_ZPL_100X150`, `PNG →
LABEL_PNG_100X150`. When `payload.label_type` is unset, create falls
back to `LabelType.PDF`.

### Options — `ShippingOption` (`units.py`)

The first `OptionEnum` arg is the SEKO wire field name. Notable
categorised options (used by the shipping-app picker via `meta.category`):

| Option key | Wire field | Type |
|---|---|---|
| `seko_carrier` | `Carrier` | str |
| `seko_ship_type` | `ShipType` | str |
| `seko_package_id` | `PackageId` | str |
| `seko_destination_id` | `DestinationId` | str |
| `seko_product_category` | `ProductCategory` | str |
| `origin_instructions` | `OriginInstructions` | str |
| `destination_instructions` | `DestinationInstructions` | str |
| `seko_is_saturday_delivery` | `IsSaturdayDelivery` | bool |
| `seko_is_signature_required` | `IsSignatureRequired` | bool |
| `seko_send_tracking_email` | `SendTrackingEmail` | bool |
| `seko_amount_collected` | `AmountCollected` | float |
| `seko_tax_collected` | `TaxCollected` | bool |
| `seko_cod_amount` | `CODAmount` | float |
| `seko_reference_2` / `seko_reference_3` | `Reference2` / `Reference3` | str |
| `seko_invoice_data` | `InvoiceData` | str |
| `seko_origin_id` | `OriginId` | int |
| `seko_print_to_printer` | `PrintToPrinter` | bool |
| `seko_cif_value` | `CIFValue` | float |
| `seko_freight_value` | `FreightValue` | float |
| `seko_send_label` | `SendLabel` | bool |
| `seko_special_instructions` | `SpecialInstructions` | str |
| `seko_insurance_value` | `InsuranceValue` | float |
| `seko_estimated_delivery_date` | `EstimatedDeliveryDate` | str |
| `seko_dangerous_goods` and `seko_dg_*` (10 fields) | `DangerousGoods`, `DG*` | mixed |

**Unified option aliases:** `saturday_delivery → seko_is_saturday_delivery`,
`signature_required → seko_is_signature_required`,
`email_notification → seko_send_tracking_email`. `doc_files` /
`doc_references` are paperless-category passthroughs (`lib.to_dict`).

`shipping_options_initializer` filters supplied options to keys present
in `ShippingOption` (`items_filter`).

## Data mapping

### Address — karrio `Address` → SEKO `DestinationType` / `AddressType`

Shipper rides on `Origin`, recipient on `Destination`, both as a
`DestinationType` wrapping an `AddressType`. Note SEKO's split of
`Suburb` (city) vs `City` (state).

```
karrio Address                  SEKO AddressType / DestinationType
─────────────────               ──────────────────────────────────
company_name      ───►          DestinationType.Name (or contact, else
                                  "Shipper"/"Recipient" on create)
company_name      ───►          AddressType.BuildingName (rate/return only;
                                  None on create Origin/Destination)
address_line(s)   ───►          AddressType.StreetAddress  (.street)
city              ───►          AddressType.Suburb
state_code        ───►          AddressType.City  (create falls back to city)
postal_code       ───►          AddressType.PostCode
country_code      ───►          AddressType.CountryCode
contact (person)  ───►          DestinationType.ContactPerson
phone_number      ───►          DestinationType.PhoneNumber
email             ───►          DestinationType.Email
tax_id            ───►          DestinationType.RecipientTaxId
instructions      ───►          DestinationType.DeliveryInstructions
                                  (origin_instructions / destination_instructions)
```

**Create-side fallbacks** (the API requires non-empty values): missing
phone → `"000 000 0000"`, missing email → `" "` (single space), missing
name → `"Shipper"` / `"Recipient"`.

### Package — karrio `Package` → SEKO `PackageType`

```
karrio Package                  SEKO PackageType
──────────────                  ────────────────
height.CM / length.CM / width.CM ─► Height / Length / Width
weight.KG          ───►         Kg
description (≤50)  ───►         Name
packaging_type     ───►         Type   (via PackagingType map)
options.seko_package_id ──►     Id
reference_number   ───►         OverLabelBarcode + PackageCode  (create only)
```

### Commodity — karrio `Commodity` → SEKO `CommodityType`

```
karrio Commodity                SEKO CommodityType
────────────────                ──────────────────
title + description (≤200) ─►   Description ("title - description"; "item" default on create)
hs_code            ───►         HarmonizedCode (create default "0000.00.00")
sku                ───►         itemSKU (also HarmonizedCode on rate)
quantity           ───►         Units
value_amount       ───►         UnitValue
weight             ───►         UnitKg
value_currency     ───►         Currency
origin_country / country_code ─► Country
metadata.image_url ───►         ImageURL
```

Commodity source: `customs.commodities` when a customs payload is
present, otherwise `packages.items`.

### Customs identifiers — `CustomsOption` → `TaxIds[]`

For each customs option whose key is in `CustomsOption` and has a value,
a `TaxIDType{IdType: option.code, IdNumber: option.state}` is appended to
`TaxIds[]` (used on both rate and create). The wire `IdType` is the
enum's `OptionEnum` code:

| Customs option | Wire `IdType` |
|---|---|
| `XIEORINumber` | `XIEORINumber` |
| `IOSSNUMBER` | `IOSSNUMBER` |
| `GBEORINUMBER` | `GBEORINUMBER` |
| `VOECNUMBER` | `VOECNUMBER` |
| `VATNUMBER` | `VATNUMBER` |
| `VENDORID` | `VENDORID` |
| `NZIRDNUMBER` | `NZIRDNUMBER` |
| `SWISS_VAT` | `SWISS VAT` |
| `OVRNUMBER` | `OVRNUMBER` |
| `EUEORINumber` | `EUEORINumber` |
| `EUVATNumber` | `EUVATNumber` |
| `LVGRegistrationNumber` | `LVGRegistrationNumber` |

Unified customs-identifier aliases: `ioss → IOSSNUMBER`, `eori_number →
EUEORINumber`, `vat_registration_number → VATNUMBER`.

`DutiesAndTaxesByReceiver` is set to `customs.duty.paid_by ==
"recipient"` when a customs payload is present, else `None`.

### Shipment-create-specific fields

| Wire field | Source |
|---|---|
| `Service` | mapped service value |
| `Carrier` | `options.seko_carrier` |
| `ShipType` | `options.seko_ship_type` |
| `ProductCategory` | `options.seko_product_category` |
| `Outputs[]` | resolved label wire code (single entry) |
| `PrintToPrinter` | `options.seko_print_to_printer`, default `True` |
| `IncludeLineDetails` | hardcoded `True` |
| `TaxCollected` | `options.seko_tax_collected`, default `True` |
| `SendLabel` | `"Y"` when `options.seko_send_label` else `None` |
| `InvoiceData` | `options.seko_invoice_data`, else first `doc_files` entry of `doc_type=commercial_invoice` + PDF format |
| `CodValue` / `CODValue` | `options.cash_on_delivery` (both fields set) |
| `InsuranceValue` / `InsuranceCurrency` | `options.seko_insurance_value` / `options.currency` |
| `CostCentreName` / `CostCentreId` | `connection_config.cost_center` / `cost_center_id` |
| `LabelBranding` | `connection_config.label_branding` |
| `ReturnAddress` | `payload.return_address or payload.shipper` |

### Rate-specific fields

`RatingRequestType` additionally carries `CostCentreName` /
`CostCentreId` from `connection_config.cost_centre_name` /
`cost_centre_id` (note the British-spelling config keys, distinct from
the create-side `cost_center*` keys), plus `CIFValue`, `FreightValue`,
`TaxCollected`, `AmountCollected`, `CodValue`.

### Rate response — `AvailableType` → `RateDetails`

```
Available[i]                    RateDetails
────────────                    ───────────
DeliveryType  ─► ShippingService.map ─► service
Cost          ───►              total_charge (lib.to_money)
(config.currency or "USD")  ─►  currency
CarrierName   ───►              meta.last_mile_carrier
Route, QuoteId, CarrierServiceType,
IsFreightForward, IsRuralDelivery,
IsSaturdayDelivery, DeliveryType ─► meta.*
```

### Shipment response — `ShippingResponseType` → `ShipmentDetails`

```
Consignments[0].Connote       ───►   tracking_number
Consignments[0].ConsignmentId ───►   shipment_identifier
Consignments[i].OutputFiles[label_type] (b64) ─► docs.label  (bundled, label_format)
Consignments[0].Cost          ───►   selected_rate.total_charge (when present)
CarrierName                   ───►   meta.last_mile_carrier / seko_carrier
SiteId, CarrierId, CarrierType, InvoiceResponse ─► meta.seko_*
all TrackingUrls / ConsignmentIds ─► meta.tracking_urls / consignment_ids
```

Shipment parse only runs `_extract_details` when the response carries any
`Consignments[]`; otherwise it returns `None` plus parsed messages. The
selected_rate is only attached when `Consignments[0].Cost` is non-null.

### Tracking response — `TrackingResponseElementType` → `TrackingDetails`

```
ConsignmentNo  ───►             tracking_number
Events[] (reversed)             events[]:
  EventDT  ─► fdate / flocaltime / fiso_timestamp (try ISO with/without .%f)
  Description ───►                description
  OmniCode or Code ───►           code, status (TrackingStatus), reason (TrackingIncidentReason)
  Location ───►                   location
Status (fallback when no events) latest_status source
Tracking  ───►                  info.carrier_tracking_link
Delivered ───►                  info.expected_delivery
Picked    ───►                  info.shipping_date
Reference1 ───►                 meta.reference
```

`delivered` is `True` when the resolved status is `delivered`. Only
elements with at least one event become a `TrackingDetails`.

## Status mapping

Tracking statuses are SEKO **`OmniCode`** values (`OP-<n>`). Mapped by
`TrackingStatus` in `units.py`:

| Karrio status | SEKO OmniCodes (examples) |
|---|---|
| `pending` | `OP-1`, `OP-8`, `OP-9`, `OP-11`, `OP-12` |
| `on_hold` | `OP-2`, `OP-6`, `OP-26`, `OP-36`, `OP-39`, `OP-41`, `OP-44`, `OP-46`, `OP-49`, `OP-52`, `OP-53`, `OP-70`, `OP-87`, `OP-88`, `OP-91` |
| `in_transit` | `OP-3`, `OP-4`, `OP-5`, `OP-7`, `OP-10`, `OP-14`, `OP-18`, `OP-20`, `OP-22`, `OP-31..33`, `OP-47`, `OP-48`, `OP-50`, `OP-51`, `OP-54`, `OP-56`, `OP-78..84`, `OP-89` |
| `out_for_delivery` | `OP-21` |
| `ready_for_pickup` | `OP-19`, `OP-25`, `OP-42` |
| `delivered` | `OP-71..77` |
| `delivery_failed` | `OP-15`, `OP-17`, `OP-23`, `OP-24`, `OP-27..30`, `OP-37`, `OP-38`, `OP-40`, `OP-43`, `OP-45`, `OP-55`, `OP-86`, `OP-92` |
| `delivery_delayed` | `OP-13`, `OP-16`, `OP-35` |
| `cancelled` | `OP-34`, `OP-67` |
| `return_to_sender` | `OP-57..66`, `OP-68`, `OP-69`, `OP-85`, `OP-90`, `OP-94` |

Unmapped codes fall back to `in_transit`. A parallel
`TrackingIncidentReason` enum maps a subset of exception codes to
normalized reasons (e.g. `OP-17`/`OP-69` → `carrier_damaged_parcel`,
`OP-28`/`OP-64` → `consignee_refused`, `OP-23`/`OP-27`/`OP-41`/`OP-61` →
`consignee_incorrect_address`), attached per-event as `reason`.

## Connection config — `ConnectionConfig` (`utils.py`)

| Config key | Type | Used by |
|---|---|---|
| `currency` | str | rate/shipment response currency (default `"USD"`) |
| `cost_center` | str | create `CostCentreName` |
| `cost_center_id` | str | create `CostCentreId` |
| `cost_centre_name` | str | rate `CostCentreName` |
| `cost_centre_id` | str | rate `CostCentreId` |
| `label_branding` | str | create `LabelBranding` |
| `shipping_options` | list | option allowlist (catalog) |
| `shipping_services` | list | service allowlist (catalog) |

## Cancel & manifest wire shapes

- **Cancel** request body is a bare JSON array of consignment IDs
  (`options.shipment_identifiers` or `[payload.shipment_identifier]`).
  Response is a flat `{id: status}` map; a value containing `"Deleted"`
  is success, any other string value is an error.
- **Manifest** request body is the bare `payload.shipment_identifiers`
  array. Response `ManifestResponseType.OutboundManifest[]` yields
  `ManifestNumber`(s), aggregated `ManifestedConnotes`, and a bundled
  base64 PDF (`ManifestContent`) surfaced as `doc.manifest`.

## Error parsing

Two layers:

1. **Transport (`provider_utils.parse_error_response`, proxy `on_error`)** —
   reads the raw HTTP body; if non-empty it is forwarded as-is, otherwise
   it wraps the HTTP status/reason into
   `{"Errors": [{"code": <status>, "Message": <reason>}]}`.

2. **Domain (`error.parse_error_response`)** — inspects the parsed body
   (dict or list) and emits `models.Message[]` from the first matching
   shape, in priority order:

| Body key | Produced code | Notes |
|---|---|---|
| `ValidationErrors` (dict) | `ValidationError` | message from `Message` or first value; `Severity` → level |
| `ValidationErrors` (list) | `ErrorCode` or `ValidationError` | one message per entry |
| `Rejected[]` | `Rejected` | message from `Reason` |
| `Errors[]` / `Error[]` | `Error` | message from `Message`; `Severity` → level |
| `Warnings[]` | `WarningCode`/`ErrorCode`/`Warning` | level defaults to `warning` |

The first of `ValidationErrors` / `Rejected` / `Errors` short-circuits
(`break`); remaining keys (and `Warnings`) are otherwise appended.
Unrecognised keys of each error object are forwarded into `Message.details`.

## References

- **Vendor:** SEKO Logistics OmniParcel API — staging
  `https://staging.omniparcel.com`, prod `https://api.omniparcel.com`.
  No public spec dir is vendored in this connector.
- **Sample JSON (source of truth for the generated types):**
  `schemas/error_response.json`, `schemas/manifest_response.json`,
  `schemas/rating_request.json`, `schemas/rating_response.json`,
  `schemas/shipping_request.json`, `schemas/shipping_response.json`,
  `schemas/tracking_response.json`.
- **Generated types:** `karrio/schemas/seko/*.py` — generated from the
  JSON samples above via the `generate` script
  (`./bin/cli codegen generate ... --no-nice-property-names`).
  Regenerate with `./bin/run-generate-on modules/connectors/seko`; never
  hand-edit.
- **Service catalog:** `karrio/providers/seko/services.csv` (loaded into
  `DEFAULT_SERVICES`).
- **Tests:** `tests/seko/test_rate.py`, `test_shipment.py`,
  `test_tracking.py`, `test_manifest.py`.
