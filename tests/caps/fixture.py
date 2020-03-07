import purplship.package as api

gateway = api.gateway["caps"].create(
    dict(
        server_url="https://ct.soa-gw.canadapost.ca",
        username="username",
        password="password",
        customer_number="1234567",
    )
)
