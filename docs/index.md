# Introduction

<p>
    <a href="https://github.com/Purplship/Purplship/actions"><img src="https://github.com/Purplship/Purplship/workflows/puprlship-sdk/badge.svg" alt="CI" style="max-width:100%;"></a>
    <a href="https://www.gnu.org/licenses/lgpl-3.0" rel="nofollow"><img src="https://img.shields.io/badge/License-LGPL%20v3-blue.svg" alt="License: LGPL v3" data-canonical-src="https://img.shields.io/badge/License-AGPL%20v3-blue.svg" style="max-width:100%;"></a>
    <a href="https://github.com/python/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black" style="max-width:100%;"></a>
    <a href="https://codecov.io/gh/Purplship/Purplship"><img src="https://codecov.io/gh/Purplship/Purplship/branch/main/graph/badge.svg" alt="codecov" style="max-width:100%;"></a>
    <a href="https://codecov.io/gh/PurplShip/purplship"><img src="https://codecov.io/gh/PurplShip/purplship/branch/main/graph/badge.svg?token=D07fio4Dn6"/></a>
</p>

## What is Purplship?


Puprlship is a modern development kit that simplifies the integration of shipping carriers services into an app.

The key features are:

- **Unified API**: A standardized set of models representing the common shipping data (`Address`, `Parcel`, `Shipment`...)
- **Intuitive API**: A library that abstracts and unifies the typical shipping API services (`Rating`, `Pickup`, `Tracking`...) 
- **Multi-carrier**: Integrate Purplship once and connect to multiple shipping carrier APIs
- **Custom carrier**: A framework to integrate a shipping carrier services within minutes


*For a complete shipping management REST API with a dashboard checkout [purplship-server](https://github.com/PurplShip/purplship-server).*


## Requirements

Python 3.7+

## Installation

```bash
# Install Purplship
pip install purplship

# Install carrier extensions
pip install purplship.canadapost
```

!!! info ""
    **Available carrier extensions**
    
    - `purplship.aramex`
    - `purplship.australiapost`
    - `purplship.canadapost`
    - `purplship.canpar`
    - `purplship.dhl-express`
    - `purplship.dhl-universal`
    - `purplship.dicom`
    - `purplship.fedex`
    - `purplship.purolator-courier`
    - `purplship.royalmail`
    - `purplship.sendle`
    - `purplship.sf-express`
    - `purplship.ups`
    - `purplship.usps`
    - `purplship.yanwen`
    - `purplship.yunexpress`


## Example

- Fetch shipping rates

```python
import purplship
from purplship.core.models import Address, Parcel, RateRequest
from purplship.mappers.canadapost.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["canadapost"].create(
    Settings(
        username="username",
        password="password",
        customer_number="123456789",
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


## License

This project is licensed under the terms of the `LGPL v3` license.
Please see [LICENSE.md](https://github.com/Purplship/Purplship/blob/main/LICENSE) for licensing details.


## Authors

- **Daniel K.** | [@DanHK91](https://twitter.com/DanHK91) | [danielk.xyz](https://danielk.xyz/)
- **Purplship Team** | hello@purplship.com | [purplship.com](https://purplship.com)
