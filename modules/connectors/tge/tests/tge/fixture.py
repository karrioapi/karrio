import karrio

gateway = karrio.gateway["tge"].create(
    dict(
        api_key="api_key",
        username="username",
        password="password",
        toll_username="toll_username",
        toll_password="toll_password",
        my_toll_token="my_toll_token",
        my_toll_identity="my_toll_identity",
        account_code="80502494",
        shipment_count=9999994,
        sssc_count=361394185,
        config=dict(
            SHIP_GS1="888041",
            SSCC_GS1="9947510",
            SHIP_range_end=9999999,
            SHIP_range_start=1,
            SSCC_range_end=361401000,
            SSCC_range_start=361391001,
        ),
    )
)
