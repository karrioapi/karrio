# PurplShip

[![Build Status](https://travis-ci.org/PurplShip/purplship.svg?branch=master)](https://travis-ci.org/PurplShip/purplship) [![codecov](https://codecov.io/gh/PurplShip/purplship/branch/master/graph/badge.svg)](https://codecov.io/gh/PurplShip/purplship)

Shipping carriers API integrations Library

- Integrate multiple carriers: DHL, FedEx, UPS, Canada Post and more with ease
- Use an intuitive, unified API across multiple carriers
- Use your developer credentials with negotiated rates

PurplSHip prevents you from reinventing the wheel and is easy to use:

```shell
import purplship

proxy = purplship.gateway['aups'].create({
    "server_url": "https://digitalapi.auspost.com.au/test",
    "username": "username",
    "password": "password",
    "account_number": "1234567"
})

response = purplship.rating.fetch({
    "shipper": {"postal_code": "H3N1S4", "country_code": "CA"},
    "recipient": {"city": "Lome", "country_code": "TG"},
    "shipment": {
        "items": [
            {"id": "1", "height": 3, "length": 10, "width": 3, "weight": 4.0}
        ]
    }
}).from_(proxy)

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
- [py-dhl](https://github.com/PurplShip/py-dhl) - The DHL xml generated datatypes library
- [py-fedex](https://github.com/PurplShip/py-fedex) - The FedEx xml generated datatypes library
- [py-aups](https://github.com/PurplShip/py-aups) - The Australia post JSON generated datatypes library
- [py-sendle](https://github.com/PurplShip/py-sendle) - The Sendle JSON generated datatypes library
- [py-usps](https://github.com/PurplShip/py-usps) - The USPS xml generated datatypes library
- [py-caps](https://github.com/PurplShip/py-caps) - The Canada Post xml generated datatypes library
- [py-ups](https://github.com/PurplShip/py-ups) - The UPS xml generated datatypes library
- [py-soap](https://github.com/PurplShip/py-soap) - The SOAP xml generated datatypes and utilities library
- [lxml](https://lxml.de/) - Processing XML and HTML with Python
- [jstruct](https://github.com/DanH91/jstruct) - JSON to python datatypes

## Contributing

Please read [CONTRIBUTING.md](https://github.com/PurplShip/purplship/blob/master/CODE_OF_CONDUCT.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

- **Daniel K.** - *Initial work* - [@DanHK91](https://twitter.com/DanHK91) | [https://danielk.xyz](https://danielk.xyz/) | [PurplShip](https://purplship.com/open-source)

See also the list of [contributors](https://github.com/PurplShip/purplship/blob/master/contributors) who participated in this project.

## License

This project is licensed under the LGPL License - see the [LICENSE.md](https://github.com/PurplShip/purplship/blob/master/LICENSE) file for details
