# Bpost integration — specification

Reference for the bpost (Belgian Post / `bpack`) connector. bpost ships
over the **Shipping Manager (SHM) "deep integration" v5 REST API**, an
XML-over-HTTP surface (the request/response bodies are XML, the transport
is REST). The connector supports shipment creation, label retrieval,
shipment cancellation, return shipments, and tracking. Rating is served
locally from a static CSV catalog (no live rate API).

Plugin status is `beta` (`karrio/plugins/bpost/__init__.py`). Vendor
integration manual / XSDs:
<https://bpost.freshdesk.com/support/solutions/articles/4000037653>.

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Data flow](#data-flow)
3. [Endpoints](#endpoints)
4. [Authentication](#authentication)
5. [Supported operations](#supported-operations)
6. [XML wire shape & namespaces](#xml-wire-shape--namespaces)
7. [Services taxonomy (delivery methods)](#services-taxonomy-delivery-methods)
8. [Options](#options)
9. [Data mapping](#data-mapping)
10. [Tracking](#tracking)
11. [Error parsing](#error-parsing)
12. [Rating (local catalog)](#rating-local-catalog)
13. [References](#references)

---

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio ShipmentRequest / ShipmentCancelRequest /
│   (karrio core)         │   TrackingRequest / RateRequest
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  providers/bpost        │   Pure data transforms.
│   shipment/create.py    │   Unified model → typed bpost XML order,
│   shipment/cancel.py    │   XML response → unified model.
│   shipment/return_…py   │   No HTTP, no side effects.
│   tracking.py           │
│   error.py              │
│   units.py              │   ShippingService (+ method() router),
│   utils.py  (Settings)  │   ShippingOption, LabelType, ConnectionConfig,
│                         │   TrackingStatus, TrackingIncidentReason
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  mappers/bpost/proxy.py │   HTTP transport only.
│   - get_rates           │   - HTTP Basic auth (account_id:passphrase)
│   - create_shipment     │   - Two-step ship: POST order, then GET label
│   - cancel_shipment     │   - Tracking fan-out (run_asynchronously)
│   - get_tracking        │   - create_return_shipment → create_shipment
│   - create_return_…     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  bpost APIs             │
│  ─────────────────────  │
│  SHM deep-integration v5│   orders (create), labels (GET), orderUpdate
│   shm-rest.bpost.cloud  │   (cancel) — XML media types
│  Tracked-mail v1        │   per-item trackingInfo (XML)
│   api.parcel.bpost.cloud│
└─────────────────────────┘
```

**Key architectural choices:**

- **XML over REST.** Requests are serialised with `lib.to_xml` against
  generateDS-built schema classes; responses are parsed with
  `lib.to_element` / `lib.to_object`. There is no SOAP envelope — the
  media type is set per call (e.g. `application/vnd.bpost.shm-order-v5+XML`).
- **Two-call shipment creation.** `POST .../orders/` registers the order
  (returns an empty body on success); the proxy then issues a separate
  `GET .../orders/{reference}/labels/{format}` to fetch the label bytes
  and barcodes. The two are stitched together in the proxy before parsing.
- **No live rating.** `get_rates` / `parse_rate_response` delegate to
  karrio's `universal` rating mixin, fed by a static service/zone catalog
  loaded from `services.csv` at import time (`DEFAULT_SERVICES`).
- **Generated schemas.** `karrio/schemas/bpost/*.py` is generated from the
  `.xsd` files in `schemas/` via generateDS (see `generate`). Don't
  hand-edit; regenerate with `./bin/run-generate-on modules/connectors/bpost`.

## Data flow

### Shipment creation + label (two HTTP calls)

```
ShipmentRequest                                   bpost SHM v5
     │                                                 │
     ├─► shipment_request()                            │
     │     - reference ← parcels[0].reference_number   │
     │       (else "ref_<uuid4>")                      │
     │     - is_international ← shipper.cc != recipient.cc
     │     - method ← ShippingService.method(service, is_international)
     │     - build OrderType (national OR international box)
     │     - ctx = {reference, label_format, label_header}
     │                                                 │
     │   ── POST /{account_id}/orders/ ───────────────►│
     │      Content-type: shm-order-v5+XML             │
     │                                                 │
     │   ◄── "" (empty body == success) ───────────────│
     │                                                 │
     ├─► proxy: body empty? → fetch label              │
     │   ── GET /{account_id}/orders/{ref}/labels/{fmt}►│
     │      Accept: <label_header media type>          │
     │   ◄── <labels><label><barcode/><bytes/></label> │
     │                                                 │
     │   ctx.label = parsed <labels>; response="<success>"
     │                                                 │
     ├─► _extract_details (only when ctx.label present)│
     │     tracking_number   ← first <barcode>         │
     │     tracking_numbers  ← all <barcode> (flattened)│
     │     shipment_identifier ← reference             │
     │     docs.label ← base64-bundled <bytes>         │
     ▼                                                 ▼
ShipmentDetails                              (both calls done)
```

If the `orders/` POST returns a non-empty body, it is treated as an error
response: no label GET is performed and `_extract_details` is skipped
(`ctx.label` stays `None`), so the parser emits only `Message`s.

### Tracking (one async call per number)

```
TrackingRequest.tracking_numbers[]              Tracked-mail v1
     │                                                 │
     ├─► tracking_request() → raw list of numbers      │
     │                                                 │
     │   run_asynchronously, one GET per item:          │
     │   ── GET .../trackedmail/item/{nb}/trackingInfo ►│
     │   ◄── <itemTracking> … </itemTracking> ─────────│
     │                                                 │
     ├─► parse: per (number, element)                  │
     │     "itemTracking" in tag → TrackingDetails     │
     │     else → Message (via error.parse_error_response)
     ▼                                                 ▼
[TrackingDetails], [Message]
```

## Endpoints

`server_url` = `https://shm-rest.bpost.cloud/services/shm`
(`utils.Settings.server_url` — single base for both test and prod; the
`test_mode` flag does not switch hosts). Tracking uses a separate host.

| Purpose | Method | Path |
|---|---|---|
| Create order | POST | `{server_url}/{account_id}/orders/` |
| Fetch label | GET | `{server_url}/{account_id}/orders/{reference}/labels/{label_format}` |
| Cancel order | POST | `{server_url}/{account_id}/orders/{reference}` |
| Tracking (per item) | GET | `https://api.parcel.bpost.cloud/services/trackedmail/item/{itemCode}/trackingInfo` |

`label_format` is `A4` or `A6` (from `LabelType`). `reference` on the
cancel call is the unified `shipment_identifier` (which equals the order
`reference`).

**Content types** (set per call in `proxy.py`):

| Call | `Content-type` / `Accept` |
|---|---|
| Create order | `Content-type: application/vnd.bpost.shm-order-v5+XML` |
| Fetch label | `Content-type: application/vnd.bpost.shm-labelRequest-v5+XML`; `Accept: <LabelType media type>` |
| Cancel order | `Content-type: application/vnd.bpost.shm-orderUpdate-v3+XML` |
| Tracking | (only `Authorization` header) |

The label `Accept` header is one of (from `LabelType`):
`application/vnd.bpost.shm-label-pdf-v3+XML` (PDF) or
`application/vnd.bpost.shm-label-image-v3+XML` (PNG).

## Authentication

HTTP **Basic** auth on every call. `utils.Settings.authorization` is
`base64(account_id:passphrase)`, sent as `Authorization: Basic <token>`.
There is no OAuth / token exchange / caching.

```
Settings.authorization
   = base64encode(f"{account_id}:{passphrase}")
        │
        ▼
   Authorization: Basic <token>     ◄── on order / label / cancel / tracking
```

Connection settings (`mappers/bpost/settings.py` + `utils.Settings`):

| Field | Required | Notes |
|---|---|---|
| `account_id` | yes | bpost SHM account; also used in every URL path |
| `passphrase` | yes | the Basic-auth secret (marked sensitive) |
| `account_country_code` | default `"BE"` | |
| `test_mode` | default `False` | does **not** change the host |
| `config` | — | connection-config blob (see below) |

### ConnectionConfig

| Key | Type | Use |
|---|---|---|
| `cost_center` | string | emitted as `<costCenter>` on every order |
| `lang` | enum `FR` / `EN` | notification language + tracking-link `lang`; default `EN` |
| `shipping_options` | list | option allowlist (standard karrio config) |
| `shipping_services` | list | service allowlist (standard karrio config) |

## Supported operations

| Operation | Wired? | Notes |
|---|---|---|
| Shipment create | yes | two-call POST order + GET label |
| Label retrieval | yes | part of create; PDF or PNG, A4 default |
| Shipment cancel | yes | `orderUpdate` status=`CANCELLED` |
| Return shipment | yes | delegates to create with `bpost_parcel_return_instructions` forced on |
| Tracking | yes | async per-item; events + status + incident reason |
| Rating | local only | universal mixin over static `services.csv` catalog |
| Pickup | no | not implemented |
| Customs (electronic) | inline | `customsInfo` + `parcelContents` embedded in international boxes |

## XML wire shape & namespaces

The order body is built as `bpost.OrderType` then serialised with
`lib.to_xml`, with the root element renamed from `OrderType` to `order`
(`.replace("OrderType", "order")`). Cancel renames `OrderUpdateType` →
`orderUpdate` the same way.

Namespace prefixes (from `shipment/create.py`):

| Prefix | Namespace URI |
|---|---|
| (default) | `…/shm/deepintegration/v5/national` |
| `common` | `…/shm/deepintegration/v5/common` |
| `tns` | `…/shm/deepintegration/v5/` |
| `international` | `…/shm/deepintegration/v5/international` |

Per-element prefix routing is supplied via `prefixes=`: `OrderType`→`tns`,
sender/receiver/options/pugoAddress/parcelsDepotAddress children→`common`,
`nationalBox` children→default (national), `internationalBox`
children→`international`. The resulting shape (national example, abridged):

```xml
<tns:order …>
  <tns:accountId>…</tns:accountId>
  <tns:reference>…</tns:reference>
  <tns:costCenter>…</tns:costCenter>
  <tns:orderLine><tns:text>…</tns:text><tns:nbOfItems>…</tns:nbOfItems></tns:orderLine>
  <tns:box>
    <tns:sender>…<common:address>…</common:address></tns:sender>
    <tns:nationalBox>
      <atHome><product>…</product><options>…</options><weight>…</weight><receiver>…</receiver></atHome>
    </tns:nationalBox>
    <tns:remark>…</tns:remark>
  </tns:box>
</tns:order>
```

Cancel body uses the **v3** namespace `…/shm/deepintegration/v3/` (not v5):

```xml
<orderUpdate xmlns="…/shm/deepintegration/v3/" …>
  <common:status>CANCELLED</common:status>
</orderUpdate>
```

Each parcel produces its own `<box>` (the connector iterates `for package
in packages`). `<remark>` carries `lib.text(payload.reference, max=50)`.

## Services taxonomy (delivery methods)

`ShippingService` enum value IS the literal bpost `<product>` string (e.g.
`"bpack 24h Pro"`, `"bpack@bpost international"`). The connector resolves
the *delivery method* (which `box` sub-element to populate) from the
service + direction via `ShippingService.method(service, is_international)`.

| `ShippingService` (key) | `<product>` value | Method bucket |
|---|---|---|
| `bpack_24h_pro` | `bpack 24h Pro` | `atHome` |
| `bpack_24h_business` | `bpack 24h business` | `atHome` |
| `bpack_bus` | `bpack Bus` | `atHome` |
| `bpack_pallet` | `bpack Pallet` | `atHome` |
| `bpack_easy_retour` | `bpack Easy Retour` | `atHome` |
| `bpack_xl` | `bpack XL` | `atHome` |
| `bpack_bpost` | `bpack@bpost` | `atBpost` |
| `bpack_24_7` | `bpack 24/7` | `at24_7` |
| `bpack_world_business` | `bpack World Business` | `international` |
| `bpack_world_express_pro` | `bpack World Express Pro` | `international` |
| `bpack_europe_business` | `bpack Europe Business` | `international` |
| `bpack_world_easy_return` | `bpack World Easy Return` | `international` |
| `bpack_bpost_international` | `bpack@bpost international` | `atIntlPugo` |
| `bpack_24_7_international` | `bpack 24/7 international` | `atIntlParcelDepot` |

Method → box element mapping:

```
direction      method               box element
─────────────  ───────────────────  ───────────────────────────
domestic       atHome               nationalBox > atHome
domestic       atBpost              nationalBox > atBpost          (pugo*)
domestic       at24_7               nationalBox > at24_7           (parcelsDepot*)
domestic       bpostOnAppointment   (defined, no services mapped → unused)
international   international        internationalBox > international
international   atIntlHome           internationalBox > atIntlHome
international   atIntlPugo           internationalBox > atIntlPugo  (pugo*)
international   atIntlParcelDepot    internationalBox > atIntlParcelDepot (parcelsDepot*)
```

**Fallback routing** (`method()`): an unrecognised service falls back to
`atIntlHome` when international, else `atHome`. `bpostOnAppointment` and
`atIntlHome` have no services explicitly mapped — they are reachable only
via the fallback / direct method selection.

`is_international` is `shipper.country_code != recipient.country_code`.
The national vs international `<box>` is chosen by `is_international`, and
within it exactly one sub-element matching `method` is populated (all
others are `None`).

`PackagingType` collapses every unified packaging to the single bpost
value `PACKAGE`.

## Options

`ShippingOption` — the first `OptionEnum` arg is the bpost option element
name. Booleans render as empty self-closing flag elements (e.g.
`<common:signed/>`); value/notification options render structured
children. `meta.category` groups options for the UI.

| Option key | Wire name | Type | Category |
|---|---|---|---|
| `bpost_info_distributed` | `infoDistributed` | notification | NOTIFICATION |
| `bpost_info_next_day` | `infoNextDay` | notification | NOTIFICATION |
| `bpost_info_reminder` | `infoReminder` | notification | NOTIFICATION |
| `bpost_keep_me_informed` | `keepMeInformed` | notification | NOTIFICATION |
| `bpost_automatic_second_presentation` | `automaticSecondPresentation` | bool | DELIVERY_OPTIONS |
| `bpost_fragile` | `fragile` | bool | — |
| `bpost_insured` | `insured` | value (basicInsurance level) | INSURANCE |
| `bpost_signed` | `signed` | bool | SIGNATURE |
| `bpost_time_slot_delivery` | `timeSlotDelivery` | bool | DELIVERY_OPTIONS |
| `bpost_saturday_delivery` | `saturdayDelivery` | bool | DELIVERY_OPTIONS |
| `bpost_sunday_delivery` | `sundayDelivery` | bool | DELIVERY_OPTIONS |
| `bpost_same_day_delivery` | `sameDayDelivery` | bool (→ notification) | DELIVERY_OPTIONS |
| `bpost_cod` | `cod` | money | COD |
| `bpost_preferred_delivery_window` | `preferredDeliveryWindow` | string | DELIVERY_OPTIONS |
| `bpost_full_service` | `fullService` | bool | — |
| `bpost_door_step_plus_service` | `doorStepPlusService` | string | DELIVERY_OPTIONS |
| `bpost_ultra_late_in_evening_delivery` | `ultraLateInEveningDelivery` | bool | DELIVERY_OPTIONS |

**Custom (PUDO / return) options** — used to populate the pickup-point /
parcel-depot sub-elements, not the `<options>` block:

| Option key | Wire name | Category |
|---|---|---|
| `bpost_pugo_id` | `pugoId` | PUDO |
| `bpost_pugo_name` | `pugoName` | PUDO |
| `bpost_pugo_address` | `pugoAddress` | PUDO |
| `bpost_parcels_depot_id` | `parcelsDepotId` | PUDO |
| `bpost_parcels_depot_name` | `parcelsDepotName` | PUDO |
| `bpost_parcels_depot_address` | `parcelsDepotAddress` | PUDO |
| `bpost_parcel_return_instructions` | `parcelReturnInstructions` | RETURN |

**Unified → bpost option aliases:** `insurance`→`bpost_insured`,
`cash_on_delivery`→`bpost_cod`, `signature_confirmation`→`bpost_signed`,
`saturday_delivery`→`bpost_saturday_delivery`.

### Option-initializer behaviour (`shipping_options_initializer`)

- If `bpost_pugo_address` or `bpost_parcels_depot_address` is supplied and
  no `hold_at_location_address` is set, the initializer turns on
  `hold_at_location` and copies that address into
  `hold_at_location_address`. `shipment_request` then derives a
  `hold_location` address used to fill the `pugoAddress` /
  `parcelsDepotAddress` blocks (falling back to the recipient).
- The `items_filter` excludes the PUDO (`pugo*` / `parcels*`) and
  `bpost_parcel_return_instructions` keys from the iterated
  `options.items()` set, so they are not treated as `<options>` flags.

### Notification options — gating

Notification-style options (`infoDistributed`, `infoNextDay`,
`infoReminder`, `keepMeInformed`, `sameDayDelivery`, `timeSlotDelivery`)
are only emitted when the option is set **and** at least one contact value
is available (`email_notification_to` / recipient email /
`sms_notification_to` / recipient phone). They carry
`language=<lang>` plus an `emailAddress` / `phoneNumber`. `keepMeInformed`
also triggers on the standard `email_notification` option. For
`infoNextDay` / `keepMeInformed`, the option's own value (when a string)
is preferred as the email address. The entire `<options>` block is omitted
when no options are present (`if any(options.items())`).

## Data mapping

### Address — karrio `Address` → bpost `AddressType` / `Party`

```
karrio Address                  bpost Party / AddressType
─────────────────               ──────────────────────────
contact (person_name)  ───►     Party.name
company_name           ───►     Party.company
email                  ───►     Party.emailAddress
phone_number           ───►     Party.phoneNumber
street_name            ───►     AddressType.streetName
address_line2          ───►     AddressType.addressLineTwo
street_number          ───►     AddressType.number
postal_code            ───►     AddressType.postalCode
city                   ───►     AddressType.locality
country_code           ───►     AddressType.countryCode
                                AddressType.box = None (always)
```

Sender is built from `payload.shipper`; `receiver` from `payload.recipient`.

### Parcel — units

| karrio | bpost field | unit |
|---|---|---|
| `weight` | `weight` (national) / `parcelWeight` (intl) | grams (`.G`) |
| `height` | `height` / `parcelHeight` | millimetres (`.MM`) |
| `length` | `length` / `parcelLength` | millimetres (`.MM`) |
| `width` | `width` / `parcelWidth` | millimetres (`.MM`) |

### Order lines

`<orderLine>` is built from the customs commodities if present, else the
parcel items: `text` ← `description or title`, `nbOfItems` ← `quantity`.
Omitted entirely when there are no lines.

### Customs (international boxes only) — `CustomsType` + `parcelContents`

Every international method (`international`, `atIntlHome`, `atIntlPugo`,
`atIntlParcelDepot`) embeds:

```
karrio                                bpost CustomsType
─────────────────────────────        ─────────────────
customs.duty.declared_value          parcelValue
  (else options.declared_value)
customs.content_description          contentDescription
customs.content_type                 shipmentType (via CustomsContentType)
options.bpost_parcel_return_…        parcelReturnInstructions (default "RTS")
customs.duty_billing_address.residential  privateAddress
customs.duty.currency                currency
  (else options.currency)
                                     amtPostagePaidByAddresse = None
```

`parcelContents` → `parcelContent[]`, one per parcel item (or customs
commodity when the parcel has none):

```
item.quantity                   numberOfItemType
item.value_amount               valueOfItem
item.title or item.description  itemDescription
item.weight                     nettoWeight
item.hs_code or item.sku        hsTariffCode
item.origin_country             originOfGoods
```

`CustomsContentType` (karrio `content_type` → bpost `shipmentType`):

| karrio | bpost |
|---|---|
| `documents` | `DOCUMENTS` |
| `gift` | `GIFT` |
| `sample` | `SAMPLE` |
| `returned` / `return_merchandise` | `RETURNED` |
| `goods` / `merchandise` | `GOODS` |
| `other` | `OTHER` |

### COD / insurance specifics

- `cod` → `CodType{codAmount, iban=None, bic=None}` — only IBAN/BIC are
  left null; the amount comes from `bpost_cod`.
- `insured` → `InsuranceType{basicInsurance=<level>, additionalInsurance=None}`,
  emitted whenever `bpost_insured.state is not None`.

### Label format (`LabelType`)

| Unified `label_type` | bpost (format, media-type) |
|---|---|
| `PDF` (and `ZPL`) | `A4`, `…shm-label-pdf-v3+XML` |
| `PNG` | `A4`, `…shm-label-image-v3+XML` |
| `PDF_A4` / `PDF_A6` | `A4` / `A6`, pdf media type |
| `PNG_A4` / `PNG_A6` | `A4` / `A6`, image media type |

`ZPL` is mapped to PDF/A4 (no native ZPL). Default when unmapped: PDF/A4.

### Shipment response — `_extract_details`

```
<labels><label>                       ShipmentDetails
───────────────                       ───────────────
label[0].mimeType  ──► "pdf" present? label_type = PDF, else PNG
label[].bytes      ──► base64-bundled  docs.label
label[].barcode[]  ──► flattened       meta.tracking_numbers
  first barcode    ──►                  tracking_number
ctx.reference      ──►                  shipment_identifier,
                                        meta.shipment_identifiers
settings.tracking_url.format(tn) ──►    meta.carrier_tracking_url
```

`tracking_url` =
`https://track.bpost.cloud/btr/web/#/search?itemCode={}&lang=<lang>`.

## Tracking

`get_tracking` fans out one GET per tracking number via
`lib.run_asynchronously`, returning `(number, element)` tuples. Each
`<itemTracking>` element is parsed into one `TrackingDetails`; anything
else (e.g. a `<systemException>`) becomes a `Message`.

Mapping (`tracking.py` `_extract_details`):

```
itemTracking                       TrackingDetails
────────────                       ───────────────
itemCode                  ──►      tracking_number
deliveryTime              ──►      estimated_delivery / info.expected_delivery
stateInfo[]               ──►      events[]: date, time, timestamp, code
                                    (stateCode), description (stateDescription),
                                    status, reason
stateInfo[0].stateCode    ──►      status (first match in TrackingStatus,
                                    else in_transit)
addressee.name            ──►      info.customer_name
itemDetail.weightInGrams  ──►      info.package_weight (÷1000, KG)
sender.address.*          ──►      info.shipment_origin_country / postal_code
addressee.address.*       ──►      info.shipment_destination_country / postal_code
costCenter, trackingId,
  customerReference        ──►     meta
pickupPoint.*              ──►     meta.pickup_point (joined text)
```

`delivered` is `status == "delivered"`. Event timestamps are parsed with
format `%Y-%m-%dT%H:%M:%S%z`.

### Status mapping (`TrackingStatus`) — bpost state code → karrio status

| karrio status | bpost state codes |
|---|---|
| `on_hold` | B00, B01, B02, C00, I03, I10, I11, I12, I18, I19, I58, I61, I66, I67, I68, I72, I88, L00 |
| `delivered` | U00–U08 |
| `in_transit` | B04, N14, R00–R05, T00 |
| `delivery_failed` | B03, B04, B05–B13, B18, B23, B24, B28, R11, R12, T03, S00 |
| `delivery_delayed` | N01–N08, N10–N13, N16, N28, N32, N91–N96, P00 |
| `ready_for_pickup` | N74, R13 |

The first matching `TrackingStatus` member (iteration order: on_hold,
delivered, in_transit, delivery_failed, delivery_delayed,
ready_for_pickup) wins; `B04` appears in both `in_transit` and
`delivery_failed` but resolves to `in_transit` by order. Default status
is `in_transit`.

### Incident reasons (`TrackingIncidentReason`) — per event

| reason | bpost codes |
|---|---|
| `carrier_damaged_parcel` | B05, B08 |
| `consignee_refused` | B03, B23 |
| `consignee_not_home` | B04, N01, N02 |
| `consignee_business_closed` | N03 |
| `consignee_incorrect_address` | B06, B07, B09, B10 |
| `customs_delay` | B00, B01, B02 |
| `delivery_exception_hold` | B11, B12, B13, B18, B24, B28 |

## Error parsing

bpost returns errors as one of two XML exception documents. `error.py`
handles both the nested (search) and top-level (root tag) forms:

1. **`<systemException>`** (namespace `…/api/shm/common/v2/`) — parsed into
   `system.systemException`. Used for unexpected/server errors; often
   carries only a `<message>` (then `code` defaults to `"500"`).
2. **`<businessException>`** (namespace `…/api/shm/v1/`) — parsed into
   `business.businessException`; carries `<code>` + `<message>` (e.g.
   `409` "The order is in CANCELLED state and cannot be modified anymore.").

```
Response element
   │
   ├─ lib.find_element("systemException", …)   ┐
   ├─ lib.find_element("businessException", …) │  collect nested matches
   │                                            │
   ├─ root tag contains "systemException"?  ───┤  + root-level match
   ├─ root tag contains "businessException"?────┘
   │
   ▼
[Message{code=<code|"500">, message=<message stripped>, details=**kwargs}]
```

For shipment create/cancel the messages drive success: cancel reports
`success = len(messages) == 0`; create only yields `ShipmentDetails` when
the label was fetched (`ctx.label is not None`). For tracking, the queried
`tracking_number` is passed through as `details`.

An empty body is success: the proxy substitutes `<success>true</success>`
for empty create / cancel responses so the parser sees a non-error element.

## Rating (local catalog)

There is no bpost rate API. `Mapper.create_rate_request` /
`parse_rate_response` delegate to `karrio.universal` rating, evaluated
against `DEFAULT_SERVICES` — a `ServiceLevel` list built at import time
from `services.csv` (`load_services_from_csv`).

CSV columns: `service_code, service_name, zone_label, country_codes,
min_weight, max_weight, max_length, max_width, max_height, rate, currency,
transit_days, domicile, international`. Rows are grouped by service
(mapped to the karrio service key via `ShippingService.map(...).name_or_key`);
multiple rows per service become `ServiceZone`s (e.g. Europe vs World
country sets). All rates in the checked-in CSV are `0.0` (placeholder
catalog defining weight/dimension limits and lanes, not real prices).
Weight unit `KG`, dimension unit `CM`. If the CSV is missing, a single
fallback "Bpost Standard Service" is returned.

## References

- **Vendor integration manual / examples / XSDs** —
  <https://bpost.freshdesk.com/support/solutions/articles/4000037653-where-can-i-find-the-bpack-integration-manual-examples-and-xsd-s->
- **bpost group** — <https://bpostgroup.com/>
- **Schema source of truth** — `schemas/*.xsd`:
  `announcement_common_v1`, `business_exception`, `common_v5`,
  `international_v5`, `national_v5`, `shm_deep_integration_v5`,
  `system_exception`, `tracking_info_v1`.
- **Generated types** — `karrio/schemas/bpost/*.py`, produced by
  generateDS (`generate` script, `--no-namespace-defs`). Do not
  hand-edit; regenerate with
  `./bin/run-generate-on modules/connectors/bpost`.
- **Service display names** — `karrio/providers/bpost/i18n.py`
  (`SERVICE_NAME_TRANSLATIONS`, `OPTION_NAME_TRANSLATIONS`).
- **Static rate catalog** — `karrio/providers/bpost/services.csv`.
