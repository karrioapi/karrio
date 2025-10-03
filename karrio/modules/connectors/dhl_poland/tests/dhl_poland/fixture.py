import karrio.sdk as karrio

gateway = karrio.gateway["dhl_poland"].create(
    dict(
        username="username",
        password="password",
    )
)
