# karrio.hermes

This package is a Hermes extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.hermes
```

## Usage

```python
import karrio.sdk as karrio
from karrio.mappers.hermes.settings import Settings


# Initialize a carrier gateway
hermes = karrio.gateway["hermes"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
