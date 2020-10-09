import purplship

gateway = purplship.gateway["canpar"].create(
    dict(
        user_id="user_id",
        password="password",
    )
)
