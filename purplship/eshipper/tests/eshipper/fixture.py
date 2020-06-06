import purplship.package as api

gateway = api.gateway["eshipper"].create(
    dict(username="username", password="password",)
)
