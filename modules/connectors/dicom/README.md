# karrio.dicom

This package is a Dicom extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.dicom
```

## Usage

```python
import karrio
from karrio.mappers.dicom.settings import Settings


# Initialize a carrier gateway
canadapost = karrio.gateway["dicom"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
