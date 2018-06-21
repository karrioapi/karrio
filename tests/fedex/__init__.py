'''

shipper = {"address": {"postal_code":"H3N1S4", "country_code":"CA"}}
recipient = {"address": {"city":"Lome", "country_code":"TG"}}
shipment_details = {"packages": [{"id":"1", "height":3, "lenght":10, "width":3,"weight":4.0}]}
from openship.mappers.fedex.fedex_client import  FedexClient
client = FedexClient(...)
from openship.mappers.fedex.fedex_proxy import init_proxy
fedexProxy = init_proxy(client)
from openship.domain.entities import Quote, jsonify
payload = Quote.create(shipper=shipper, recipient=recipient, shipment_details=shipment_details)
request = fedexProxy.mapper.create_quote_request(payload)
response = fedexProxy.get_quotes(request)
quotes = fedexProxy.mapper.parse_quote_response(response)
print(jsonify(quotes))

'''