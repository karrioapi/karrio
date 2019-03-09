import purplship

proxy = purplship.gateway["sendle"].create(
    {
        "server_url": "https://sandbox.sendle.com",
        "sendle_id": "username",
        "api_key": "password",
    }
)
