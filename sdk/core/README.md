# <a href="https://next.purplship.com" target="_blank"><picture><source srcset="./server/main/purplship/server/static/extra/branding/logo-inverted.svg" media="(prefers-color-scheme: dark)"/><img alt="Purplship" src="./server/main/purplship/server/static/extra/branding/logo.svg" height="50px" /></picture></a>

[![puprlship-tests](https://github.com/purplship/purplship/actions/workflows/tests.yml/badge.svg)](https://github.com/purplship/purplship/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/cc2ac4fcb6004bca84e42a90d8acfe41)](https://www.codacy.com/gh/purplship/purplship/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=purplship/purplship&amp;utm_campaign=Badge_Grade)

purplship is a multi-carrier shipping SDK.

The key features are:

- **Unified API**: A standardized set of models representing the common shipping data (`Address`, `Parcel`, `Shipment`...)
- **Intuitive API**: A library that abstracts and unifies the typical shipping API services (`Rating`, `Shipping`, `Tracking`...)
- **Multi-carrier**: Integrate purplship once and connect to multiple shipping carrier APIs
- **Custom carrier**: A framework to integrate a shipping carrier services within hours instead of months

## Requirements

Python 3.7+

## Installation

```bash
# install purplship core
pip install purplship

# eg: install the purplship canadapost extention
pip install purplship.canadapost
```

<details>
<summary>Additional carrier extensions</summary>

- `purplship.aramex`
- `purplship.australiapost`
- `purplship.canadapost`
- `purplship.canpar`
- `purplship.dhl-express`
- `purplship.dhl-universal`
- `purplship.dicom`
- `purplship.fedex`
- `purplship.purolator`
- `purplship.royalmail`
- `purplship.sendle`
- `purplship.sf-express`
- `purplship.tnt`
- `purplship.ups`
- `purplship.usps`
- `purplship.usps-international`
- `purplship.yanwen`
- `purplship.yunexpress`

</details>

## Usage

<details>
<summary>Rates Fetching</summary>

- Fetch shipping rates

```python
import purplship
from purplship.core.models import Address, Parcel, RateRequest
from purplship.mappers.canadapost.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["canadapost"].create(
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
response = purplship.Rating.fetch(rate_request).from_(canadapost)

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

- [**Documentation**](https://next.purplship.com/docs)
- [**Community Discussions**](https://github.com/purplship/purplship/discussions)
- [**Issue Tracker**](https://github.com/purplship/purplship/issues)
- [**Blog**](https://next.purplship.com/blog)

> [Join us on Discord](https://discord.gg/gS88uE7sEx)
