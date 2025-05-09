import karrio.sdk as karrio

gateway = karrio.gateway["canpar"].create(
    dict(
        username="user_id",
        password="password",
    )
)
