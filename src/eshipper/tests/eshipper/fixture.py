import purplship

gateway = purplship.gateway["eshipper"].create(
    dict(
        username="username",
        password="password",
    )
)
