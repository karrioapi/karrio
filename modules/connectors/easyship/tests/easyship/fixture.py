import karrio.sdk as karrio

gateway = karrio.gateway["easyship"].create(
    dict(
        access_token="access_token",
    )
)
