import karrio

gateway = karrio.gateway["australiapost"].create(
    dict(
        api_key="api-key",
        password="password",
        account_number="account-number",
    )
)
