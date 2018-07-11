from openship.mappers.dhl import DHLClient, DHLProxy

proxy = DHLProxy(DHLClient(
  "https://xmlpi-ea.dhl.com/XMLShippingServlet",
  "site_id",
  "password",
  "account_number",
  "carrier_name"
))

def strip(text):
  return text.replace('\t','').replace('\n','').replace(' ','')