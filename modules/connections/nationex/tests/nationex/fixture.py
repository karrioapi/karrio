import karrio

gateway = karrio.gateway["nationex"].create(
    dict(
        api_key="XXXXXXXXXXXX",
        customer_id="113300",
        billing_account="165556",
    )
)
