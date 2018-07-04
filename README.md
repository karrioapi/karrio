# OpenShip

Shipping carriers API integrations Library

- Integrate multiple carriers: DHL, FedEx and more with ease
- Use an intuitive unified API accross multiple cariers
- Move fast by just reading the carrier API documentation
- Use your own developer credentials with negociated rates
- Tested

Openship prevent you from reinvinting the wheel and is easy to use:

```shell
>>> from openship.mappers.dhl import  DHLClient, DHLProxy
>>> from openship.domain.entities Tracking
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

OpenShip is compatible with Python 3 +

```shell
$ Python --version
Python 3.6.5
```

### Installing

OpenShip can be installed with [pip](https://pip.pypa.io/):

For latest dev versions

```shell
  pip install --process-dependency-links -e git://github.com/OpenShip/openship.git#egg=openship
```

Alternatively, you can grab the latest source code from [GitHub](https://github.com/OpenShip/openship):

```shell
git clone https://github.com/OpenShip/openship.git
cd openship
python setup.py install
```

For released version (change '@version' at your convenience)

```shell
pip install --process-dependency-links git+git://github.com/OpenShip/openship.git@v1.0-beta
```

## Running the tests

```shell
python -m unittest -v
```

## Documentation

OpenShip has usage and reference documentation at [doc.openship.xyz](https://doc.openship.xyz).

## Built With

- [generateDs-helpers](https://github.com/OpenShip/generateDs-helpers) - [generateDs](http://www.davekuhlman.org/generateDS.html) object manipulation helpers
- [py-dhl](https://github.com/OpenShip/py-fedex) - The DHL xml generated datatypes library
- [py-fedex](https://github.com/OpenShip/py-dhl) - The FedEx xml generated datatypes library
- [lxml](https://lxml.de/) - Processing XML and HTML with Python

## Contributing

Please read [CONTRIBUTING.md](https://github.com/OpenShip/openship/blob/master/CODE_OF_CONDUCT.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

- **Daniel K.** - *Initial work* - [@DanHK91](https://twitter.com/DanHK91) | [https://danielk.xyz](https://danielk.xyz/) | [OpenShip](https://openship.xyz/)

See also the list of [contributors](https://github.com/OpenShip/openship/blob/master/contributors) who participated in this project.

## License

This project is licensed under the LGPL License - see the [LICENSE.md](https://github.com/OpenShip/openship/blob/master/LICENSE) file for details