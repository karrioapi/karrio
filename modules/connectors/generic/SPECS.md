# Generic (Custom Carrier) integration — specification

Reference for the `generic` connector — karrio's **custom-carrier**
extension. Unlike every other connector under
`karrio/modules/connectors/`, `generic` has **no external vendor, no
remote API, and no `schemas/` directory**. It models a user-defined
carrier whose rates come from a static rate sheet stored on the
connection and whose labels are rendered locally from a Jinja template.
It is the engine behind "add your own carrier" / manual / label-less
shipping in the JTL Shipping platform.

The plugin advertises itself as `label="Custom Carrier"`,
`id="generic"`, `status="production-ready"`
(`karrio/plugins/generic/__init__.py`).

## What "generic" means

A real vendor connector (gls, parcelone, fedex, …) translates the
unified karrio model into a carrier's wire format, sends it over HTTP,
and parses the response. The `generic` connector does none of that.
Instead:

- **Rates** are computed *locally* by matching the request's
  destination + weight against a rate sheet (`Settings.services`,
  a list of `ServiceLevel` with `zones`). No HTTP call.
- **Labels** are generated *locally* by rendering a Jinja template
  (`Settings.label_template`, or a built-in default) to SVG/ZPL/PDF.
  No HTTP call.
- **Tracking** is not implemented — there is no carrier to query.
- The "carrier" is whatever the merchant configures:
  `custom_carrier_name`, `display_name`, and a set of services with
  prices live entirely on the connection settings.

This makes `generic` the right fit for: an in-house courier, a regional
carrier with no API, freight priced from a spreadsheet, or any flow
where a merchant wants karrio-shaped rates + a printable label without a
carrier integration.

The bulk of the logic lives in the shared **`karrio.universal`**
package (`karrio/modules/sdk/karrio/universal/`), not in the connector
itself. The connector is a thin wiring layer that points karrio's
Mapper/Proxy at the universal rating/shipping mixins.

## Architecture overview

```
┌──────────────────────────────┐
│  Unified shipping model       │   karrio RateRequest /
│   (karrio core)               │   ShipmentRequest
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│  mappers/generic/mapper.py    │   Delegates verbatim to
│   create_rate_request         │   karrio.universal.providers.*
│   create_shipment_request     │   No carrier-specific transform.
│   parse_rate_response         │
│   parse_shipment_response     │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│  mappers/generic/proxy.py     │   NOT an HTTP transport.
│   get_rates      ───────────► │   = RatingMixinProxy.get_rates
│   create_shipment ──────────► │   = ShippingMixinProxy.create_shipment
│   (built via type(...) )      │   Both run pure-Python locally.
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────┐
│  karrio.universal  (shared, in karrio/modules/sdk)         │
│  ────────────────────────────────────────────────────     │
│  RatingMixinProxy.get_rates                                │
│    → providers/rating/utils.get_available_rates            │
│        zone matching, weight/dim checks, surcharges        │
│  ShippingMixinProxy.create_shipment                        │
│    → generate_service_label                                │
│        → addons/label.generate_label (Jinja → SVG/ZPL)     │
│        → addons/renderer.render_label  (→ PDF/ZPL/base64)  │
└────────────────────────────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────┐
│  Settings (the "carrier")     │   custom_carrier_name, display_name,
│   providers/generic/utils.py  │   services[] (rate sheet),
│   mappers/generic/settings.py │   label_template, metadata, config
└──────────────────────────────┘
```

Key choices:

- **No `karrio/providers/generic/{rate,shipment,tracking}.py`.** The
  connector's `providers/generic/` holds only `units.py` (default
  service + enums) and `utils.py` (the `Settings.carrier_name`
  property). All request/response logic is imported from
  `karrio.universal`.
- **`Proxy` is synthesized with `type(...)`** rather than a class body
  (`mappers/generic/proxy.py`). It binds `get_rates` and
  `create_shipment` directly to the universal mixin methods.
- **No `schemas/` directory** and nothing to regenerate — there is no
  vendor OpenAPI/WSDL.
- **No tracking, no cancel, no pickup, no customs, no manifest.** Only
  rating and shipment (label) creation are wired
  (`mapper.py` exposes exactly four methods).

## Data flow

### Rating (local, no HTTP)

```
RateRequest                         RatingMixinProxy.get_rates
    │                                       │
    ├─► lib.to_address(shipper)             │
    ├─► lib.to_address(recipient)           │
    ├─► lib.to_packages(parcels)            │
    │                                       │
    ├─► is_domicile? (shipper.country ==    │
    │     recipient.country, OR             │
    │     account_country_code == recip.)   │
    ├─► selected_services = settings        │
    │     services ∩ request.services       │
    │                                       │
    │   per package:                        │
    │     get_available_rates(...)          │
    │       for each active ServiceLevel:   │
    │         - destination covered?        │
    │         - weight/dim within limits?   │
    │         - find_best_matching_zone()   │
    │         - base_rate + surcharges      │
    │       → RateDetails | Message         │
    │                                       │
    ▼                                       ▼
parse_rate_response                  list[(pkg_ref, ([RateDetails],
   lib.to_multi_piece_rates                          [Message]))]
```

### Shipment / label (local, no HTTP)

```
ShipmentRequest                     ShippingMixinProxy.create_shipment
    │                                       │
    ├─► lib.to_packages(parcels)            │
    ├─► resolve service_name from           │
    │     settings.services matching        │
    │     request.service (+ honor          │
    │     options.service_name variant)     │
    │                                       │
    │   per package:                        │
    │     tracking_number =                 │
    │       parcel.reference_number         │
    │       else random hex                 │
    │     generate_label(...)               │
    │       Jinja template → SVG/ZPL        │
    │       render_label → base64           │
    │     → ServiceLabel                    │
    │                                       │
    ▼                                       ▼
parse_shipment_response             list[(pkg_ref, ServiceLabel)]
   to_multi_piece_shipment
   → ShipmentDetails{
       tracking_number,
       shipment_identifier = tracking_number,
       docs.label,
       meta.service_name }
```

## Endpoints

None. There is no remote API. Both operations run in-process:

| Purpose | Mechanism |
|---|---|
| Rate | `RatingMixinProxy.get_rates` — local zone matching |
| Shipment / label | `ShippingMixinProxy.create_shipment` — local Jinja render |
| Tracking | not implemented |

The one outbound HTTP call that *can* occur is **internal to label
rendering**: a ZPL-template-to-PDF conversion hits
`http://api.labelary.com/v1/printers/...` in `addons/renderer.render_label`
(only when `template_type == "ZPL"` and `label_type == "PDF"`). This is
a rendering utility, not a carrier API.

## Authentication

None. There are no credentials, tokens, or API keys. `Settings` carries
identity/config only:

| Field | Source | Purpose |
|---|---|---|
| `carrier_id` | required (default `"custom-carrier"`) | connection id surfaced on rate/shipment results |
| `custom_carrier_name` | required | the carrier name shown on `RateDetails` / `ShipmentDetails` (overrides `carrier_name`, which is the constant `"generic"`) |
| `display_name` | required | human label, printed on the default label (`CARR:`) |
| `account_country_code` | optional | used as an origin fallback for the domicile/international decision |
| `account_number` | optional | identity only |
| `test_mode` | default `False` | identity only |
| `metadata` | dict | passed into the label template (`carrier.metadata.*` — e.g. GS1 barcode parts) |
| `config` | dict | drives `connection_config` (`text_color`, `brand_color`) |
| `services` | `list[ServiceLevel]` | the rate sheet (see below) |
| `label_template` | `LabelTemplate` | optional custom Jinja template |

`Settings` is composed from three bases
(`mappers/generic/settings.py`): `provider_utils.Settings`
(`carrier_name="generic"`), `RatingMixinSettings`, and
`ShippingMixinSettings`.

## Supported operations

| Operation | Wired? | Notes |
|---|---|---|
| Rate | yes | local rate-sheet evaluation |
| Shipment create | yes | local label generation |
| Shipment cancel | no | nothing to cancel — no carrier |
| Tracking | no | no carrier to query |
| Pickup | no | — |
| Customs / paperless | no | — |
| Manifest | no | — |

`has_intl_accounts=True` is declared in the plugin metadata, but
international handling is purely the domicile/international zone logic
below — there is no customs surface.

## Services & options

`providers/generic/units.py` defines the bare enums plus the default
rate sheet:

| Enum | Member | Wire/code value |
|---|---|---|
| `Service` | `standard_service` | `"standard"` |
| `Option` | `tracking_number_reference` | `"tracking_number"` |
| `ConnectionConfig` | `text_color`, `brand_color` | label styling hints |

The real "service catalog" is **not** these enums — it is
`Settings.services`, a list of `ServiceLevel`. When a connection
supplies no services, `Settings.shipping_services` falls back to
`DEFAULT_SERVICES`:

```python
DEFAULT_SERVICES = [
    models.ServiceLevel(
        service_name="Standard Service",
        service_code="standard_service",
        currency="USD",
        transit_days=1,
        zones=[models.ServiceZone(label="Zone 1", rate=0.0)],
    ),
]
```

## Rate sheet model

Rates are evaluated against the `ServiceLevel` / `ServiceZone` /
`Surcharge` data types (`karrio/core/models.py`). The merchant defines
these; the universal rating proxy reads them. The fields that drive
matching and pricing:

### `ServiceLevel`

| Field | Role in rating |
|---|---|
| `service_code` / `service_name` | identity; `service_code` is what the caller selects via `request.services` |
| `active` | inactive services are skipped |
| `currency` | rate currency |
| `zones[]` | candidate `ServiceZone` rate cells |
| `domicile` / `international` | destination gating (see below) |
| `weight_unit` / `dimension_unit` | unit basis for limit checks |
| `min_weight` / `max_weight` | package weight bounds (emit `invalid_weight`) |
| `max_length` / `max_height` / `max_width` | dimension bounds (emit `invalid_dimension`) |
| `dim_factor` / `use_volumetric` | volumetric (dimensional) weight: billable = max(actual, L×W×H / dim_factor) |
| `surcharges[]` | fixed or percentage add-ons |
| `cost` | COGS (service-level), overridable per zone |
| `transit_days` | default transit (zone can override) |
| `features` | normalized to a string list on `meta.service_features` |
| `metadata.shipping_method` | display-name override surfaced on `meta.shipping_method` |
| `pricing_config.excluded_markup_ids` | merged into `meta.excluded_markup_ids` |

### `ServiceZone`

| Field | Role |
|---|---|
| `rate` | sell price for the cell |
| `cost` | COGS for the cell (overrides service `cost`) |
| `country_codes` / `cities` / `postal_codes` | location match; empty = wildcard (matches all) |
| `min_weight` / `max_weight` | weight band, **inclusive min / exclusive max** |
| `transit_days` / `transit_time` | overrides service transit |
| `meta.excluded_markup_ids` / `excluded_surcharge_ids` / `plan_costs` | merged into rate `meta` |

## Rating invariants (the heart of the rate engine)

These live in `karrio/universal/providers/rating/utils.py`. Capturing
them here because they are easy to get wrong when authoring a rate
sheet.

### Domicile vs international

```
has_origin     = shipper.country_code OR settings.account_country_code present
is_domicile    = has_origin AND (shipper.country == recipient.country
                                 OR account_country_code == recipient.country)
is_international = NOT is_domicile
```

### Destination coverage

A service covers the destination when any of:

- `domicile is True` and the shipment is domicile, OR
- `international is True` and the shipment is international, OR
- **both flags are `None`** (the generic default — "matches all"), OR
- both flags are `True`.

A service with `domicile=False`/`international=False` rows is otherwise
suppressed — **except** when a zone *explicitly enumerates* the
recipient's country/city/postal code. An explicit zone match is treated
as authoritative proof the service serves that destination and
**overrides** a stale/contradictory `domicile`/`international` flag.
(Real bug this guards: a UPS "Standard to Door" row left
`international=False` but carried AT rate cells; without the override it
was dropped and every DE→AT shipment quoted the Saturday-service rate.)

### Selected vs implicit services

- `request.services` empty → **all** active services are quoted
  (implicit).
- `request.services` non-empty → only the listed `service_code`s are
  quoted; others are excluded.

### Zone selection (most-specific wins)

`find_best_matching_zone` keeps only zones that match both location and
weight, then sorts by:

1. **specificity**: postal_codes (1000) > cities (100) > country_codes
   (10); +5 if any weight bound, +5 more if both bounds defined;
2. **tightest weight range** (smallest max−min gap);
3. **lowest rate** (tie-breaker).

A zone with no location restrictions is a **wildcard** that matches all
destinations but is *not* an "explicit" match (see override above).

### Weight band semantics

Weight matching is **inclusive min, exclusive max**: `min ≤ w < max`.
A package at exactly `max` falls through to the next band. Limit checks
use volumetric billable weight when `use_volumetric` + `dim_factor` are
set.

### Surcharges

`surcharge_type="percentage"` applies `base_rate × amount / 100`;
anything else is a flat `amount`. Each surcharge becomes a
`ChargeDetails`; `total_charge = round(base_rate + Σ surcharges, 2)`.
The base rate is emitted as a `"Base Charge"` charge carrying the
zone/service COGS in `cost`.

### Rate `meta`

Each emitted `RateDetails.meta` carries: `carrier_service_code`,
`service_name`, `shipping_charges`, `shipping_currency`,
`service_features`, and conditionally `shipping_method`,
`excluded_markup_ids`, `excluded_surcharge_ids`, `plan_costs`.

### Rating error codes

| Code | When |
|---|---|
| `destination_not_supported` | explicitly-requested service whose flags/zones don't cover the destination. Deferred and **suppressed** if a sibling entry with the same `service_code` does cover it. |
| `invalid_dimension` | package length/height/width exceeds the service max |
| `invalid_weight` | package weight exceeds the service max |

## Shipment / label invariants

From `karrio/universal/providers/shipping/shipment.py`,
`.../mappers/shipping_proxy.py`, and `karrio/addons/label.py`.

- **Tracking number** = `parcel.reference_number` when present, else a
  random 10-hex-digit number (`uuid4` derived). It is reused as
  `shipment_identifier`.
- **Multi-piece**: one `ServiceLabel` per parcel, aggregated by
  `to_multi_piece_shipment`. The package ref is `parcel.id` or the
  1-based index.
- **Label type** comes from `request.label_type` (defaults `"PDF"`).
- **Service-name variant resolution**: several `ServiceLevel`s can
  share a `service_code` (e.g. UPS Standard / Saturday / Return all map
  to one carrier code). At booking the gateway merges the chosen
  variant's `service_name` onto `options.service_name`; the label
  generator honors that so the label prints the right variant rather
  than whichever row the iterator hit first.
- **`ShipmentDetails.carrier_name`** is `custom_carrier_name` (falling
  back to the `"generic"` constant), so the merchant's chosen name —
  not `"generic"` — appears on results.

### Label template

`Settings.label_template.template` (a Jinja string) or the built-in
default in `addons/label.py`. Two built-ins exist:
`DEFAULT_SVG_LABEL_TEMPLATE` and `DEFAULT_ZPL_LABEL_TEMPLATE`. The
template renders a shipping label with FROM/TO blocks, a `(421)`
SHIP-TO-postal barcode, and a `(00)` SSCC serial-container barcode built
from `carrier.metadata` GS1 parts (`APP_ID`, `EXTENSION_DIGIT`,
`GS1_PREFIX`, the last 6 digits of the tracking number, `CHECK_DIGIT`).
The template context also exposes the parcel `items`, the first item's
`metadata`, `package_index` of `total_packages`, `carton` counts, and
`CountryISO`.

Rendering matrix (`addons/renderer.render_label`):

| `template_type` | `label_type` | Output |
|---|---|---|
| SVG | PDF | SVG → PDF (local), base64 |
| SVG | ZPL | SVG → ZPL (local), base64 |
| ZPL | PDF | ZPL → PDF via `api.labelary.com`, base64 |
| else | (passthrough) | raw template, base64 |

`item.metadata` keys feed the label freely (the sample request shows
EDI-style keys: `RFF_CN`, `BGM`, `RFF_ON`, `DEPT`, `CTL`, `XXNC`,
`NAD_UD`, `RFF_AJY`, `RFF_AEM`). These are not carrier fields — they are
whatever the merchant's label template references.

## Error parsing

There is **no `error.py`** and no carrier error envelope to parse —
there is no carrier. Errors are produced in two ways:

1. **Rating**: `get_available_rates` returns `models.Message`
   instances inline (`destination_not_supported`, `invalid_weight`,
   `invalid_dimension`) tagged with `carrier_id` / `carrier_name`.
2. **Request validation**: `karrio.core.units.Packages` raises
   `FieldError` for missing/invalid parcel fields (e.g. a missing
   `weight`), formatted as `parcel[i].field → {code, message}`
   (`tests/generic/test_errors.py`).

Shipment creation returns an empty message list — local label
generation does not produce carrier errors.

## References

- **Connector code**: `karrio/modules/connectors/generic/`
  - `karrio/plugins/generic/__init__.py` — plugin metadata
  - `karrio/mappers/generic/{mapper,proxy,settings}.py` — wiring
  - `karrio/providers/generic/{units,utils}.py` — defaults + identity
- **Shared engine** (`karrio/modules/sdk/karrio/`):
  - `universal/mappers/rating_proxy.py`,
    `universal/providers/rating/{rate,utils}.py` — rate evaluation
  - `universal/mappers/shipping_proxy.py`,
    `universal/providers/shipping/{shipment,utils}.py` — label flow
  - `addons/label.py`, `addons/renderer.py` — Jinja templates + SVG/ZPL
    rendering
  - `core/models.py` — `ServiceLevel`, `ServiceZone`, `Surcharge`,
    `LabelTemplate`, `ServiceLabel`
- **Tests**: `tests/generic/test_rate.py` (rate-sheet matching),
  `test_shipment.py` (label generation), `test_errors.py` (field
  validation).

No schema regeneration applies — this connector has no `schemas/`
directory and no generated vendor types.
