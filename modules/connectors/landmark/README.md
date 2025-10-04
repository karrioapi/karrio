# karrio.landmark

This package is a Landmark Global extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.landmark
```

## Usage

```python
import karrio.sdk as karrio
from karrio.mappers.landmark.settings import Settings


# Initialize a carrier gateway
landmark = karrio.gateway["landmark"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
