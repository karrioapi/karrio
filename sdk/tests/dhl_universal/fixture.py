import purplship

gateway = purplship.gateway["dhl_universal"].create(
    dict(
        consumer_key="xxxxxxxxxxxxxxxxxx",
        consumer_secret="xxxxxxxxxxxxxx",
    )
)
