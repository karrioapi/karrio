import purplship.package as api

gateway = api.gateway["freightcom"].create(
    dict(
        username="username",
        password="password",
    )
)
