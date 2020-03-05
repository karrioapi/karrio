import purplship.package as api

proxy = api.gateway["aups"].create(
    {
        "api_key": "username",
        "password": "password",
        "account_number": "1234567",
        "api": "Postage",
    }
)
