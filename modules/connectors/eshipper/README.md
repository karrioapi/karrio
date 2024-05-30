
# karrio.eshipper

This package is a eShipper extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.eshipper
```

## Usage

```python
import karrio
from karrio.mappers.eshipper.settings import Settings


# Initialize a carrier gateway
eshipper = karrio.gateway["eshipper"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
