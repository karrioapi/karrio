import purplship

gateway = purplship.gateway["ics_courier"].create(
    dict(
        account_id="account_id",
        password="password"
    )
)
