# Karrio DPD Group Integration

This is the Karrio integration for DPD Group shipping services.

## Features

- Shipment creation
- Tracking
- Label generation

## Installation

```bash
pip install karrio-dpd-group
```

## Usage

```python
import karrio
from karrio.mappers.dpd_group import Settings

settings = Settings(
    api_key="your_api_key",
    test_mode=True
)

# Create shipment
shipment_request = {...}
shipment = karrio.Shipment.create(shipment_request).from_(settings).parse()
```

## API Documentation

- PREPROD: https://nst-preprod.dpsin.dpdgroup.com/api/v1.1/
- PROD: https://shipping.dpdgroup.com/api/v1.1/
- Docs: https://nst-preprod.dpsin.dpdgroup.com/api/docs/
