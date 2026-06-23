# Hermes integration — specification

Reference for the Hermes Germany (Hermes Einrichtungs Service / HSI)
connector. Hermes exposes a **JSON REST** API for shipment-order /
label creation, pickup orders, and shipment-info tracking, behind an
**OAuth2 password-flow** token endpoint. This connector supports
**rate quotes (rate-sheet based), shipment create, return shipment,
pickup schedule/cancel, and tracking**. There is no shipment-cancel or
pickup-update surface on the vendor API.

The **vendor source of truth** lives under `vendor/`:
`openapi.yaml` (combined order/shipment spec), `openapi-shipment.yaml`,
`openapi-auth.yaml`, `openapi-POD.yaml` (proof of delivery), and
`Hermes Germany Eventcodes.csv` (the tracking event-code catalog).

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Data flow](#data-flow)
3. [Endpoints](#endpoints)
4. [Authentication](#authentication)
5. [Supported operations](#supported-operations)
6. [Services & catalog (rate-sheet)](#services--catalog-rate-sheet)
7. [Options](#options)
8. [Connection config](#connection-config)
9. [Data mapping](#data-mapping)
10. [Multi-piece handling](#multi-piece-handling)
11. [Wire-shape invariants & gotchas](#wire-shape-invariants--gotchas)
12. [Tracking](#tracking)
13. [Error parsing](#error-parsing)
14. [ParcelShop finder (karrio.Location)](#parcelshop-finder-karriolocation)
15. [References](#references)

---

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio ShipmentRequest / RateRequest /
│   (karrio core)         │   PickupRequest / TrackingRequest
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  providers/hermes       │   Pure data transforms.
│   shipment/create.py    │   Unified model → typed Hermes request,
│   shipment/             │   typed Hermes response → unified model.
│     return_shipment.py  │   No HTTP, no side effects.
│   pickup/create.py      │
│   pickup/cancel.py      │
│   tracking.py           │
│   error.py              │
│   units.py              │   ShippingService, ShippingOption,
│   utils.py              │   ConnectionConfig, TrackingStatus,
│                         │   LabelType, OAuth login + token cache,
│                         │   multi-piece helpers, services.csv loader
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  mappers/hermes/proxy.py│   HTTP transport only.
│   - get_rates           │   - OAuth password-flow token (cached)
│   - create_shipment     │   - Bearer auth on every call
│   - create_return_…     │   - Sequential multi-piece label calls
│   - schedule_pickup     │   - Accept header selects label format
│   - cancel_pickup       │   - Accept-Language (DE/EN) on every call
│   - get_tracking        │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Hermes APIs            │
│  ─────────────────────  │
│  HSI services REST      │   /shipmentorders/labels, /pickuporders,
│   (de-api.hermesworld)  │   /shipmentinfo
│  OAuth2 authme          │   password-flow access_token
│  Rate sheet (local)     │   services.csv → universal rating provider
└─────────────────────────┘
```

**Key architectural choices:**

- **Rating is rate-sheet only.** Hermes exposes no live rate API. The
  connector mixes in karrio's `universal.mappers.rating_proxy` /
  `universal.providers.rating` and projects a static catalog loaded
  from `services.csv` (`provider_units.DEFAULT_SERVICES`). Domestic
  vs international filtering is driven by the `domicile` /
  `international` flags per service zone.
- **OAuth2 password grant**, not client-credentials. The token is
  cached per `hermes|<username>|<client_id>` key and refreshed 5
  minutes before expiry.
- **Multi-piece = sequential per-package calls.** One
  `ShipmentRequestType` is built per parcel; the proxy POSTs them in
  order, capturing the first response's `shipmentOrderID` and
  injecting it as `parentShipmentOrderID` into parts 2..N.
- **Generated schemas** — `karrio/schemas/hermes/*.py` is generated
  from `schemas/*.json` with `kcli ... --no-nice-property-names` (the
  Hermes API uses camelCase field names, preserved verbatim). Don't
  hand-edit; regenerate with `./bin/run-generate-on
  modules/connectors/hermes`.

## Data flow

### Single-parcel shipment (one HTTP call)

```
ShipmentRequest                          Hermes HSI
     │                                        │
     │  shipment_request()                    │
     ├─► to_address(shipper/recipient)        │
     │   to_packages()                        │
     │   to_shipping_options(initializer)     │
     │   _split_name() → first/last           │
     │                                        │
     ├─► [ShipmentRequestType] (1 elem)       │
     │     ctx{is_multi_piece: False}         │
     │                                        │
     ├─► lib.to_dict → JSON                   │
     │                                        │
     │   ─ POST /shipmentorders/labels ──────►│
     │     Accept: <label mediatype +json>    │  validate
     │     Authorization: Bearer <token>      │  label gen
     │                                        │
     │   ◄ { shipmentID, shipmentOrderID,     │
     │       labelImage(b64), labelMediatype, │
     │       commInvoiceImage? } ─────────────│
     │                                        │
     ├─► _extract_details:                    │
     │     shipmentID      → tracking_number  │
     │     shipmentOrderID → shipment_id      │
     │     labelImage      → docs.label       │
     │     commInvoiceImage→ docs.invoice     │
     ▼                                        ▼
ShipmentDetails (single-piece)         (no further call)
```

### Multi-piece shipment (N sequential HTTP calls)

```
ShipmentRequest                                   Hermes HSI
     │                                                 │
     ├─► shipment_request() builds N requests          │
     │     part 1: partNumber=1, numberOfParts=N,      │
     │             parentShipmentOrderID=None           │
     │     part i: partNumber=i, numberOfParts=N,      │
     │             parentShipmentOrderID=None (filled   │
     │             by proxy)                            │
     │     ctx{is_multi_piece: True}                    │
     │                                                 │
     │   ─ POST /shipmentorders/labels (part 1) ──────►│
     │   ◄ { shipmentOrderID = PARENT } ───────────────│
     │                                                 │
     ├─► inject_parent_shipment_id(PARENT) into        │
     │     service.multipartService of parts 2..N      │
     │                                                 │
     │   ─ POST .../labels (part 2) ──────────────────►│
     │   ─ POST .../labels (part N) ──────────────────►│
     │                                                 │
     ├─► parse_shipment_response:                      │
     │     lib.to_multi_piece_shipment(all responses)  │
     ▼                                                 ▼
ShipmentDetails (aggregated, 1 parent + parts)
```

## Endpoints

`{base}` resolves from `Settings.server_url`:

| Mode | Base URL |
|---|---|
| Test (`test_mode=True`) | `https://de-api-int.hermesworld.com/services/hsi` |
| Prod | `https://de-api.hermesworld.com/services/hsi` |

| Purpose | Method | Path |
|---|---|---|
| OAuth token | POST | `{token_url}` (see [Authentication](#authentication)) |
| Create shipment / label | POST | `{base}/shipmentorders/labels` |
| Create return shipment | POST | `{base}/shipmentorders/labels` (same endpoint, return option forced) |
| Schedule pickup | POST | `{base}/pickuporders` |
| Cancel pickup | DELETE | `{base}/pickuporders/{pickupOrderID}` |
| Tracking (shipment info) | GET | `{base}/shipmentinfo?shipmentID=...&shipmentID=...` |
| ParcelShop finder | GET | `{psf_url}/findParcelShopBy{Address,Location,AddressString}` (separate PSF API; see [ParcelShop finder](#parcelshop-finder-karriolocation)) |

Tracking accepts multiple IDs as repeated `shipmentID` query params,
one per requested tracking number.

Every call sends `Content-Type: application/json` (except OAuth, which
is form-encoded), `Authorization: Bearer <token>`, and
`Accept-Language` from `connection_config.language` (default `DE`).
The shipment create call additionally sets `Accept` to the label
mediatype (see [Label formats](#label-formats)).

## Authentication

OAuth2 **password grant** (Resource Owner Password Credentials).
Credentials live on `Settings`: `username`, `password`, `client_id`,
`client_secret`.

```
                                         ┌──────────────────┐
get_access_token(settings)               │  connection_cache│
       │                                 │  (thread-safe)   │
       ▼                                 │                  │
┌──────────────┐    miss / expiring      │ key:             │
│ access_token │◄────────────────────────│  hermes|         │
│  property    │   (buffer 5 min)        │  <username>|     │
│              │                         │  <client_id>     │
│              │    cache hit            │                  │
│              │────────────────────────►│                  │
└──────┬───────┘                         └──────────────────┘
       │  login()
       ▼  POST {token_url}
   ┌───────────────────────────────────────────────────┐
   │ Content-Type: application/x-www-form-urlencoded     │
   │ Body: grant_type=password & username & password &   │
   │       client_id & client_secret                     │
   └───────────────────────────────────────────────────┘
       │
       ▼  { access_token, expires_in, ... }
   stamped with expiry = now + expires_in (default 3600s)
```

Token URLs:

| Mode | Token URL |
|---|---|
| Test | `https://authme-int.myhermes.de/authorization-facade/oauth2/access_token` |
| Prod | `https://authme.myhermes.de/authorization-facade/oauth2/access_token` |

`login()` raises `ParsedMessagesError` if the token response is not a
dict, or if `error.parse_error_response` finds an `error` key (OAuth2
error shape). `get_access_token()` tolerates either a dict (returns
`access_token`) or a bare string token.

## Supported operations

| Operation | Wired? | Provider entry point | Notes |
|---|---|---|---|
| Rate | yes (rate-sheet) | `universal_provider.rate_request` / `parse_rate_response` | No live rate API; uses `services.csv` |
| Shipment create | yes | `shipment.create.shipment_request` | Single + multi-piece |
| Return shipment | yes | `shipment.return_shipment.return_shipment_request` | Delegates to create with `hermes_return_enabled=True` |
| Shipment cancel | **no** | — | No DELETE endpoint for shipments (see `mapper.py`) |
| Pickup schedule | yes | `pickup.create.pickup_request` | One-time pickups only |
| Pickup cancel | yes | `pickup.cancel.pickup_cancel_request` | DELETE by `pickupOrderID` |
| Pickup update | **no** | — | No PUT endpoint for pickups |
| Tracking | yes | `tracking.tracking_request` | GET with repeated `shipmentID` params |
| Location (ParcelShop finder) | yes | `location.location_request` / `parse_location_response` | Separate PSF API + `apiKey`; backs `karrio.Location` |

## Services & catalog (rate-sheet)

Hermes services are an internal karrio taxonomy backed by the
rate-sheet rows in `services.csv`. `ShippingService` (`units.py`):

| Service code | services.csv rows | Scope |
|---|---|---|
| `hermes_standard` | DE, 0.01–31.5 kg | domestic |
| `hermes_next_day` | DE, 0.01–31.5 kg, transit 1 day | domestic |
| `hermes_stated_day` | DE, 0.01–31.5 kg, transit 1–5 days | domestic |
| `hermes_parcel_shop` | DE, 0.01–25 kg | domestic (PUDO) |
| `hermes_international` | AT, BE, CH, CZ, DK, ES, FI, FR, GB, HU, IE, IT, LU, NL, PL, PT, SE, SK; 0.01–31.5 kg | international |

`load_services_from_csv()` groups CSV rows by service into
`models.ServiceLevel` objects with per-zone `min/max_weight`,
dimensions (cm), `transit_days` (first integer of an `N-M` range),
`country_codes`, `domicile`, and `international` flags. All `rate`
values in the shipped CSV are `0.0` (placeholder — Hermes pricing is
contract-specific). The carrier service code is mapped to the karrio
code via `ShippingService.map(service_code).name_or_key`. If the CSV
is missing, a single `hermes_standard` fallback is returned.

`Settings.shipping_services` returns the configured `services` list if
any, else `DEFAULT_SERVICES`.

### Wire `productType` / packaging

`Parcel.productType` on the wire is a Hermes product type, mapped from
the unified packaging type via `PackagingType`:

| karrio packaging | wire `productType` |
|---|---|
| `hermes_parcel`, `envelope`, `pak`, `tube`, `small_box`, `medium_box`, `your_packaging` | `PARCEL` |
| `hermes_bag` | `BAG` |
| `hermes_bike` | `BIKE` |
| `hermes_large_item`, `pallet` | `LARGE_ITEM` |

`ParcelClass` (`XS/S/M/L/XL`) is sent on shipment create from the
`hermes_parcel_class` option when set (catalogue SS01), and is omitted
otherwise so Hermes derives it from the dimensions. The size class is
also used on **pickup** parcel counts.

## Options

`ShippingOption` (`units.py`) — the first `OptionEnum` arg is the wire
field name. Options serialise inline onto the `service` block (and
`customsAndTaxes`) of the shipment request.

### Delivery options

| Option | Wire field | Type | Notes |
|---|---|---|---|
| `hermes_next_day` | `nextDayService` | bool | next-day delivery |
| `hermes_bulk_goods` | `bulkGoodService` | bool | bulky goods (Sperrgut) |
| `hermes_redirection_prohibited` | `redirectionProhibitedService` | bool | no redirect to neighbour |
| `hermes_stated_day` | `statedDay` | str | `YYYY-MM-DD`; wrapped in `statedDayService` |
| `hermes_time_slot` | `timeSlot` | str | `FORENOON/NOON/AFTERNOON/EVENING`; wrapped in `statedTimeService` |
| `hermes_parcel_class` | `parcelClass` | str | `XS..XL` |

### Signature / ident

| Option | Wire field | Notes |
|---|---|---|
| `hermes_signature` (`signature_required`) | `signatureService` | bool |
| `hermes_household_signature` | `householdSignatureService` | bool |
| `hermes_ident_id` | `identID` | wrapped in `identService` |
| `hermes_ident_type` | `identType` | e.g. `GERMAN_IDENTITY_CARD` |
| `hermes_ident_fsk` | `identVerifyFsk` | min age, e.g. `18` |
| `hermes_ident_birthday` | `identVerifyBirthday` | `YYYY-MM-DD` |

The `identService` block is emitted when `identVerifyFsk` **or**
`identID` is set.

### PUDO (parcel shop)

| Option | Wire field | Notes |
|---|---|---|
| `hermes_parcel_shop_id` | `psID` | triggers `parcelShopDeliveryService` (by-ID) |
| `hermes_parcel_shop_selection_rule` | `psSelectionRule` | `SELECT_BY_RECEIVER_ADDRESS` (no `psID`) triggers address-autoselect; with a `psID` the rule is **forced** to `SELECT_BY_ID` (see gotcha below) |
| `hermes_parcel_shop_customer_firstname` | `psCustomerFirstName` | defaults to recipient first name |
| `hermes_parcel_shop_customer_lastname` | `psCustomerLastName` | defaults to recipient last name |
| `hermes_exclude_parcel_shop_auth` | `excludeParcelShopAuthorization` | bool |

### Notification / COD / dangerous goods / return / reference

| Option | Wire field | Block |
|---|---|---|
| `hermes_notification_email` | `notificationEmail` | `customerAlertService` (emitted when email set) |
| `hermes_notification_type` | `notificationType` | `customerAlertService`; default `EMAIL` |
| `hermes_cod_amount` (`cash_on_delivery`) | `codAmount` | `cashOnDeliveryService.amount` + `bankTransferAmount` |
| `hermes_cod_currency` | `codCurrency` | default `EUR` |
| `hermes_cod_distribution` | `codDistribution` | — |
| `hermes_limited_quantities` | `limitedQuantitiesService` | bool |
| `hermes_return_enabled` | `returnService` | bool (forced on by return-shipment flow) |
| `hermes_include_return_label` | `includeReturnLabel` | bool |
| `hermes_digital_sales_return` | `digitalSalesReturn` | bool |
| `hermes_customer_reference_1` | `clientReference` | str; wins over `payload.reference`, rendered on the label |
| `hermes_customer_reference_2` | `clientReference2` | str; wins over the legacy `clientReference2` option key |

### Internal / multipart (not configurable in the shipping-method editor)

`tanService`, `lateInjectionService`, `partNumber`, `numberOfParts`,
`parentShipmentOrderID` (all `configurable=False`). These back the
multi-piece machinery; callers normally don't set them directly.

### Stated-day default

`shipping_options_initializer()` defaults `hermes_stated_day` to two
business days from today (`_next_business_days(2)`) when the selected
`service` is `hermes_stated_day` and no date was supplied. Hermes
requires `statedDay` to be **≥ 2 days out and never a Sunday/German
public holiday**; skipping Sat/Sun satisfies the ≥2-day and no-Sunday
rules. Holidays are **not** enumerated — callers needing holiday
awareness must pass an explicit date. The initializer mutates a local
copy of the options dict so injected defaults never leak across
requests through the shared class-level `{}` default.

## Connection config

`ConnectionConfig` (`units.py`):

| Key | Type | Default | Purpose |
|---|---|---|---|
| `shipping_options` | list | — | per-connection default options |
| `shipping_services` | list | — | per-connection service allowlist |
| `label_type` | str | `PDF` | label format (`PDF`/`ZPL`/`PNG`) |
| `language` | str | `DE` | `Accept-Language` for responses (`DE`/`EN`) |
| `psf_api_key` | str | — | ParcelShop Finder `apiKey` header (see [ParcelShop finder](#parcelshop-finder-karriolocation)) |
| `psf_base_url` | str | — | override for the PSF base URL (default derives `{host}/psfinder-api` from the HSI host) |

### Label formats

`label_type` selects the `Accept` header via `LabelType.map(...)`.
These are the `+json` variants so the label comes back **base64 in the
JSON body** (`labelImage`) rather than as a raw binary stream:

| `label_type` | Accept header |
|---|---|
| `PDF` (default) | `application/shippinglabel-pdf+json` |
| `ZPL` | `application/shippinglabel-zpl+json;dpi=300` |
| `PNG` | `application/shippinglabel-data+json` |

`parse_shipment_response` derives the unified `label_type` from the
response `labelMediatype` (e.g. `application/pdf` → `PDF`), defaulting
to `application/pdf` → `PDF`.

## Data mapping

### Address — karrio `Address` → Hermes `ErAddressType`

```
karrio Address               Hermes ErAddressType
─────────────────            ────────────────────
street_name        ───►      street            (max 50)
street_number      ───►      houseNumber        (max 5, "" if absent)
postal_code        ───►      zipCode
city               ───►      town               (max 30)
country_code       ───►      countryCode
address_line2      ───►      addressAddition    (max 50)
(unused)                     addressAddition2
company_name       ───►      addressAddition3   (max 20)
```

Names are split by `_split_name()`: first token → `firstname`, the
remainder → `lastname` (single-token names reuse the token for both).
Receiver name → `receiverName` (`ErNameType`); recipient phone/email →
`receiverContact` (`ReceiverContactType` with `phone`, `mail`),
emitted only when phone or email present.

### Sender (divergent shipper)

`senderName` / `senderAddress` are emitted only when the shipper
carries a `person_name` / `street` respectively. When absent, the
account's default sender is used (Hermes resolves it server-side).

### Parcel — karrio `Package` → Hermes `ParcelType`

```
karrio Package          Hermes ParcelType        Unit
──────────────          ─────────────────        ────
height          ───►    parcelHeight             mm (int)
width           ───►    parcelWidth              mm (int)
length          ───►    parcelDepth              mm (int)
weight          ───►    parcelWeight             grams (int)
packaging_type  ───►    productType              PackagingType map
hermes_parcel_class ►    parcelClass              from option (else omitted)
(unused)                parcelVolume             None
```

Dimensions are sent in **millimetres** and weight in **grams**
(`package.height.MM`, `package.weight.G`).

### Customs — karrio `Customs` → Hermes `CustomsAndTaxesType`

Emitted only when `payload.customs` is present.

```
karrio Customs                     Hermes CustomsAndTaxesType
──────────────                     ──────────────────────────
duty.currency (or "EUR")  ───►     currency
commodities[i]            ───►     items[i] (ItemType):
   sku                    ───►        sku
   origin_country         ───►        countryCodeOfManufacture
   value_amount × 100     ───►        value          (int, minor units)
   weight × 1000          ───►        weight         (int, grams)
   quantity (or 1)        ───►        quantity
   description / title    ───►        description
   hs_code                ───►        hsCode
shipper                   ───►     shipmentOriginAddress
                                     (ShipmentOriginAddressType:
                                      firstname, lastname, company,
                                      street, houseNumber, zipCode,
                                      town, state, countryCode,
                                      addressAddition, phone, mail)
```

`value` is sent as an **integer in minor units** (`value_amount × 100`)
and item `weight` as **grams** (`weight × 1000`). The commercial
invoice comes back on `commInvoiceImage` → `docs.invoice`.

### Pickup — karrio `PickupRequest` → Hermes `PickupCreateRequestType`

```
karrio PickupRequest        Hermes PickupCreateRequestType
────────────────────        ──────────────────────────────
address             ───►    pickupAddress (PickupAddressType)
address.person_name ───►    pickupName (split first/last)
address.phone_number───►    phone
pickup_date         ───►    pickupDate
ready_time          ───►    pickupTimeSlot (mapped, see below)
len(parcels)        ───►    parcelCount.pickupParcelCountM
```

Parcel counts are bucketed by size (`pickupParcelCountXS..XL`); the
connector defaults **all** parcels to the M (medium) bucket
(`pickupParcelCountM = len(parcels)`, else 1). `ready_time` hour maps
to a Hermes pickup slot (`PickupTimeSlot`):

| `ready_time` hour | wire `pickupTimeSlot` |
|---|---|
| < 12 | `BETWEEN_10_AND_13` |
| 12–13 | `BETWEEN_12_AND_15` |
| ≥ 14 | `BETWEEN_14_AND_17` |

Only **one-time** pickups are supported; any other `pickup_type`
raises a `FieldError` instructing the caller to arrange recurring
pickups directly with Hermes. The response `pickupOrderID` becomes the
`confirmation_number`; cancel sends it back in the URL path.

### Shipment identifiers (two-tier)

```
shipment create response
  ├─ shipmentID       ───► tracking_number  (customer-facing; 14 or 20 chars)
  │                         meta.shipment_id
  └─ shipmentOrderID  ───► shipment_identifier (internal Hermes handle)
                            meta.shipment_order_id
                            (also the multi-piece parent linker)
```

## Multi-piece handling

Pattern B — **per-package request**:

- First package: `partNumber=1`, `numberOfParts=N`,
  `parentShipmentOrderID=None`.
- Packages 2..N: `partNumber=i`, `numberOfParts=N`,
  `parentShipmentOrderID=<first shipmentOrderID>`.

The provider builds all N typed requests up front (`service.multipartService`
populated, parent left `None`). The proxy walks them sequentially:
after the first POST it reads `shipmentOrderID` via
`extract_shipment_order_id()` and, for each subsequent request,
`inject_parent_shipment_id()` writes it into
`service.multipartService.parentShipmentOrderID`. The `is_multi_piece`
flag rides in the `Serializable.ctx`. Responses are aggregated by
`lib.to_multi_piece_shipment`.

For a **single** parcel, a `multipartService` block is only emitted if
the caller explicitly set `hermes_number_of_parts` (the internal
multipart options).

The `service` block is emitted only when at least one service-bearing
condition is truthy (any flag/value option set, or `is_multi_piece`);
otherwise it is `None` and omitted from the wire payload.

## Wire-shape invariants & gotchas

- **ParcelShop is a `oneOf` discriminated on `psSelectionRule`.** With a
  `psID`, the rule is forced to `SELECT_BY_ID` (the carrier spec
  `ParcelShopDeliveryById` fixes it; any other value combined with `psID`
  triggers error **`e091`**). With no `psID` but
  `hermes_parcel_shop_selection_rule = SELECT_BY_RECEIVER_ADDRESS`, the
  block is emitted for address-autoselect (`psID` omitted). With neither,
  no `parcelShopDeliveryService` block is sent.
- **Parcel-shop customer names default to the recipient.**
  `psCustomerFirstName` / `psCustomerLastName` describe the person
  picking up at the shop, so they fall back to the recipient's
  first/last name when not explicitly provided.
- **Weight in grams, dimensions in millimetres**, both serialised as
  integers — not the kg/cm of the unified model.
- **Customs `value` is in minor units** (`× 100`) and item weight in
  **grams** (`× 1000`).
- **`statedDay` ≥ 2 business days, never Sunday/holiday** — defaulted
  by the option initializer for `hermes_stated_day`; holidays not
  enumerated.
- **COD mirrors amount/currency** onto both the `amount`/`currency`
  and `bankTransferAmount`/`bankTransferCurrency` fields.
- **Label is base64 in the JSON body** (`labelImage`) because the
  `Accept` header uses the `…+json` mediatype variants, not the raw
  binary label formats.
- **Return shipments reuse the create endpoint.** `return_shipment_request`
  rebuilds the `ShipmentRequest` with `hermes_return_enabled=True` and
  delegates to `shipment_request`; the proxy routes
  `create_return_shipment` straight to `create_shipment`.
- **Generated schema field names are camelCase verbatim** — the
  `generate` script runs `kcli` with `--no-nice-property-names`. Don't
  rename them in `karrio/schemas/hermes/`.

## Tracking

`GET /shipmentinfo` with one `shipmentID=` query param per requested
number. The response (`TrackingResponseType`) carries
`shipmentinfo[]`; each entry has either status events or a `result`
with an error `code`/`message` (codes starting with `e`).

Per shipment, events are reversed to **most-recent-first** (karrio
convention). Each event maps to a `TrackingEvent` with `date`/`time`
parsed from `timestamp` (`%Y-%m-%dT%H:%M:%S%z`), `description`, `code`,
`location` (`scanningUnit.city, scanningUnit.countryCode`), `timestamp`,
and a normalised `status`. `estimated_delivery` comes from
`deliveryForecast.date`. `TrackingInfo` carries
`carrier_tracking_link`, destination country/postal code; `meta`
carries `client_id`, `client_reference`, `client_reference2`,
`part_number`, `international_shipment_id`.

### Status mapping

`TrackingStatus` keys off the Hermes **2x2 event codes** (the
`2x2 Code` column of `Hermes Germany Eventcodes.csv`):

| karrio status | Hermes 2x2 codes |
|---|---|
| `pending` | `0000` |
| `in_transit` | `1000`, `2000` |
| `out_for_delivery` | `3000` |
| `delivered` | `3500` |
| `delivery_failed` | `4000`, `4500` |
| `ready_for_pickup` | `5000` |
| `on_hold` | `6000` |
| `delivery_delayed` | `7000` |

`_match_status` scans the enum for a code membership; unmatched codes
fall back to `in_transit` for the overall status. `delivered` is set
when the overall status resolves to `delivered`. Hermes does not
provide granular incident-reason codes, so event `reason` is always
`None` (`_match_reason`).

> Note: the full vendor catalog (`Hermes Germany Eventcodes.csv`) maps
> a wide 3x3 code space down to 2x2 codes; many real-world 2x2 values
> (e.g. `1510`, `4025`, `3710`) are not in the enum above and therefore
> resolve to the `in_transit` fallback at the overall-status level
> while still surfacing their raw `code`/`description` per event.

## Error parsing

`error.parse_error_response` handles three shapes:

1. **Non-dict response** → single `PARSE_ERROR` message with a
   truncated repr of the payload.
2. **OAuth2 error** → when the body has an `error` key, emits a
   message with `code = error` and `message = error_description`
   (used by `login()` to fail authentication).
3. **Hermes result codes** → iterates `listOfResultCodes[]`. Entries
   are treated as **errors** when the code starts with `e`
   (or is non-empty and not a `w…` warning); `w…` codes are
   warnings, surfaced separately by `parse_warning_response`.

```
response
   │
   ├─ not a dict?        ──► [Message PARSE_ERROR]
   │
   ├─ "error" key?       ──► [Message <error>/<error_description>]
   │
   └─ listOfResultCodes  ──► for each {code, message}:
        code startswith "e"          → error Message
        code startswith "w"          → warning (parse_warning_response)
        non-empty, not "w"           → error Message
```

Shipment / pickup / tracking parsers all funnel carrier errors through
`parse_error_response`; tracking additionally emits a per-shipment
`Message` when an individual `shipmentinfo.result.code` starts with
`e`.

## ParcelShop finder (karrio.Location)

The PSF (ParcelShop Finder) Search API is a **separate Hermes service**
from HSI. It backs the unified `karrio.Location` interface
(`location.location_request` / `parse_location_response`, proxy
`get_locations`, mapper `create_location_request` /
`parse_location_response`) so a merchant can resolve nearby ParcelShops
to feed back into `hermes_parcel_shop_id` (catalogue KA07 / SS07).

- **Auth** — an `apiKey` request header, distinct from the HSI OAuth
  token, supplied per connection via `config.psf_api_key`. Without it,
  `get_locations` short-circuits to a `MISSING_PSF_API_KEY` message and
  makes **no** HTTP call.
- **Base URL** — `Settings.psf_url` derives `{host}/psfinder-api` from
  the HSI host (so it follows `test_mode`); override per connection via
  `config.psf_base_url`. Confirm the production host with Hermes.
- **Endpoint selection** (`location_request`):

  | Inputs | Endpoint |
  |---|---|
  | `options.lat` + `options.lng` | `findParcelShopByLocation` |
  | structured `address` (city + zip + street) | `findParcelShopByAddress` |
  | otherwise | `findParcelShopByAddressString` |

  `radius_km` → `maxDist` (max 300), `max_results` → `maxResult`
  (max 100), `options.type_id` → `typeId`, `options.open_now` →
  `openNow`, `address.country_code` → `country` (default `DE`).
- **Response mapping** (`ParcelshopType` → `LocationDetails`):
  `parcelShopNumber` → `location_id`; `typeID` → `location_type`
  (`0` → `parcel_shop`, `1` → `locker`); `name`/`description` → `name`;
  `street`+`houseNumber`/`city`/`zip`/`countryIsoA2Code`/`phone` →
  `address`; `latitude`/`longitude`/`distance` pass through; `hours[]` →
  `opening_hours`. The PSF response is a JSON **array**; each element is
  parsed via `lib.to_object(ParcelshopType, ...)`.
- **Schema** — `karrio/schemas/hermes/parcelshop.py` is generated from
  `schemas/parcelshop.json` (one `ParcelshopType` element).

## References

- **Vendor specs** (`vendor/`):
  - `openapi.yaml` — combined order / shipment-label spec (incl.
    `ParcelShopDeliveryById`)
  - `openapi-shipment.yaml` — shipment surface
  - `openapi-auth.yaml` — OAuth2 password-flow token endpoint
  - `openapi-POD.yaml` — proof of delivery
  - `Hermes Germany Eventcodes.csv` — tracking event-code catalog
    (3x3 → 2x2 mapping, DE/EN descriptions)
- **Live API docs** — <https://de-api-int.hermesworld.com/docs/applications/order>
- **Vendor site** — <https://www.hermesworld.com>
- **Rate sheet** — `karrio/providers/hermes/services.csv`
- **Generated schemas** — `karrio/schemas/hermes/*.py` are generated
  from `schemas/*.json` via `kcli ... --no-nice-property-names` (see
  `generate`). Never hand-edit; regenerate with
  `./bin/run-generate-on modules/connectors/hermes`.
```
