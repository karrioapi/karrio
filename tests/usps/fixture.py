import purplship.api as api

gateway = api.gateway["usps"].create({"username": "username", "password": "password"})
