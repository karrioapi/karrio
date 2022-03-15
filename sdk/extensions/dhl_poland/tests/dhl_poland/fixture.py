import karrio

gateway = karrio.gateway["dhl_poland"].create(
    dict(
        username="username",
        password="password",
    )
)
