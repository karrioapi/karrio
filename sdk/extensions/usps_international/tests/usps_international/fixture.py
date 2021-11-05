import purplship

gateway = purplship.gateway["usps_international"].create(
    {"username": "username", "password": "password", "mailer_id": "847654321"}
)
