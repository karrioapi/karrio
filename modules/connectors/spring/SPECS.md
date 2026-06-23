# Spring (Spring GDS) integration — specification

Reference for the Spring GDS connector. Spring (a.k.a. Mailing Technology
"XBS" API) is a cross-border / postal-consolidation broker that fans out
to downstream carriers (PostNL, Royal Mail, DPD, Hermes, Colis Privé,
Italian Post, USPS-side products, Packeta, Austrian Post, …) and picks the
last-mile carrier from the service code + destination.

Protocol: **JSON over a single HTTP endpoint** (`mtapi.net`). There is no
REST resource hierarchy and no OAuth — every operation is a POST of a JSON
envelope whose `Command` field selects the action (`OrderShipment`,
`VoidShipment`, `TrackShipment`). The connector documents itself as
`status="beta"` in its plugin metadata.

This connector is generated from JSON samples under `schemas/` via kcli;
the typed modules under `karrio/schemas/spring/*.py` are build artefacts —
see [References](#references).

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio ShipmentRequest / ShipmentCancelRequest
│   (karrio core)         │   TrackingRequest / RateRequest
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  providers/spring       │   Pure data transforms. No HTTP, no side effects.
│   shipment/create.py    │   Unified model → typed Spring envelope,
│   shipment/cancel.py    │   typed Spring response → unified model.
│   shipment/return_…py    │   (return = create with same payload)
│   tracking.py           │
│   error.py              │   ErrorLevel → list[Message]
│   units.py              │   ShippingService (60+ codes), ShippingOption,
│                         │   TrackingStatus, TrackingIncidentReason,
│                         │   LabelFormat, CustomsContentType, CustomsDuty
│   utils.py              │   Settings: server_url, tracking_url
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  mappers/spring/proxy.py│   HTTP transport only.
│   - create_shipment     │   - per-package parallel POST (fan-out)
│   - cancel_shipment     │   - per-tracking-number parallel POST
│   - get_tracking        │   - single shared endpoint, Command-dispatched
│   - create_return_…      │   - Content-Type: text/json
│   - get_rates           │   - rating served by karrio universal mixin
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Spring XBS API          │
│   POST https://mtapi.net │   Command: OrderShipment / VoidShipment /
│   (?testMode=1 in test)  │            TrackShipment
└─────────────────────────┘
```

**Key architectural choices:**

- **Single endpoint, command-dispatched.** Every operation POSTs to the
  same URL; the JSON `Command` field (`OrderShipment`, `VoidShipment`,
  `TrackShipment`) selects the action. There is no per-operation path.
- **Per-package fan-out.** Spring is a one-package-per-call carrier.
  `create_shipment` builds one `ShipmentRequestType` per parcel and fires
  them in parallel via `lib.run_asynchronously`; the parser aggregates the
  N responses with `lib.to_multi_piece_shipment`. Tracking is likewise
  one-shipment-per-call, fanned out and re-keyed by tracking number.
- **No native rating.** `get_rates` / `parse_rate_response` delegate to
  karrio's `universal` rating mixin (`rating_proxy` / `universal.providers.rating`)
  driven by the static `DEFAULT_SERVICES` catalog loaded from
  `services.csv`. Spring's live API is not queried for rates.
- **Static service catalog from CSV.** `units.load_services_from_csv()`
  reads `karrio/providers/spring/services.csv` at import time into
  `DEFAULT_SERVICES` (a list of `ServiceLevel` with weight-banded zones).
- **Generated schemas** — `karrio/schemas/spring/*.py` is generated from
  `schemas/*.json`. Regenerate with `./bin/run-generate-on
  modules/connectors/spring`; never hand-edit.

## Data flow

### Shipment create (per-package fan-out, one HTTP call per parcel)

```
ShipmentRequest                                   Spring XBS API
     │                                                  │
     ├─► shipment_request()                             │
     │     to_address(shipper)   → ConsignorAddress     │
     │     to_address(recipient) → ConsigneeAddress     │
     │     to_packages()         → one request / parcel │
     │     to_customs_info()     → Products[] + duty    │
     │     map service → Service code                   │
     │     resolve LabelFormat                          │
     │                                                  │
     ├─► [ShipmentRequestType, ...]  (one per parcel)   │
     │     Command="OrderShipment"                      │
     │                                                  │
     │   ─── POST mtapi.net (×N, parallel) ────────────►│
     │       Content-Type: text/json                    │
     │                                                  │
     │   ◄── [{ErrorLevel, Shipment{TrackingNumber,     │
     │          LabelImage, Carrier, ...}}, ...] ───────│
     │                                                  │
     ├─► _extract_details per response                  │
     │     (only when Shipment present + ErrorLevel∈{0,1})│
     │   to_multi_piece_shipment([...])                 │
     │                                                  │
     ▼                                                  ▼
ShipmentDetails (aggregated)                       (no further call)
```

### Tracking (per-number fan-out)

```
TrackingRequest                                   Spring XBS API
     │                                                  │
     ├─► tracking_request()                             │
     │     one TrackingRequestType per number           │
     │     Command="TrackShipment"                      │
     │                                                  │
     │   ─── POST mtapi.net (×N, parallel) ────────────►│
     │       proxy keeps (TrackingNumber, response)     │
     │                                                  │
     │   ◄── (number, {ErrorLevel, Shipment{Events[]}})─│
     │                                                  │
     ├─► _extract_details (ErrorLevel==0 + Shipment)    │
     │     events reversed (newest first)               │
     │     latest Code → TrackingStatus                 │
     │     per-event Code → status + incident reason    │
     │                                                  │
     ▼                                                  ▼
list[TrackingDetails]                              list[Message] for failures
```

## Endpoints

Single base URL, switched by `test_mode`:

| Mode | Base URL |
|---|---|
| Production | `https://mtapi.net/` |
| Test | `https://mtapi.net/?testMode=1` |

All operations POST to that URL; the action is the JSON `Command` field.

| Purpose | Method | URL | `Command` |
|---|---|---|---|
| Create shipment | POST | `{server_url}` | `OrderShipment` |
| Cancel / void shipment | POST | `{server_url}` | `VoidShipment` |
| Track shipment | POST | `{server_url}` | `TrackShipment` |
| Create return shipment | POST | `{server_url}` | `OrderShipment` (delegates to create) |
| Rates | — | (not called) | served locally by universal rating mixin |

`Content-Type` on every call is `text/json` (not `application/json`).
Public tracking URL template (for end users, not an API call):
`https://www.mailingtechnology.com/tracking/?tn={}`.

## Authentication

API-key only. The key is sent **in the request body** as the `Apikey`
field on every envelope — there is no auth header and no token exchange.

| Setting | Field | Notes |
|---|---|---|
| `api_key` | `Apikey` | required; the only credential. (A commented-out `sensitive` metadata marker exists in `settings.py` but is not active.) |
| `test_mode` | — | toggles `?testMode=1` on the base URL |
| `account_country_code` | — | generic karrio setting |
| `services` | — | per-connection `ServiceLevel` overrides; falls back to `DEFAULT_SERVICES` |
| `config` | — | holds `ConnectionConfig` (see below) |

## Supported operations

| Operation | Wired | Notes |
|---|---|---|
| Rate | yes (local) | universal rating mixin over `DEFAULT_SERVICES`; no live call |
| Shipment create | yes | per-package fan-out, multi-piece aggregation |
| Shipment cancel (void) | yes | `VoidShipment` by `TrackingNumber` |
| Return shipment | yes | wrapper that re-runs create with the same payload |
| Tracking | yes | per-number fan-out, event + status mapping |
| Pickup | no | not implemented |
| Document upload / manifest | no | not implemented |

## Services & options

### Connection config

| Config key | Type | Default |
|---|---|---|
| `label_format` | str | `PDF` |

### Label formats (`LabelFormat`)

`PDF` · `PNG` · `ZPL300` (ZPL 300 dpi) · `ZPL200` (ZPL 203 dpi) ·
`ZPL` (alias for ZPL300) · `EPL` (EPL 203 dpi).

Resolution order in `create.py`:
`payload.label_type` → `connection_config.label_format` → `"PDF"`.

### Packaging (`PackagingType`)

Spring has a single packaging type, `PACKAGE`. Every unified packaging
preset (`envelope`, `pak`, `tube`, `pallet`, `small_box`, `medium_box`,
`your_packaging`) collapses onto `PACKAGE`.

### Services (`ShippingService`) — karrio code → wire `Service`

Spring service codes are short alphanumeric strings sent on
`Shipment.Service`. The "routed" services let Spring auto-select the best
downstream carrier; the rest pin a specific downstream carrier/product.

| Group | karrio code | wire |
|---|---|---|
| Routed | `spring_tracked` | `TRCK` |
| Routed | `spring_signature` | `SIGN` |
| Routed | `spring_untracked` | `UNTR` |
| Routed | `spring_collect` | `CLLCT` |
| Express/special | `spring_express` | `EXPR` |
| Express/special | `spring_import` | `IMPRT` |
| Express/special | `spring_back_returns` | `BACK` |
| Express/special | `spring_back_tracked` | `BACKT` |
| Express/special | `spring_no_label` | `NOLABEL` |
| PostNL Parcel | `spring_postnl_parcel_eu` | `PPLEU` |
| PostNL Parcel | `spring_postnl_parcel_benelux` | `PPND` |
| PostNL Parcel | `spring_postnl_parcel_benelux_sign` | `PPNDS` |
| PostNL Parcel | `spring_postnl_parcel_benelux_no_neighbor` | `PPHD` |
| PostNL Parcel | `spring_postnl_parcel_benelux_sign_no_neighbor` | `PPHDS` |
| PostNL Parcel | `spring_postnl_parcel_benelux_upu` | `PPLUP` |
| PostNL Parcel | `spring_postnl_parcel_globalpack_ems` | `PPLGE` |
| PostNL Parcel | `spring_postnl_parcel_globalpack_upu` | `PPLGU` |
| PostNL Parcel | `spring_postnl_parcel_epg` | `PPLEP` |
| PostNL Parcel | `spring_postnl_parcel_epg_noneu` | `PPNEU` |
| PostNL Parcel | `spring_postnl_lightweight_china` | `PPLLW` |
| PostNL Parcel | `spring_postnl_collect_service` | `PPLCS` |
| PostNL Packet (<2kg) | `spring_postnl_packet_tracked` | `PPTT` |
| PostNL Packet | `spring_postnl_packet_registered` | `PPTR` |
| PostNL Packet | `spring_postnl_packet_non_tracked` | `PPNT` |
| PostNL Packet | `spring_postnl_packet_boxable_bag_trace` | `PPBBT` |
| PostNL Packet | `spring_postnl_packet_bag_trace` | `PPBT` |
| PostNL Packet | `spring_postnl_packet_boxable_tracked` | `PPBTT` |
| PostNL Packet | `spring_postnl_packet_boxable_non_tracked` | `PPBNT` |
| Royal Mail | `spring_royal_mail_tracked_24` | `RM24` |
| Royal Mail | `spring_royal_mail_tracked_24_sign` | `RM24S` |
| Royal Mail | `spring_royal_mail_tracked_48` | `RM48` |
| Royal Mail | `spring_royal_mail_tracked_48_2` | `RM482` |
| Royal Mail | `spring_royal_mail_tracked_48_sign` | `RM48S` |
| Sending (ES/PT) | `spring_sending_mainland` | `SEND` |
| Sending (ES/PT) | `spring_sending_islands` | `SEND2` |
| Italian Post | `spring_italian_post_crono` | `ITCR` |
| Italian Post | `spring_italian_post_crono_express` | `ITCRX` |
| German | `spring_dpd_de` | `DPDDE` |
| German | `spring_hermes_sign` | `HEHDS` |
| German | `spring_hermes_collect` | `HEDCS` |
| French | `spring_colis_prive` | `CPHD` |
| French | `spring_colis_prive_sign` | `CPHDS` |
| Spring Commercial | `spring_com_standard` | `SCST` |
| Spring Commercial | `spring_com_standard_sign` | `SCSTS` |
| Spring Commercial | `spring_com_express` | `SCEX` |
| Spring Commercial | `spring_com_express_sign` | `SCEXS` |
| USA | `spring_usa_parcel_ground` | `UPGR` |
| USA | `spring_usa_parcel_ground_sign` | `UPGRS` |
| USA | `spring_usa_parcel_express` | `UPEX` |
| USA | `spring_usa_parcel_express_sign` | `UPEXS` |
| USA | `spring_usa_parcel_max` | `UPMA` |
| USA | `spring_usa_parcel_max_sign` | `UPMAS` |
| USA | `spring_usa_parcel_ground_dg` | `UPDG` |
| USA | `spring_usa_parcel_ground_dg_sign` | `UDGS` |
| USA | `spring_usa_parcel_plus_ground_dg` | `UPPDG` |
| USA | `spring_usa_parcel_plus_ground_dg_sign` | `UPDGS` |
| Other | `spring_packeta` | `PACHD` |
| Other | `spring_mailalliance_boxable` | `MABNT` |
| Other | `spring_austrian_post` | `ATEHD` |

The service is mapped via `ShippingService.map(payload.service).value_or_key`
— an unknown service falls through as the supplied key.

### Options (`ShippingOption`) — karrio key → wire field

Each option's `OptionEnum` first argument is the wire field name placed on
`Shipment.*` (or `ConsignorAddress.*`). `service_level=True` marks options
that can be pinned on a shipping method.

| Option key | Wire field | Type | Where it lands |
|---|---|---|---|
| `spring_customs_duty` | `CustomsDuty` | str | `Shipment.CustomsDuty` |
| `spring_declaration_type` | `DeclarationType` | str | `Shipment.DeclarationType` |
| `spring_dangerous_goods` | `DangerousGoods` | bool | `Shipment.DangerousGoods` (`Y`/`N`) |
| `spring_shipping_value` | `ShippingValue` | float | `Shipment.ShippingValue` |
| `spring_display_id` | `DisplayId` | str | `Shipment.DisplayId` |
| `spring_invoice_number` | `InvoiceNumber` | str | `Shipment.InvoiceNumber` |
| `spring_order_reference` | `OrderReference` | str | `Shipment.OrderReference` |
| `spring_order_date` | `OrderDate` | str | `Shipment.OrderDate` |
| `spring_consignor_vat` | `ConsignorVat` | str | `ConsignorAddress.Vat` (falls back to `shipper.tax_id`) |
| `spring_consignor_eori` | `ConsignorEori` | str | `ConsignorAddress.Eori` |
| `spring_consignor_nl_vat` | `ConsignorNlVat` | str | `ConsignorAddress.NlVat` |
| `spring_consignor_eu_eori` | `ConsignorEuEori` | str | `ConsignorAddress.EuEori` |
| `spring_consignor_gb_eori` | `ConsignorGbEori` | str | `ConsignorAddress.GbEori` |
| `spring_consignor_ioss` | `ConsignorIoss` | str | `ConsignorAddress.Ioss` |
| `spring_consignor_local_tax_number` | `ConsignorLocalTaxNumber` | str | `ConsignorAddress.LocalTaxNumber` |
| `spring_export_carrier_name` | `ExportCarrierName` | str | `Shipment.ExportCarrierName` (BACK service) |
| `spring_export_awb` | `ExportAwb` | str | `Shipment.ExportAwb` (BACK service) |
| `spring_pudo_location_id` | `PudoLocationId` | str | `ConsigneeAddress.PudoLocationId` (collect/PUDO) |

Unified-option aliases: `dangerous_goods` → `spring_dangerous_goods`,
`shipment_date` → `spring_order_date`.

## Data mapping

### Address — karrio `Address` → Spring `ConsignorAddressType` / `AddressType`

The shipper maps to the richer `ConsignorAddressType` (extra tax-id
fields); the recipient maps to `AddressType`.

```
karrio Address                 Spring address field
─────────────────              ────────────────────
person_name / company_name ─►  Name (person_name, else company_name)
company_name               ─►  Company
address_line1              ─►  AddressLine1
address_line2              ─►  AddressLine2
(none)                     ─►  AddressLine3  (always None from create.py)
city                       ─►  City
state_code                 ─►  State
postal_code                ─►  Zip
country_code               ─►  Country
phone_number               ─►  Phone
email                      ─►  Email
tax_id                     ─►  Vat (consignor: only if no spring_consignor_vat)
```

Consignor-only tax fields (`Eori`, `NlVat`, `EuEori`, `GbEori`, `Ioss`,
`LocalTaxNumber`) come solely from the `spring_consignor_*` options.
Consignee-only field `PudoLocationId` comes from `spring_pudo_location_id`.
The `ImporterAddress` block exists in the generated schema (and JSON
sample) but the connector does **not** populate it.

### Parcel / shipment

```
karrio parcel                  Shipment field
─────────────                  ──────────────
weight.KG                  ─►  Weight (string)         + WeightUnit="kg"
length.CM / width.CM /     ─►  Length / Width / Height (string, omitted if 0)
  height.CM                     + DimUnit="cm" (only if any dim present)
parcel.description         ─►  Description (else customs.content_description)
label_type/config/"PDF"    ─►  LabelFormat
```

`ShipperReference` is the shipment reference. For multi-piece it is
suffixed with a 1-based index: `{reference}-{n}`; single-package keeps the
bare reference. The base reference defaults to a random `uuid4().hex` when
`payload.reference` is absent.

### Customs — `CustomsInfo` → `Shipment.Products[]` + duty fields

```
karrio CustomsInfo             Spring field
──────────────────             ────────────
commodities[i].description /   Products[i].Description (lib.text, max 60)
  title
commodities[i].sku         ─►  Products[i].Sku
commodities[i].hs_code     ─►  Products[i].HsCode
commodities[i].origin_country  Products[i].OriginCountry (else shipper country)
commodities[i].quantity    ─►  Products[i].Quantity (string, default "1")
commodities[i].value_amount ─► Products[i].Value (string, default "0")
commodities[i].weight      ─►  Products[i].Weight (string, default "0")

(sum of product values, else  Shipment.Value
  duty.declared_value)
content_type               ─►  Shipment.DeclarationType (via CustomsContentType)
incoterm                   ─►  Shipment.CustomsDuty (via CustomsDuty, default "DDU")
duty.currency / option     ─►  Shipment.Currency
```

`Products` is sent as `[]` (empty list, never `None`) when there are no
commodities — an explicit guard against the jstruct `[None]`
serialization bug for `JList` fields.

Customs declaration type (`CustomsContentType`):

| karrio `content_type` | Spring `DeclarationType` |
|---|---|
| `sale_of_goods` | `SaleOfGoods` |
| `documents` | `Documents` |
| `gift` | `Gift` |
| `returned_goods` | `ReturnedGoods` |
| `commercial_sample` | `CommercialSample` |

Customs duty / incoterm (`CustomsDuty`), default `DDU`:

| karrio `incoterm` | Spring `CustomsDuty` | Meaning |
|---|---|---|
| `DDU` | `DDU` | Delivered Duty Unpaid (default) |
| `DDP` | `DDP` | Delivered Duty Paid ("Spring Clear") |

`spring_customs_duty` (option) overrides the incoterm-derived value.

### Shipment response → `ShipmentDetails`

```
ShipmentResponse.Shipment      ShipmentDetails
─────────────────────────      ───────────────
TrackingNumber             ─►  tracking_number AND shipment_identifier
LabelImage                 ─►  docs.label (base64)
LabelFormat (else "PDF")   ─►  label_type
Service / Carrier /            meta.{service, carrier, shipper_reference,
  ShipperReference /             carrier_tracking_number,
  CarrierTrackingNumber /        carrier_local_tracking_number,
  CarrierLocalTrackingNumber /   carrier_tracking_url, display_id, label_type}
  CarrierTrackingUrl /
  DisplayId / LabelType
```

`tracking_number` doubles as `shipment_identifier`; cancel uses it as the
`VoidShipment` key.

### Tracking response → `TrackingDetails`

```
TrackingResponse.Shipment      TrackingDetails
─────────────────────────      ───────────────
Events[] (reversed → newest    events[]:
  first)                         DateTime  ─► date, time, timestamp (ISO 8601)
                                 Description ─► description
                                 Code        ─► code, status, reason
                                 City,State,Country ─► location (", " joined)
latest Events[0].Code      ─►  status (via TrackingStatus; default in_transit)
TrackingNumber / queried   ─►  tracking_number
CarrierTrackingUrl         ─►  info.carrier_tracking_link
Weight / WeightUnit        ─►  info.package_weight / package_weight_unit
Service/Carrier/DisplayId/…─►  meta.*
```

`delivered` is set when the resolved status equals `delivered`.

## Tracking status & incident mapping

`Shipment.Events[].Code` (numeric, sent as int in samples, matched as
string) maps to karrio `TrackingStatus` (per Spring XBS API doc §3). The
latest event drives the shipment-level status; an unmatched latest code
falls back to `in_transit`.

| karrio status | Spring codes |
|---|---|
| `pending` | `0` (parcel created), `12` (preparation) |
| `on_hold` | `40` (in customs), `41` (customs exception), `31` (delivery exception – action required) |
| `in_transit` | `15`, `18`, `19`, `20`, `21`, `22`, `25`, `93`, `2101`, `2102`, `2103`, `9101`, `9102`, `9999` |
| `out_for_delivery` | `9301` |
| `delivery_delayed` | `9302` |
| `ready_for_pickup` | `92` (awaiting collection) |
| `delivery_failed` | `91` (delivery attempted), `111` (lost/destroyed), `1001` (incomplete data), `4106` (consignment cancelled) |
| `delivered` | `100` (delivered), `101` (delivered to destination country) |
| `return_to_sender` | `124`, `125`, `12406`, `12501`, `12502`, `12503`, `12504`, `12505`, `12506` |

Exception codes additionally resolve to a normalized incident reason
(`TrackingIncidentReason`) on the event's `reason` field:

| Incident reason | Spring codes |
|---|---|
| `carrier_parcel_lost` | `111` |
| `carrier_damaged_parcel` | `12503` |
| `consignee_refused` | `12501` |
| `consignee_not_available` | `91`, `12504` |
| `consignee_incorrect_address` | `12502` |
| `customs_delay` | `40`, `41` |
| `delivery_exception_delayed` | `9302` |
| `delivery_exception_action_required` | `31` |
| `delivery_exception_cancelled` | `4106` |
| `delivery_exception_incomplete_data` | `1001` |
| `return_by_agreement` | `12505` |
| `return_destroyed` | `12506` |

## Returns

`return_shipment_request` is a thin wrapper: it re-runs the standard
`shipment_request` with the same payload (options copied through). The
return is driven by the chosen service code (`spring_back_returns` /
`BACK`, `spring_back_tracked` / `BACKT`) and the BACK-only options
`spring_export_carrier_name` / `spring_export_awb`, rather than by a
separate request shape.

## Error parsing

Spring signals success/failure with an `ErrorLevel` integer on every
response (not HTTP status codes):

| `ErrorLevel` | Meaning |
|---|---|
| `0` | Command completed without errors |
| `1` | Command completed **with** errors (e.g. shipment created but flagged) |
| `10` | Fatal error — command not completed at all |

```
response (dict)
   │
   ├─ not a dict?           ─► []  (no messages)
   ├─ ErrorLevel == 0       ─► []  (success)
   └─ ErrorLevel in (1,10)  ─► [Message(
                                  code=str(ErrorLevel),
                                  message=Error  (else level-specific default),
                                  details={**kwargs})]
```

Notes:

- Shipment parsing extracts details when `Shipment` is present **and**
  `ErrorLevel ∈ {0, 1}` — i.e. an `ErrorLevel 1` shipment is still surfaced
  (label + tracking) *and* its error is emitted as a `Message`.
- Cancel treats success as `ErrorLevel == 0` with no messages.
- Tracking passes the queried `tracking_number` through `**kwargs` into
  `Message.details` so failures can be correlated.
- `Error` is the human-readable message; when blank a level-specific
  default is used (`"Command completed with errors"` / `"Fatal error,
  command not completed"`).

## Localization

Service and option display names are translated for the JTL surface in
`karrio/providers/spring/i18n.py` (`SERVICE_NAME_TRANSLATIONS` /
`OPTION_NAME_TRANSLATIONS`, `gettext_lazy`), keyed by karrio service/option
code.

## References

- **Vendor API** — Spring GDS / Mailing Technology "XBS" JSON API at
  `https://mtapi.net/` (test: `?testMode=1`). Tracking codes per the XBS
  API documentation §3 (referenced in `units.py`); the connector ships no
  `vendor/` directory.
- **Public tracking** —
  `https://www.mailingtechnology.com/tracking/?tn={trackingNumber}`.
- **Generated schemas** — `karrio/schemas/spring/*.py` is generated from
  the JSON samples under `schemas/` (`shipment_request.json`,
  `shipment_response.json`, `shipment_cancel_request.json`,
  `shipment_cancel_response.json`, `tracking_request.json`,
  `tracking_response.json`, `error_response.json`) by the `./generate`
  script (`kcli codegen generate`). Regenerate with
  `./bin/run-generate-on modules/connectors/spring` — never hand-edit the
  generated `.py` modules.
- **Service catalog** — `karrio/providers/spring/services.csv` is the
  source for `DEFAULT_SERVICES` (weight-banded `ServiceLevel` zones used by
  the local universal rating mixin).
- **Plugin metadata** — `karrio/plugins/spring/__init__.py`
  (`id="spring"`, `label="Spring"`, `status="beta"`, `is_hub=False`).
