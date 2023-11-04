import karrio

gateway = karrio.gateway["asendia_us"].create(
    dict(
        username="username",
        password="password",
        api_key="x_asendia_one_api_key",
        account_number="account_number",
        config=dict(
            processing_location="SFO",
        ),
    )
)
