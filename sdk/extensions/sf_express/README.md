# karrio.sf_express

This package is a SF-Express extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.sf_express
```

## Usage

```python
import karrio
from karrio.mappers.sf_express.settings import Settings


# Initialize a carrier gateway
canadapost = karrio.gateway["sf_express"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.karrio.com) for Shipping API requests
