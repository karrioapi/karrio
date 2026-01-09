# karrio.spring

This package is a Spring extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.spring
```

## Usage

```python
import karrio.sdk as karrio
from karrio.mappers.spring.settings import Settings


# Initialize a carrier gateway
spring = karrio.gateway["spring"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
