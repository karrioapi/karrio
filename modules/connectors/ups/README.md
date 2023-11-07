# karrio.ups

This package is a UPS extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.ups
```

## Usage

```python
import karrio
from karrio.mappers.ups.settings import Settings


# Initialize a carrier gateway
ups = karrio.gateway["ups"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
