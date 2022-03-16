import karrio

gateway = karrio.gateway["aramex"].create(
    dict(
        username="testingapi@aramex.com",
        password="R123456789$r",
        account_pin="331421",
        account_entity="AMM",
        account_number="20016",
        account_country_code="JO",
    )
)
