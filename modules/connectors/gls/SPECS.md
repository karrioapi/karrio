# GLS integration — specification

Reference for the GLS connector. Documents the vendor's
ShipIT / Customs / T&T / Document Management API contract, the
unified-model conventions on top of it, and the design decisions that
shaped the integration.

The **vendor source of truth** is the GLS ShipIT doxygen REST docs at
<https://shipit.gls-group.eu/webservices/5_0_11/doxygen/WS-REST-API/>.
Five reference request samples kept verbatim under
`vendor/gls-validated-samples/` are the ground truth the connector's
output is matched against. Avoid the Developer-Portal YAML files —
they contain fields (`PartnerReference`, `Volume`, PascalCase service
names like `SaturdayService`) that the live API rejects.

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Data flow](#data-flow)
3. [Endpoints](#endpoints)
4. [Authentication](#authentication)
5. [Wire-shape invariants](#wire-shape-invariants)
6. [Identifiers (two-tier)](#identifiers-two-tier)
7. [Services taxonomy](#services-taxonomy)
8. [Data mapping](#data-mapping)
9. [Country routing + IncotermCode](#country-routing--incotermcode)
10. [Customs Consignment v3 (second call)](#customs-consignment-v3-second-call)
11. [Document Management — paperless trade](#document-management--paperless-trade)
12. [Tracking](#tracking)
13. [Error parsing](#error-parsing)
14. [Per-shipment routing override](#per-shipment-routing-override)
15. [References](#references)

---

## Architecture overview

```
┌─────────────────────────┐
│  Unified shipping model │   karrio ShipmentRequest / CustomsInfo /
│   (karrio core)         │   PickupRequest / TrackingRequest
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  providers/gls          │   Pure data transforms.
│   shipment/create.py    │   Unified model → typed GLS request,
│   shipment/cancel.py    │   typed GLS response → unified model.
│   pickup/create.py      │   No HTTP, no side effects.
│   tracking.py           │
│   document.py           │
│   error.py              │
│   units.py              │   ShippingService, ShippingOption,
│                         │   TrackingStatus, Incoterm, ...
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  mappers/gls/proxy.py   │   HTTP transport only.
│   - create_shipment     │   - OAuth token caching
│   - cancel_shipment     │   - Headers: glsVersion1+json
│   - schedule_pickup     │   - Customs-consignment chaining
│   - get_tracking        │   - Document upload (prepare + PUT)
│   - upload_document     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  GLS APIs               │
│  ─────────────────────  │
│  ShipIT Farm v1         │   create / cancel / sporadic collection
│  Track & Trace v1       │   parcel events + status
│  Customs Mgmt v3        │   customs consignments
│  Document Mgmt v1       │   paperless trade upload
│  OAuth2 v2              │   client_credentials token
└─────────────────────────┘
```

**Key architectural choices:**

- **Single-call shipment creation** for domestic / EU lanes;
  **two-call flow** for customs destinations (label POST, then
  Customs Consignment v3 POST keyed by the parcel numbers returned
  on the first response).
- **OAuth2 `client_credentials`** with a per-connection cached
  access token (refreshed 30 minutes before expiry).
- **No dynamic catalog** — ShipIT does not expose a per-account
  product/service catalog; service availability is gated by
  per-account entitlements GLS enables server-side. The static
  catalog in `units.py` is the union of doxygen-defined services.
- **Generated schemas** — `karrio/schemas/gls/*.py` is generated from
  `schemas/*.json` (kcli infers types). Don't hand-edit; regenerate
  with `./bin/run-generate-on modules/connectors/gls`.

## Data flow

### Domestic / EU shipment (one HTTP call)

```
ShipmentRequest                      GLS ShipIT Farm
     │                                       │
     │  create_shipment_request              │
     ├─────► to_address()                    │
     │       to_packages()                   │
     │       to_shipping_options()           │
     │       map service → Product           │
     │                                       │
     ├─► ShipmentRequestType (typed)         │
     │                                       │
     ├─► lib.to_dict → JSON                  │
     │                                       │
     │   ─── POST /rs/shipments ────────────►│
     │                                       │  validate
     │                                       │  label gen
     │   ◄── CreatedShipment{                │  routing
     │         ParcelData[], PrintData[]} ───│
     │                                       │
     ├─► _extract_details:                   │
     │       ParcelNumber → tracking_number  │
     │       TrackID → shipment_identifier   │
     │       PrintData[].Data → docs.label   │
     │                                       │
     ▼                                       ▼
ShipmentDetails                       (no further call)
```

### International / customs shipment (two HTTP calls)

```
ShipmentRequest                                              GLS APIs
     │                                                         │
     ├─► create_shipment_request                               │
     │     - typed ShipmentRequestType                         │
     │     - typed CustomsConsignmentRequestType (in ctx)      │
     │                                                         │
     │   ─── POST /shipit-farm/.../rs/shipments ──────────────►│
     │                                                         │
     │   ◄── CreatedShipment{ ParcelData[].ParcelNumber } ─────│
     │                                                         │
     ├─► utils.post_customs_consignment:                       │
     │     stamp parcelNumbers from response                   │
     │                                                         │
     │   ─── POST /customs-mgmt/.../customs-consignments ─────►│
     │                                                         │
     │   ◄── customs accepted ─────────────────────────────────│
     │                                                         │
     ▼                                                         ▼
ShipmentDetails                                          (both calls done)
```

If the label POST returns an error, the proxy skips the customs call
rather than firing it with an empty `parcelNumbers` array (which the
customs API rejects).

### Paperless trade document upload (two HTTP calls per document)

```
DocumentUploadRequest                              GLS Document Mgmt
        │                                                  │
        ├─► document_upload_request                        │
        │     - envelope JSON per DocumentFile             │
        │                                                  │
        │   ─── POST /documents/customs/prepare-upload ──►│
        │                                                  │
        │   ◄── { documentId, uploadURL (15 min) } ────────│
        │                                                  │
        ├─► PUT binary body to uploadURL                   │
        │     - no auth header (URL carries credentials)   │
        │     - Content-Type: application/pdf or octet     │
        │                                                  │
        │   ─── PUT {uploadURL} ──────────────────────────►│
        │   ◄── 200 OK ───────────────────────────────────│
        │                                                  │
        ▼                                                  ▼
list[DocumentDetails]                          documentId in linkedDocuments
                                               of the customs consignment
```

**`upload_document` orchestration (`flow="post_upload"`).** The proxy method is
the carrier-side landing for post-create paperless trade and runs the chain
end-to-end:

1. For each `DocumentFile`: prepare-upload + S3 PUT (`utils.upload_one_document`).
2. One Customs Consignment v3 POST (`utils.post_customs_consignment`) stamping
   `parcelNumbers` (the ShipIT `TrackID` from `ctx.tracking_number`) and
   `linkedDocuments` (the `documentId`s from the prepare-upload responses).

Steps in (1) always fire; the customs POST fires only when the upload request
carries a customs payload in `ctx` (see `document.document_upload_request`). The
customs response — success body **or** parsed error envelope — is appended to the
returned list so the parser can surface a customs rejection as a message;
without it a failed customs submission would look like a clean upload (document
uploaded, customs silently failed). Every wire call groups under the same
`request_log_id`, and the flow produces a `DocumentUploadRecord` linked to the
shipment.

## Endpoints

Test mode: `api-sandbox.gls-group.net`. Prod: `api.gls-group.net`.

| Purpose | Method | Path |
|---|---|---|
| OAuth token | POST | `/oauth2/v2/token` |
| Create shipment | POST | `/shipit-farm/v1/backend/rs/shipments` |
| Cancel shipment | POST | `/shipit-farm/v1/backend/rs/shipments/cancel/{trackID}` |
| Sporadic collection (pickup) | POST | `/shipit-farm/v1/backend/rs/sporadiccollection` |
| ParcelShop — by ID | GET | `/shipit-farm/v1/backend/rs/parcelshop/{ParcelShopID}` |
| ParcelShop — by country | GET | `/shipit-farm/v1/backend/rs/parcelshop/country/{countryCode}` |
| ParcelShop — by address | POST | `/shipit-farm/v1/backend/rs/parcelshop/address` |
| ParcelShop — by distance | POST | `/shipit-farm/v1/backend/rs/parcelshop/distance` |
| Customs consignment v3 | POST | `/customs-management/export/public/v3/customs-consignments` |
| Document mgmt — prepare upload | POST | `/document-management/v1/documents/customs/prepare-upload` |
| Document mgmt — binary upload | PUT | pre-signed `uploadURL` from prepare-upload (no auth header; 15 min) |
| Track & Trace (batch ≤ 10) | GET | `/track-and-trace-v1/tracking/simple/trackids/{ids,comma-joined}` |

**Content type** for ShipIT JSON is `application/glsVersion1+json`
(distinct from the generic `application/json` used by the customs /
document management / tracking APIs).

## Authentication

OAuth2 `client_credentials` grant with HTTP Basic Auth header
(`base64(client_id:client_secret)`). Access tokens are cached per
`gls|<client_id>|<client_secret>` key and refreshed when their expiry
is within 30 minutes. Every shipping / customs / tracking / pickup /
document call carries `Authorization: Bearer <access_token>`.

```
client_credentials                       ┌──────────────┐
       │                                 │ Token Cache  │
       ▼                                 │  (per conn)  │
┌──────────────┐    miss / expired       │              │
│ access_token │◄────────────────────────│ key:         │
│  property    │                         │  gls|<cid>|  │
│              │    cache hit            │  <secret>    │
│              │────────────────────────►│              │
└──────┬───────┘                         └──────────────┘
       │
       ▼  POST /oauth2/v2/token
   ┌───────────────────────────────────────┐
   │ Authorization: Basic b64(cid:secret)  │
   │ Content-Type: application/x-www-…     │
   │ Body: grant_type=client_credentials   │
   └───────────────────────────────────────┘
```

## Wire-shape invariants

- **`Shipment.Middleware`** is mandatory. The connector ships with
  the constant `provider_units.MIDDLEWARE = "JTLviaGLS"` for the JTL
  integration; downstream forks should replace this constant with
  their integration-partner string before deploying. GLS uses the
  value for billing attribution.
- **`PartnerReference` does not exist** in ShipIT and is rejected
  by the live API. The connector emits no such field.
- **`Volume` section does not exist** in ShipIT — shipments are
  weight-only on the wire. No `Volume{H,W,L}` block is sent.
- **`Shipment.Identifier`** is optional. GLS prints it in their logs
  as the source-software marker. Configured per connection via the
  `app_identifier` config or globally via the `GLS_APP_IDENTIFIER`
  env var. Not used for billing.
- **`Shipper.ContactID`** is mandatory. GLS resolves the registered
  shipper from this ID. A divergent sender must go under
  `AlternativeShipperAddress` — populating `Shipper.Address` directly
  is rejected with `REAL_SHIPPER_NOT_ALLOWED` unless the account is
  specially enabled by GLS.
- **Address email field is `eMail`** (lowercase leading `e`). It is
  emitted on every `Shipper.AlternativeShipperAddress` and
  `Consignee.Address`. ShopDelivery / FlexDelivery + AddonLiability
  surface `CONSIGNEE_ADDRESS_EMAIL_MANDATORY` / "not available for the
  shipper" if it is missing, so the field is always sent.
- **`Shipment.Service[]` flag combinations are contract-gated.**
  Sandbox transcripts show: SaturdayService cannot ride alongside
  FlexDelivery / Signature / AddresseeOnly; time-definite slots
  (`service_0800..1300`) require **Product=EXPRESS**; FlexDelivery
  must not combine with SignatureService on PARCEL. Validate every
  combo with `validateParcels` before shipping; per-tenant
  entitlements gate the rest.

## Identifiers (two-tier)

Shipment creation responses return two distinct identifiers per
parcel:

```
CreatedShipment.ParcelData[i]
  │
  ├─ ParcelNumber  ───►  tracking_number  (customer-facing, on label)
  │                       meta.tracking_numbers[]
  │
  └─ TrackID       ───►  shipment_identifier  (internal GLS handle)
                          meta.track_ids[]
```

`TrackID` is what `POST /rs/shipments/cancel/{trackID}` expects;
`ParcelNumber` is what the Customs Consignment v3 call binds to via
`parcelNumbers`.

## Services taxonomy

GLS encodes services as `service_*` codes. **Case matters** — the
doxygen mixes lowercase and (for the bare Saturday flag) capital
`service_Saturday`. The previous PascalCase forms
(`SaturdayService`, `FlexDeliveryService`, …) are response-side
`ServiceArea.Header` labels and are not valid request values.

The wire shape splits services into four buckets matching the doxygen
`rest_shipment_processing.html` service-attribute tables.

```
ShipmentRequestType
├── Shipment
│   ├── Service: []      ◄─── bucket 1: flag (w/o attrs) services
│   │                          bucket 2: time-definite slot (flag)
│   │                          bucket 3: attribute-bearing services
│   └── ShipmentUnit: []
│        └── Service: [] ◄─── bucket 4: per-unit attribute services
```

### 1. Generic flag services on `Shipment.Service[]`

Each rides as `{"Service": {"ServiceName": "service_*"}}`. No extra
attributes. Driven from `provider_units.SHIPMENT_FLAG_OPTIONS`:

| Option | Wire `ServiceName` |
|---|---|
| `gls_saturday_delivery` | `service_Saturday` |
| `gls_flex_delivery` | `service_flexdelivery` |
| `gls_addressee_only` | `service_addresseeonly` |
| `gls_signature_service` | `service_signature` |
| `gls_guaranteed24` | `service_guaranteed24` |
| `gls_t24` | `service_t24` |
| `gls_t48` | `service_t48` |
| `gls_tyre` | `service_tyre` |
| `gls_private_delivery` | `service_privatedelivery` |
| `gls_inbound_logistics` | `service_inbound` |
| `gls_document_return` | `service_documentreturn` |
| `gls_complete_delivery_consignment` | `service_completedeliveryconsignment` |

### 2. Time-definite slot — flag service with slot-encoded name

Same `{"Service": {"ServiceName": …}}` wrapper, but the slot is baked
into the ServiceName itself. Allowed values:

`service_0800` · `service_0900` · `service_1000` · `service_1200`
· `service_1300` · `service_saturday_0900` · `service_saturday_1000`
· `service_saturday_1200`.

Driven by `gls_time_definite_service`. A bool `True` or an
unrecognised string falls back to `service_1200`. Per the doxygen
service-attribute table the time-definite services are marked
`Parcel²/Express` — `EXPRESS` is the typical Product for these slots.

### 3. Attribute-bearing services on `Shipment.Service[]`

Each rides under its own wrapper key, carrying both `ServiceName`
and additional fields per doxygen table 9:

| Wrapper key | Gate option | Attribute fields | Constraints |
|---|---|---|---|
| `Deposit` | `gls_deposit_service` | `PlaceOfDeposit` (mandatory) | max 60 chars; Letterbox variant max 121 |
| `ShopDelivery` | `gls_shop_delivery` | `ParcelShopID` (mandatory) | format `{partnerID}-{localID}`, max 50 |
| `IdentPin` | `gls_ident_pin_service` | `PIN` (mandatory) + `Birthdate` (opt.) | PIN 4-digit alphanumeric; Birthdate `YYYY-MM-DD`, < today |
| `Ident` | `gls_ident_service` | `Birthdate`, `Firstname`, `Lastname`, `Nationality.CountryCode` (all mandatory) | Names max 40; CountryCode ISO 2-letter |
| `DeliveryAtWork` | `gls_delivery_at_work_service` | `RecipientName`, `Building`, `Floor` (mandatory); `AlternateRecipientName`, `Room`, `Phonenumber` (opt.) | Names max 40; defaults: RecipientName ← recipient.person_name, Phonenumber ← recipient.phone_number |
| `Intercompany` | `gls_intercompany_service` | `Address`, `NumberOfLabels` (mandatory); `ExpectedWeight` (opt.) | Address from `payload.return_address`; NumberOfLabels default 1; ExpectedWeight kg > 0 |
| `Exchange` | `gls_exchange_service` | `Address` (mandatory); `ExpectedWeight` (opt.) | Address from `payload.return_address` |
| `PickAndShip` | `gls_pick_and_ship` | `PickupDate` (mandatory) | YYYY-MM-DD, > today; sourced from `shipping_date` |
| `PickAndReturn` | `gls_pick_and_return` | `PickupDate` (mandatory) | YYYY-MM-DD, > today; sourced from `shipping_date` |
| `ShopReturn` | `gls_shop_return` *or* `gls_return_enabled` | `NumberOfLabels` (mandatory, fixed `1`); `ReturnQR` (opt.) | ReturnQR ∈ {PDF, PNG, ZPL} |

**Mutual-exclusion rule**: if both `gls_pick_and_return` and
`gls_shop_return` are set, `PickAndReturn` wins so we never ship a
confused `Service[]` with both wrappers. `gls_return_enabled` is the
unified "return label" flag that maps onto `ShopReturn`.

**Generated-type collapses** (kcli structurally-collapsed):
- `PickAndShip` and `PickAndReturn` use the same `PickAndType`
  (identical `{ServiceName, PickupDate}` shape).
- `Intercompany` and `Exchange` use the same `ExchangeType`.

### 4. Per-ShipmentUnit attribute services

These ride per-unit, not at shipment level, on
`ShipmentUnit[i].Service[]`:

| Wrapper key | Gate option | Attribute fields | Constraints |
|---|---|---|---|
| `AddonLiability` | `insurance` (standard option) | `Amount`, `Currency` (mandatory); `ParcelContent` (opt.) | Amount > 0; Currency ISO 4217; ParcelContent max 255 |
| `Cash` | `gls_cash_service` | `Reason`, `Amount`, `Currency` (all mandatory) | Reason max 160; Amount sourced from `cash_on_delivery` standard option; Currency ISO 4217 |
| `HazardousGoods` | `gls_hazardous_goods_service` | `HazardousGood[i].GLSHazNo`, `HazardousGood[i].Weight` (mandatory) | GLSHazNo max 8 alphanumeric; Weight kg > 0, max 2 decimals |
| `ExWorks` | `gls_ex_works_service` | — (bare wrapper) | — |
| `LimitedQuantities` | `gls_limited_quantity` | `Weight` (opt.) | kg > 0, max 2 decimals; portion of parcel gross weight ≤ LQ-class limit |

**Generated-type collapse**: `Cash` and `AddonLiability` use the
same `AddonLiabilityType` (both share `{ServiceName, Amount,
Currency}` plus optional fields).

`AddonLiability` is gated by the standard karrio `insurance` option
(not a `gls_*` option), so its `ServiceName` is the literal
`"service_addonliability"` rather than `option.code`.

### Not a service — wire `Product`

ShipIT `Shipment.Product` is one of `PARCEL` or `EXPRESS`. The actual
delivery network is selected from the recipient address. There is no
`service_premium`, `service_express`, etc. — these are Product-level
concerns, not service-level.

## Data mapping

### Address — karrio `Address` → ShipIT `AddressType`

```
karrio Address                          ShipIT AddressType
─────────────────                       ──────────────────
company_name           ───►             Name1 (or person_name if no company)
person_name            ───►             Name2 (when Name1 is the company)
                                        ContactPerson
address_line1          ───►             Street
address_line2          ───►             StreetNumber
postal_code            ───►             ZIPCode
city                   ───►             City
state_code             ───►             (not used by ShipIT)
country_code           ───►             CountryCode
phone_number           ───►             FixedLinePhonenumber
email                  ───►             (intentionally dropped — API rejects)
```

### Shipper — `Shipper.ContactID` + optional `AlternativeShipperAddress`

```
Shipper {
    ContactID:                     ◄─── settings.contact_id (or per-shipment override)
    AlternativeShipperAddress {    ◄─── lib.to_address(payload.shipper)
        Name1, Name2, ...
    }
    // NOTE: Address is intentionally NOT populated — REAL_SHIPPER_NOT_ALLOWED
}
```

### Shipment-level services aggregation

```
ShippingOption gates                            Shipment.Service[]
────────────────────                            ──────────────────
gls_saturday_delivery     ┐
gls_flex_delivery         │ (12 flag options)
gls_addressee_only        ├─► [{Service: {ServiceName: option.code}}, ...]
gls_signature_service     │      iterated via SHIPMENT_FLAG_OPTIONS
... + 8 more flag options ┘

gls_time_definite_service ───► [{Service: {ServiceName: <slot-encoded>}}]
                                  resolved by time_definite_service_name()

gls_deposit_service       ───► [{Deposit: {ServiceName, PlaceOfDeposit}}]
gls_shop_delivery         ───► [{ShopDelivery: {ServiceName, ParcelShopID}}]
gls_ident_pin_service     ───► [{IdentPin: {ServiceName, PIN, Birthdate}}]
gls_ident_service         ───► [{Ident: {ServiceName, Birthdate, Firstname, Lastname, Nationality.CountryCode}}]
gls_delivery_at_work_*    ───► [{DeliveryAtWork: {...}}]
gls_intercompany_*        ───► [{Intercompany: {ServiceName, Address, NumberOfLabels, ExpectedWeight}}]
gls_exchange_*            ───► [{Exchange: {ServiceName, Address, ExpectedWeight}}]
gls_pick_and_ship         ───► [{PickAndShip: {ServiceName, PickupDate}}]
gls_pick_and_return       ───► [{PickAndReturn: {ServiceName, PickupDate}}]
gls_shop_return /         ───► [{ShopReturn: {ServiceName, NumberOfLabels=1}}]
  gls_return_enabled            (only one of the return wrappers — PickAndReturn wins)
```

### Per-ShipmentUnit services aggregation (per parcel)

```
ShippingOption gates                       ShipmentUnit[i].Service[]
────────────────────                       ─────────────────────────
insurance (standard option) ───► [{AddonLiability: {ServiceName="service_addonliability",
                                                    Amount, Currency}}]
gls_cash_service +
  cash_on_delivery +
  gls_cash_reason           ───► [{Cash: {ServiceName, Reason, Amount, Currency}}]

gls_hazardous_goods_*       ───► [{HazardousGoods: {ServiceName,
                                     HazardousGood: [{GLSHazNo, Weight}]}}]

gls_ex_works_service        ───► [{ExWorks: {ServiceName}}]

gls_limited_quantity +
  gls_limited_quantity_weight ─► [{LimitedQuantities: {ServiceName, Weight}}]
```

### Customs — `CustomsInfo` → `CustomsConsignmentRequestType`

```
karrio CustomsInfo                       CustomsConsignmentRequestType
──────────────────                       ─────────────────────────────
(post-shipment, parcel numbers)  ───►    parcelNumbers (stamped by proxy)
incoterm                         ───►    glsIncotermCode (via Incoterm enum)
commodities.weight.KG (total)    ───►    totalGrossWeight{amount, unit:"KGM"}

reference / invoice              ───►    customerReference
                                         invoice.invoiceNumber

shipper                          ───►    exporter.address (Address mapping above)
   federal_tax_id                ───►    exporter.taxId
   (customs.shipper_eori)        ───►    exporter.eoriNumber
                                         exporter.isCommercial = True

recipient                        ───►    importer.address
   federal_tax_id                ───►    importer.taxId
   (customs.recipient_eori)      ───►    importer.eoriNumber
                                         importer.isCommercial = bool(recipient.company_name)

commodities[i]                   ───►    lineItems[i] {
   quantity                              quantity {amount, unit:"PCE"}
   hs_code                       ───►      commodityCode
   description / title           ───►      goodsDescription
   origin_country                ───►      countryOfOrigin
   value_amount                  ───►      valueInInvoiceCurrency
   weight                        ───►      grossWeight {amount, unit:"KGM"}
                                           netWeight {amount, unit:"KGM"}
                                         }
```

### Tracking — `TrackingResponseType` → `TrackingDetails`

```
TrackingResponseType.parcels[i]                    TrackingDetails
───────────────────────────────                    ───────────────
requested ─────────► (fallback: unitno)       ───► tracking_number
status    ─────────► via TrackingStatus enum  ───► status
events[]                                           events[]:
  eventDateTime  ───►                                date, time
  description    ───►                                description
  city, postalCode, country ───►                     location
  code           ───►                                code

errorCode / errorMessage                           (emitted as Message
   present                                          if errorCode set)
```

## Country routing + IncotermCode

The `is_international` / `is_customs_destination` split:

- **`is_international`** is `True` when shipper and recipient
  countries differ. GLS uses `Shipment.IncotermCode` as a signal to
  route every cross-border parcel onto the international network —
  EU or not.
- **`is_customs_destination`** is strictly narrower: `True` for non-EU
  destinations **plus** `GB / CH / NO / LI`. Every customs destination
  is international, but EU cross-border shipments are international
  without needing a customs declaration.

EU member states (27) live in `provider_units.EU_MEMBER_STATES`;
non-EU neighbours that still need customs paperwork live in
`CUSTOMS_NON_EU_NEIGHBOURS`.

karrio standard ISO Incoterm → GLS 2-digit `glsIncotermCode`:

| karrio | GLS | Meaning |
|---|---|---|
| `DDP` | `"10"` | exporter pays duties + taxes + clearance |
| `DAP` | `"20"` | importer pays duties + taxes + clearance |
| `DDU` | `"20"` | deprecated since 2010, treated as DAP |
| `EXW` | `"20"` | importer pays everything; closest GLS code is DAP |

GLS-specific variants (procedure 40/42, low-value, broker clearance —
codes 11/12/18/21/25/30/33/40/41/50/91) collapse onto the closest ISO
family rather than being exposed as extra options.

Defaults to `DDU` (→ `"20"`) on every international shipment when the
caller doesn't supply `customs.incoterm`.

## Customs Consignment v3 (second call) — opt-in

The Customs Consignment v3 API
(`/customs-management/export/public/v3/customs-consignments`) is a
**separate, optional electronic export-declaration surface**, not the
mechanism ShipIT uses to mark a shipment as cross-border. The
rest_shipment_processing doxygen shows that ShipIT itself carries
customs intent via `Shipment.IncotermCode` (`10` DDP, `20` DAP, `30`
DDU) on the createParcels payload — the GlobalBusinessParcel /
GlobalExpressParcel routing is selected from the recipient's
`CountryCode` alongside that incoterm.

Because the v3 surface is a separate API:

- It requires its own OAuth client entitlement. ShipIT-only
  credentials return HTTP `403 "Credential not allowed to access
  API"` against the v3 endpoint even when the createParcels POST
  succeeded — verified live for DE → US (Product=EXPRESS, TN
  `601079548470`) and DE → CA (Product=PARCEL, TN `601079548456`).
  Per GLS feedback the OAuth client (App-ID
  `2f98863e-cf7f-4cd7-b993-8432e5882d43` in our case) must be
  separately whitelisted for the customs-management surface.
- Most merchants only need ShipIT — the connector default is
  **off**. Set `ConnectionConfig.submit_customs_consignment = True`
  on a connection to fire the second leg.

When enabled, it fires only when `is_customs_destination(recipient_country)`
is `True` and a `customs` payload is present. The proxy dispatches it
after the label POST returns, so the proxy stays a thin transport
layer.

### Paperless trade — 4-step orchestration

When the merchant enables paperless trade (`options.paperless_trade = True`
+ `options.doc_files`) AND `submit_customs_consignment` is on AND the
destination is non-EU, the proxy runs the full chain per GLS's documented
process (Timo, 2026-06-03):

```
 1. Auth                       — POST /oauth2/v2/token             (cached)
 2. ShipIT — label             — POST /shipit-farm/v1/.../rs/shipments
 3. Document Management v1     — POST /document-management/v1/documents/customs/prepare-upload
                                  then PUT <uploadURL>             (binary, no auth)
 4. Customs Consignment v3     — POST /customs-management/.../customs-consignments
                                  body carries:
                                    parcelNumbers   ← step 2
                                    linkedDocuments ← step 3 documentIds
```

Verified live (2026-06-03) with a generated commercial-invoice PDF
attached via the unified `doc_files` option (TN `601079548647`):

  - Steps 1 + 2 succeed end-to-end (tracking number returned).
  - Step 3 prepare-upload returns HTTP `403 "Credential not allowed
    to access API"` — wire shape is doxygen-correct
    (`{attributes: {documentType: "COMMERCIAL_INVOICE", documentFormat:
    "pdf", displayFileName: "<file>.pdf"}}`).
  - Step 4 also returns `403` (same OAuth scope gap).

Both surfaces are gated by separate OAuth client entitlements that
the JTL sandbox client does not yet carry. Once GLS whitelists the
App-ID for the customs-management + document-management scopes, the
connector will complete steps 3 + 4 end-to-end without code changes.

Failure handling: if step 3 returns no `documentId`, the proxy
omits `linkedDocuments` from step 4 (rather than send `[null]`).
If step 2 returns no parcel numbers, both steps 3 and 4 are
skipped. Each leg is best-effort so a paperless failure cannot
invalidate a successfully created label.

Wire facts:

- **Weight unit** is `KGM` (UN/CEFACT). Single allowed value on
  `Weight.unit`.
- **Quantity unit** is `PCE` on every line item.
- **Commodity weights** are already converted to KG by
  `lib.to_customs_info` upstream, so we emit them straight onto the
  `grossWeight` / `netWeight` / `totalGrossWeight` blocks.
- **`exporter.isCommercial`** is hardcoded `True` (SaaS shipping for
  merchants). **`importer.isCommercial`** is derived from whether the
  recipient has a `company_name`.
- **`invoice.invoiceDate`** defaults to today when the customs payload
  doesn't carry one.
- **`linkedDocuments`** receives `documentId` values returned by the
  Document Management prepare-upload flow.

## Document Management — paperless trade

Per document, two legs:

1. **POST** `/documents/customs/prepare-upload` with the JSON
   envelope. GLS returns `documentId` + pre-signed `uploadURL`.
2. **PUT** the binary body to `uploadURL` — no auth header, the URL
   carries credentials and is valid for 15 minutes.
   `Content-Type` is `application/pdf` for `.pdf`, else
   `application/octet-stream`.

The connector returns the list of prepare-upload bodies (one per
document) so callers can stamp `documentId` into
`CustomsConsignmentRequestType.linkedDocuments`.

karrio standard document types → GLS `documentType` enum (see
`UploadDocumentType`):

| karrio | GLS |
|---|---|
| `commercial_invoice` | `COMMERCIAL_INVOICE` |
| `certificate_of_origin` | `PROOF_OF_PREFERENCE` |
| `pro_forma_invoice` | `COMMERCIAL_INVOICE` |
| `packing_list` | `PACKING_LIST` |
| `other` | `COMMERCIAL_INVOICE` |

Callers can also pass a raw GLS code (`MULTIPLE_INVOICES`,
`EXPORT_DECLARATION`, `T_PAPER`, `CUSTOMS_RECEIPT`,
`CHARGE_BACK_IMPORT_CUST_INVOICE`, `IMPORT_ENTRY_ADVICE`) through
`doc_type` and it is forwarded as-is.

## Per-shipment routing override

`gls_contact_id` overrides the connection-level `Shipper.ContactID`
per shipment. GLS requires one Contact-ID per pickup location, so
this lets a shipping method point at a warehouse-specific Contact-ID
without duplicating the connection.

## Source-software marker

`Shipment.Identifier` is the free-text marker GLS shows in their logs
to recognise the source software. Configured at connection level via
`app_identifier` (hidden from the shipping-app config editor) or
globally via the `GLS_APP_IDENTIFIER` env var. Billing attribution is
**not** carried here — it rides on `Shipment.Middleware`.

## Tracking

The Track & Trace v1 API accepts up to 10 tracking numbers per call,
comma-joined in the URL path. Response `ParcelsResponseDTO` carries
`parcels[]`; each parcel either has events + status or an
`errorCode` / `errorMessage` (no events). The parser produces one
`TrackingDetails` per successful parcel and one `Message` per failed
one.

Status mapping (`TrackingStatus`) is derived from the
`ecitrackandtrace.yaml` `ParcelDTO.status` enum:

| karrio | GLS codes |
|---|---|
| `pending` | `PLANNEDPICKUP`, `INPICKUP`, `PREADVICE` |
| `in_transit` | `INTRANSIT`, `INWAREHOUSE` |
| `out_for_delivery` | `INDELIVERY` |
| `delivered` | `DELIVERED`, `DELIVEREDPS`, `FINAL` |
| `delivery_failed` | `NOTPICKEDUP`, `NOTDELIVERED` |
| `cancelled` | `CANCELED` |
| `ready_for_pickup` | `DELIVEREDPS` |

GLS returns two identifiers per parcel:

- **`requested`** — the full parcel number the caller queried with, and
  what the platform **stores** on the `Tracking` record (e.g.
  `604831862623`).
- **`unitno`** — GLS's internal unit number, the parcel number **minus its
  trailing check digit** (e.g. `60483186262`).

`tracking_number` on the unified object is therefore `parcel.requested`,
falling back to `parcel.unitno`. The fallback ordering matters: on a
refresh, parsed details are matched back to the tracker **by tracking
number** (`instance.tracking_number`), which is the stored `requested`
value. Keying off `unitno` makes that match fail, so the fetched
status/events are silently dropped and the tracker freezes at creation
(the production bug behind this fix — every GLS tracker stuck on the
synthetic `CREATED` event). The fixture in `test_tracking.py` keeps
`requested` and `unitno` distinct so the test fails if the order is
flipped.

## Error parsing

GLS returns errors in two distinct shapes:

1. **JSON body** with `errors[].code` / `errors[].message` /
   `errors[].field` / `errors[].details` — passed straight through
   typed `ErrorResponseType` parsing.
2. **HTTP response headers** with empty body, carrying `error` and
   `message` headers — the proxy's `parse_error_response` re-wraps
   these as a JSON envelope with the same shape so downstream
   `error.parse_error_response` doesn't have to special-case.

```
Response                       ┌──────────────────────────────┐
   │                           │ provider_utils                │
   ├─► body has content? ────► │   parse_error_response        │
   │                           │     - JSON body: forward      │
   │                           │     - text body: wrap as JSON │
   ├─► headers carry error?─►  │   - re-wrap headers → JSON    │
   │                           └──────────────┬───────────────┘
   ▼                                          ▼
   {errors: [{code, message,            error.parse_error_response
              field, details}]}                 │
                                                ▼
                                         list[Message]
```

## References

- **Doxygen (authoritative)** —
  <https://shipit.gls-group.eu/webservices/5_0_11/doxygen/WS-REST-API/>
  - `rest_shipment_processing.html` — ShipIT createParcels / cancel /
    validateParcels / sporadic collection
  - `rest_tracking.html` — Track & Trace doxygen surface
  - `rest_sporadic_collection.html` — sporadic collection details
  - `rest_parcel_shop.html` — ParcelShop lookup
- **Validated request samples** — `vendor/gls-validated-samples/*.json`
  (addressee-only, signature, flex-delivery, pick&return, shop-return).
- **YAML files in `vendor/`** — the older OpenAPI YAMLs survive as
  `vendor/customs-consignments-v3.yaml`, `vendor/document-management-v1.yaml`,
  `vendor/ecitrackandtrace.yaml`, `vendor/authentification-service-v2.yaml`.
  Use them for the customs / docs / tracking / auth surfaces; for
  ShipIT itself prefer the doxygen.
