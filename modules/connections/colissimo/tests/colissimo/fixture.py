import karrio

gateway = karrio.gateway["colissimo"].create(
    dict(
        contract_number="MY_LOGIN",
        password="MY_PASSWORD",
        laposte_api_key="xxxxx",
    )
)
