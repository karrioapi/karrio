import karrio.sdk as karrio

gateway = karrio.gateway["dpd_group"].create(
    dict(
        api_key="test_api_key_12345",
        test_mode=True,
    )
)
