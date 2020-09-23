import purplship.api as api

gateway = api.gateway["purolator_courier"].create(
    dict(
        username="test",
        password="password",
        user_token="token",
        account_number="12398576956",
        language="en",
        carrier_id="purolator_courier",
    )
)
