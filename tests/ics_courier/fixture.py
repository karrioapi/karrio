import purplship

gateway = purplship.gateway["ics_courier"].create(
    dict(
        username="user_id",
        password="password",
        account_number="12345667"
    )
)
