# PurplShip

[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)


## Overview

PurplShip is an open source library that makes shipping carrier API integration
easy.
PurplShip proposes an intuitive unified API, to make multi-carrier integration seamless.

- Integrate multiple carriers: DHL, FedEx, UPS, Canada Post and more with ease
- Use an intuitive, unified API across multiple carriers
- Use your developer credentials and your negotiated rates

PurplShip helps quickly getting started with shipping services as it is easy to use:

```python
import purplship

dhl = purplship.gateway['dhl'].create({
    "site_id": "username",
    "password": "password"
})

response = purplship.rating.fetch({
    "shipper": {"postal_code": "H3N1S4", "country_code": "CA"},
    "recipient": {"city": "Lome", "country_code": "TG"},
    "parcel": {"height": 3, "length": 10, "width": 3, "weight": 4.0}
}).from_(dhl)

rates = response.parse()
```

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

PurplShip is compatible with Python 3 +

```shell
$ Python --version
Python 3.6.5
```

### Installing

PurplShip can be installed with [pip](https://pip.pypa.io/):

For released version (specify a purplship.freight==version if needed)

```shell
pip install -f https://git.io/purplship purplship.freight
```

## Documentation

PurplShip has usage and reference documentation at [doc.purplship.com](https://doc.purplship.com).


## Contributing

Please read [CONTRIBUTING.md](https://github.com/PurplShip/purplship/blob/master/CODE_OF_CONDUCT.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

- **Daniel K.** - *Initial work* - [@DanHK91](https://twitter.com/DanHK91) | [https://danielk.xyz](https://danielk.xyz/) | [PurplShip](https://purplship.com/open-source)

## License

This project is licensed under the LGPLv3 License - see the [LICENSE.md](https://github.com/PurplShip/purplship/blob/master/LICENSE) file for details
