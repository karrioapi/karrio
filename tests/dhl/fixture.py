from openship.mappers.dhl import DHLClient, DHLProxy

proxy = DHLProxy(DHLClient(
  "https://xmlpi-ea.dhl.com/XMLShippingServlet",
  "site_id",
  "password",
  "1203598305",
  "carrier_name"
))