import karrio

gateway = karrio.gateway["asendia_us"].create(
    dict(
        username="username",
        password="password",
        x_asendia_one_api_key="x_asendia_one_api_key",
        account_number="account_number",
    )
)
