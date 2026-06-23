# DHL Parcel Poland integration — specification

Reference for the DHL Parcel Poland (`dhl24.com.pl`) connector. DHL
Poland exposes a **SOAP/XML web service** (`webapi2`); the connector
speaks that protocol for shipment create / cancel / return and tracking,
and serves **rates from a static CSV catalog** via karrio's universal
rating mixin (no live rate API). The vendor source of truth is the
`webapi2` WSDL/XSD documented at
<https://dhl24.com.pl/en/webapi2/doc.html>; the connector's typed schema
is generated from `schemas/webapi2.xsd`.

Carrier id: `dhl_poland`. Display label: **DHL Parcel Poland**
(`karrio/plugins/dhl_poland/__init__.py`, status `production-ready`).

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio ShipmentRequest / RateRequest /
│   (karrio core)         │   ShipmentCancelRequest / TrackingRequest
└───────────┬─────────────┘
            │
            ▼
┌──────────────────────────────────────────────┐
│  providers/dhl_poland          Pure transforms │
│   shipment/create.py    unified → SOAP createShipment, response → ShipmentDetails
│   shipment/cancel.py    unified → deleteShipment
│   shipment/return_shipment.py  forces ROD option, delegates to create
│   tracking.py           getTrackAndTraceInfo per number
│   error.py              SOAP Fault → Message
│   units.py              Service, ShippingOption, PackagingType,
│                         PaymentType, LabelType, CustomsContentType,
│                         services.csv catalog loader
│   utils.py              Settings (server_url, auth_data, SOAP serialize)
└───────────┬────────────────────────────────────┘
            │                         ▲
            │                         │ rates handled by
            ▼                         │ karrio.universal rating mixin
┌─────────────────────────┐          │ (no DHL Poland rate API call)
│  mappers/dhl_poland      │   ┌──────┴───────────────────────┐
│   proxy.py    SOAP POST  │   │ universal.providers.rating   │
│   _send_request(soapaction)  │  reads Settings.shipping_services
│   - create_shipment      │   │  ← provider_units.DEFAULT_SERVICES
│   - cancel_shipment      │   │     (loaded from services.csv)    │
│   - create_return_shipment│  └──────────────────────────────┘
│   - get_tracking (async) │
│   mapper.py   create_rate_request → universal_provider.rate_request
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  DHL Poland webapi2      │   single SOAP endpoint, dispatched by
│  (SOAP 1.1 / XML)        │   the `soapaction` header per operation
└─────────────────────────┘
```

**Key architectural choices:**

- **SOAP, not JSON.** Every shipment/tracking call POSTs an XML SOAP
  envelope to one endpoint and selects the operation via the
  `soapaction` HTTP header. There is no REST surface.
- **Rates are catalog-only.** `Mapper.create_rate_request` delegates to
  `karrio.universal.providers.rating`. The connector does not call any
  DHL Poland rate endpoint — quotes are computed from the static
  `services.csv` catalog projected into `Settings.shipping_services`.
- **Tracking is multi-number async fan-out.** `Proxy.get_tracking`
  sends one `getTrackAndTraceInfo` SOAP call per tracking number via
  `lib.run_asynchronously`, keyed by tracking number.
- **Returns reuse create.** `return_shipment_request` forces the
  `dhl_poland_return_of_document` (ROD) option on and delegates to the
  standard `shipment_request`.
- **Generated schema** — `karrio/schemas/dhl_poland/services.py` is
  generated from `schemas/webapi2.xsd` via `generateDS`. Don't
  hand-edit; regenerate with
  `./bin/run-generate-on modules/connectors/dhl_poland`.

## Data flow

### Shipment create (one SOAP call)

```
ShipmentRequest                          DHL Poland webapi2
     │                                          │
     ├─► shipment_request()                     │
     │     lib.to_packages / to_address         │
     │     to_customs_info / to_shipping_options│
     │     map service → Service enum value     │
     │     map label_type → LabelType           │
     │     payment.paid_by → PaymentType        │
     │                                          │
     ├─► createShipment envelope (typed XSD)    │
     │     authData = username/password         │
     │                                          │
     ├─► settings.serialize(req, "createShipment", server_url)
     │     SOAP-env wrap; strip ns prefix off the operation element
     │                                          │
     │   ─── POST ?ws=1 ───────────────────────►│
     │       soapaction: <server_url>#createShipment
     │       Content-Type: text/xml; charset=utf-8
     │                                          │
     │   ◄── createShipmentResult{ ─────────────│
     │         shipmentNotificationNumber,      │
     │         shipmentTrackingNumber,          │
     │         label{labelContent, fvProformaContent}}
     │                                          │
     ├─► _extract_details:                      │
     │     shipmentNotificationNumber → tracking_number
     │     shipmentTrackingNumber    → shipment_identifier
     │     label.labelContent        → docs.label
     │     label.fvProformaContent   → docs.invoice
     │     meta.carrier_tracking_link = tracking_url.format(notif#)
     ▼                                          ▼
ShipmentDetails                          (no further call)
```

### Tracking (async fan-out, one SOAP call per number)

```
TrackingRequest                          DHL Poland webapi2
     │  tracking_numbers[]                      │
     ├─► tracking_request(): one getTrackAndTraceInfo
     │     envelope per number (body_prefix="") │
     │                                          │
     ├─► Proxy.get_tracking: lib.run_asynchronously
     │     per number → _send_request(soapaction=…#getTrackAndTraceInfo)
     │                                          │
     │   ─── POST (×N) ────────────────────────►│
     │   ◄── getTrackAndTraceInfoResult / Fault │
     │                                          │
     ├─► parse_tracking_response keyed by number:
     │     result with getTrackAndTraceInfoResult → TrackingDetails
     │     result with Fault                      → Message(tracking_number=n)
     ▼                                          ▼
list[TrackingDetails] + list[Message]
```

## Endpoints

All operations POST to a **single** SOAP service URL; the operation is
selected by the `soapaction` header.

| Mode | Service URL |
|---|---|
| Test (`test_mode=True`) | `https://sandbox.dhl24.com.pl/webapi2/provider/service.html?ws=1` |
| Production | `https://dhl24.com.pl/webapi2/provider/service.html?ws=1` |

| Purpose | Method | soapaction (`{server_url}#…`) |
|---|---|---|
| Create shipment | POST | `#createShipment` |
| Cancel shipment | POST | `#deleteShipment` |
| Create return shipment | POST | `#createShipment` (delegates to create) |
| Tracking (per number) | POST | `#getTrackAndTraceInfo` |
| Rates | — | no HTTP call (universal CSV catalog) |

`Content-Type: text/xml; charset=utf-8` on every request
(`mappers/dhl_poland/proxy.py`).

**Tracking link** (display only):
`https://www.dhl.com/pl-en/home/tracking/tracking-parcel.html?submit=1&tracking-id={notification_number}`.

## Authentication

Plain `username` / `password` carried in the SOAP body, not headers.
`Settings.auth_data` builds an `AuthData{username, password}` element
that is embedded as the `authData` argument of every operation
(`createShipment`, `deleteShipment`, `getTrackAndTraceInfo`). There is
no OAuth, no token caching.

Settings fields (`mappers/dhl_poland/settings.py`):

| Field | Required | Notes |
|---|---|---|
| `username` | yes | webapi2 login |
| `password` | yes | webapi2 password (marked sensitive) |
| `account_number` | no | default billing account; used when payment has none |
| `account_country_code` | no | default `"PL"` |
| `test_mode` | no | routes to the `sandbox.dhl24.com.pl` host |
| `services` | no | overrides the default CSV catalog for rating |

## SOAP serialization quirk

`Settings.serialize` (`utils.py`) wraps the typed body in a
`soap-env` envelope, then **strips the `soap-env:` namespace prefix off
the operation element itself** (e.g. rewrites `<soap-env:createShipment`
to `<createShipment` and the matching close tag). The operation element
must sit in the service's default namespace (`xmlns="{server_url}"`)
while the SOAP envelope keeps the `soap-env` prefix — webapi2 rejects a
prefixed operation element. `apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "")`
forces the body content into the default namespace before export.

## Supported operations

| Operation | Wired | Notes |
|---|---|---|
| Rate | yes | universal CSV catalog only (no live API) |
| Shipment create | yes | single SOAP call; returns label + optional proforma invoice |
| Shipment cancel | yes | `deleteShipment` by `shipment_identifier` |
| Return shipment | yes | forces ROD option, reuses create |
| Tracking | yes | async per-number fan-out |
| Pickup | no | not implemented |
| Manifest / document | no | not implemented |

## Services & options

### Services — `units.py:Service` (wire `serviceType`)

| karrio service code | Wire | CSV name |
|---|---|---|
| `dhl_poland_premium` | `PR` | DHL Premium (PL domestic) |
| `dhl_poland_polska` | `AH` | DHL Polska |
| `dhl_poland_09` | `09` | DHL 09 (PL domestic) |
| `dhl_poland_12` | `12` | DHL 12 (PL domestic) |
| `dhl_poland_connect` | `EK` | DHL Connect (Europe) |
| `dhl_poland_international` | `PI` | DHL International (Worldwide) |

**Service default** (`create.py`): if the caller doesn't pick a service,
`shipment_request` chooses `AH` (`dhl_poland_polska`) when shipper and
recipient countries differ (`is_international`), otherwise `09`
(`dhl_poland_09`).

The rating catalog (`services.csv`) carries weight/dimension bounds and
zones per service: `PR`/`09`/`12`/`AH` are domestic (`PL`,
`domicile=true`), `EK` is European (country list incl. `DE`, …),
`PI` is worldwide/international. All rates in the shipped CSV are `0.0`
PLN placeholders — the catalog drives *availability and limits*, not
real pricing.

### Options — `units.py:ShippingOption` (wire `serviceType` in `specialServices`)

| karrio option | Wire code | Type | Category |
|---|---|---|---|
| `dhl_poland_delivery_in_18_22_hours` | `1722` | bool | DELIVERY_OPTIONS |
| `dhl_poland_delivery_on_saturday` | `SATURDAY` | bool | DELIVERY_OPTIONS |
| `dhl_poland_pickup_on_staturday` | `NAD_SOBOTA` | bool | DELIVERY_OPTIONS |
| `dhl_poland_insuration` | `UBEZP` | float | INSURANCE |
| `dhl_poland_collect_on_delivery` | `COD` | float | COD |
| `dhl_poland_information_to_receiver` | `PDI` | — | NOTIFICATION |
| `dhl_poland_return_of_document` | `ROD` | bool | RETURN |
| `dhl_poland_proof_of_delivery` | `POD` | bool | DELIVERY_OPTIONS |
| `dhl_poland_delivery_to_neighbour` | `SAS` | bool | DELIVERY_OPTIONS |
| `dhl_poland_self_collect` | `ODB` | bool | PUDO |

**Unified-option aliases:**

| karrio standard option | DHL Poland option |
|---|---|
| `insurance` | `dhl_poland_insuration` (`UBEZP`) |
| `cash_on_delivery` | `dhl_poland_collect_on_delivery` (`COD`) |
| `saturday_delivery` | `dhl_poland_delivery_on_saturday` (`SATURDAY`) |

Each enabled option emits one `Service{serviceType=option.code,
serviceValue=lib.to_money(option.state)}` element inside
`shipmentInfo.specialServices` (`ArrayOfService`). The whole
`specialServices` block is omitted when no options are set. The wire
code is read from `option.code` (the first `OptionEnum` arg) — there is
no parallel option→code dict.

### Packaging — `units.py:PackagingType` (wire `Package.type_`)

| Wire | karrio packaging |
|---|---|
| `ENVELOPE` | `envelope` |
| `PACKAGE` | `pak`, `tube`, `small_box`, `medium_box`, `large_box`, `your_packaging` |
| `PALLET` | `pallet` |

Default when unspecified: `your_packaging` → `PACKAGE`.

### Label type — `units.py:LabelType` (wire `labelType`)

| Wire | Meaning | karrio alias |
|---|---|---|
| `BLP` | BLP label | `PDF` |
| `LBLP` | A4 PDF label | — |
| `ZBLP` | ZPL label | `ZPL` |

Default: `PDF` → `BLP` when `payload.label_type` is unset.

### Payment — `units.py:PaymentType` (wire `billing.shippingPaymentType`)

| Wire | karrio `paid_by` |
|---|---|
| `SHIPPER` | `sender` |
| `RECEIVER` | `recipient` |
| `USER` | `third_party` |

`billing.paymentType` is hardcoded `"BANK_TRANSFER"`;
`billingAccountNumber` is `payment.account_number` falling back to
`settings.account_number`.

## Data mapping

### Address — karrio `Address` → webapi2 `Address` / `ReceiverAddress`

```
karrio Address                      webapi2 Address / ReceiverAddress
─────────────────                   ─────────────────────────────────
company_name (or person_name)  ───► name
address_line1                  ───► street
street_number (or "N/A")       ───► houseNumber
address_line2                  ───► apartmentNumber
postal_code (dashes stripped)  ───► postalCode      (e.g. 00-001 → 00001)
city                           ───► city
country_code                   ───► country         (receiver only)
residential → "C", else "B"    ───► addressType     (receiver only)
```

Contact / pre-advice: when any of person_name / phone / email is
present, both `preaviso` and `contact` are populated with a
`PreavisoContact{personName, phoneNumber, emailAddress}` (same values
to both). `ReceiverAddress` Packstation/Postfiliale fields
(`isPackstation`, `isPostfiliale`, `postnummer`) are sent as `None`.

> Quirk in `create.py`: the **receiver** `houseNumber` is currently
> populated from `shipper.street_number` (not `recipient.street_number`).
> Documented here as the actual code behaviour.

### Shipment-level fields (`shipmentInfo`)

| webapi2 field | Value |
|---|---|
| `dropOffType` | `"REGULAR_PICKUP"` (constant) |
| `serviceType` | mapped `Service` value (see default rule above) |
| `wayBill` | `None` |
| `shipmentTime.shipmentDate` | `options.shipment_date` or today (`%Y-%m-%d`) |
| `shipmentTime.shipmentStartHour` / `shipmentEndHour` | both `"10:00"` (constant) |
| `content` | `parcels[0].content` or `"N/A"` |
| `reference` | `payload.reference` |

### Parcel — `Package` (per parcel, in `pieceList`/`ArrayOfPackage`)

| webapi2 field | Source |
|---|---|
| `type_` | `PackagingType[packaging_type or "your_packaging"]` |
| `weight` | `package.weight.KG` |
| `width` / `height` / `length` | `package.{width,height,length}.CM` |
| `quantity` | `len(customs.commodities)` if customs defined, else `1` |

### Customs — `CustomsInfo` → `CustomsData` (only when `customs.is_defined`)

| webapi2 field | Source |
|---|---|
| `customsType` | `"S"` (constant) |
| `firstName` | `customs.duty.bil_to.company_name` (fallback `shipper.company_name`, then `"N/A"`) |
| `secondaryName` | `customs.duty.bil_to.person_name` (fallback `shipper.person_name`, then `"N/A"`) |
| `costsOfShipment` | `customs.duty.declared_value` or `options.declard_value` |
| `currency` | `customs.duty.currency` or `options.currency` |
| `nipNr` | `customs.options.nip_number` |
| `eoriNr` | `customs.options.eori_number` |
| `vatRegistrationNumber` | `customs.options.vat_registration_number` |
| `categoryOfItem` | `CustomsContentType[content_type or "other"]` |
| `invoiceNr` | `customs.invoice` |
| `invoiceDate` | `customs.invoice_date` |
| `countryOfOrigin` | `shipper.country_code` |
| `grossWeight` | `packages.weight.KG` |
| `customsItem[i]` | per-commodity `CustomsItemData` (below) |
| `customAgreements` | `{notExceedValue, notProhibitedGoods, notRestrictedGoods}` all `True` |

Per-commodity `CustomsItemData`:

| webapi2 field | Source |
|---|---|
| `nameEn` / `namePl` | `item.title` or `item.description` or `"N/A"`, truncated to 35 chars |
| `quantity` | `item.quantity` |
| `weight` | `item.weight` converted to KG |
| `value` | `item.value_amount` |
| `tariffCode` | `item.hs_code` or `item.sku` |

### Customs content type — `units.py:CustomsContentType` (wire `categoryOfItem`)

| Wire | Meaning | karrio `content_type` |
|---|---|---|
| `9` | other | `other` (default) |
| `11` | sale of goods | `merchandise` |
| `21` | return of goods | `return_merchandise` |
| `31` | gifts | `gift` |
| `32` | samples of goods | `sample` |
| `91` | documents | `documents` |

## Identifiers (two-tier)

Shipment create returns two distinct numbers:

```
createShipmentResult
  ├─ shipmentNotificationNumber ─► tracking_number      (customer-facing, on label)
  │                                meta.carrier_tracking_link
  └─ shipmentTrackingNumber     ─► shipment_identifier  (handle for deleteShipment)
```

`deleteShipment` (cancel) keys on `shipmentIdentificationNumber` =
karrio `shipment_identifier`.

## Tracking response mapping

`getTrackAndTraceInfoResult` → `TrackAndTraceResponse`; events are the
repeated `item` elements parsed to `TrackAndTraceEvent`.

```
TrackAndTraceResponse                   TrackingDetails
─────────────────────                   ───────────────
shipmentId             ─────────►       tracking_number
receivedBy (truthy)    ─────────►       delivered
item[i] (TrackAndTraceEvent):
  timestamp            ─────────►       event.date / time / timestamp
                                          (parsed "%Y-%m-%d %H:%M:%S")
  description          ─────────►       event.description
  terminal             ─────────►       event.location
  status               ─────────►       event.code
```

There is **no `TrackingStatus` enum** — the connector does not map
DHL Poland event codes onto karrio's canonical status set. `delivered`
is derived solely from whether `receivedBy` is non-empty; raw `status`
is passed through as the event `code`.

## Return shipments

`return_shipment_request` (`shipment/return_shipment.py`) takes the
inbound `ShipmentRequest`, merges `dhl_poland_return_of_document: True`
(ROD) into its options, and calls the standard `create.shipment_request`.
The response is parsed by the same `parse_shipment_response`. Returns
therefore travel as ordinary `createShipment` calls with the ROD service
flag — there is no dedicated return endpoint.

## Error parsing

DHL Poland reports failures as SOAP `Fault` elements. `error.py` finds
every `Fault` (via `XP.find("Fault", …, pysoap.envelope.Fault)`) and
maps each to a karrio `Message`:

```
SOAP Fault                         Message
──────────                         ───────
faultstring   ─────────►           message
faultcode     ─────────►           code
(details kwarg)─────────►          details   (tracking_number on track calls)
```

- **Shipment create**: a `createShipmentResult` element present means
  success; otherwise the Faults become the returned messages.
- **Cancel**: success is `len(errors) == 0`; a `ConfirmationDetails`
  (operation `"Cancel Shipment"`) is only returned when there are no
  Faults.
- **Tracking**: per number, a node carrying `Fault` yields a `Message`
  stamped with that `tracking_number`; nodes carrying
  `getTrackAndTraceInfoResult` yield `TrackingDetails`.

## References

- **Vendor docs** — webapi2 documentation:
  <https://dhl24.com.pl/en/webapi2/doc.html> (website
  <https://dhl24.com.pl/en>).
- **Schema source of truth** — `schemas/webapi2.xsd`. The typed Python
  module `karrio/schemas/dhl_poland/services.py` is generated from it
  with `generateDS` (see the `generate` script). Never hand-edit the
  generated module; regenerate with
  `./bin/run-generate-on modules/connectors/dhl_poland`.
- **Rating catalog** — `karrio/providers/dhl_poland/services.csv`
  (loaded by `units.load_services_from_csv` into `DEFAULT_SERVICES`).
  Adjust service availability, weight/dimension bounds, zones, and
  country lists there; rates currently ship as `0.0` PLN placeholders.
- **Tests** — `tests/dhl_poland/` (`test_rate.py`, `test_shipment.py`,
  `test_tracking.py`). Run with
  `python -m unittest discover -v -f modules/connectors/dhl_poland/tests`.
