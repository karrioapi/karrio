
# karrio.dhl_freight

This package is a DHL Freight (palletized road freight, LTL/groupage) extension of the
[karrio](https://pypi.org/project/karrio) multi-carrier shipping SDK.

DHL Freight covers domestic and international **palletized road freight** (>35 kg)
through DHL's European groupage network. It is distinct from DHL Express
(parcel/air) and DHL Parcel DE (domestic parcel).

- [SPECS.md](./SPECS.md) — technical reference: endpoints, auth, data mapping,
  wire-shape invariants, error parsing.
- [PRD.md](./PRD.md) — phased plan and karrio-core architecture flags.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.dhl_freight
```

## Usage

```python
import karrio.sdk as karrio
from karrio.mappers.dhl_freight.settings import Settings


# Initialize a carrier gateway
dhl_freight = karrio.gateway["dhl_freight"].create(
    Settings(
        client_id="...",        # OAuth Consumer Key
        client_secret="...",    # OAuth Consumer Secret
        test_mode=True,          # sandbox vs production
    )
)
```

## API surface (2026/R03)

| Capability        | Endpoint                                                                | Status        |
|-------------------|-------------------------------------------------------------------------|---------------|
| Shipment booking  | `POST /freight/shipping/orders/v1/sendtransportinstruction`             | Implemented   |
| Label / Print     | (separate **DHL Freight Print API**)                                    | Not in scope  |
| Rating            | (separate **DHL Freight Rates API**)                                    | Not in scope  |
| Tracking          | (separate **DHL Freight Tracking API**)                                 | Not in scope  |
| Pickup booking    | Embedded in the shipment booking (`pickupDate`, `Pickup` party)         | Implemented   |

Production base: `https://api.dhl.com/freight/shipping/orders/v1`
Sandbox base:    `https://api-sandbox.dhl.com/freight/shipping/orders/v1`
Token endpoint:  `https://api(-sandbox).dhl.com/auth/v1/token` (OAuth2 `client_credentials`, 30 min validity)
Rate limit:      250 calls / day (HTTP 429 when exceeded)

## Vendor assets

Pinned reference material from the DHL Developer Portal lives in
[`vendors/`](./vendors). Update by re-downloading from
https://developer.dhl.com/api-reference/shipment-booking-dhl-freight and bumping
the filenames with the new sprint label.

| File                                                            | Source                                                                                                                          |
|-----------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| `DHL_Freight_Shipment_Booking_SANDBOX_2026_R03.postman_collection.json` | https://developer.dhl.com/sites/default/files/2026-05/DHL%20%20Freight%20Shipment%20Booking%20-%20SANDBOX%20-%202026_R03.json  |
| `DHL_Freight_APIs_Product_Manual_2026_R03.pdf`                  | https://developer.dhl.com/sites/default/files/2026-05/DHL%20API%20Developer%20Portal%20-%20DHL%20Freight%20APIs%20Product%20Manual%20-%202026%20R03_3.pdf |

DHL does not publish an OpenAPI/Swagger spec for this API; the Postman
collection sample payload and the Product Manual PDF are the canonical
schema sources. See [PRD.md](./PRD.md) for how `schemas/shipping_request.json`
is derived from them.

Check the [karrio multi-carrier SDK docs](https://docs.karrio.io) for general
shipping API requests.
