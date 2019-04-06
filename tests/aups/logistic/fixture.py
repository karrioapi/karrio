import purplship

proxy = purplship.gateway["aups"].create(
    {
        "api_key": "username",
        "password": "password",
        "account_number": "1234567",
    }
)
