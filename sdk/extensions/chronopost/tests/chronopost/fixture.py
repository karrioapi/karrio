import karrio

gateway = karrio.gateway["chronopost"].create(
    dict(account_number="1234", password="password")
)
