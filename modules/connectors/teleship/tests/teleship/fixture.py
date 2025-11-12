"""Teleship carrier tests fixtures."""

import karrio.sdk as karrio


gateway = karrio.gateway["teleship"].create(
    dict(
        id="123456789",
        test_mode=True,
        carrier_id="teleship",
        client_id="TEST_CLIENT_ID",
        client_secret="TEST_CLIENT_SECRET",
    )
)
