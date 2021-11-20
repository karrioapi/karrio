import purplship

gateway = purplship.gateway["dhl_poland"].create(
    dict(
        username="username",
        password="password",
    )
)
