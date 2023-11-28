
# karrio.dpd

This package is a DPD extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.dpd
```

## Usage

```python
import karrio
from karrio.mappers.dpd.settings import Settings


# Initialize a carrier gateway
dpd = karrio.gateway["dpd"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
