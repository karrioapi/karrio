# DHL Express integration — specification

Reference for the DHL Express connector. DHL Express is integrated over
the legacy **XML-PI (XML Services)** SOAP-style API: every operation —
rate quote, address validation, shipment creation, tracking, and pickup
book/modify/cancel — is a distinct XML document `POST`ed to a single
servlet (`/XMLShippingServlet`). There is no JSON surface and no OAuth;
each request carries a `ServiceHeader` with `SiteID` + `Password`.

The **vendor source of truth** is the set of XSD schemas under
`schemas/*.xsd` (DHL XML-PI). The generated Python types under
`karrio/schemas/dhl_express/*.py` are produced from those XSDs by
`generateDS` (see [References](#references)). DHL's public docs live at
<https://developer.dhl.com/api-reference/dhl-express-xml>.

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Data flow](#data-flow)
3. [Endpoints](#endpoints)
4. [Authentication](#authentication)
5. [Supported operations](#supported-operations)
6. [Services](#services)
7. [Options (Special Services)](#options-special-services)
8. [Packaging](#packaging)
9. [Labels](#labels)
10. [Data mapping](#data-mapping)
11. [Customs & paperless trade](#customs--paperless-trade)
12. [Carrier-specific invariants & gotchas](#carrier-specific-invariants--gotchas)
13. [Tracking](#tracking)
14. [Error parsing](#error-parsing)
15. [References](#references)

---

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio RateRequest / ShipmentRequest /
│   (karrio core)         │   TrackingRequest / PickupRequest /
│                         │   AddressValidationRequest / CustomsInfo
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  providers/dhl_express  │   Pure data transforms.
│   rate.py               │   Unified model → typed DHL XML request,
│   shipment.py           │   typed XML response → unified model.
│   return_shipment.py    │   No HTTP, no side effects.
│   tracking.py           │
│   address.py            │   Each builder serialises to XML via
│   pickup/create.py      │   lib.to_xml / XP.export with a hand-written
│   pickup/update.py      │   namespacedef_ and a schemaVersion fixup.
│   pickup/cancel.py      │
│   error.py              │
│   units.py              │   ShippingService, ShippingOption,
│   utils.py (Settings)   │   PackageType, LabelType, Incoterm,
│   i18n.py               │   TrackingStatus, CountryRegion, ...
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ mappers/dhl_express/    │   HTTP transport only. Every method funnels
│   proxy.py              │   through _send_request → POST to the single
│                         │   /XMLShippingServlet endpoint with
│                         │   Content-Type: application/xml.
│   settings.py           │   site_id / password / account_number / ...
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  DHL XML-PI (XML Services)                      │
│  ─────────────────────────────────────────────  │
│  Test: https://xmlpitest-ea.dhl.com            │
│  Prod: https://xmlpi-ea.dhl.com                │
│  All operations → POST /XMLShippingServlet      │
│  Routing/DCT/ShipVal/Tracking/Pickup discriminate│
│  by the XML root element, not by path.          │
└─────────────────────────┘
```

**Key architectural choices:**

- **Single servlet, many message types.** The proxy does not vary the
  URL per operation — every call is `POST /XMLShippingServlet`. The
  operation is identified by the XML root element of the serialized
  request (`p:DCTRequest`, `req:ShipmentRequest`,
  `req:KnownTrackingRequest`, `req:BookPURequest`, `ns1:RouteRequest`,
  …).
- **Static service catalog.** XML-PI does not expose a per-account
  product catalog. `units.py` carries the union of DHL global product
  codes (`ShippingService`) plus a CSV-backed `service_levels` table
  (`services.csv`) for the dashboard.
- **`schemaVersion` string fixup.** `generateDS` emits e.g.
  `schemaVersion="3"` / `"10"` / `"2."`; DHL requires `"3.0"` / `"10.0"`
  / `"2.0"`. Every serializer ends with a `.replace(...)` to repair the
  attribute. Do not remove these.
- **Generated schemas.** `karrio/schemas/dhl_express/*.py` is generated
  from `schemas/*.xsd`. Regenerate with `./generate` (or
  `./bin/run-generate-on modules/connectors/dhl_express`); never
  hand-edit.

## Data flow

### Rate (DCT GetQuote — one HTTP call)

```
RateRequest                              DHL XML-PI
   │                                          │
   ├─► rate_request                           │
   │     to_packages(), to_services()         │
   │     to_shipping_options()                │
   │     is_dutiable = intl & !doc & !(EU→EU) │
   │     build DCTRequest/GetQuoteType        │
   │                                          │
   ├─► lib.to_xml (p:DCTRequest) ─────────────│
   │   schemaVersion 3 → 3.0                   │
   │                                          │
   │   ─── POST /XMLShippingServlet ──────────►│
   │   ◄── DCTResponse{ QtdShp[] } ────────────│
   │                                          │
   ├─► parse_rate_response                     │
   │     find QtdShp; drop rows where          │
   │       ShippingCharge ≤ 0                   │
   │     skip " DOC" products unless            │
   │       ctx.is_document or skip_service_filter│
   │     transit = DlvyDate − PricingDate       │
   ▼                                          ▼
list[RateDetails]
```

### Shipment (ShipmentValidate — one HTTP call)

```
ShipmentRequest                          DHL XML-PI
   │                                          │
   ├─► shipment_request                       │
   │     guard: shipper.country must equal     │
   │       account_country_code (if set) else  │
   │       OriginNotServicedError              │
   │     to_address(), to_packages(max 300kg)  │
   │     map service → GlobalProductCode        │
   │     build dhl.ShipmentRequest (v10.0)      │
   │     SpecialService[] from options          │
   │     Dutiable/ExportDeclaration if dutiable │
   │     DocImages if paperless_trade           │
   │                                          │
   ├─► lib.to_xml (req:ShipmentRequest) ───────│
   │   schemaVersion 10 → 10.0; strip b'' on    │
   │   <Image> base64                            │
   │                                          │
   │   ─── POST /XMLShippingServlet ──────────►│
   │   ◄── ShipmentResponse{                    │
   │         AirwayBillNumber, LabelImage,      │
   │         MultiLabel[], charges } ───────────│
   │                                          │
   ├─► parse_shipment_response                  │
   │     present iff AirwayBillNumber found     │
   │     AirwayBillNumber → tracking_number     │
   │                       & shipment_identifier│
   │     LabelImage.OutputImage → docs.label    │
   │     MultiLabel CustomInvoiceImage → invoice│
   │     other MultiLabel → extra_documents     │
   ▼                                          ▼
ShipmentDetails
```

### Return shipment

`return_shipment_request` is a thin wrapper: it forces
`options.dhl_return_undeliverable = True` onto the payload and delegates
to `shipment_request`. The proxy's `create_return_shipment` calls
`create_shipment` unchanged. Same response parsing.

### Tracking (KnownTrackingRequest — one HTTP call)

```
TrackingRequest                          DHL XML-PI
   │                                          │
   ├─► tracking_request                        │
   │     AWBNumber = payload.tracking_numbers   │
   │     LanguageCode (opt, "en")               │
   │     LevelOfDetails (opt, ALL_CHECK_POINTS) │
   │                                          │
   │   ─── POST /XMLShippingServlet ──────────►│
   │   ◄── TrackingResponse{ AWBInfo[] } ───────│
   │                                          │
   ├─► parse_tracking_response                  │
   │     one TrackingDetails per AWBInfo that   │
   │       has a ShipmentInfo                    │
   │     status ← last event's ServiceEvent     │
   │       .EventCode via TrackingStatus enum    │
   ▼                                          ▼
list[TrackingDetails]
```

### Pickup (Book / Modify / Cancel — one HTTP call each)

```
PickupRequest         BookPURequest    ─► ConfirmationNumber
PickupUpdateRequest   ModifyPURequest  ─► ConfirmationNumber
PickupCancelRequest   CancelPURequest  ─► ConfirmationNumber (success flag)
```

Each builds its XML, `POST`s to `/XMLShippingServlet`, and parses the
returned `ConfirmationNumber`. The pickup serializers additionally run
`reformat_time(...)` to truncate `ReadyByTime` / `CloseTime` /
`CancelTime` from `HH:MM:SS` to `HH:MM` (see gotchas).

## Endpoints

DHL XML-PI exposes a **single servlet**; the operation is encoded in the
XML body, not the path.

Test host: `https://xmlpitest-ea.dhl.com`.
Prod host: `https://xmlpi-ea.dhl.com`.
(`Settings.server_url` switches on `test_mode`.)

| Purpose | Method | Path | XML root element |
|---|---|---|---|
| Rate quote | POST | `/XMLShippingServlet` | `p:DCTRequest` → `GetQuote` |
| Address validation | POST | `/XMLShippingServlet` | `ns1:RouteRequest` |
| Create shipment | POST | `/XMLShippingServlet` | `req:ShipmentRequest` |
| Create return shipment | POST | `/XMLShippingServlet` | `req:ShipmentRequest` (return option forced) |
| Tracking | POST | `/XMLShippingServlet` | `req:KnownTrackingRequest` |
| Book pickup | POST | `/XMLShippingServlet` | `req:BookPURequest` |
| Modify pickup | POST | `/XMLShippingServlet` | `req:ModifyPURequest` |
| Cancel pickup | POST | `/XMLShippingServlet` | `req:CancelPURequest` |

`Content-Type: application/xml` on every call.

The tracking deep-link surfaced to the customer is
`https://www.dhl.com/ca-en/home/tracking/tracking-parcel.html?submit=1&tracking-id={}`.

## Authentication

No OAuth, no token cache. Plain credentials embedded in every request's
`ServiceHeader`:

```
Request
└── ServiceHeader
     ├── MessageReference  (fixed 31-char literal "1234567890123456789012345678901")
     ├── MessageTime       (time.strftime("%Y-%m-%dT%H:%M:%S"))
     ├── SiteID            ◄── settings.site_id
     └── Password          ◄── settings.password
```

Settings fields (`mappers/dhl_express/settings.py`):

| Field | Required | Purpose |
|---|---|---|
| `site_id` | yes | XML-PI SiteID |
| `password` | yes | XML-PI password |
| `account_number` | no | DHL account; used as `ShipperID` / `ShipperAccountNumber` / billing / DCT `PaymentAccountNumber` |
| `account_country_code` | no | Origin guard + default currency (`CountryCurrency.map`, fallback `USD`) |
| `software_name` | no | DCT/ShipVal/Routing `MetaData.SoftwareName` (default `"3PV"`) |
| `metadata` | no | server-internal |
| `config` | no | projected into `ConnectionConfig` |
| `test_mode` | no | switches host between test/prod |

## Supported operations

| Operation | Wired | Request type | Notes |
|---|---|---|---|
| Rate | ✅ | `DCTRequest`/`GetQuote` | drops zero-charge & " DOC" rows |
| Address validation | ✅ | `RouteRequest` | success when any `Note.ActionNote == "Success"` |
| Shipment create | ✅ | `ShipmentRequest` v10.0 | AWB = tracking number; label + docs |
| Return shipment | ✅ | `ShipmentRequest` v10.0 | forces `dhl_return_undeliverable` |
| Tracking | ✅ | `KnownTrackingRequest` v1.0 | batched AWB list |
| Pickup book | ✅ | `BookPURequest` v3.0 | one-time pickups only |
| Pickup update | ✅ | `ModifyPURequest` v3.0 | |
| Pickup cancel | ✅ | `CancelPURequest` v3.0 | reason hardcoded `"006"` |
| Document upload | inherits base | — | `proxy.upload_document` / `mapper.create_document_upload_request` defer to `super()`; no DHL-specific implementation |
| Shipment cancel / void | ❌ | — | not implemented |

## Services

DHL global product codes are single-character. The connector maps them
via `ShippingService` (`provider/units.py`). The value is the DHL
`GlobalProductCode` / `LocalProductCode`.

| Service key | Code |
|---|---|
| `dhl_logistics_services` | `0` |
| `dhl_domestic_express_12_00` | `1` |
| `dhl_express_choice` | `2` |
| `dhl_express_choice_nondoc` | `3` |
| `dhl_jetline` | `4` |
| `dhl_sprintline` | `5` |
| `dhl_air_capacity_sales` | `6` |
| `dhl_express_easy` | `7` |
| `dhl_express_easy_nondoc` | `8` |
| `dhl_parcel_product` | `9` |
| `dhl_accounting` | `A` |
| `dhl_breakbulk_express` | `B` |
| `dhl_medical_express` | `C` |
| `dhl_express_worldwide_doc` | `D` |
| `dhl_express_9_00_nondoc` | `E` |
| `dhl_freight_worldwide_nondoc` | `F` |
| `dhl_economy_select_domestic` | `G` |
| `dhl_economy_select_nondoc` | `H` |
| `dhl_express_domestic_9_00` | `I` |
| `dhl_jumbo_box_nondoc` | `J` |
| `dhl_express_9_00` | `K` |
| `dhl_express_10_30` | `L` |
| `dhl_express_10_30_nondoc` | `M` |
| `dhl_express_domestic` | `N` |
| `dhl_express_domestic_10_30` | `O` |
| `dhl_express_worldwide_nondoc` | `P` |
| `dhl_medical_express_nondoc` | `Q` |
| `dhl_globalmail` | `R` |
| `dhl_same_day` | `S` |
| `dhl_express_12_00` | `T` |
| `dhl_express_worldwide` | `U` |
| `dhl_parcel_product_nondoc` | `V` |
| `dhl_economy_select` | `W` |
| `dhl_express_envelope` | `X` |
| `dhl_express_12_00_nondoc` | `Y` |
| `dhl_destination_charges` | `Z` |
| `dhl_express_all` | `None` |

### Service auto-selection (`shipping_services_initializer`)

When the caller supplies **no** recognised service, the initializer
applies defaults driven by the **origin region**
(`CountryRegion.map(origin_country)`):

- **Region `AM` (Americas):** picks a concrete product from
  international/document/envelope flags
  (`dhl_express_worldwide_doc`, `dhl_express_worldwide_nondoc`,
  `dhl_express_envelope_doc`, `dhl_domestic_express_doc`).
- **Any non-`AM` region:** collapses to the catch-all
  `dhl_express_all` (code `None`) and lets DHL route — the connector
  does not pre-select a product outside the Americas.

`services.csv` provides the dashboard `service_levels` table (name,
carrier code, weight/dim limits, `domicile` vs `international`,
feature tags). It is loaded once at import (`DEFAULT_SERVICES`).

## Options (Special Services)

Options map to DHL `SpecialService` codes via `ShippingOption`. The wire
code is the first positional arg of `lib.OptionEnum`; the enum carries a
`meta` dict (`category`, `configurable`, `service_level`). On a shipment
each active option becomes one
`SpecialService{SpecialServiceType=code, ChargeValue?, CurrencyCode?}`;
on a rate each becomes a `QtdShpExChrg{SpecialServiceType=code}`.

The catalog is large (full list in `units.py`). Representative codes by
category:

| Category | Examples (key → code) |
|---|---|
| DELIVERY_OPTIONS | `dhl_saturday_delivery → AA`, `dhl_saturday_pickup → AB`, `dhl_holiday_delivery → AC`, `dhl_domestic_saturday_delivery → AG` |
| SIGNATURE | `dhl_delivery_signature → SA`, `dhl_content_signature → SB`, `dhl_named_signature → SC`, `dhl_adult_signature → SD`, `dhl_no_signature_required → SX` |
| INSURANCE | `dhl_shipment_insurance → II` (float), `dhl_contract_insurance → IC` (float), `dhl_extended_liability → IB` |
| COD | `dhl_cash_on_delivery → KB` (float) |
| NOTIFICATION | `dhl_delivery_notification → JA`, `dhl_pickup_notification → JC`, `dhl_proactive_tracking → JD`, `dhl_prealert_notification → JY` |
| DANGEROUS_GOOD | `dhl_dangerous_goods → HE`, `dhl_dry_ice_un1845 → HC`, `dhl_lithium_ion_pi965_section_ii → HB`, `dhl_biological_un3373 → HY`, … |
| PAPERLESS | `dhl_paperless_trade → WY` |
| RETURN | `dhl_return_undeliverable → TG` |
| SIGNATURE/PUDO/etc. | `dhl_hold_for_collection → LX`, premium delivery windows `dhl_premium_09_00 → Y1` / `Y2` / `Y3` |

Unified-option aliases (karrio standard option → DHL option):

| karrio option | DHL option | code |
|---|---|---|
| `insurance` | `dhl_shipment_insurance` | `II` |
| `paperless_trade` | `dhl_paperless_trade` | `WY` |
| `cash_on_delivery` | `dhl_cash_on_delivery` | `KB` |
| `saturday_delivery` | `dhl_saturday_delivery` | `AA` |

`dhl_shipment_content` (`content`) is a **custom** option, not a
`SpecialService` — it is filtered out of the SpecialService list and used
only to populate `ShipmentDetails.Contents`.

### `shipping_options_initializer` behaviour

- If `origin_country` is in `UNSUPPORTED_PAPERLESS_COUNTRIES`, the
  initializer forces `dhl_paperless_trade = False` (large country list in
  `units.py` — paperless trade is not available from those origins).
- Package-level options are merged in.
- `dhl_shipment_content` is explicitly excluded from the
  `ShippingOptions` filter.

## Packaging

Two related enums plus presets:

- **`PackageType`** — ShipVal `PackageType` / `Piece.PackageType` codes
  (`dhl_express_envelope → EE`, `dhl_jumbo_box → JB`, `dhl_your_packaging
  → YP`, …). Unified types map: `envelope → EE`, `pak → DF`, `medium_box
  → JB`, `large_box → BP`, `small_box → JJ`, `your_packaging → YP`,
  `pallet/tube → FR/OD`.
- **`DCTPackageType`** — rate (DCT) `PackageTypeCode`
  (`FLY` / `COY` / `NCY` / `PAL` / `DBL` / `BOX`). Unified types map:
  `envelope/pak → FLY`, `tube → COY`, `pallet → PAL`, all boxes → `BOX`,
  `your_packaging → BOX`.
- **`PackagePresets`** — DHL branded packaging (envelope, flyers, boxes
  2–8, tube, jumbo box / junior, didgeridoo box) with default
  weight/dimensions in CM/KG (`PRESET_DEFAULTS`).

`MeasurementOptions` enforces a minimum dimension of 1 (cm or in).
`COUNTRY_PREFERED_UNITS` pins Jamaica (`JM`) to KG/CM; otherwise units
follow the packages' compatible units. Shipment weight is capped at
**300 KG** (`to_packages(max_weight=...)`).

`DimensionUnit` (`CM → C`, `IN → I`) and `WeightUnit` (`KG → K`,
`LB → L`) are the single-character wire codes DHL expects in
`ShipmentDetails.WeightUnit` / `DimensionUnit` and DCT.

## Labels

`LabelType` maps a requested label type to a `(LabelImageFormat,
LabelTemplate)` pair sent as `LabelImageFormat` + `Label.LabelTemplate`:

| Label type | Format | Template |
|---|---|---|
| `PDF_6x4` (and unified `PDF`) | `PDF` | `6X4_PDF` |
| `PDF_8x4` | `PDF` | `8X4_PDF` |
| `PDF_8x4_A4` | `PDF` | `8X4_A4_PDF` |
| `PDF_6x4_A4` | `PDF` | `6X4_A4_PDF` |
| `PDF_8x4_CI` | `PDF` | `8X4_CI_PDF` |
| `PDF_8x4_RU_A4` | `PDF` | `8X4_RU_A4_PDF` |
| `ZPL_8x4` | `ZPL2` | `8X4_thermal` |
| `ZPL_6x4` (and unified `ZPL`) | `ZPL2` | `6X4_thermal` |
| `ZPL_8x4_CI` | `ZPL2` | `8X4_CI_thermal` |

Default when `payload.label_type` is unset: `PDF_6x4`. The response
`LabelImage.OutputImage` (binary) is base64-encoded into `docs.label`.
`RequestQRCode` is hardcoded `"N"`, `SinglePieceImage` `"N"`.

## Data mapping

### Address — karrio `Address` → ShipVal `Shipper` / `Consignee`

```
karrio Address                 DHL ShipVal
─────────────────             ─────────────────────
company_name      ──► CompanyName (or "N/A" if empty)
person_name       ──► Contact.PersonName
phone_number      ──► Contact.PhoneNumber (or "0000")
email             ──► Contact.Email
address_line1     ──► AddressLine1
address_line2     ──► AddressLine2 (optional)
street_name       ──► StreetName
street_number     ──► StreetNumber
city              ──► City
state_code        ──► DivisionCode
postal_code       ──► PostalCode
country_code      ──► CountryCode
country_name      ──► CountryName
tax_id            ──► RegistrationNumbers.RegistrationNumber[
                        Number=tax_id,
                        NumberTypeCode="VAT",
                        NumberIssuerCountryCode=country_code]
```

`Shipper` additionally carries `ShipperID` / `RegisteredAccount` =
`settings.account_number` (or `"N/A"`), and `EORI_No` from
`customs.options.eori_number`.

### Billing — `Payment` → `Billing`

```
payment.paid_by   ──► ShippingPaymentType (PaymentType: sender→S, recipient→R, third_party→T)
account_number    ──► ShipperAccountNumber = settings.account_number
                      BillingAccountNumber = payment.account_number
duty.account_number ► DutyAccountNumber
```

Default payment when none supplied: `paid_by="sender"`,
`account_number=settings.account_number`.

### Pieces — `Parcel` → `ShipmentDetails.Pieces.Piece`

```
parcel              DHL Piece
──────              ───────────────────
(index, 1-based) ──► PieceID
packaging_type   ──► PackageType (shipment package_type or per-piece map)
length/width/height ► Depth / Width / Height (MeasurementOptions, min 1)
weight           ──► Weight
content/description ► PieceContents
parcel.id        ──► PieceReference.ReferenceID (max 30)
description      ──► AdditionalInformation.CustomerDescription
```

### Rate — DCT `QtdShp` → `RateDetails`

```
QtdShpType                     RateDetails
──────────                     ───────────
GlobalProductCode  ──► service (ShippingService.map → name_or_key)
ShippingCharge     ──► total_charge   (row dropped if ≤ 0)
CurrencyCode       ──► currency
WeightCharge       ──► extra_charges["Base charge"]
QtdShpExChrg[]     ──► extra_charges[LocalServiceTypeName → ChargeValue]
DeliveryDate − PricingDate ► transit_days
LocalProductName   ──► meta.service_name ("DHL {name}")
```

" DOC" products are filtered out unless the shipment is documents-only
(`ctx.is_document`) or `connection_config.skip_service_filter` is on.

### Shipment response → `ShipmentDetails`

| DHL field | Unified |
|---|---|
| `AirwayBillNumber` | `tracking_number` + `shipment_identifier` |
| `LabelImage.OutputImage` | `docs.label` (base64) |
| `MultiLabel` `DocName == "CustomInvoiceImage"` | `docs.invoice` |
| other `MultiLabel` | `docs.extra_documents[]` (category via `ShippingDocumentCategory`/`doc_category_map`) |
| `ShippingCharge` / `PackageCharge` | `selected_rate.total_charge` / extra charge + `meta.package_charge` |

Document category map: `TransportLabel → transport_label`,
`CustomInvoiceImage → commercial_invoice`, `ArchiveDocument →
archive_document`, `ShipmentReceipt → shipment_receipt`,
`WaybillDoc → waybill_document`, else `other`.

## Customs & paperless trade

International dutiable shipments
(`is_dutiable = is_international and not is_document and not (EU→EU)`)
carry three correlated blocks on the ShipVal request:

- **`Dutiable`** — `DeclaredValue` / `DeclaredCurrency`, `TermsOfTrade`
  (= `customs.incoterm`, default `"DDP"`), `ExportLicense`, `ShipperEIN`
  (EIN option or duty-billing tax id), optional `Filing`
  (`FilingType=AES_4` + `AES4EIN` when `customs.options.aes` is set).
- **`ExportDeclaration`** — invoice (`InvoiceNumber` default `"0000000"`,
  `InvoiceDate` default today), `ExportReason` / `ExportReasonCode`
  (`ExportReasonCode` enum), `ShipmentPurpose` (`COMMERCIAL` vs
  `PERSONAL` from `customs.commercial_invoice`), `PlaceOfIncoterm`
  forced `"N/A"`, and one `ExportLineItem` per commodity:

  ```
  commodity[i]            ExportLineItem
  ────────────            ──────────────
  (index, 1-based)  ──► LineNumber
  quantity          ──► Quantity (QuantityUnit="PCS")
  description/title ──► Description (max 75)
  value_amount      ──► Value
  hs_code           ──► CommodityCode / ImportCommodityCode
  weight            ──► Weight / GrossWeight (WeightUnit via WeightUnit enum)
  origin_country    ──► ManufactureCountryCode / ...Name (fallback shipper country)
  ```

- **`UseDHLInvoice="Y"`**, `DHLInvoiceLanguageCode="en"`,
  `DHLInvoiceType` = `CMI` (commercial) or `PFI` (proforma).

`Incoterm` enum lists EXW/FCA/CPT/CFR/CIP/CIF/DAT/DAP/DDP/FAS/FOB. The
`ExportReasonCode` enum maps karrio content types to single-char DHL
codes (e.g. `permanent → P`, `gift → G`, `sample → S`,
`commercial_purpose_or_sale → C`); unified `documents`/`other` → `None`.

### Paperless trade (electronic trade documents)

When `options.dhl_paperless_trade` is on:

- **`DocImages.DocImage[]`** — built from `options.doc_files` (base64
  `doc_file`, `doc_format` default `PDF`, `Type` via
  `UploadDocumentType.map(doc_type)` default `CIN`). The serializer
  strips the Python `b'...'` wrapper around the base64 `<Image>` payload
  (`.replace("<Image>b'", "<Image>")` etc.).
- **`ExportDeclaration.CustomsDocuments`** — built from
  `options.doc_references` (each `doc_id` → `CustomsDocument{
  CustomsDocumentID, CustomsDocumentType="IN"}`) when paperless and
  references are present.

`UploadDocumentType` enum: `HWB`, `INV`, `PNV`, `COO`, `NAF`, `CIN`,
`DCL`; unified-type aliases `certificate_of_origin → COO`,
`commercial_invoice → CIN`, `pro_forma_invoice → PNV`,
`packing_list → DCL`, `other → INV`.

## Carrier-specific invariants & gotchas

- **Single servlet routing.** All eight operations POST to the same
  `/XMLShippingServlet`. The XML root element is the only discriminator.
- **`schemaVersion` repair is mandatory.** generateDS serialises the
  version attribute without the trailing `.0`. Each serializer fixes it
  up: rate `3 → 3.0`, shipment `10 → 10.0`, tracking `1 → 1.0`,
  routing `2. → 2.0`, pickups `3 → 3.0`. Removing these breaks schema
  validation at DHL.
- **Base64 `<Image>` byte-prefix strip.** ShipVal `DocImage.Image` is set
  to raw decoded bytes; the XML export wraps them as `b'...'`, so the
  serializer post-processes `<Image>b'…'</Image>` → `<Image>…</Image>`.
- **Origin guard.** If `account_country_code` is set and the shipper
  country differs, `shipment_request` raises
  `errors.OriginNotServicedError` before building anything.
- **Pickup time truncation (`reformat_time`).** DHL pickup messages want
  `HH:MM`, but the request builders compose `HH:MM:SS`. `reformat_time`
  rewrites `ReadyByTime` / `CloseTime` (book + modify) and `CancelTime`
  (cancel) down to minutes. The function is a literal string splice on
  the serialized XML, not a typed transform.
- **One-time pickups only.** `pickup_request` raises a `FieldError` for
  any `pickup_type` other than `one_time` — recurring/daily pickups must
  be arranged with DHL directly.
- **Cancel reason hardcoded `"006"`** on every `CancelPURequest`.
- **`dhl_express_all` (code `None`).** Outside the Americas region the
  default service collapses to the null-coded catch-all so DHL routes the
  shipment; the connector does not force a product.
- **`MessageReference` is a fixed 31-char constant.** Every
  `ServiceHeader` carries the literal
  `"1234567890123456789012345678901"`.
- **Phone fallback `"0000"`, company fallback `"N/A"`.** Empty contact
  phone and company name are backfilled so DHL does not reject the
  envelope.
- **Rate filtering.** Quotes with `ShippingCharge ≤ 0` are dropped, as
  are " DOC" products for non-document shipments (unless
  `skip_service_filter`).
- **`is_dutiable` logic is shared** between rate and shipment:
  international AND not documents AND not intra-EU. Intra-EU cross-border
  shipments are treated as non-dutiable.
- **Legacy `XP` / `DF` / `NF` helpers** are still used in `address.py`
  and the pickup builders (the older karrio utility surface), alongside
  the newer `lib.*` helpers used elsewhere. Both produce the same XML.
- **Old-style `.build(response)` parsing.** Pickup responses are parsed
  by instantiating the generated class (`BookPUResponse()` /
  `ModifyPUResponse()`) and calling `.build(element)`, rather than
  `lib.to_object`.

## Tracking

`KnownTrackingRequest` carries the full `AWBNumber` list (batched),
`LanguageCode` (default `en`), and `LevelOfDetails` (default
`ALL_CHECK_POINTS`). The parser yields one `TrackingDetails` per
`AWBInfo` that contains a `ShipmentInfo`.

Per-shipment status is taken from the **last** `ShipmentEvent`'s
`ServiceEvent.EventCode`, matched against `TrackingStatus`:

| Unified status | DHL event codes |
|---|---|
| `delivered` | `OK` |
| `picked_up` | `PU`, `PL`, `OR` |
| `in_transit` | `DF`, `AF`, `AR`, `IT`, `TR`, `CC`, `CD` (default fallback) |
| `out_for_delivery` | `WC` |
| `on_hold` | `BA`, `HP`, `OH` |
| `delivery_failed` | `CM`, `DM`, `DP`, `DS`, `NH`, `RD`, `RT`, `SS`, `ST` |
| `delivery_delayed` | `IR`, `MD`, `TD`, `UD` |

`delivered` is also set true if any event code is `OK`. Events are
emitted oldest-first (`reversed(events)`), each with `date`, `time`
(`flocaltime`), `code`, `location` (`ServiceArea.Description`),
`description` (`ServiceEvent.Description` + `Signatory`), an ISO
`timestamp`, a per-event `status`, and a normalized `reason` via
`TrackingIncidentReason` (maps exception codes to families like
`customs_delay`, `consignee_refused`, `weather_delay`, …).

`TrackingInfo` carries `customer_name` (`Consignee`),
`carrier_tracking_link`, `shipping_date`, `package_weight`, and
`package_weight_unit` (`WeightUnit.map`).

## Error parsing

`error.parse_error_response` scans the response for `Condition` elements
(typed `dhl.ConditionType`) and emits one `Message` per condition:

```
Response                       ┌──────────────────────────────┐
   │  (any operation)          │ provider_error                 │
   ├─► find_element            │   parse_error_response         │
   │     "Condition" ────────► │     Condition.ConditionCode    │ → Message.code
   │                           │     Condition.ConditionData    │ → Message.message
   └───────────────────────────┘
```

Every parser (`rate`, `shipment`, `tracking`, `pickup*`, `address`)
calls `parse_error_response` on the same deserialized element, so
`Condition`-shaped faults surface uniformly as `Message`s alongside any
successful payload. There is no separate transport-error envelope —
faults ride in the same XML document as the response.

Address validation additionally reads `Note.ActionNote == "Success"` to
set the boolean `success` flag.

## References

- **DHL XML-PI docs** —
  <https://developer.dhl.com/api-reference/dhl-express-xml>
- **XSD source of truth** — `schemas/*.xsd`, including:
  - `ship-val-global-req-10.0.xsd` / `ship-val-global-res-10.0.xsd` — shipment
  - `DCT-req_global-3.0.xsd` / `DCT-Response_global-3.0.xsd` — rate quote
  - `TrackingRequestKnown-1.0.xsd` / `TrackingResponse.xsd` — tracking
  - `book-pickup-global-req-3.0.xsd` / `modify-pickup-global-req-3.0.xsd` /
    `cancel-pickup-global-req-3.0.xsd` (+ responses) — pickup
  - `routing-global-req-2.0.xsd` / `routing-global-res.xsd` — address validation
  - `datatypes_global_v10.xsd`, `datatypes_global_v62.xsd`,
    `pickupdatatypes_global-3.0.xsd`, `err-res.xsd`, … — shared datatypes
- **Generated Python types** — `karrio/schemas/dhl_express/*.py`, produced
  from the XSDs by `generateDS` (see `generate`). **Do not hand-edit.**
  Regenerate with `./generate` or
  `./bin/run-generate-on modules/connectors/dhl_express`.
- **Service catalog** — `karrio/providers/dhl_express/services.csv`
  (loaded into `DEFAULT_SERVICES` for the dashboard `service_levels`).
- **Localized service names** — `karrio/providers/dhl_express/i18n.py`
  (`SERVICE_NAME_TRANSLATIONS`).
```