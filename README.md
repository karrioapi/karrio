# PurplShip

[![Build Status](https://travis-ci.org/PurplShip/purplship.svg?branch=master)](https://travis-ci.org/PurplShip/purplship)
[![codecov](https://codecov.io/gh/PurplShip/purplship/branch/master/graph/badge.svg)](https://codecov.io/gh/PurplShip/purplship)
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
import purplship.shipping as api

dhl = api.gateway['dhl'].create({
    "site_id": "username",
    "password": "password"
})

response = api.rating.fetch({
    "shipper": {"postal_code": "H3N1S4", "country_code": "CA"},
    "recipient": {"city": "Lome", "country_code": "TG"},
    "shipment": {
        "items": [
            {"height": 3, "length": 10, "width": 3, "weight": 4.0}
        ]
    }
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

For released version (specify a purplship==version if needed)

```shell
pip install -f https://git.io/purplship purplship
```

Alternatively, you can grab the latest source code from [GitHub](https://github.com/PurplShip/purplship):

```shell
git clone https://github.com/PurplShip/purplship.git
pip install --process-dependency-links -e purplship
```

## Running the tests

```shell
python -m unittest -v
```

## Documentation

PurplShip has usage and reference documentation at [doc.purplship.com](https://doc.purplship.com).

## Built With

- [generateDs-helpers](https://github.com/PurplShip/generateDs-helpers) - [generateDs](http://www.davekuhlman.org/generateDS.html) object manipulation helpers
- [py-dhl](https://github.com/PurplShip/purplship-carriers/tree/master/py-dhl) - The DHL xml generated datatypes library
- [py-fedex](https://github.com/PurplShip/purplship-carriers/tree/master/py-fedex) - The FedEx xml generated datatypes library
- [py-aups](https://github.com/PurplShip/purplship-carriers/tree/master/py-aups) - The Australia post JSON generated datatypes library
- [py-sendle](https://github.com/PurplShip/purplship-carriers/tree/master/py-sendle) - The Sendle JSON generated datatypes library
- [py-usps](https://github.com/PurplShip/purplship-carriers/tree/master/py-usps) - The USPS xml generated datatypes library
- [py-caps](https://github.com/PurplShip/purplship-carriers/tree/master/py-caps) - The Canada Post xml generated datatypes library
- [py-ups](https://github.com/PurplShip/purplship-carriers/tree/master/py-ups) - The UPS xml generated datatypes library
- [py-soap](https://github.com/PurplShip/py-soap) - The SOAP xml generated datatypes and utilities library
- [lxml](https://lxml.de/) - Processing XML and HTML with Python
- [jstruct](https://github.com/DanH91/jstruct) - JSON to python datatypes


## Authors

- **Daniel K.** - *Initial work* - [@DanHK91](https://twitter.com/DanHK91) | [https://danielk.xyz](https://danielk.xyz/) | [PurplShip](https://purplship.com/open-source)

## License

This project is licensed under the LGPLv3 License - see the [LICENSE.md](https://github.com/PurplShip/purplship/blob/master/LICENSE) file for details
