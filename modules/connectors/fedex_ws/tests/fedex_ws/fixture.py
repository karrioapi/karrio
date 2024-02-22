import karrio

gateway = karrio.gateway["fedex_ws"].create(
    dict(
        user_key="user_key",
        password="password",
        meter_number="1293587",
        account_number="2349857",
        carrier_id="carrier_id",
    )
)
