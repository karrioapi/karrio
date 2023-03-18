import karrio

gateway = karrio.gateway["dpdhl"].create(
    dict(
        username="developerid",
        password="password",
        app_id="app_01",
        app_token="pass",
        zt_id="zt12345",
        zt_password="geheim",
        account_number="2222222222",
        test_mode=True,
    )
)
