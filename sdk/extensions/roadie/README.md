
# karrio.roadie

This package is a Roadie extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.roadie
```

## Usage

```python
import karrio
from karrio.mappers.roadie.settings import Settings


# Initialize a carrier gateway
roadie = karrio.gateway["roadie"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
