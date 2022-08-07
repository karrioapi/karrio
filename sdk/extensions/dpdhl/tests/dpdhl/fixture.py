import karrio

gateway = karrio.gateway["dpdhl"].create(
    dict(
        username="username",
        password="password",
        signature="pass",
        app_id="2222222222_01",
        account_number="22222222220104",
    )
)
