import karrio

gateway = karrio.gateway["usps"].create(
    {"username": "username", "password": "password", "mailer_id": "847654321"}
)
