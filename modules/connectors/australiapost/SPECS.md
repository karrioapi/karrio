# Australia Post integration — specification

Reference for the Australia Post connector. It talks to the Australia
Post **Shipping & Tracking REST API** (`digitalapi.auspost.com.au`,
JSON over HTTPS, HTTP Basic auth + an `Account-Number` header). The
connector supports rating, shipment creation (label download),
shipment cancellation, return shipments, tracking, and order/manifest
creation.

The **vendor source of truth** is the Australia Post developer portal:
<https://developers.auspost.com.au/apis/shipping-and-tracking/reference>.
Plugin status is `beta` (`karrio/plugins/australiapost/__init__.py`).

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Data flow](#data-flow)
3. [Endpoints](#endpoints)
4. [Authentication](#authentication)
5. [Supported operations](#supported-operations)
6. [Services & options](#services--options)
7. [Data mapping](#data-mapping)
8. [Identifiers](#identifiers)
9. [Connector-specific invariants](#connector-specific-invariants)
10. [Error parsing](#error-parsing)
11. [References](#references)

---

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio RateRequest / ShipmentRequest /
│   (karrio core)         │   ShipmentCancelRequest / TrackingRequest /
└───────────┬─────────────┘   ManifestRequest
            │
            ▼
┌─────────────────────────┐
│  providers/australiapost│   Pure data transforms.
│   rate.py               │   Unified model → typed AusPost request,
│   shipment/create.py    │   typed AusPost response → unified model.
│   shipment/cancel.py    │   No HTTP, no side effects.
│   shipment/return_…py   │
│   tracking.py           │
│   manifest.py           │
│   error.py              │
│   units.py              │   ShippingService, ShippingOption,
│   utils.py (Settings)   │   PackagingType, LabelType, TrackingStatus,
│                         │   CustomsContentType, ServiceLabelGroup
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ mappers/australiapost/  │   HTTP transport only.
│   proxy.py              │   - Basic auth + Account-Number header
│                         │   - shipment = 3-call chain
│                         │   - manifest = 2-call chain
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Australia Post API     │   digitalapi.auspost.com.au
│  /shipping/v1/prices    │   rate
│  /shipping/v1/shipments │   create / cancel shipment
│  /shipping/v1/labels    │   request labels
│  /shipping/v1/track     │   tracking
│  /shipping/v1/orders     │   order / manifest
└─────────────────────────┘
```

**Key architectural choices:**

- **Multi-call shipment creation.** Creating a shipment is a chain of
  up to three HTTP calls in `proxy.create_shipment`: (1) `POST
  /shipments` to create the shipment, (2) `POST /labels` to request
  the label PDF/ZPL, (3) `GET <label url>` to download the rendered
  label as base64. Calls 2 and 3 are conditional — see
  [Data flow](#data-flow).
- **Manifest = order summary.** `create_manifest` posts an order to
  `POST /orders`, then `GET …/orders/{order_id}/summary` to fetch the
  base64 manifest document.
- **No OAuth.** Authentication is HTTP Basic (`api_key:password`,
  base64-encoded) plus an `Account-Number` header on every call.
- **Static service catalog from CSV.** `DEFAULT_SERVICES` is built at
  import time from `providers/australiapost/services.csv` via
  `load_services_from_csv()` — there is no live catalog fetch.
- **Generated schemas** — `karrio/schemas/australiapost/*.py` is
  generated from `schemas/*.json` (kcli infers types). Don't
  hand-edit; regenerate with
  `./bin/run-generate-on modules/connectors/australiapost`.

## Data flow

### Shipment create (up to 3 HTTP calls)

```
ShipmentRequest                                Australia Post API
     │                                                │
     ├─► shipment_request()                           │
     │     - build ShipmentRequestType (shipment)     │
     │     - build LabelRequestType (label) with      │
     │       shipment_id placeholder "[SHIPMENT_ID]"  │
     │                                                │
     │   ─── POST /shipping/v1/shipments ────────────►│
     │   ◄── { shipments: [{ shipment_id, items }] } ─│
     │                                                │
     ├─► proxy reads shipments[0].shipment_id         │
     │     (if None → stop, return [resp, {}, None])  │
     │     substitutes it into the label JSON         │
     │     body, replacing "[SHIPMENT_ID]"            │
     │                                                │
     │   ─── POST /shipping/v1/labels ───────────────►│
     │   ◄── { labels: [{ url, request_id }] } ───────│
     │                                                │
     ├─► proxy reads labels[0].url                    │
     │     (if None → stop, return [resp, labelresp]) │
     │                                                │
     │   ─── GET <label url> ────────────────────────►│
     │   ◄── binary label (base64-encoded by proxy) ──│
     │                                                │
     ▼                                                ▼
ShipmentDetails                              (label bytes in docs.label)
```

`parse_shipment_response` only emits a `ShipmentDetails` when the
third element (the downloaded label) is not `None`; otherwise it
returns `None` plus whatever error messages the shipment/label
responses carried.

### Manifest / order (2 HTTP calls)

```
ManifestRequest                                Australia Post API
     │                                                │
     ├─► manifest_request()                           │
     │     - ManifestRequestType                      │
     │       payment_method = "CHARGE_TO_ACCOUNT"     │
     │       shipments[] from shipment_identifiers    │
     │                                                │
     │   ─── POST /shipping/v1/orders ───────────────►│
     │   ◄── { order: { order_id, … } } ──────────────│
     │                                                │
     ├─► proxy reads order.order_id                   │
     │     (if None → no summary call)                │
     │                                                │
     │   ─── GET …/orders/{order_id}/summary ────────►│
     │   ◄── manifest document (base64) ──────────────│
     │                                                │
     ▼                                                ▼
ManifestDetails                            (doc.manifest = base64 summary)
```

### Rate (single HTTP call)

```
RateRequest ─► rate_request() ─► POST /shipping/v1/prices/items
            ◄─ { items: [{ prices: [...] }] } ◄─ parse_rate_response
```

## Endpoints

Test mode base URL: `https://digitalapi.auspost.com.au/test`.
Prod base URL: `https://digitalapi.auspost.com.au`.
(`Settings.server_url` switches on `test_mode`.)

| Purpose | Method | Path |
|---|---|---|
| Rate (price items) | POST | `/shipping/v1/prices/items` |
| Create shipment | POST | `/shipping/v1/shipments` |
| Request labels | POST | `/shipping/v1/labels` |
| Download label | GET | `<labels[].url>` (absolute URL returned by `/labels`) |
| Cancel shipment | DELETE | `/shipping/v1/shipments/{shipment_id}` |
| Tracking | GET | `/shipping/v1/track?tracking_ids={ids,comma-joined}` |
| Create order (manifest) | POST | `/shipping/v1/orders` |
| Order summary (manifest doc) | GET | `/shipping/v1/accounts/{account_number}/orders/{order_id}/summary` |

Tracking link surfaced to the customer:
`https://auspost.com.au/mypost/beta/track/details/{tracking_id}`
(`Settings.tracking_url`).

## Authentication

HTTP Basic auth. The connection settings carry three credentials
(`mappers/australiapost/settings.py`):

| Setting | Purpose |
|---|---|
| `api_key` | Basic-auth username |
| `password` | Basic-auth password |
| `account_number` | Sent as the `Account-Number` header on every call |

`Settings.authorization` computes
`base64(f"{api_key}:{password}")`. Every request sends:

```
Accept: application/json
Content-Type: application/json
Account-Number: <account_number>
Authorization: Basic <base64(api_key:password)>
```

The label-download `GET` (call 3 of shipment create) is the one
exception — it hits the absolute `url` returned by `/labels` with
**no headers**, and the proxy base64-encodes the binary body via
`decoder=lib.encode_base64`.

Other defaults on the connection: `carrier_id="australiapost"`,
`account_country_code="AU"`, `test_mode=False`.

## Supported operations

| Operation | Wired? | Provider entry point |
|---|---|---|
| Rating | yes | `rate.rate_request` / `parse_rate_response` |
| Shipment create | yes | `shipment/create.py` |
| Shipment cancel | yes | `shipment/cancel.py` (HTTP `DELETE`) |
| Return shipment | yes | `shipment/return_shipment.py` (delegates to create) |
| Tracking | yes | `tracking.py` |
| Manifest (order) | yes | `manifest.py` |
| Pickup | no | — (not implemented) |

`create_return_shipment` in the proxy is an alias that calls
`create_shipment`. The provider-side `return_shipment_request` simply
re-runs `shipment_request` on a copy of the payload — there is no
distinct return-label wire shape; the wrapper exists so the return
flow has its own entry point.

## Services & options

### Shipping services — `ShippingService` (`units.py`)

The wire value is the Australia Post **product id**. The commented-out
human-readable names are kept in `units.py` for reference but are not
the wire value.

| karrio service | Wire `product_id` |
|---|---|
| `australiapost_parcel_post` | `T28` |
| `australiapost_express_post` | `E34` |
| `australiapost_parcel_post_signature` | `3D55` |
| `australiapost_express_post_signature` | `3J55` |
| `australiapost_intl_standard_pack_track` | `PTI8` |
| `australiapost_intl_standard_with_signature` | `PTI7` |
| `australiapost_intl_express_merch` | `ECM8` |
| `australiapost_intl_express_docs` | `ECD8` |
| `australiapost_eparcel_post_returns` | `PR` |
| `australiapost_express_eparcel_post_returns` | `XPR` |

`DEFAULT_SERVICES` (the `service_levels` exposed in plugin metadata)
is loaded from `services.csv`. Each CSV row contributes a
`ServiceZone` (rate, weight band, transit days, country codes) onto
the matching `ServiceLevel`; rows are keyed by `service_code` and
grouped per karrio service name. Weight unit `KG`, dimension unit
`CM`, currency `AUD`.

### Service label groups — `ServiceLabelGroup`

The label-request `groups[].group` value (the label template family)
is derived from the service name via `ServiceLabelGroup.map(...)`,
defaulting to `australiapost_parcel_post` ("Parcel Post") when no
match. Wire values: `Parcel Post`, `Express Post`, `Startrack
Courier`, `StarTrack`, `On Demand`, `International`, `Commercial`.

### Options — `ShippingOption` (`units.py`)

| karrio option | Wire code | Type / meta |
|---|---|---|
| `australiapost_delivery_date` | `DELIVERY_DATE` | feature, category `DELIVERY_OPTIONS` |
| `australiapost_delivery_time_start` | `DELIVERY_TIMES` | feature, category `DELIVERY_OPTIONS` |
| `australiapost_delivery_time_end` | `DELIVERY_TIMES` | feature, category `DELIVERY_OPTIONS` |
| `australiapost_pickup_date` | `PICKUP_DATE` | feature |
| `australiapost_pickup_time` | `PICKUP_TIME` | feature |
| `australiapost_identity_on_delivery` | `IDENTITY_ON_DELIVERY` | feature, category `SIGNATURE` |
| `australiapost_print_at_depot` | `PRINT_AT_DEPOT` | feature, bool |
| `australiapost_transit_cover` | `TRANSIT_COVER` | float, category `INSURANCE` |
| `australiapost_sameday_identity_on_delivery` | `SAMEDAY_IDENTITY_ON_DELIVERY` | feature, category `SIGNATURE` |
| `australiapost_authority_to_leave` | `authority_to_leave` | item flag, bool |
| `australiapost_allow_partial_delivery` | `allow_partial_delivery` | item flag, bool |
| `australiapost_contains_dangerous_goods` | `contains_dangerous_goods` | item flag, bool |
| `insurance` (unified) | → `australiapost_transit_cover` | float |

`shipping_options_initializer` filters out the three item-level flags
(`authority_to_leave`, `allow_partial_delivery`,
`contains_dangerous_goods`) from the generic shipping-option set —
they are read directly off the package options when building each
`ItemType`, not emitted as shipment `features`.

The first eight feature options map onto the shipment item's
`features` block (`FeaturesType`); the `features` block is only
emitted when at least one of those options (or a `customs` payload)
is present. A `customs` payload additionally emits
`COMMERCIAL_CLEARANCE` in `features`.

### Packaging — `PackagingType`

| karrio | Wire | | karrio | Wire |
|---|---|---|---|---|
| `box` | `BOX` | | `envelope` | `ENV` |
| `carton` | `CTN` | | `item` | `ITM` |
| `pallet` | `PAL` | | `jiffy_bag` | `JIF` |
| `satchel` | `SAT` | | `skid` | `SKI` |
| `bag` | `BAG` | | | |

Unified aliases: `pak`→`SAT`, `tube`→`ITM`, `small_box`/`medium_box`/
`your_packaging`→`BOX`.

### Label formats — `LabelType`

`LabelType.map(label_type or "PDF").value` yields a `(format, layout)`
tuple. `format` ∈ `{PDF, ZPL}` feeds the label preference; `layout`
(e.g. `A4-1pp`, `A6-1pp`, `A4-3pp`) feeds `groups[].layout`. Unified
`PDF` / `ZPL` / `PNG` all collapse to `PDF_A4_1pp` (`("PDF",
"A4-1pp")`).

## Data mapping

### Rate request — `RateRequest` → `RateRequestType`

```
karrio                         AusPost rate_request
──────                         ────────────────────
shipper.postal_code   ───►     from.postcode      (key "from" on wire)
shipper.country_code  ───►     from.country
recipient.postal_code ───►     to.postcode
recipient.country_code ───►    to.country
parcels[i]            ───►     items[i] {
  parcel.id / index            item_reference
  length.CM/width.CM/height.CM length / width / height
  weight.KG                    weight
  packaging_type               packaging_type (PackagingType.map)
  services[]                   product_ids[]  (ShippingService values)
  australiapost_transit_cover  features.TRANSIT_COVER.attributes.cover_amount
}
```

The serializer builds the typed request under the field
`rate_request_from`, then string-replaces `rate_request_from` → `from`
in the JSON (Python keyword collision workaround).

### Rate response — `items[].prices[]` → `RateDetails`

```
PriceElementType.product_id        ───►  service (ShippingService.map)
  calculated_price                 ───►  total_charge
  calculated_price_ex_gst          ───►  extra_charges["base charge"]
  calculated_gst                   ───►  extra_charges["GST"]
  features{}.attributes.price.calculated_price ─► extra_charges[<feature.type>]
  product_type                     ───►  meta.service_name
```

Currency is hardcoded `AUD`. `parse_rate_response` aggregates
per-item prices with `lib.to_multi_piece_rates` (item index 1..N as
the piece key).

### Shipment request — `ShipmentRequest` → `ShipmentRequestType`

Address mapping (both `from` and `to`, via `FromType`):

```
karrio Address          AusPost FromType
──────────────          ────────────────
contact            ───► name
address_lines      ───► lines[]
city               ───► suburb
state_code         ───► state
postal_code        ───► postcode
country_code       ───► country
email              ───► email
phone_number       ───► phone
```

The shipper is built into the typed field `shipment_from`, then the
serializer string-replaces `shipment_from` → `from` in the JSON
(again a `from` keyword workaround). `movement_type` is hardcoded
`"DESPATCH"`. `email_tracking_enabled` ← `options.email_notification`.

Per-package → `items[i]`:

```
package.id / index                    ───► item_reference
service.value_or_key                  ───► product_id
length.CM / width.CM / height.CM      ───► length / width / height
weight.KG                             ───► weight
transportable_by_air (option)         ───► transportable_by_air
australiapost_authority_to_leave      ───► authority_to_leave
australiapost_allow_partial_delivery  ───► allow_partial_delivery
australiapost_contains_dangerous_goods ──► contains_dangerous_goods
parcel.description                    ───► item_description
<feature options>                     ───► features { … }
```

Feature sub-objects (only emitted when their option is set):

| Feature key | Source option(s) | Attribute fields |
|---|---|---|
| `DELIVERY_DATE` | `australiapost_delivery_date` | `date` |
| `DELIVERY_TIMES` | `australiapost_delivery_time_start` / `_end` | `windows.start`, `windows.end` |
| `PICKUP_DATE` | `australiapost_pickup_date` | `attributes.date` |
| `PICKUP_TIME` | `australiapost_pickup_time` | `attributes.time` |
| `IDENTITY_ON_DELIVERY` | `australiapost_identity_on_delivery` | `attributes.id_capture_type` |
| `PRINT_AT_DEPOT` | `australiapost_print_at_depot` | `attributes.enabled` |
| `SAMEDAY_IDENTITY_ON_DELIVERY` | `australiapost_sameday_identity_on_delivery` | `attributes.id_option` |
| `COMMERCIAL_CLEARANCE` | presence of `payload.customs` | — (bare object) |

### Customs (international only)

`is_intl` is `True` when shipper and recipient country codes differ.
When `payload.customs` is present, each item also carries:

```
karrio CustomsInfo                  AusPost item field
──────────────────                 ──────────────────
content_type → CustomsContentType  classification_type (default "OTHER")
commercial_invoice                 commercial_value
content_description                description_of_other
options.export_declaration_number  export_declaration_number
options.import_reference_number    import_reference_number
commodities[i] (or package.items)  item_contents[i] {
  country                            country_of_origin
  description                        description
  sku                                sku
  quantity                           quantity
  hs_code                            tariff_code
  value_amount                       value
  weight                             weight
}
```

`item_contents` is only populated for international shipments
(`is_intl`); domestic shipments send `[]`. The source list is
`package.items` when present, else `customs.commodities`.

`CustomsContentType` mapping (`units.py`):

| karrio `content_type` | Wire `classification_type` |
|---|---|
| `document` / `documents` | `DOCUMENT` |
| `gift` | `GIFT` |
| `sample` | `SAMPLE` |
| `merchandise` | `SALE_OF_GOODS` |
| `return_merchandise` | `RETURN` |
| `other` | `OTHER` |

### Label request — `LabelRequestType`

```
wait_for_label_url = True
preferences[0] = {
  type: "PRINT",
  format: <PDF|ZPL>,                  ← LabelType
  groups[0] = {
    group: <ServiceLabelGroup>,       ← from service, default "Parcel Post"
    layout: <A4-1pp|A6-1pp|…>,        ← LabelType
    branded: True,
    left_offset: 0, top_offset: 0,
  }
}
shipments[0].shipment_id = "[SHIPMENT_ID]"   ← placeholder replaced by proxy
```

### Shipment response → `ShipmentDetails`

```
shipments[0].items[i].tracking_details.consignment_id ─► tracking_number (item 0)
shipments[0].items[i].tracking_details.article_id     ─► meta.article_ids[]
shipments[0].shipment_id                              ─► shipment_identifier
labels[0].request_id                                  ─► meta.label_request_id
downloaded label (base64)                             ─► docs.label
                                                       meta.manifest_required = True
                                                       meta.carrier_tracking_link
```

`tracking_number` is `consignment_id` of the first item;
`meta.tracking_numbers` is the full list of consignment ids.

### Tracking response → `TrackingDetails`

```
tracking_results[i].tracking_id          ─► tracking_number
trackable_items[0].status                ─► status (TrackingStatus)
trackable_items[0].product_type          ─► info.shipment_service
trackable_items[0].events[]              ─► events[] {
  date (%Y-%m-%dT%H:%M:%S%z)               date / time / timestamp
  description                              description
  location                                 location
}                                          status, reason (per event)
```

`TrackingStatus` maps the event/status **description string** (not a
code) to a karrio status:

| karrio status | AusPost status strings |
|---|---|
| `on_hold` | `Possible delay`, `Held by courier` |
| `delivered` | `Delivered`, `Delivered in Full` |
| `in_transit` | `In transit` (also the default fallback) |
| `delivery_failed` | `Article damaged`, `Cancelled`, `Cannot be delivered`, `Unsuccessful Delivery` |
| `delivery_delayed` | `Possible delay`, `To be Re-Delivered` |
| `out_for_delivery` | `On Board for Delivery` |
| `ready_for_pickup` | `Awaiting collection`, `Ready for Pickup` |

When `item.status` matches no bucket, status defaults to
`in_transit`. `delivered` is set when the resolved status equals
`delivered`.

`TrackingIncidentReason` further maps the same status strings to a
normalized incident reason on each event (e.g. `Article damaged`
→ `carrier_damaged_parcel`, `Possible delay` → `carrier_delay`,
`Unsuccessful Delivery` → `consignee_not_available`, `Held by
courier` → `delivery_exception_hold`, `Cannot be delivered`
→ `delivery_exception_undeliverable`, `Cancelled`
→ `delivery_exception_cancelled`, `To be Re-Delivered`
→ `delivery_exception_redelivery`).

### Manifest response → `ManifestDetails`

```
order.order_id              ─► meta.order_id
order.order_reference       ─► meta.order_reference
order.order_creation_date   ─► meta.order_creation_date
ctx.manifest (base64)       ─► doc.manifest
```

## Identifiers

A created shipment surfaces three distinct ids:

| Wire field | Meaning | Surfaced as |
|---|---|---|
| `shipments[].shipment_id` | AusPost shipment handle | `shipment_identifier`; cancel uses it; manifest `shipments[].shipment_id` |
| `items[].tracking_details.consignment_id` | consignment / tracking number | `tracking_number`, `meta.tracking_numbers[]` |
| `items[].tracking_details.article_id` | per-article barcode id | `meta.article_ids[]` |

Cancel (`DELETE /shipments/{shipment_id}`) keys on
`shipment_identifier`; tracking queries on the consignment /
tracking id.

## Connector-specific invariants

- **`[SHIPMENT_ID]` placeholder.** `shipment_request` builds the label
  body with a literal `"[SHIPMENT_ID]"` string; the proxy performs a
  text replace with the real `shipment_id` from the create response
  before posting `/labels`. The shipment and label bodies are carried
  together in one `Serializable` (`{shipment, label}`).
- **`from` keyword workarounds.** Both rate and shipment requests
  build the sender block under a non-keyword field name
  (`rate_request_from`, `shipment_from`) and string-replace it to
  `from` in the serialized JSON, because `from` is a reserved Python
  identifier and can't be an attrs field.
- **Label download is a third leg with no auth.** The `/labels`
  response returns an absolute `url`; the proxy `GET`s it with no
  headers and base64-encodes the response. The parser only returns a
  `ShipmentDetails` if that label byte string came back.
- **Three calls are best-effort short-circuited.** If `shipment_id`
  is missing the proxy stops after call 1; if the label `url` is
  missing it stops after call 2. The Deserializable always normalizes
  to `[shipment_dict, label_dict_or_{}, label_or_None]`.
- **`meta.manifest_required = True`** is stamped on every shipment —
  AusPost shipments must be manifested (via `/orders`) before
  dispatch.
- **Item-level delivery flags** (`authority_to_leave`,
  `allow_partial_delivery`, `contains_dangerous_goods`) are
  deliberately excluded from the generic option set by
  `shipping_options_initializer` and read straight off the package
  options onto each `ItemType`.
- **`payment_method` is hardcoded `CHARGE_TO_ACCOUNT`** on manifest
  orders; `movement_type` is hardcoded `DESPATCH` on shipments.

## Error parsing

`error.parse_error_response` (`error.py`) normalizes both `errors[]`
and `warnings[]` arrays found in any response object (it accepts a
single dict or a list of dicts). The AusPost error shape is
heterogeneous, so the parser reads several alternative field names per
entry (`error_response.json` shows all of them):

```
Message.code    ← error.code  | error.error_code | error.error
Message.message ← error.message | error.error_description | error.name
Message.details ← { field, context, messages, **kwargs }
```

`**kwargs` lets callers attach context — tracking passes
`tracking_number=result.tracking_id` so per-item tracking errors carry
the offending id.

Where errors are checked per response:

- **Rate** — top-level `errors`/`warnings` plus each `items[]` entry
  that carries `errors`/`warnings`.
- **Shipment** — both the shipment response and the label response are
  scanned.
- **Tracking** — top-level plus each `tracking_results[]` entry with
  `errors` (carrying the `tracking_id`).
- **Cancel** — success is "no error messages" (the proxy decodes the
  `DELETE` to `{ok: True}`).

## References

- **Vendor docs** —
  <https://developers.auspost.com.au/apis/shipping-and-tracking/reference>
  (Australia Post Shipping & Tracking API). Plugin website
  `https://auspost.com.au/`.
- **Sample payloads / generated-schema source** — `schemas/*.json`
  (`rate_request`, `rate_response`, `shipment_request`,
  `shipment_response`, `label_request`, `label_response`,
  `tracking_request`, `tracking_response`, `manifest_request`,
  `manifest_response`, `error_response`). Generated Python lives under
  `karrio/schemas/australiapost/*.py`.
- **Service catalog** — `karrio/providers/australiapost/services.csv`
  (loaded into `DEFAULT_SERVICES` at import).
- **Regenerate schemas** —
  `./bin/run-generate-on modules/connectors/australiapost`
  (driven by the connector's `generate` script). Never hand-edit
  `karrio/schemas/australiapost/*.py`.
```
