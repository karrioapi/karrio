"""SmartKargo carrier tests fixtures."""

import karrio.sdk as karrio


gateway = karrio.gateway["smartkargo"].create(
    dict(
        id="123456789",
        test_mode=True,
        carrier_id="smartkargo",
        api_key="TEST_API_KEY",
        account_number="TEST_ACCOUNT",
        account_id="TEST_ID",
    )
)