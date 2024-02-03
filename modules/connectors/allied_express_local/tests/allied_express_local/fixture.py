import karrio

gateway = karrio.gateway["allied_express_local"].create(
    dict(
        username="username",
        password="password",
        account="ACCOUNT",
    )
)
