"""Teleship carrier tests fixtures."""

import karrio.sdk as karrio


gateway = karrio.gateway["teleship"].create(
    dict(
        id="123456789",
        test_mode=True,
        carrier_id="teleship",
        account_number="123456789",
        api_key="TEST_API_KEY",
    )
)