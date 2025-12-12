"""MyDHL carrier tests fixtures."""

import karrio.sdk as karrio


gateway = karrio.gateway["mydhl"].create(
    dict(
        id="123456789",
        test_mode=True,
        carrier_id="mydhl",
        account_number="123456789",
        username="TEST_USERNAME",
        password="TEST_PASSWORD",
    )
)