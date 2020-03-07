import purplship.package as api

gateway = api.gateway["dhl"].create(
    dict(
        server_url="https://xmlpi-ea.dhl.com/XMLShippingServlet",
        site_id="site_id",
        password="password",
        carrier_name="carrier_name",
    )
)
