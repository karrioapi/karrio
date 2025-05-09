import karrio.sdk as karrio

gateway = karrio.gateway["freightcom"].create(
    dict(
        username="username",
        password="password",
    )
)
