# karrio.dpd_meta

This package is a DPD Meta extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.dpd_meta
```

## Usage

```python
import karrio.sdk as karrio
from karrio.mappers.dpd_meta.settings import Settings


# Initialize a carrier gateway
dpd_meta = karrio.gateway["dpd_meta"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests

## DPD Public Web Services (Depot lookup / Shop2Shop)

In reseller / brokerage setups the DPD account belongs to the broker, so the
customer's `sendingDepot` is not known from the credentials and must be
resolved per shipment from the shipper's country + postal code. The
connector ships with proxy support for the two SOAP services DPD provides
for this purpose:

- `LoginService_V2_0.getAuth` — exchanges `delisId + password` for an
  `authToken` valid for 24h (cached in the connection cache).
- `DepotDataService_V1_0.getDepotData` — resolves a depot from
  `country + zipCode` (or by depot number).

The proxy exposes a `find_locations(...)` method for ad-hoc lookups
(shop finder) and automatically queries the depot service to inject
`sendingDepot` for **Shop2Shop / Shop2Home** shipments (DPD SoCodes
`345`, `404`, `337`, `338`) when no `sendingDepot` is already present in
the request.

Vendor reference PDFs are kept under `vendor/`:

- `LoginService_V2_0_C0.pdf`
- `DepotDataService_V1_0.pdf`
- `dpd-api.developer.guidelines-A4-20250115.pdf`
