import purplship

gateway = purplship.gateway["canpar"].create(
    dict(
        username="user_id",
        password="password",
    )
)
