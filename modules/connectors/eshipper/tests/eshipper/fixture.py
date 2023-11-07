import karrio

gateway = karrio.gateway["eshipper"].create(
    dict(
        username="username",
        password="password",
    )
)
