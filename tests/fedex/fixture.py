from purplship.mappers.fedex import FedexClient, FedexProxy

proxy = FedexProxy(
    FedexClient(
        server_url="https://wsbeta.fedex.com:443/web-services",
        user_key="user_key",
        password="password",
        meter_number="1293587",
        account_number="2349857",
        carrier_name="carrier_name",
    )
)
