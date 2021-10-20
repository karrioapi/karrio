# purplship.eshipper

This package is a eShipper extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install purplship.eshipper
```

## Usage

```python
import purplship
from purplship.mappers.eshipper.settings import Settings


# Initialize a carrier gateway
eshipper = purplship.gateway["eshipper"].create(
    Settings(
        ...
    )
)
```

Check the [purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
