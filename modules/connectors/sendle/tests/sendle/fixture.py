import karrio

gateway = karrio.gateway["sendle"].create(
    dict(
        sendle_id="sendle_id",
        api_key="api_key",
    )
)
