
# karrio.dpd_belux

This package is a DPD Belux extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.dpd_belux
```

## Usage

```python
import karrio
from karrio.mappers.dpd_belux.settings import Settings


# Initialize a carrier gateway
dpd_belux = karrio.gateway["dpd_belux"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
