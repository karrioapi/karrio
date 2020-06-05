import purplship.package as api

gateway = api.gateway["dhl"].create(
    dict(
        site_id="site_id",
        password="password",
        carrier_id="carrier_id",
        account_number="123456789",
        id="testing_id",
    )
)
