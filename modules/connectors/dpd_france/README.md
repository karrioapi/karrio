# karrio.dpd_france

DPD France (cargoNET / EPrintWebservice) extension of the
[karrio](https://pypi.org/project/karrio) multi-carrier shipping SDK.

> Status: **beta** — pending live API verification.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.dpd_france
```

## Usage

```python
import karrio.sdk as karrio
from karrio.mappers.dpd_france.settings import Settings


dpd_france = karrio.gateway["dpd_france"].create(
    Settings(
        userid="...",
        password="...",
        customer_center_number=123,
        customer_number=456789,
        language="EN",
        test_mode=True,
    )
)
```

## Supported features

| Feature | cargoNET op | Karrio interface | Status |
|---|---|---|---|
| Shipment create + label | `CreateShipmentWithLabelsBc` | `Shipment.create` | Supported |
| Shipment cancel | `TerminateShipment` | `Shipment.cancel` | Supported |
| Tracking | `GetShipmentTrace` | `Tracking.fetch` | Supported |
| Pickup schedule | `CreateCollectionRequestBc` | `Pickup.schedule` | Supported |
| Pickup cancel | `TerminateCollectionRequestBc` | `Pickup.cancel` | Supported |
| Return shipment | `CreateReverseInverseShipmentWithLabelsBc` | `Shipment.create(is_return=True)` | Supported |
| Multi-piece (Pattern B) | N × `CreateShipmentWithLabelsBc` | `parcels: list[Parcel]` | Supported |
| Rating | (not exposed by cargoNET) | `Rating.fetch` | Not supported |
| Pickup at customer site | `CreatePickupAtCustomerBc` | (deferred) | Deferred |

## Multi-piece behaviour

cargoNET's `CreateMultiShipmentBc` op excludes Predict / Relais / Retour
services and does not return labels. This connector therefore implements
multi-piece shipments via Pattern B: one parallel `CreateShipmentWithLabelsBc`
call per parcel, aggregated through `lib.to_multi_piece_shipment` (master
tracking number + bundled label PDF + `meta.tracking_numbers` /
`meta.shipment_identifiers` lists). Single-parcel and N-parcel paths share
the same code.

## Vendor documentation

The PDF specifications for both the EPrintWebservice (shipping) and
Webtrace_Service (tracking) APIs live under
[`vendor/`](./vendor/README.md), along with SOAPAction strings, namespace
notes, and IP-whitelisting requirements.

Check the [Karrio multi-carrier SDK docs](https://docs.karrio.io) for the
unified Shipping API request reference.
