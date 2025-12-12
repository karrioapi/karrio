# karrio.dpd_group

This package is a DPD Group extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.dpd_group
```

## Usage

```python
import karrio.sdk as karrio
from karrio.mappers.dpd_group.settings import Settings


# Initialize a carrier gateway
dpd_group = karrio.gateway["dpd_group"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
