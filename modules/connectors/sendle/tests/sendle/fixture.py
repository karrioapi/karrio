import karrio

gateway = karrio.gateway["sendle"].create(
    dict(
        sendle_id="sendle_id",
        sendle_api_key="sendle_api_key",
    )
)
