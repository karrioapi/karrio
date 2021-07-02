import purplship

gateway = purplship.gateway["usps"].create(
    {"username": "username", "password": "password", "mailer_id": "847654321"}
)
