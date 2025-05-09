import karrio.sdk as karrio

gateway = karrio.gateway["allied_express_local"].create(
    dict(
        username="username",
        password="password",
        account="ACCOUNT",
    )
)
