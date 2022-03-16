# <a href="https://karrio.io" target="_blank"><img alt="Karrio" src="https://docs.karrio.io/img/logo.svg" height="50px" /></a>

[![puprlship-tests](https://github.com/karrioapi/karrio/actions/workflows/tests.yml/badge.svg)](https://github.com/karrioapi/karrio/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/cc2ac4fcb6004bca84e42a90d8acfe41)](https://www.codacy.com/gh/karrio/karrio/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=karrio/karrio&amp;utm_campaign=Badge_Grade)

karrio is a multi-carrier shipping SDK.

The key features are:

- **Unified API**: A standardized set of models representing the common shipping data (`Address`, `Parcel`, `Shipment`...)
- **Intuitive API**: A library that abstracts and unifies the typical shipping API services (`Rating`, `Shipping`, `Tracking`...)
- **Multi-carrier**: Integrate karrio once and connect to multiple shipping carrier APIs
- **Custom carrier**: A framework to integrate a shipping carrier services within hours instead of months

## Requirements

Python 3.7+

## Installation

```bash
# install karrio core
pip install karrio

# eg: install the karrio canadapost extention
pip install karrio.canadapost
```

<details>
<summary>Additional carrier extensions</summary>

- `karrio.aramex`
- `karrio.australiapost`
- `karrio.canadapost`
- `karrio.canpar`
- `karrio.dhl-express`
- `karrio.dhl-universal`
- `karrio.dicom`
- `karrio.fedex`
- `karrio.purolator`
- `karrio.royalmail`
- `karrio.sendle`
- `karrio.sf-express`
- `karrio.tnt`
- `karrio.ups`
- `karrio.usps`
- `karrio.usps-international`
- `karrio.yanwen`
- `karrio.yunexpress`

</details>

## Usage

<details>
<summary>Rates Fetching</summary>

- Fetch shipping rates

```python
import karrio
from karrio.core.models import Address, Parcel, RateRequest
from karrio.mappers.canadapost.settings import Settings


# Initialize a carrier gateway
canadapost = karrio.gateway["canadapost"].create(
    Settings(
        username="6e93d53968881714",
        password="0bfa9fcb9853d1f51ee57a",
        customer_number="2004381",
        contract_id="42708517",
        test=True
    )
)

# Fetching shipment rates

# Provide the shipper's address
shipper = Address(
    postal_code="V6M2V9",
    city="Vancouver",
    country_code="CA",
    state_code="BC",
    address_line1="5840 Oak St"
)

# Provide the recipient's address
recipient = Address(
    postal_code="E1C4Z8",
    city="Moncton",
    country_code="CA",
    state_code="NB",
    residential=False,
    address_line1="125 Church St"
)

# Specify your package dimensions and weight
parcel = Parcel(
    height=3.0,
    length=6.0,
    width=3.0,
    weight=0.5,
    weight_unit='KG',
    dimension_unit='CM'
)

# Prepare a rate request
rate_request = RateRequest(
    shipper=shipper,
    recipient=recipient,
    parcels=[parcel],
    services=["canadapost_xpresspost"],
)

# Send a rate request using a carrier gateway
response = karrio.Rating.fetch(rate_request).from_(canadapost)

# Parse the returned response
rates, messages = response.parse()

print(rates)
# [
#     RateDetails(
#         carrier_name="canadapost",
#         carrier_id="canadapost",
#         currency="CAD",
#         transit_days=2,
#         service="canadapost_xpresspost",
#         discount=1.38,
#         base_charge=12.26,
#         total_charge=13.64,
#         duties_and_taxes=0.0,
#         extra_charges=[
#             ChargeDetails(name="Automation discount", amount=-0.37, currency="CAD"),
#             ChargeDetails(name="Fuel surcharge", amount=1.75, currency="CAD"),
#         ],
#         meta=None,
#         id=None,
#     )
# ]
```

</details>

## Resources

- [**Documentation**](https://docs.karrio.io)
- [**Community Discussions**](https://github.com/karrioapi/karrio/discussions)
- [**Issue Tracker**](https://github.com/karrioapi/karrio/issues)
- [**Blog**](https://docs.karrio.io/blog)

> [Join us on Discord](https://discord.gg/gS88uE7sEx)
