from purplship.mappers.caps import CanadaPostClient, CanadaPostProxy

proxy = CanadaPostProxy(CanadaPostClient(
  server_url="https://ct.soa-gw.canadapost.ca",
  username="username",
  password="password",
  customer_number="1234567"
))