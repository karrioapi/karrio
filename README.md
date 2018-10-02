# PurplShip

[![Build Status](https://travis-ci.org/PurplShip/purplship.svg?branch=master)](https://travis-ci.org/PurplShip/purplship) [![codecov](https://codecov.io/gh/PurplShip/purplship/branch/master/graph/badge.svg)](https://codecov.io/gh/PurplShip/purplship)

Shipping carriers API integrations Library

- Integrate multiple carriers: DHL, FedEx and more with ease
- Use an intuitive, unified API across multiple carriers
- Move fast by just reading the carrier API documentation
- Use your developer credentials with negotiated rates
- Tested

PurplSHip prevents you from reinventing the wheel and is easy to use:

```shell
>>> from purplship.mappers.dhl import  DHLClient, DHLProxy
>>> from purplship.domain.entities import Tracking
>>> client = DHLClient(
    "https://xmlpi-ea.dhl.com/XMLShippingServlet",
    "YOUR_DHL_SITE_ID",
    "YOUR_DHL_SITE_PASSWORD",
    "YOUR_DHL_ACCOUNT_NUMBER",
    "CARRIER_NAME"
  )
>>> proxy = DHLProxy(client)
>>> payload = Tracking.create(tracking_numbers=["8346088391"])
>>> tracking_req_xml_obj = proxy.mapper.create_tracking_request(payload)
>>> response = proxy.get_trackings(tracking_req_xml_obj)
>>> trackings = proxy.mapper.parse_tracking_response(response)
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

For latest dev versions

```shell
pip install --process-dependency-links -e git://github.com/PurplShip/purplship.git#egg=purplship
```

Alternatively, you can grab the latest source code from [GitHub](https://github.com/PurplShip/purplship):

```shell
git clone https://github.com/PurplShip/purplship.git
cd purplship
python install setup.py
```

For released version (specify a version if needed)

```shell
pip install -f https://git.io/fxTZ6 purplship
```

## Running the tests

```shell
python -m unittest -v
```

## Documentation

PurplShip has usage and reference documentation at [doc.purplship.com](https://doc.purplship.com).

## Built With

- [generateDs-helpers](https://github.com/PurplShip/generateDs-helpers) - [generateDs](http://www.davekuhlman.org/generateDS.html) object manipulation helpers
- [py-dhl](https://github.com/PurplShip/py-fedex) - The DHL xml generated datatypes library
- [py-fedex](https://github.com/PurplShip/py-dhl) - The FedEx xml generated datatypes library
- [py-caps](https://github.com/PurplShip/py-caps) - The Canada Post xml generated datatypes library
- [py-ups](https://github.com/PurplShip/py-ups) - The UPS xml generated datatypes library
- [py-soap](https://github.com/PurplShip/py-soap) - The SOAP xml generated datatypes and utilities library
- [lxml](https://lxml.de/) - Processing XML and HTML with Python

## Contributing

Please read [CONTRIBUTING.md](https://github.com/PurplShip/purplship/blob/master/CODE_OF_CONDUCT.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

- **Daniel K.** - *Initial work* - [@DanHK91](https://twitter.com/DanHK91) | [https://danielk.xyz](https://danielk.xyz/) | [PurplShip](https://purplship.com/)

See also the list of [contributors](https://github.com/PurplShip/purplship/blob/master/contributors) who participated in this project.

## License

This project is licensed under the LGPL License - see the [LICENSE.md](https://github.com/PurplShip/purplship/blob/master/LICENSE) file for details