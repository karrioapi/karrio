import karrio

gateway = karrio.gateway["geodis"].create(
    dict(
        api_key="api_key",
        identifier="identifier",
    )
)
