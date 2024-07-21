import karrio

gateway = karrio.gateway["hay_post"].create(
    dict(
        username="username",
        password="password",
        customer_id="2004381",
        customer_type="1",
    )
)
