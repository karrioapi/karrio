import karrio

gateway = karrio.gateway["tge"].create(
    dict(
        username="username",
        password="password",
        account="ACCOUNT",
    )
)
