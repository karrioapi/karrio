import purplship

gateway = purplship.gateway["usps"].create(
    {"username": "username", "password": "password"}
)
