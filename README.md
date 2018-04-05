# open_mappers

Shipping providers and data structures mappers.
The project is entended to offer a unified interface for different shipping providers.

**Note: The project is the first beta version of my draft that I am making Open Source.**
**Written with Python 3**

Use DHL mapper and providers to send rate request

```python
from open_mappers.mappers.dhl.dhl_mapper import initProvider, DHLClient
from open_mappers.domain import entities as E

dhlClient = DHLClient(
  "https://xmlpi-ea.dhl.com/XMLShippingServlet",
  "YOUR_DHL_SITE_ID",
  "YOUR_DHL_SITE_PASSWORD",
  "YOUR_DHL_ACCOUNT_NUMBER"
)

dhlProvider = initProvider(dhlClient)

shipper = {"Address": {"PostalCode":"H3N1S4", "CountryCode":"CA"}}
recipient = {"Address": {"City":"Lome", "CountryCode":"TG"}}
shipmentDetails = {"Packages": [{"Id":"1", "Height":3, "Lenght":10, "Width":3,"Weight":4.0}]}

quoteRequest = E.createQuoteRequest(
  Shipper=shipper,
  Recipient=recipient,
  ShipmentDetails=shipmentDetails
)

request = dhlProvider.mapper.quote_request(quoteRequest)
response = dhlProvider.get_quotes(request)

quotes = dhlProvider.mapper.quote_response(response)

```

Use Fedex mapper and providers to send rate request

```python
from open_mappers.mappers.dhl.fedex_mapper import initProvider, FedexClient
from open_mappers.domain import entities as E

fedexClient = FedexClient(
  "https://wsbeta.fedex.com:443/web-services",
  "FEDEX_USER_KEY",
  "FEDEX_PASSWORD",
  "FEDEX_ACCOUNT_NUMBER",
  "FEDEX_METER_NUMBER"
)

fedexProvider = initProvider(fedexClient)

shipper = {"Address": {"PostalCode":"H3N1S4", "CountryCode":"CA"}}
recipient = {"Address": {"City":"Lome", "CountryCode":"TG"}}
shipmentDetails = {"Packages": [{"Id":"1", "Height":3, "Lenght":10, "Width":3,"Weight":4.0}]}

quoteRequest = E.createQuoteRequest(
  Shipper=shipper,
  Recipient=recipient,
  ShipmentDetails=shipmentDetails
)

request = fedexProvider.mapper.quote_request(quoteRequest)
response = fedexProvider.get_quotes(request)

quotes = fedexProvider.mapper.quote_response(response)

```

TODOS:

- Add tests
- Add more features coverage to providers mappers
- Add Dependencies packages
  . [py-dhl](https://github.com/OpenShip/py-dhl),
  . [py-fedex](https://github.com/OpenShip/py-fedex),
  . [py-soap](https://github.com/OpenShip/py-soap)

Contributions are welcome.