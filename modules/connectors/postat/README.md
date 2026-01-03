# karrio.postat

This package is a Post AT (Austrian Post) extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.postat
```

## Usage

```python
import karrio.sdk as karrio
from karrio.mappers.postat.settings import Settings


# Initialize a carrier gateway
postat = karrio.gateway["postat"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
