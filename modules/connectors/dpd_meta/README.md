# karrio.dpd_meta

This package is a DPD Group extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

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
