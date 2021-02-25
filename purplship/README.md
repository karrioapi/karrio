<p align="center">
  <p align="center">
    <a href="https://purplship.com" target="_blank">
      <img src="https://github.com/PurplShip/purplship-server/raw/main/src/purpleserver/purpleserver/static/purpleserver/img/icon.png" alt="Purplship" height="100">
    </a>
  </p>
  <h2 align="center">
    Purplship - The Open Source multi-carrier shipping SDK
  </h2>
  <p align="center">
    <a href="https://github.com/Purplship/Purplship/actions"><img src="https://github.com/Purplship/Purplship/workflows/PuprlShip/badge.svg" alt="CI" style="max-width:100%;"></a>
    <a href="https://www.gnu.org/licenses/lgpl-3.0" rel="nofollow"><img src="https://img.shields.io/badge/License-LGPL%20v3-blue.svg" alt="License: AGPL v3" data-canonical-src="https://img.shields.io/badge/License-AGPL%20v3-blue.svg" style="max-width:100%;"></a>
    <a href="https://github.com/python/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black" style="max-width:100%;"></a>
    <a href="https://codecov.io/gh/PurplShip/purplship"><img src="https://codecov.io/gh/PurplShip/purplship/branch/main/graph/badge.svg?token=D07fio4Dn6"/></a>
    <a href="https://app.codacy.com/manual/DanH91/Purplship?utm_source=github.com&utm_medium=referral&utm_content=Purplship/Purplship&utm_campaign=Badge_Grade_Dashboard"><img src="https://api.codacy.com/project/badge/Grade/a57baa23a1ca4403a37a8b7134609709" alt="Codacy Badge" style="max-width:100%;"></a>
  </p>
</p>

Puprlship is a modern development kit that simplifies the integration of shipping carriers services into an app.

The key features are:

- **Unified API**: A standardized set of models representing the common shipping data (`Address`, `Parcel`, `Shipment`...)
- **Intuitive API**: A library that abstracts and unifies the typical shipping API services (`Rating`, `Pickup`, `Tracking`...) 
- **Multi-carrier**: Integrate Purplship once and connect to multiple shipping carrier APIs
- **Custom carrier**: A framework to integrate a shipping carrier services within hours instead of months


*For a complete shipping management REST API with a dashboard checkout [purplship-server](https://github.com/PurplShip/purplship-server).*


## Requirements

Python 3.7+

## Installation

```bash
# install purplship core
pip install purplship

# install the purplship canadapost extention
pip install purplship.canadapost
```

Additional extensions:

<details>
<summary>Available carriers</summary>

- `purplship.aramex`
- `purplship.australiapost`
- `purplship.canadapost`
- `purplship.canpar`
- `purplship.dhl-express`
- `purplship.dhl-universal`
- `purplship.dicom`
- `purplship.fedex-express`
- `purplship.purolator-courier`
- `purplship.royalmail`
- `purplship.sendle`
- `purplship.sf-express`
- `purplship.ups-package`
- `purplship.usps`
- `purplship.yanwen`
- `purplship.yunexpress`

</details>

## Usage

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

## Resources

- [**Documentation**](https://sdk.purplship.com)
- [**Bug Tracker**](https://github.com/PurplShip/purplship/issues)
- [**Community on Discord**](https://discord.gg/kXEa3UMRHd)

## Contributing

We encourage you to contribute to Purplship! Please check out the
[Contributing to Purplship guide](/docs/development/contributing.md) for guidelines about how to proceed.
[Join us!](https://gitter.im/Purplship/Purplship?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

Do you want to extend Purplship and integrate a custom carrier, check out [Extending Purplship](https://sdk.purplship.com/development/extending/)

## License

This project is licensed under the terms of the `LGPL v3` license.
Please see [LICENSE.md](/LICENSE) for licensing details.


## Authors

- **Daniel K.** | [@DanHK91](https://twitter.com/DanHK91) | [danielk.xyz](https://danielk.xyz/)
- **Purplship Team** | hello@purplship.com | [purplship.com](https://purplship.com)
