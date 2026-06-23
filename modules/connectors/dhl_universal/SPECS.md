# DHL Universal Tracking integration — specification

Reference for the `dhl_universal` connector. It wraps DHL's
**Unified Shipment Tracking API** — a single JSON REST endpoint that
tracks parcels across DHL's many business units (Express, Parcel DE,
Parcel NL, eCommerce, Freight, …) by tracking number alone.

This connector is **tracking-only**. No rate, shipment create/cancel,
pickup, address-validation, or document operations are wired — only the
mapper's `create_tracking_request` / `parse_tracking_response` methods
are active; every other mapper method is commented out (see
`mappers/dhl_universal/mapper.py`).

Vendor source of truth: DHL Developer Portal —
<https://developer.dhl.com/api-reference/shipment-tracking>. The
connector's `pyproject.toml` declares it `production-ready`.

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio TrackingRequest
│   (karrio core)         │   (tracking_numbers[])
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  providers/dhl_universal│   Pure data transforms.
│   tracking.py           │   - tracking_request: numbers → typed
│   error.py              │     dhl.TrackingRequest[] (one per number)
│   units.py              │   - parse_tracking_response: dhl.Shipment
│   utils.py (Settings)   │     → TrackingDetails
│                         │   TrackingStatus enum.
│                         │   No HTTP, no side effects.
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ mappers/dhl_universal/  │   HTTP transport only.
│   proxy.py              │   - get_tracking: async fan-out, one
│   settings.py           │     GET per tracking number
│                         │   - DHL-API-Key header auth
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  DHL Unified Tracking   │
│  GET /track/shipments   │   api-eu.dhl.com
└─────────────────────────┘
```

**Key architectural choices:**

- **One HTTP call per tracking number.** The proxy does not batch.
  `tracking_request` builds a list of `dhl.TrackingRequest` objects
  (one per number); the proxy's `exec_async` fans them out into
  parallel `GET /track/shipments` calls and collects the raw dict
  responses into a list.
- **No OAuth.** Auth is a single static `DHL-API-Key` request header
  carrying `settings.consumer_key`. `consumer_secret` is stored on the
  connection but is **not sent** by the tracking proxy.
- **No dynamic catalog / no services / no options.** Tracking takes no
  service or option inputs; `units.py` contains only the
  `TrackingStatus` enum.
- **Generated schema** — `karrio/schemas/dhl_universal/tracking.py` is
  generated from `schemas/tracking.json` (kcli infers types). Don't
  hand-edit; regenerate with
  `./bin/run-generate-on modules/connectors/dhl_universal`.

## Data flow

### Tracking (one HTTP call per number, fanned out)

```
TrackingRequest                              DHL Unified Tracking
(tracking_numbers[])                                  │
     │                                                │
     ├─► create_tracking_request                      │
     │     for each number →                          │
     │       dhl.TrackingRequest{                      │
     │         trackingNumber, language:"en"}          │
     │     lib.to_dict (drops None fields)             │
     │                                                │
     ├─► proxy.get_tracking (exec_async fan-out):     │
     │     per request → urlencode query              │
     │                                                │
     │   ─── GET /track/shipments?language=en&        │
     │         trackingNumber=<n> ───────────────────►│
     │       header: DHL-API-Key: <consumer_key>      │
     │                                                │
     │   ◄── {shipments:[{...}]}  (success)  ─────────│
     │   ◄── {title,detail,status,instance} (error) ──│
     │                                                │
     ├─► parse_tracking_response:                     │
     │     split list: has "shipments" → detail,      │
     │                 else → error                    │
     │     _extract_detail(shipments[0])              │
     │                                                │
     ▼                                                ▼
(TrackingDetails[], Message[])              (one call per number done)
```

The proxy returns the raw list of per-number response dicts. The parser
partitions that list: entries containing a `shipments` key become
`TrackingDetails`; everything else is treated as an error envelope and
passed to `error.parse_error_response`. Only the **first** shipment of
each response (`d["shipments"][0]`) is used.

## Endpoints

Single server URL for all environments (no separate test/sandbox host;
`test_mode` does not switch the base URL).

| Purpose | Method | Path |
|---|---|---|
| Track shipments | GET | `https://api-eu.dhl.com/track/shipments?{query}` |

Query string is `urllib.parse.urlencode` of the serialized request — in
practice `language` + `trackingNumber` (other fields are `None` and
stripped by `lib.to_dict` before serialization).

`Settings.tracking_url` (the public, human-facing tracking page, used
only to populate `TrackingInfo.carrier_tracking_link`) is:

```
https://www.dhl.com/<country>-<language>/home/tracking/tracking-parcel.html?submit=1&tracking-id={id}
```

where `<country>` is `account_country_code` (default `DE`) and
`<language>` is the connection `language` (default `en`), lowercased
(e.g. `de-en`).

## Authentication

API-key scheme. Every tracking call carries:

```
Accept:      application/json
DHL-API-Key: <settings.consumer_key>
```

| Setting | Required | Sent on the wire | Notes |
|---|---|---|---|
| `consumer_key` | yes | yes — `DHL-API-Key` header | the DHL API key |
| `consumer_secret` | yes (settings field) | no | stored on the connection; the tracking proxy never transmits it |
| `language` | no (default `en`) | yes — in request body / query | enum: `en`, `de` (`utils.LanguageEnum`) |
| `account_country_code` | no (default `DE`) | no | used only to build the public `tracking_url` |

There is no token exchange, refresh, or caching.

## Supported operations

| Operation | Wired? | Notes |
|---|---|---|
| Tracking | yes | `GET /track/shipments`, one call per number |
| Rate | no | `create_rate_request` / `parse_rate_response` commented out |
| Shipment create | no | commented out in `mapper.py` |
| Shipment cancel | no | commented out |
| Pickup (schedule/update/cancel) | no | commented out |
| Address validation | no | commented out |
| Document upload / manifest | no | not present |

## Services & options

None. Tracking has no service or option enums. `units.py` defines only
`TrackingStatus` (see status mapping below).

## Data mapping

### Request — karrio `TrackingRequest` → `dhl.TrackingRequest`

```
karrio TrackingRequest                  dhl.TrackingRequest (wire)
──────────────────────                  ──────────────────────────
tracking_numbers[i]      ───►           trackingNumber          (one request per number)
(constant)               ───►           language: "en"          (hardcoded in tracking_request)
                                        service                 (not set — None, dropped)
                                        requesterCountryCode    (not set — None, dropped)
                                        originCountryCode       (not set — None, dropped)
                                        recipientPostalCode     (not set — None, dropped)
                                        offset / limit          (not set — None, dropped)
```

Note: `tracking_request(payload, _)` ignores the `settings` argument and
hardcodes `language="en"` on the request body regardless of the
connection's `language` setting. (The connection `language` still
influences the public `tracking_url`.)

### Response — `dhl.Shipment` → `TrackingDetails`

```
dhl.Shipment                                 TrackingDetails
────────────                                 ───────────────
id                          ───►             tracking_number (str(id))
status (mapped, see below)  ───►             status
estimatedTimeOfDelivery     ───►             estimated_delivery
events[i]                                    events[i]:
  timestamp                 ───►               date, time, timestamp
  description / status      ───►               description (fallback " ")
  location.address.addressLocality ─►          location
  statusCode                ───►               code (fallback "")
  statusCode / status (mapped) ──►             status
details.product.productName ───►             info.shipment_service
details.receiver            ───►             info.customer_name
                                               (givenName+familyName, else
                                                name, else organizationName)
destination.address.{countryCode,postalCode} ► info.shipment_destination_*
origin.address.{countryCode,postalCode}      ► info.shipment_origin_*
details.weight.{value,unitText}             ───► info.package_weight(_unit)
details.proofOfDelivery.signed              ───► info.signed_by
details.references.number                   ───► meta.reference
status == "delivered"                       ───► delivered (bool)
Settings.tracking_url.format(id)            ───► info.carrier_tracking_link
```

All `info.*` extractions are wrapped in `lib.failsafe(...)`, so a
missing nested object yields `None` rather than raising.

Event timestamps are normalized by `shorten_date` (split on `.` to drop
sub-second precision) and parsed with `try_formats`:
`%Y-%m-%d`, `%Y-%m-%dT%H:%M:%S`, `%Y-%m-%dT%H:%M:%SZ`,
`%Y-%m-%dT%H:%M:%S%z`.

## Status mapping

`provider_units.TrackingStatus` — DHL `statusCode` / `status` (lowercased)
matched against each enum's value list:

| karrio status | DHL value(s) matched |
|---|---|
| `delivered` | `delivered` |
| `in_transit` | `transit` |
| `delivery_failed` | `failure` |
| `delivery_delayed` | `unknown` |

**Shipment-level status resolution** (`_extract_detail`): the latest
status is taken as the first non-empty of
`shipment.status.statusCode` → `shipment.status.status` →
`shipment.events[0].statusCode`, lowercased. It is matched against the
enum **substring-style** (`latest_status in status.value`), and if no
enum matches it **defaults to `in_transit`**.

Quirk worth knowing: DHL's `statusCode` enum (`pre-transit`,
`transit`, `delivered`, `failure`, `unknown`) is checked *before*
`status`. A response whose `status` is e.g. `DELIVERED` but whose
`statusCode` is `pre-transit` resolves to **`in_transit`** (the default),
because `pre-transit` is not in any value list and `statusCode` takes
precedence over `status`. This is exactly what the connector's own test
fixture exercises (sample: `statusCode="pre-transit"`, `status="DELIVERED"`
→ shipment status `in_transit`).

**Event-level status resolution**: matched on
`event.statusCode` OR `event.status` (lowercased) against the same enum;
no default — unmatched events get `status=None`. (In the test fixture the
event resolves to `delivered` via `event.status="DELIVERED"`, even though
the parent shipment resolves to `in_transit`.)

## Error parsing

A response dict is treated as an error whenever it does **not** contain a
`shipments` key. Each such dict is parsed into the generated
`dhl.Error` shape and mapped to a `Message`:

```
DHL error envelope                     karrio Message
──────────────────                     ──────────────
status   ───►                          code (str)
detail   ───►                          message
title    ───►                          details.title
instance ───►                          details.instance
```

Example DHL error body (HTTP 404, no shipment found):

```json
{
  "title": "No result found",
  "detail": "No shipment with given tracking number found.",
  "status": 404,
  "instance": "/shipment/8264715546"
}
```

→

```
Message(code="404",
        message="No shipment with given tracking number found.",
        details={"title": "No result found",
                 "instance": "/shipment/8264715546"})
```

Because errors and successes are partitioned by the presence of the
`shipments` key, a batch of N tracking numbers can return a mix of
`TrackingDetails` and `Message` objects in a single
`parse_tracking_response` call.

## References

- **DHL Unified Shipment Tracking API** (vendor, authoritative) —
  <https://developer.dhl.com/api-reference/shipment-tracking>
- **Carrier site** — <https://www.dhl.com/>
- **Generated schema provenance** —
  `karrio/schemas/dhl_universal/tracking.py` is generated from
  `schemas/tracking.json` via the connector's `generate` script
  (`kcli codegen generate ... --no-nice-property-names
  --no-append-type-suffix`). Regenerate with
  `./bin/run-generate-on modules/connectors/dhl_universal` — never
  hand-edit the generated `.py`. The sample JSON in
  `schemas/tracking.json` is the source of truth for the type tree
  (request, response, error shapes).
```