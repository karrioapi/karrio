from openship.mappers.fedex import FedexClient, FedexProxy

proxy = FedexProxy(FedexClient(
  "https://wsbeta.fedex.com:443/web-services",
  "user_key",
  "password",
  "2349857",
  "1293587",
  "carrier_name"  
))