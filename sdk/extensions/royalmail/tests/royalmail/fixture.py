import purplship

gateway = purplship.gateway["royalmail"].create(
    dict(
        client_id="x-ibm-client-id",
        client_secret="x-ibm-client-secret",
    )
)
