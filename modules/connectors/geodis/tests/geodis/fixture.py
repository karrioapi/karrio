import karrio

gateway = karrio.gateway["geodis"].create(
    dict(
        api_key="api_key",
        identifier="identifier",
        code_client="601911",
        config=dict(agency_code="020017"),
    )
)
