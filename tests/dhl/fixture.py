from purplship.mappers.dhl import DHLClient, DHLProxy

proxy = DHLProxy(DHLClient(
  server_url="https://xmlpi-ea.dhl.com/XMLShippingServlet",
  site_id="site_id",
  password="password",
  carrier_name="carrier_name"
))