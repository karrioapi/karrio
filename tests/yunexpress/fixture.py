import purplship

gateway = purplship.gateway["yunexpress"].create(
    dict(
        customer_number="customer_number",
        api_secret="api_secret",
    )
)
