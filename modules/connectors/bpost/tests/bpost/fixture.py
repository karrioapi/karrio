import karrio

gateway = karrio.gateway["bpost"].create(
    dict(
        account_id="123456",
        passphrase="passphrase",
        config=dict(lang="EN", cost_center="Cost Center"),
    )
)
