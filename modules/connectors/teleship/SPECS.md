# Teleship integration — specification

Reference for the Teleship connector. Teleship is an international shipping
platform exposing a **JSON REST** API over OAuth2 `client_credentials`. The
connector wires rate, shipment create/void, tracking, pickup
schedule/cancel, manifest, landed-cost (duties & taxes), and webhook
register/deregister, plus three carrier **hooks** (webhook event ingestion,
OAuth authorize, OAuth callback).

The **vendor source of truth** is the public OpenAPI 3.0 spec kept verbatim
at `vendors/openapi-public.json` and the live developer docs at
<https://developers.teleship.com>.

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Data flow](#data-flow)
3. [Endpoints](#endpoints)
4. [Authentication](#authentication)
5. [Supported operations](#supported-operations)
6. [Services & options](#services--options)
7. [Data mapping](#data-mapping)
8. [Customs / international](#customs--international)
9. [Identifiers](#identifiers)
10. [Webhooks & OAuth hooks](#webhooks--oauth-hooks)
11. [Tracking](#tracking)
12. [Error parsing](#error-parsing)
13. [References](#references)

---

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio RateRequest / ShipmentRequest /
│   (karrio core)         │   TrackingRequest / PickupRequest /
│                         │   ManifestRequest / DutiesCalculationRequest /
│                         │   Webhook + OAuth payloads
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  providers/teleship     │   Pure data transforms.
│   rate.py               │   Unified model → typed Teleship request,
│   shipment/create.py    │   typed Teleship response → unified model.
│   shipment/cancel.py    │   No HTTP, no side effects.
│   tracking.py           │
│   pickup/schedule.py    │
│   pickup/cancel.py      │
│   manifest.py           │
│   duties.py             │
│   webhook/register.py   │
│   webhook/deregister.py │
│   hooks/oauth.py        │   on_oauth_authorize / on_oauth_callback
│   hooks/event.py        │   on_webhook_event (HMAC-SHA256 verify)
│   error.py              │
│   units.py              │   ShippingService, ShippingOption,
│                         │   PackagingType, CustomsContentType,
│                         │   CustomsOption, TrackingStatus,
│                         │   ConnectionConfig, SYSTEM_CONFIG,
│                         │   DEFAULT_SERVICES (from services.csv)
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  mappers/teleship       │   HTTP transport only.
│   proxy.py              │   - OAuth token caching (thread-safe)
│   hooks.py              │   - Bearer auth on every API call
│   mapper.py             │   - async fan-out (rate / shipment)
│   settings.py           │   - concurrent tracking fetch
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Teleship API           │
│  ─────────────────────  │
│  OAuth   /oauth/token   │   client_credentials → accessToken
│  Rates / Shipments      │   /api/rates/quotes, /api/shipments/labels
│  Tracking / Pickups     │   /api/tracking/{n}, /api/pickups
│  Manifests / Webhooks   │   /api/manifests, /api/webhooks
│  Trade engine           │   /api/trade-engine/duties-taxes
└─────────────────────────┘
```

**Key architectural choices:**

- **Per-parcel fan-out** for rates and shipments. `rate_request` /
  `shipment_request` build a `list[...RequestType]` (one entry per package);
  the proxy fires them with `lib.run_asynchronously`. Responses are
  re-aggregated via `lib.to_multi_piece_rates` / `lib.to_multi_piece_shipment`.
- **OAuth2 `client_credentials`** with a per-connection cached access token
  refreshed 30 minutes before expiry (`connection_cache.thread_safe`).
- **Static service catalog** projected from `services.csv` into
  `DEFAULT_SERVICES` (`models.ServiceLevel` rows) at import time. There is
  no live catalog fetch.
- **Generated schemas** — `karrio/schemas/teleship/*.py` is generated from
  `schemas/*.json` (kcli, `--no-nice-property-names`). Don't hand-edit;
  regenerate with `./bin/run-generate-on modules/connectors/teleship`.

## Data flow

### Shipment creation (per-parcel fan-out)

```
ShipmentRequest                                  Teleship API
     │                                                │
     ├─► authenticate() ── POST /oauth/token ────────►│  (cached, 30-min buffer)
     │   ◄── { accessToken, expiresIn } ──────────────│
     │                                                │
     ├─► shipment_request:                            │
     │     to_address / to_packages / to_customs      │
     │     map service → serviceCode                  │
     │     one ShipmentRequestType per package        │
     │                                                │
     │   ─── POST /api/shipments/labels ─────────────►│  (async, one call/parcel)
     │       Authorization: Bearer <token>            │
     │                                                │
     │   ◄── { shipment: { shipmentId, trackingNumber,│
     │            rate, documents[] } } ──────────────│
     │                                                │
     ├─► _extract_details:                            │
     │     trackingNumber → tracking_number           │
     │     shipmentId     → shipment_identifier       │
     │     documents[type=LABEL].base64String → label │
     │     documents[type=INVOICE].base64String → inv │
     │                                                │
     ▼   to_multi_piece_shipment(N responses)         ▼
ShipmentDetails                                  (label per parcel)
```

### Tracking (concurrent per number)

```
TrackingRequest                                  Teleship API
     │  payload.tracking_numbers                      │
     ├─► authenticate() (cached token)                │
     │                                                │
     │   ─── GET /api/tracking/{number} ─────────────►│  (lib.run_concurently)
     │       (one call per tracking number)           │
     │   ◄── TrackingResponseType{ events[], ... } ───│
     │                                                │
     ├─► _extract_details: events → TrackingEvent[]   │
     │     status from last_event.code via            │
     │     TrackingStatus enum (default in_transit)   │
     ▼                                                ▼
list[TrackingDetails]
```

## Endpoints

Test mode host: `https://sandbox.teleship.com`. Prod host:
`https://api.teleship.com`. Both overridable via the `TELESHIP_SERVER_URL`
env var. `{base}` below = the resolved host.

| Purpose | Method | Path |
|---|---|---|
| OAuth token | POST | `{base}/oauth/token` |
| OAuth authorize (hook URL) | GET | `{base}/oauth/authorize?...` |
| Rate quotes | POST | `{base}/api/rates/quotes` |
| Create shipment (label) | POST | `{base}/api/shipments/labels` |
| Void shipment | POST | `{base}/api/shipments/labels/{shipmentId}/void` |
| Tracking | GET | `{base}/api/tracking/{trackingNumber}` |
| Schedule pickup | POST | `{base}/api/pickups` |
| Cancel pickup | POST | `{base}/api/pickups/{pickupId}/cancel` |
| Create manifest | POST | `{base}/api/manifests` |
| Duties & taxes | POST | `{base}/api/trade-engine/duties-taxes` |
| Register webhook | POST | `{base}/api/webhooks` |
| Deregister webhook | DELETE | `{base}/api/webhooks/{webhookId}` |

`Content-Type: application/json` on every API call (the token call uses
`application/x-www-form-urlencoded`). The webhook DELETE returns `204 No
Content`; the proxy decodes an empty body to `{}`.

Tracking link template (customer-facing): `https://track.teleship.com/{}`.

## Authentication

OAuth2 `client_credentials` grant. The token request is a form POST to
`/oauth/token` with body fields `grant_type=client_credentials`,
`clientId`, `clientSecret`. The response carries `accessToken` and
`expiresIn` (seconds); the proxy stamps an `expiry` and caches it.

```
client_credentials                       ┌──────────────────────────┐
       │                                 │ connection_cache          │
       ▼                                 │  .thread_safe             │
┌──────────────┐    miss / expiring      │  key:                     │
│ authenticate │◄────────────────────────│   teleship|<cid>|<secret> │
│  (proxy)     │                         │  token_field: accessToken │
│              │    cache hit            │  buffer_minutes: 30       │
│              │────────────────────────►│                           │
└──────┬───────┘                         └──────────────────────────┘
       │
       ▼  every API call carries:
   Authorization: Bearer <accessToken>
```

Connection credential fields (`mappers/teleship/settings.py`): `client_id`,
`client_secret`. (The `attr.ib(metadata={"sensitive": True})` markers are
present as commented-out alternatives.)

**System-level OAuth app config** (`SYSTEM_CONFIG` in `units.py`,
server-side constance keys) backs the OAuth *authorize* hook — distinct
from the per-connection `client_id` / `client_secret`:

| Key | Purpose |
|---|---|
| `TELESHIP_OAUTH_CLIENT_ID` | OAuth app client id (prod) |
| `TELESHIP_OAUTH_CLIENT_SECRET` | OAuth app client secret (prod) |
| `TELESHIP_SANDBOX_OAUTH_CLIENT_ID` | OAuth app client id (sandbox) |
| `TELESHIP_SANDBOX_OAUTH_CLIENT_SECRET` | OAuth app client secret (sandbox) |

> Note: in `settings.py` the `oauth_client_id` / `oauth_client_secret`
> properties select the **non-sandbox** keys when `test_mode` is true and
> the sandbox keys otherwise — the inverse of the host selection. Documented
> as-is.

## Supported operations

| Operation | Wired in | Notes |
|---|---|---|
| Rate | `rate.py` + `proxy.get_rates` | per-parcel async fan-out |
| Shipment create | `shipment/create.py` + `proxy.create_shipment` | per-parcel async fan-out; label + invoice base64 |
| Shipment void | `shipment/cancel.py` + `proxy.cancel_shipment` | POST `.../void`; success on status `cancelled`/`voided` |
| Tracking | `tracking.py` + `proxy.get_tracking` | concurrent per number |
| Pickup schedule | `pickup/schedule.py` + `proxy.schedule_pickup` | |
| Pickup cancel | `pickup/cancel.py` + `proxy.cancel_pickup` | success on no-error / empty body |
| Manifest | `manifest.py` + `proxy.create_manifest` | by `shipment_identifiers` |
| Duties & taxes | `duties.py` + `proxy.calculate_duties` | landed-cost estimate |
| Webhook register | `webhook/register.py` + `proxy.register_webhook` | defaults `enabledEvents=["*"]` |
| Webhook deregister | `webhook/deregister.py` + `proxy.deregister_webhook` | DELETE → 204 |
| Webhook event hook | `hooks/event.py` | HMAC-SHA256 signature verify |
| OAuth authorize hook | `hooks/oauth.py` | builds `/oauth/authorize` URL |
| OAuth callback hook | `hooks/oauth.py` | extracts account credentials |

`is_hub=False` in plugin metadata.

## Services & options

### Shipping services (`ShippingService`)

| karrio key | wire `serviceCode` |
|---|---|
| `teleship_expedited_pickup` | `TELESHIP-EXPEDITED-PICKUP` |
| `teleship_expedited_dropoff` | `TELESHIP-EXPEDITED-DROPOFF` |
| `teleship_standard_dropoff` | `TELESHIP-STANDARD-DROPOFF` |
| `teleship_standard_pickup` | `TELESHIP-STANDARD-PICKUP` |
| `teleship_postal_dropoff` | `TELESHIP-POSTAL-DROPOFF` |
| `teleship_postal_pickup` | `TELESHIP-POSTAL-PICKUP` |

Per the vendor spec, `*-PICKUP` codes are "Teleship End-to-End" (first-mile
collection included); `*-DROPOFF` codes are "Teleship Hub Direct" (shipper
delivers to a Teleship hub, first mile not included). The static
`DEFAULT_SERVICES` catalog (built from `services.csv`) carries zone /
weight / dimension bounds; all rows are currency `USD`, `domicile=true`,
country `US`, weight `KG`, dimension `CM`, with `0.0` placeholder rates.

### Shipping options (`ShippingOption`)

Surfaced on `additionalServices` (booleans) or as references. The first arg
of each `OptionEnum` is the wire key.

| karrio option | wire key | type | meta category |
|---|---|---|---|
| `teleship_signature_required` | `signatureRequired` | bool | SIGNATURE |
| `teleship_delivery_warranty` | `deliveryWarranty` | bool | INSURANCE |
| `teleship_delivery_PUDO` | `deliveryPUDO` | bool | PUDO |
| `teleship_low_carbon` | `lowCarbon` | bool | — |
| `teleship_duty_tax_calculation` | `dutyTaxCalculation` | bool | — |
| `teleship_customer_reference` | `customerReference` | str | — |
| `teleship_order_tracking_reference` | `orderTrackingReference` | str | — |
| `teleship_commercial_invoice_reference` | `commercialInvoiceReference` | str | INVOICE |

The `additionalServices` block is only emitted when **any** of the five
boolean flags is set; otherwise it is `None` and stripped.

### Packaging types (`PackagingType` → wire `packageType`)

| wire value | unified aliases |
|---|---|
| `envelope` | `pak` |
| `tube` | — |
| `parcel` | `small_box`, `medium_box`, `your_packaging` |

Default when unset: `your_packaging` → `parcel`.

### Connection config (`ConnectionConfig`)

| key | type | default |
|---|---|---|
| `shipping_options` | list | — |
| `shipping_services` | list | — |
| `label_format` | enum `LabelType` (`PDF`/`ZPL`/`PNG`) | `PDF` |

> `hooks/event.py` reads `settings.connection_config.webhook_secret.state`
> for HMAC verification, but `webhook_secret` is **not** declared in
> `ConnectionConfig`. With no declared key, `.state` resolves to `None`, so
> `verify_webhook_signature` returns `True` (skips verification) unless a
> `webhook_secret` value is supplied through the connection config. See
> [Webhooks & OAuth hooks](#webhooks--oauth-hooks).

## Data mapping

### Address — karrio `Address` → Teleship `BillToType` / `AddressType`

Used identically for `shipTo`, `shipFrom`, `returnTo`, `billTo`,
`importerOfRecord`, and pickup/manifest addresses.

```
karrio Address                 Teleship
─────────────────              ─────────────────
contact (person)   ───►        name   (falls back to "N/A" when empty)
company_name       ───►        company
email              ───►        email
phone_number       ───►        phone
address_line1      ───►        address.line1
address_line2      ───►        address.line2
city               ───►        address.city
state_code         ───►        address.state
postal_code        ───►        address.postcode
country_code       ───►        address.country
state_tax_id       ───►        stateTaxId    (billTo / importerOfRecord)
federal_tax_id     ───►        countryTaxId  (billTo / importerOfRecord)
```

`returnTo` / `billTo` blocks are only emitted when the corresponding
`payload.return_address` / `payload.billing_address` is present.

### Parcel — weight & dimensions

```
package.weight.value / .unit.lower()   ───► weight { value, unit }
package.length/width/height (.value)   ───► dimensions { length, width, height, unit (lower) }
```

`dimensions` is only sent when **all three** of length/width/height are
truthy; otherwise omitted.

### Commodities — `Commodity` → `CommodityType`

```
sku                 ───► sku
hs_code             ───► hsCode
title / description ───► title (max 200); description (max 200, only when title present)
category            ───► category
value_amount/curr   ───► value { amount, currency }
quantity            ───► quantity
weight / unit       ───► unitWeight { value, unit (lower) }
origin_country      ───► countryOfOrigin
image_url           ───► imageUrl
product_url         ───► productUrl
(compliance)        ───► compliance = None
```

Source list: `package.items` when populated, else `customs.commodities`.

### Rate response — `RateType` → `RateDetails`

```
rate.service.code        ───► service (via ShippingService.map)
rate.price               ───► total_charge
rate.currency            ───► currency
rate.transit             ───► transit_days
rate.charges[]           ───► extra_charges[] { name, amount, currency }
rate.estimatedDelivery   ───► meta.estimated_delivery (fdate, ISO ± millis)
```

### Shipment response — `ShipmentType` → `ShipmentDetails`

```
trackingNumber          ───► tracking_number
shipmentId              ───► shipment_identifier
documents[type=LABEL]   ───► docs.label    (base64String), label_type ← format (default PDF)
documents[type=INVOICE] ───► docs.invoice  (base64String)
rate.*                  ───► selected_rate (price, currency, transit, charges, estimatedDelivery)
customerReference       ───► meta.customer_reference
shipDate                ───► meta.ship_date
```

## Customs / international

`is_intl` = `recipient.country_code != shipper.country_code`. The `customs`
block is emitted on rate / shipment requests only when `payload.customs` is
present **and** the shipment is international.

### Content type (`CustomsContentType` → wire `contentType`)

| karrio | wire (PascalCase) |
|---|---|
| `documents` | `Documents` |
| `gift` | `Gift` |
| `sample` | `Sample` |
| `other` | `Other` |
| `commercial_goods` | `CommercialGoods` |
| `return_of_goods` | `ReturnOfGoods` |
| `merchandise` (alias) | `CommercialGoods` |

Default content type when unset: `other` → `Other` (rate/shipment);
`CommercialGoods` literal default in the duties request.

### Customs identifiers (`CustomsOption` → wire keys on `customs`)

| karrio customs option | wire field |
|---|---|
| `eori_number` | `EORI` |
| `ioss` | `IOSS` |
| `vat` / `vat_registration_number` | `VAT` |
| `ein` | `EIN` |
| `voec_number` | `VOECNUMBER` |
| `importer_gst` | `importerGST` |
| `exporter_gst` | `exporterGST` |
| `consignee_gst` | `consigneeGST` |

Additional customs fields: `contentType`, `invoiceDate`, `invoiceNumber`
(← `customs.invoice`), `GPSRContactInfo` (← `teleship_gpsr_contact_info`
option), and `importerOfRecord` (← `customs.duty_billing_address`, only when
present).

The duties/taxes request (`duties.py`) additionally sends `incoterms`
(← `customs.options.incoterms`), top-level `currency` (← `options.currency`),
and `orderTrackingReference` (← `payload.reference`); it maps `shipTo` /
`shipFrom` using `person_name` (not `contact`).

## Identifiers

| Teleship field | Meaning | Surfaced as |
|---|---|---|
| `shipment.shipmentId` | Teleship internal shipment id | `shipment_identifier`; consumed by void, manifest, pickup |
| `shipment.trackingNumber` | customer-facing tracking number | `tracking_number` |
| `firstMile.trackingNumber` | first-mile carrier number | tracking `info.shipment_service` (carrier) |
| `lastMile.trackingNumber` | last-mile carrier number | tracking `meta.last_mile_tracking` |

Void keys off `shipmentId` (`payload.shipment_identifier`); pickup cancel
keys off `pickupId` (`payload.confirmation_number`); webhook deregister keys
off `webhookId` (`payload.webhook_id`).

## Webhooks & OAuth hooks

### Webhook event (`on_webhook_event`)

Webhook payload shape:

```
{
  "eventName": "label.generated",   // or "shipment.updated", ...
  "objectType": "shipment",
  "objectId": "<uuid>",
  "data": { ... }                   // event-specific
}
```

- **Signature**: HMAC-SHA256 over the JSON body using the configured
  `webhook_secret`, compared (constant-time, `hmac.compare_digest`) against
  the `x-teleship-signature` header. If either the header or the secret is
  missing, verification is **skipped** (returns `True`).
- Tracking details are extracted (`_extract_webhook_tracking`) only when
  `eventName == "shipment.updated"` and `data.trackingNumber` is present.
  Webhook timestamps include milliseconds (`2025-11-27T05:48:00.000Z`), so
  the parser tries both `%Y-%m-%dT%H:%M:%S.%fZ` and `%Y-%m-%dT%H:%M:%SZ`.
- The hook returns `WebhookEventDetails` with `tracking_number`,
  `shipment_identifier` (← `objectId`), and the parsed `tracking`.

### Webhook registration

`webhook_registration_request` posts `{ url, description, enabled: true,
enabledEvents }`, defaulting `enabledEvents` to `["*"]` when none supplied.
The response surfaces `id` → `webhook_identifier` and `secret` → `secret`.

### OAuth authorize (`on_oauth_authorize`)

Builds `{server_url}/oauth/authorize?...` with query params `redirectUri`,
`state`, `responseType=code`, `clientId` (← system config `oauth_client_id`),
`scope` (default `"read_accounts write_shipments"`). Emits an
`OAUTH_CONFIG_ERROR` message if `oauth_client_id` is unset.

### OAuth callback (`on_oauth_callback`)

Reads `code`, `account_client_id`, `account_client_secret` from the callback
query. Returns `{ client_id, client_secret }` (the per-account API
credentials) to seed the connection. Emits `OAUTH_CALLBACK_ERROR` when the
code or account credentials are missing.

## Tracking

`TrackingResponseType` → `TrackingDetails`:

```
trackingNumber          ───► tracking_number
events[]                ───► events[] { date, time, description, code, location, timestamp, status }
                              (timestamp parsed as %Y-%m-%dT%H:%M:%SZ)
estimatedDelivery       ───► estimated_delivery (ISO ± millis)
firstMile.carrier       ───► info.shipment_service
lastMile.carrier/number ───► meta.last_mile_carrier / last_mile_tracking
shipFrom/shipTo.country ───► info.shipment_origin_country / shipment_destination_country
shipmentId              ───► meta.shipment_id
customerReference       ───► meta.customer_reference
shipDate                ───► meta.ship_date
```

Status is derived from the **most recent** event's `code` matched against
`TrackingStatus`, defaulting to `in_transit` when no match:

| karrio status | Teleship event codes |
|---|---|
| `delivered` | `delivered` |
| `in_transit` | `in_transit`, `collected`, `in_hub`, `out_for_delivery`, `customs_cleared` |
| `out_for_delivery` | `out_for_delivery` |
| `delivery_failed` | `delivery_failed`, `returned`, `cancelled` |
| `pending` | `pending`, `created`, `label_created` |

> Note: `out_for_delivery` appears under both `in_transit` and
> `out_for_delivery`; `list(TrackingStatus)` ordering resolves the match to
> whichever member is iterated first. `delivered` sets `delivered=True`.

## Error parsing

`error.parse_error_response` (`error.py`) handles two shapes and is invoked
across every parser:

1. **`messages[]` array** — `{ "messages": [{ code, message, level,
   timestamp, details }] }` (the generated `ErrorResponseType` /
   `MessageType`). Each becomes a `models.Message`.
2. **single `error`** — `{ "error": {...} }` (dict) or `{ "error": [...] }`
   (list) is normalized into the same per-message mapping.

```
response                       ┌──────────────────────────────┐
   │                           │ parse_error_response          │
   ├─► .messages[] present ──► │   messages[] → Message[]      │
   │                           │   error{}/error[] → Message[] │
   ├─► .error present ───────► │   code=str(code), message,    │
   │                           │   level, details={timestamp,  │
   ▼                           │     details, **kwargs}        │
   list[Message]               └──────────────────────────────┘
```

`kwargs` (e.g. `tracking_number`) are folded into `Message.details`. Token
acquisition raises `errors.ParsedMessagesError` if `/oauth/token` returns
any message.

## References

- **Vendor OpenAPI (authoritative)** — `vendors/openapi-public.json`
  (OpenAPI 3.0; `/api/services`, `/api/rates/quotes`,
  `/api/shipments/labels`, `/api/tracking/{n}`, `/api/pickups`,
  `/api/manifests`, `/api/trade-engine/duties-taxes`, `/api/webhooks`,
  `/oauth/*`).
- **Developer docs** — <https://developers.teleship.com>;
  website <https://www.teleship.com>.
- **Static service catalog** — `karrio/providers/teleship/services.csv`
  (projected into `DEFAULT_SERVICES`).
- **Generated schemas** — `karrio/schemas/teleship/*.py` is generated from
  `schemas/*.json` by the connector's `generate` script (kcli,
  `--no-nice-property-names`). Regenerate with
  `./bin/run-generate-on modules/connectors/teleship` — never hand-edit.
