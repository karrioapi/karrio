import karrio

gateway = karrio.gateway["easypost"].create(
    dict(
        username="username",
        password="password",
    )
)
