import purplship.package as api

gateway = api.gateway["freightcom"].create(
    dict(
        username="username",
        password="password",
        server_url="https://test.freightcom.com/rpc2",
    )
)
