import karrio

gateway = karrio.gateway["canpar"].create(
    dict(
        username="user_id",
        password="password",
    )
)
