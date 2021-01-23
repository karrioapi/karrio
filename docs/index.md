# Introduction

<p>
    <a href="https://github.com/Purplship/Purplship/actions"><img src="https://github.com/Purplship/Purplship/workflows/PuprlShip/badge.svg" alt="CI" style="max-width:100%;"></a>
    <a href="https://opensource.org/licenses/MIT" rel="nofollow"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT" data-canonical-src="https://img.shields.io/badge/License-MIT-blue.svg" style="max-width:100%;"></a>
    <a href="https://github.com/python/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black" style="max-width:100%;"></a>
    <a href="https://codecov.io/gh/Purplship/Purplship"><img src="https://codecov.io/gh/Purplship/Purplship/branch/main/graph/badge.svg" alt="codecov" style="max-width:100%;"></a>
    <a href="https://app.codacy.com/manual/DanH91/Purplship?utm_source=github.com&utm_medium=referral&utm_content=Purplship/Purplship&utm_campaign=Badge_Grade_Dashboard"><img src="https://api.codacy.com/project/badge/Grade/a57baa23a1ca4403a37a8b7134609709" alt="Codacy Badge" style="max-width:100%;"></a>
    <a href="https://gitter.im/Purplship/Purplship?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge"><img src="https://badges.gitter.im/Purplship/purplship.svg" alt="Join the chat at https://gitter.im/Purplship/Purplship" style="max-width:100%;"></a>
</p>

## Multi-carrier Shipping SDK

Purplship is a system for connecting multiple logistics carriers API.

In addition to providing a unified and simplified interface across logistics carriers APIs, 
Purplship offers a framework to facilitate the full access of advanced and specific carriers capabilities 
while simplifying the addition of new carrier APIs.

With Purplship you can:

- Integrate one or multiple carriers web services `Canada Post`, `DHL`, `FedEx`, `UPS`, `USPS` ...
- Use a modern and intuitive, unified API across carriers
- Achieve a record integration time with a better developer experience


## Integration

**Purplship SDK** is ideal 

  - for an integration as a Python library
  - if you want more control or a partial integration of a selected set of APIs
  - to integrate custom shipping carrier services 


For a complete shipping management REST API with a dashboard checkout [purplship-server](https://github.com/PurplShip/purplship-server).


## Installation

```bash
# Get the latest core dependencies version freeze
curl -L -O https://raw.githubusercontent.com/PurplShip/purplship/main/requirements.txt
```


!!! info ""
    **Add carrier extensions**
    
    ```text
    # requirement.txt
    ...
    purplship.canadapost
    purplship.dhl_express
    purplship.fedex_express
    purplship.purolator_courier
    purplship.ups_package
    ```

```bash
# Install purplship
pip install -f https://git.io/purplship -r requirements.txt
```

## Usage

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
shipper = Address(
    postal_code="V6M2V9",
    city="Vancouver",
    country_code="CA",
    state_code="BC",
    address_line1="5840 Oak St"
)

recipient = Address(
    postal_code="E1C4Z8",
    city="Moncton",
    country_code="CA",
    state_code="NB",
    residential=False,
    address_line1="125 Church St"
)

parcel = Parcel(
    height=3.0,
    length=6.0,
    width=3.0,
    weight=0.5,
    weight_unit='KG',
    dimension_unit='CM'
)

request = purplship.Rating.fetch(
    RateRequest(
        shipper=shipper,
        recipient=recipient,
        parcels=[parcel],
        services=["canadapost_priority"]
    )
)

rates = request.from_(canadapost).parse()
```

```json
[
  [],
    [
        {
            "base_charge": 12.26,
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "discount": 1.38,
            "duties_and_taxes": 0.0,
            "transit_days": 2,
            "extra_charges": [
                {"amount": -0.37, "currency": "CAD", "name": "Automation discount"},
                {"amount": 1.75, "currency": "CAD", "name": "Fuel surcharge"}
            ],
            "service": "canadapost_xpresspost",
            "total_charge": 13.64
        }
    ]
]
```

## License

This project is licensed under the terms of the `LGPL v3` license.
Please see [LICENSE.md](https://github.com/Purplship/Purplship/blob/master/LICENSE) for licensing details.


## Authors

- **Purplship Team** | hello@purplship.com | [purplship.com](https://purplship.com)
- **Daniel K.** | [@DanHK91](https://twitter.com/DanHK91) | [danielk.xyz](https://danielk.xyz/)
