import karrio

gateway = karrio.gateway["mydhl"].create(
    dict(
        username="username",
        password="password",
        api_key="api_key",
    )
)
