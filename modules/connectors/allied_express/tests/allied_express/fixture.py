import karrio.sdk as karrio

gateway = karrio.gateway["allied_express"].create(
    dict(
        username="username",
        password="password",
        account="ACCOUNT",
    )
)
