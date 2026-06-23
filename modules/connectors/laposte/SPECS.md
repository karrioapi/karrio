# La Poste integration — specification

Reference for the La Poste connector. La Poste is the French national
postal operator; this connector integrates its **Suivi v2** parcel
tracking API (JSON REST) at `https://api.laposte.fr/suivi/v2`.

**The connector is tracking-only.** It implements `get_tracking` and
nothing else — there is no rate, shipment create/cancel, pickup,
document, or manifest support wired. The mapper exposes only
`create_tracking_request` / `parse_tracking_response`; `units.py`
carries a single placeholder `ShippingService` and an empty
`ShippingOption` enum (services exist only as a static
`DEFAULT_SERVICES` catalog for the picker — see
[Services & static catalog](#services--static-catalog)).

The vendor source of truth is the La Poste *Suivi* developer product on
the La Poste Open API portal (<https://developer.laposte.fr/>). The two
generated schema modules are inferred from the sample JSON kept under
`schemas/` (`tracking_response.json`, `error.json`).

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Data flow](#data-flow)
3. [Endpoints](#endpoints)
4. [Authentication](#authentication)
5. [Supported operations](#supported-operations)
6. [Services & static catalog](#services--static-catalog)
7. [Data mapping — tracking](#data-mapping--tracking)
8. [Status mapping](#status-mapping)
9. [Incident-reason mapping](#incident-reason-mapping)
10. [Error parsing](#error-parsing)
11. [Vendor quirks / invariants](#vendor-quirks--invariants)
12. [References](#references)

---

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio TrackingRequest / TrackingDetails
│   (karrio core)         │   (tracking is the only operation)
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  providers/laposte      │   Pure data transforms. No HTTP.
│   tracking.py           │   tracking_request: TrackingRequest →
│   error.py              │     list[str] of idShip numbers
│   units.py              │   parse_tracking_response: JSON →
│   utils.py              │     TrackingDetails + Message
│                         │   TrackingStatus / TrackingIncidentReason
│                         │   ShippingService (placeholder),
│                         │   ShippingOption (empty), DEFAULT_SERVICES
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  mappers/laposte/proxy  │   HTTP transport only.
│   get_tracking          │   - GET /idships/{ids}?lang=...
│                         │   - Header X-Okapi-Key: <api_key>
│                         │   - comma-joins tracking numbers in path
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  La Poste Suivi v2 API  │
│  api.laposte.fr/suivi/v2│   GET /idships/{idship,...}
└─────────────────────────┘
```

**Key architectural notes:**

- **Tracking-only connector.** `mapper.py` defines only
  `create_tracking_request` and `parse_tracking_response`. There is no
  `proxy` method beyond `get_tracking`, and no shipment / rate / pickup
  provider modules exist.
- **No transport-side batching split.** The proxy comma-joins every
  requested `idShip` into a single GET path
  (`/idships/{id1,id2,...}`). It does not chunk; the caller's tracking
  number list is sent as-is.
- **Static service catalog only.** `DEFAULT_SERVICES` is built from
  `services.csv` at import time and surfaced as `service_levels` in the
  plugin metadata for the rate-shopping picker. No service code is ever
  sent on the wire (there is no shipment surface).
- **Generated schemas** — `karrio/schemas/laposte/*.py` is generated
  from `schemas/*.json` (kcli infers types). Don't hand-edit;
  regenerate with `./bin/run-generate-on modules/connectors/laposte`.

## Data flow

### Tracking (one HTTP call)

```
TrackingRequest                              La Poste Suivi v2
     │                                              │
     │  create_tracking_request                     │
     ├─► tracking_request():                        │
     │     return payload.tracking_numbers          │
     │     (Serializable list[str])                 │
     │                                              │
     ├─► proxy.get_tracking:                        │
     │     idships = ",".join(numbers)              │
     │                                              │
     │   ─ GET /idships/{idships}?lang=fr_FR ──────►│
     │       X-Okapi-Key: <api_key>                 │  lookup
     │                                              │  per idShip
     │   ◄── [{ returnCode, shipment{...} }, ...] ──│
     │                                              │
     ├─► parse_tracking_response:                   │
     │     - normalize dict → list                  │
     │     - error.parse_error_response(all)        │
     │     - keep responses where                   │
     │       str(returnCode).startswith("20")       │
     │     - _extract_details per shipment:         │
     │         idShip → tracking_number             │
     │         event[0].code → status (first event) │
     │         event[] → TrackingEvent[]            │
     │         isFinal → delivered                  │
     │                                              │
     ▼                                              ▼
(list[TrackingDetails], list[Message])
```

The response is whatever La Poste returns: when multiple `idShip`
values are queried the API returns a JSON **array** of per-shipment
objects; a single lookup may return a bare object. `parse_tracking_response`
normalizes both via `responses = response if isinstance(response, list)
else [response]`.

## Endpoints

Single base URL for both test and prod (no separate sandbox host in the
connector): `https://api.laposte.fr/suivi/v2`.

| Purpose | Method | Path |
|---|---|---|
| Track parcels (1..N idShips) | GET | `/idships/{idship[,idship...]}?lang={lang}` |

`{lang}` is taken from `settings.lang` (default `fr_FR`).

## Authentication

API-key header auth. No OAuth, no token caching.

- Credential field: `Settings.api_key` (required).
- Sent on every request as the header **`X-Okapi-Key: <api_key>`**
  (La Poste's Okapi gateway key — the portal-issued application key).
- `accept: application/json` is also sent.

```
┌──────────────────────────────────────────┐
│ GET /suivi/v2/idships/EW112720413FR?lang= │
│ accept: application/json                   │
│ X-Okapi-Key: <api_key>                     │
└──────────────────────────────────────────┘
```

### Settings

| Field | Type | Default | Notes |
|---|---|---|---|
| `api_key` | str | — (required) | Okapi application key (`X-Okapi-Key`) |
| `lang` | `LangEnum` (`fr_FR`, `en_US`) | `fr_FR` | response language; appended as `?lang=` |
| `carrier_id` | str | `"laposte"` | |
| `account_country_code` | str | `"FR"` | |
| `test_mode` | bool | `False` | not used to switch hosts (single URL) |

`carrier_name` is fixed to `"laposte"`. `tracking_url` template is
`https://www.laposte.fr/outils/suivre-vos-envois?code={}`.

## Supported operations

| Operation | Wired? | Notes |
|---|---|---|
| Tracking | yes | `get_tracking` → Suivi v2 `/idships` |
| Rating | no | no `rate.py`; `ShippingOption` empty |
| Shipment create | no | no shipment provider module |
| Shipment cancel | no | — |
| Pickup | no | — |
| Document upload / manifest | no | — |

The plugin metadata (`karrio/plugins/laposte/__init__.py`) declares
`is_hub=False`, `status="production-ready"`, `id="laposte"`,
`label="La Poste"`, and exposes `services=ShippingService`,
`options=ShippingOption`, `service_levels=DEFAULT_SERVICES`.

## Services & static catalog

There is no per-account service catalog fetch and no shipment surface,
so services are not sent anywhere. They exist purely as a static
`service_levels` catalog for the picker.

`ShippingService` (`units.py`) has a single member:

| karrio service key | wire value |
|---|---|
| `laposte_standard_service` | `La Poste Standard Service` |

`PackagingType` collapses every unified packaging type
(`envelope`, `pak`, `tube`, `pallet`, `small_box`, `medium_box`,
`your_packaging`) onto a single `PACKAGE` code. (Unused on the wire —
there is no shipment request.)

`ShippingOption` is empty (no carrier options defined).

`DEFAULT_SERVICES` is loaded from
`karrio/providers/laposte/services.csv` by `load_services_from_csv()` at
import time. The CSV models the **Colissimo** product across three zones
with weight-banded `ServiceZone` rows:

| Zone | Countries | Weight bands (kg) | Transit (days) | Domicile | International |
|---|---|---|---|---|---|
| France | `FR` | 0.01–1, 1–3, 3–5, 5–10, 10–20, 20–30 | 2 | true | false |
| Europe | `DE,BE,NL,LU,ES,IT,PT,AT,CH,GB,PL,CZ,DK,SE` | same bands | 3–5 | false | true |
| Worldwide | (none → all) | same bands | 5–10 | false | true |

All rows: `max_length=100`, `max_width=60`, `max_height=60` cm,
`weight_unit=KG`, `dimension_unit=CM`, `currency=EUR`, `rate=0.0`
(placeholder — no real pricing). `transit_days` takes the lower bound of
ranges like `3-5`. Rows sharing a `service_code` are merged into one
`ServiceLevel`, accumulating their `ServiceZone` entries.

## Data mapping — tracking

### Request — `TrackingRequest` → wire

`tracking_request()` returns `payload.tracking_numbers` verbatim (a
`list[str]`). The proxy comma-joins them into the URL path.

### Response — `tracking_response.Shipment` → `TrackingDetails`

```
La Poste Shipment field            karrio TrackingDetails
───────────────────────            ──────────────────────
idShip            ───►             tracking_number
event[0].code     ───►             status   (see status mapping; first
                                            event drives the top-level status)
isFinal           ───►             delivered (bool)
deliveryDate      ───►             estimated_delivery (fdate)
event[]           ───►             events[] (see below)

info (TrackingInfo):
  url             ───►             carrier_tracking_link
  estimDate       ───►             expected_delivery
  product         ───►             shipment_service  (e.g. "colissimo")
  entryDate       ───►             shipping_date
  contextData.originCountry  ───►  shipment_origin_country
  contextData.arrivalCountry ───►  shipment_destination_country
```

### Event mapping — `Event` → `TrackingEvent`

```
Event field                        TrackingEvent
───────────                        ─────────────
date    ───►                       date       (fdate, %Y-%m-%dT%H:%M:%S%z)
date    ───►                       time       (flocaltime, same format)
date    ───►                       timestamp  (fiso_timestamp)
label   ───►                       description
code    ───►                       code
code    ───► via TrackingStatus    status
code    ───► via TrackingIncident… reason
(none)  ───►                       location   (always None)
```

Dates are parsed with the ISO-8601-with-offset format
`%Y-%m-%dT%H:%M:%S%z` (e.g. `2023-03-09T09:38:00+01:00`).

## Status mapping

`TrackingStatus` (`units.py`) maps La Poste event codes to unified
statuses. Both the top-level shipment status and each event's status are
resolved by matching `event.code` against these lists; the first match
wins, otherwise it falls back to `in_transit`.

| karrio status | La Poste codes |
|---|---|
| `delivered` | `DI1` |
| `out_for_delivery` | `MD2`, `ET1` |
| `in_transit` | `""` (empty — the fallback/default bucket) |

Notes:
- `in_transit` is the **default**. The top-level status falls back to
  `in_transit.name` when no code matches; event-level status falls back
  to `None`. (`in_transit`'s value list is `[""]`, so it only matches an
  empty code directly — its real role is the named default.)
- Codes seen in samples but not mapped to a status (`ET2`, `ET3`, `PC1`,
  `DR1`) resolve to no event status and contribute to the default
  shipment status.

## Incident-reason mapping

`TrackingIncidentReason` (`units.py`) maps exception codes to normalized
reasons, surfaced on `TrackingEvent.reason`. Only codes with non-empty
lists are reachable:

| karrio reason | La Poste codes |
|---|---|
| `carrier_address_not_found` | `AN1` |
| `consignee_refused` | `RE1` |
| `consignee_not_available` | `ND1`, `AG1` |
| `consignee_not_home` | `ND1` |
| `consignee_incorrect_address` | `AN1` |
| `customs_delay` | `DO1` |

All other reason buckets (`carrier_damaged_parcel`, `carrier_parcel_lost`,
`consignee_business_closed`, `weather_delay`, `unknown`, …) are present in
the enum but carry empty lists, so they never match. `ND1` and `AN1` each
appear under two reasons; `next()` returns the first enum member in
declaration order (`consignee_not_available` for `ND1`,
`carrier_address_not_found` for `AN1`).

## Error parsing

`error.parse_error_response` (`error.py`) is run over **all** response
objects. A response is treated as an error when either:

- `str(returnCode)` does **not** start with `"20"` (i.e. not a 2xx), or
- the object carries a top-level `code` field.

Each error object is coerced to the generated `error.Error` type and
emitted as a `models.Message`:

```
Error field                 Message field
───────────                 ─────────────
returnCode or code   ───►   code      (returnCode preferred)
returnMessage or message ─► message   (returnMessage preferred)
                            details = {**kwargs}
                            carrier_id / carrier_name from settings
```

The two error shapes the connector handles (from `schemas/error.json`):

1. **HTTP-level rejection** — `{returnCode: 400, returnMessage: "...",
   lang, scope, idShip}` (e.g. invalid tracking-number format). Mapped
   to `code=400`, `message=<returnMessage>`.
2. **Gateway / quota error** — `{..., code: "TOO_MANY_REQUESTS",
   message: "max quota reached (100 calls per 1s)"}`. The presence of
   `code` flags it as an error even if `returnCode` were 2xx.

Successful (`2xx`) tracking entries flow to `_extract_details`; error
entries flow to `Message`. Because the error filter and the success
filter run independently over the same list, a mixed multi-idShip
response yields both `TrackingDetails` and `Message` entries.

## Vendor quirks / invariants

- **Top-level status is driven by `event[0].code`** (the first/most
  recent event), not by `isFinal` or `timeline`. `delivered` is set
  separately from `shipment.isFinal`.
- **`returnCode` is the success gate.** Parsing keeps only responses
  where `str(returnCode).startswith("20")`. A `returnCode` like `204`
  would also pass this prefix check.
- **Single host, no sandbox switch.** `test_mode` does not change the
  base URL; the connector always hits `api.laposte.fr/suivi/v2`.
- **`X-Okapi-Key`, not Bearer.** La Poste's Okapi API gateway uses a
  static application key header — there is no token exchange.
- **`event.label` is the human description** and is returned in the
  language requested via `?lang=` (French by default; samples are in
  French).
- **`location` is always `None`** — the Suivi v2 event payload
  (`{code, label, date}`) carries no structured location; `country`
  fields live on `timeline[]`, which the parser does not read for
  events.
- **`timeline[]` is ignored by the parser.** Only `event[]`,
  `contextData`, and the scalar shipment fields are mapped.
- **kcli type inference.** `returnCode` is inferred as `int` (sample
  values `200` / `400`); `holder` as `int`; `isFinal` / `status` as
  `bool`. The connector compares `str(res.get("returnCode"))` to absorb
  either int or string.

## References

- **Vendor portal** — La Poste Open API portal,
  *Suivi* product: <https://developer.laposte.fr/>
- **Tracking URL template** (consumer-facing) —
  `https://www.laposte.fr/outils/suivre-vos-envois?code={idShip}`
- **Generated schemas** — `karrio/schemas/laposte/tracking_response.py`,
  `karrio/schemas/laposte/error.py`, inferred from
  `schemas/tracking_response.json` and `schemas/error.json`. Regenerate
  with `./bin/run-generate-on modules/connectors/laposte` (the connector
  `generate` script runs `error.json` then `tracking_response.json`
  through kcli with `--no-nice-property-names --no-append-type-suffix`).
  **Never hand-edit** the generated `.py` files.
- **Static service catalog source** —
  `karrio/providers/laposte/services.csv` (Colissimo zones/bands).
