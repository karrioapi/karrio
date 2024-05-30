# karrio.eshipper_xml

This package is a eShipper XML extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.eshipper_xml
```

## Usage

```python
import karrio
from karrio.mappers.eshipper_xml.settings import Settings


# Initialize a carrier gateway
eshipper_xml = karrio.gateway["eshipper_xml"].create(
    Settings(
        ...
    )
)
```

Check the [karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
