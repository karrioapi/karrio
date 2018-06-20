'''

shipper = {"address": {"postal_code":"H3N1S4", "country_code":"CA"}}
recipient = {"address": {"city":"Lome", "country_code":"TG"}}
shipment_details = {"packages": [{"id":"1", "height":3, "lenght":10, "width":3,"weight":4.0}]}
from open_mappers.mappers.dhl.dhl_client import  DHLClient
client = DHLClient(...)
from open_mappers.mappers.dhl.dhl_proxy import init_proxy
dhlProxy = init_proxy(client)
from open_mappers.domain.entities import Quote, jsonify
payload = Quote.create(shipper=shipper, recipient=recipient, shipment_details=shipment_details)
request = dhlProxy.mapper.create_quote_request(payload)
response = dhlProxy.get_quotes(request)
quotes = dhlProxy.mapper.parse_quote_response(response)
print(jsonify(quotes))

'''