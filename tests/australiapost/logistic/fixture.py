import purplship.package as api

gateway = api.gateway["australiapost"].create(
    {"api_key": "username", "password": "password", "account_number": "1234567"}
)
