import purplship.package as api

gateway = api.gateway["usps"].create(
    {
        "server_url": "http://production.shippingapis.com/ShippingAPI.dll",
        "username": "username",
        "password": "password",
    }
)
