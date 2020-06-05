import purplship.package as api

gateway = api.gateway["fedex"].create(
    dict(
        user_key="user_key",
        password="password",
        meter_number="1293587",
        account_number="2349857",
        carrier_id="carrier_id",
    )
)
