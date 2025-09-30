# karrio.dtdc

This package is a DTDC extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.dtdc
```

## Usage

```python
import karrio.sdk as karrio
from karrio.mappers.dtdc.settings import Settings


# Initialize a carrier gateway
dtdc = karrio.gateway["dtdc"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
