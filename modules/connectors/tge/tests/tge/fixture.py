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
        sscc_count=341761001,
        config=dict(
            SHIP_GS1="888041",
            SSCC_GS1="9327510",
            SHIP_range_end=9999999,
            SHIP_range_start=1,
            SSCC_range_end=341781000,
            SSCC_range_start=341761001,
        ),
    )
)
