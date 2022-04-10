import karrio

gateway = karrio.gateway["amazon_mws"].create(
    dict(
        username="username",
        password="password",
    )
)
