import purplship.package as api

gateway = api.gateway["purolator"].create(
    dict(
        user_token="token",
        account_number="12398576956",
        language="en",
        carrier_name="purolator",
    )
)
