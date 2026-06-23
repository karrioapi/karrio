# ParcelOne integration — specification

Reference for the ParcelOne connector. Anything specific to the vendor's
API contract, the JTL conventions on top of it, or the historical
decisions about what we send and why lives here, not as comments in the
code.

## Architecture

- **Per-parcel fan-out**: one `ShippingRequestType` per parcel. The
  parser aggregates N responses into one `ShipmentDetails` via
  `lib.to_multi_piece_shipment`.
- **Dynamic catalog**: `Settings.profile` fetches `GET /shippingapi/v1/profile`
  per connection on first access and projects the live CEP / Product /
  ServiceID portfolio into the unified catalog. Falls back to
  `STATIC_PROFILE` (captured from the JTL sandbox on 2026-05-22) when
  the live fetch fails or times out.
- **Generated schemas**: `karrio/schemas/parcelone/*.py` is generated from
  `schemas/*.json`. Regenerate with `./bin/run-generate-on
  modules/connectors/parcelone` — do not hand-edit.

## Endpoints

| Purpose | Method | Path |
|---|---|---|
| Shipment | POST | `{base}/shippingapi/v1/shipment` |
| Profile (catalog) | GET | `{base}/shippingapi/v1/profile` |
| Tracking (TrackLMC) | GET | `{tracklmc_url}/shipment/{trackno}` |

## Identifiers (two-tier)

ParcelOne returns two distinct tracking numbers on a successful
shipment:

| Field | Meaning | Where we surface it |
|---|---|---|
| `ActionResult.TrackingID` | ParcelOne internal ID | `meta.parcelOneTrackingID` (also `parcelOneShipmentID` / `parcelOneShipmentRef`) — for portal lookups |
| `PackageResults[].TrackingID` | Last-mile-carrier number | `tracking_number` — the customer-facing value |

`ShipmentRef` is echoed on `ShipToData.Reference` and
`IntDocData.ShipToRef` so the label, customs paperwork and tracking
portal all correlate back to a single shipment.

## Auto-attached services

### LBL (carrier-branded label, non-PA1)

Non-PA1 CEPs whose per-product catalog lists `LBL` get
`ServiceID="LBL"` attached automatically so the customer sees the
carrier-branded label instead of a ParcelOne label. Toggleable per
connection via `force_carrier_label` (default `True`). Confirmed
correct by ParcelOne (Mark Friebus, 2026-06).

### LMC (PA1) — NOT auto-attached

Previously auto-attached on PA1 shipments to capture the last-mile-
carrier tracking number. ParcelOne advised against this for Shipping
2.0 (Mark Friebus, 2026-06): the LMC number now arrives natively in
`PackageResults[].TrackingID` whenever the selected product carries
it (e.g. `plusZ`). The `parcelone_last_mile_tracking` option is kept
as `LMC` in the option enum but is not auto-attached anywhere in the
code.

### SDO — wire-code ambiguity

The wire code `SDO` is overloaded across CEPs:

- **PA1**: "Saturday Delivery Only"
- **Non-PA1**: "Shipment Destruction"

Two distinct option enums (`parcelone_saturday_delivery` and
`parcelone_shipment_destruction`) reference the same `SDO` wire code;
the meaning is disambiguated at the CEP level.

## Returns

ParcelOne uses **two different return mechanisms by carrier** (Mark
Friebus, 2026-06):

- **Non-UPS CEPs** → the `SRO` service. `ReturnShipmentIndicator` must
  **not** be sent (it is rejected with "Return Shipments not available
  for this CEP!"), so it stays `0`.
- **UPS CEP** → `ReturnShipmentIndicator` (UPS-exclusive). The `SRO`
  service is **not** sent. The indicator selects the return type:
  `2`=Print+Mail by UPS, `3`=Return Service 1-Attempt, `5`=Return
  Service 3-Attempt, `8`=Electronic Return Label by URL, `9`=Print
  Return Label (default). Override via `options.parcelone_return_indicator`.
  UPS returns also require a goods description in `Package.Remarks`
  (UPS-9120201) — defaulted to `"Goods"` when no parcel content/description
  is supplied (Mark Friebus, 2026-06).

| Service | Trigger | Outbound label | Return label |
|---|---|---|---|
| `SRO` (non-UPS) | `payload.is_return` or `options.parcelone_return_only` | none | `DocumentsResults[].Document` — parser promotes to `docs.label` |
| `ReturnShipmentIndicator` (UPS) | `payload.is_return` or `options.parcelone_return_only` on a UPS CEP | none | per indicator value |
| `SRL` | `options.parcelone_return_label` only | `PackageResults[].Label` | `DocumentsResults[]` — parser surfaces as `docs.extra_documents` |
| `SRLMD` / `SROMD` | same options, alternate-CEP aliases | as above | as above |

`SRL` is **not** auto-attached on `payload.return_address`. The
unified `return_address` is used by many flows that don't want a
ParcelOne return label charged on the shipment.

## Locker / PUDO delivery (`ShipToData.BranchID`)

For locker / parcel-shop / post-office delivery (e.g. the PPL and MFR
CEPs), the PUDO point identifier is sent as `ShipToData.BranchID` via
`options.parcelone_branch_id`. ParcelOne routes the shipment to that
branch (Mark Friebus, 2026-06).

## Customs payload

Customs paperwork is sent on `IntDocData` for every international
shipment that carries a `customs` payload.

### Format defaults

| Field | Value |
|---|---|
| `LabelFormat.Orientation` | `0` |
| `LabelFormat.Size` | from `connection_config.label_size` (default `A6`) |
| `DocumentFormat` | `{Type: <label_format>, Orientation: 0}` (international only) |
| `InternationalDocumentFormat.Size` | `"CN23"` by default; override per connection via `customs.options.cn_form_size` (e.g. `"CN22"` for low-value senders) |

### Flags

- `Invoice=1` when `customs.invoice` (invoice number) is provided
- `PrintInternationalDocuments=1` on every international shipment
- `ReturnShipmentIndicator` — UPS-only; see [Returns](#returns)

### `ItemCategory` mapping

karrio `content_type` → ParcelOne `ItemCategory` int:

| karrio | int |
|---|---|
| gift | 1 |
| documents | 2 |
| sample | 3 |
| return_merchandise | 4 |
| merchandise / other | 5 |

Return shipments override `ItemCategory` to `4` regardless of
`content_type`.

### Aggregate totals

- `TotalValue` summed from commodities (`value_amount × quantity`).
  DHL Weltpaket rejects with `1099 CustomsDetails::getPostalCharges()
  returned null` when this is missing.
- `TotalWeightkg` from parcel weight.
- `Postage` = `0.0` (placeholder; we are not metering).
- `Currency` from `customs.duty.currency` → `options.currency` →
  `"EUR"`.
- `ConsignerCustomsID` — the sender/consigner customs reference
  (EORI-style, e.g. `F1050`, `194082`, `DE284968554884383`). Sourced
  from `customs.duty.account_number`, falling back to
  `customs.options.consigner_customs_id`.
- `ServiceLevel` is intentionally **not** sent. ParcelOne confirmed it
  is unused with no active routing/customs logic behind it (Mark
  Friebus, 2026-06).

### Per-commodity (`CustomDetails`)

- `ItemValuePerItem` / `NetWeightPerItem` are the per-unit variants
  ParcelOne expects. karrio's `value_amount` / `weight` are also
  per-unit, so the mapping is direct. The aggregate variants
  (`ItemValue` / `NetWeight`) are not used.
- `AdditionalInfo` is a flexible Key/Value passthrough. ParcelOne's
  plugin imports populate it with barcode (`EAN`, `Barcode_EAN_13`,
  `Barcode_UPC_1`, …), product/category URL (`urlPath`) and document
  (`Document0`, `Document1`, …) references, and map the keys per
  integration on their side (Mark Friebus, 2026-06). The connector
  therefore forwards **every** `Commodity.metadata` entry verbatim via
  `units.additional_info_for_commodity()`, with two normalisations:
  - the GTIN aliases `ean` / `EAN` / `gtin` / `GTIN` collapse to a
    single `EAN` entry (emitted first);
  - `Commodity.product_url` is surfaced as `urlPath` when metadata does
    not already carry that key.

  The field is left off entirely (not `[None]`) when a commodity has no
  metadata and no `product_url`.

## `ShipToData` / `ShipmentContact`

| Field | Source |
|---|---|
| `Reference` | echoes `ShipmentRef` |
| `Name1` | recipient's company name, else person name |
| `Name2` | recipient's person name when `Name1` is the company |
| `ShipmentContact.AttentionName` | recipient person name (printed under company line on label) |
| `PrivateAddressIndicator` | `1` if recipient is residential, else `0` |

## `ShipmentRef` composition

- **Single parcel** (`len(packages) == 1`): `lib.text(payload.reference, max=20)`
- **Multi-parcel**: `f"{lib.text(payload.reference, max=17)}-{index}"` —
  17-char prefix plus 1-based index, keeping the total ≤ 20 chars.

The same value flows to `ShippingData.ShipmentRef`,
`ShipToData.Reference`, and `IntDocData.ShipToRef`.

## Multi-piece fan-out (UPS)

ParcelOne accepts one parcel per shipment for PA1 and DHL. UPS
supports multi-piece on some products. Per ParcelOne (Mark Friebus,
2026-06), the existing fan-out (one parcel per shipment, N requests)
is operationally safe across the portfolio and aligns with what they
recommend. No optimisation needed unless a concrete customer case
surfaces a benefit.

## Per-shipment routing overrides

Both `consigner_id` and `mandator_id` can be overridden per shipment
via the `parcelone_consigner_id` / `parcelone_mandator_id` options
(both `service_level=True`). Multi-warehouse / multi-mandator
merchants can therefore pin the right values from a shipping method
without duplicating connections.

## `OptionEnum` ↔ wire-code convention

`lib.OptionEnum("LMC", bool, ...)` — the first positional arg is the
ParcelOne `ServiceID`. Iterate `options.items()` and read `.code` to
recover the wire code; do not maintain a parallel `{option_key:
wire_code, ...}` dict. Same pattern FedEx uses.

`OptionEnum`'s `default` arg seeds the type, not `.state`. Fall back
in code when reading: `state if state is not None else <default>`.

## Source-software marker

`ShippingData.Software` carries an integrator brand string ParcelOne
shows in their portal / logs. Configured at connection level via
`app_identifier` (hidden from the shipping-app config editor) or
globally via the `PARCELONE_APP_IDENTIFIER` env var (default
`"JTL-Shipping"`). Same pattern DHL Parcel DE / GLS use.

## Dynamic-metadata tuning

`Settings.profile` is cached per connection at module level. The
cache key includes connection identity, mandator and consigner, so
settings changes bust naturally.

Env vars (settable via constance / Django settings):

| Env var | Default | Purpose |
|---|---|---|
| `PARCELONE_DYNAMIC_TTL_SECONDS` | `3600` (1h) | Successful `/profile` projection cache lifetime |
| `PARCELONE_DYNAMIC_TIMEOUT_SECONDS` | `1.5` | Wall-clock deadline on the live fetch |
| `PARCELONE_DYNAMIC_NEGATIVE_TTL_SECONDS` | `60` | Error / timeout cache lifetime so we don't hammer a flaky vendor |

`/profile` is authoritative for ParcelOne. The dynamic-metadata
projection **replaces** the static catalog rather than unioning with
it, so the picker never offers a service the API would reject for a
given (CEP, Product).
