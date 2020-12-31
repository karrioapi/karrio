import purplship

gateway = purplship.gateway["freightcom"].create(
    dict(
        username="username",
        password="password",
    )
)
