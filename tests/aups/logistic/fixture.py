import purplship.package as api

gateway = api.gateway["aups"].create(
    {"api_key": "username", "password": "password", "account_number": "1234567"}
)
