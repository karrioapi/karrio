import karrio

gateway = karrio.gateway["purolator"].create(
    dict(
        username="test",
        password="password",
        user_token="token",
        account_number="12398576956",
        language="en",
        carrier_id="purolator",
    )
)
