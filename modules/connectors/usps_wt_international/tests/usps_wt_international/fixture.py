import karrio

gateway = karrio.gateway["usps_wt_international"].create(
    {"username": "username", "password": "password", "mailer_id": "847654321"}
)
