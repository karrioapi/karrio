import karrio

gateway = karrio.gateway["dhl_parcel_de"].create(
    dict(
        username="username",
        password="password",
        dhl_api_key="dhl_api_key",
        customer_number="33333333330102",
        tracking_consumer_key="consumer_key",
        tracking_consumer_secret="consumer_secret",
    )
)
