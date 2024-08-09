import karrio

gateway = karrio.gateway["usps_wt"].create(
    {"username": "username", "password": "password", "mailer_id": "847654321"}
)
