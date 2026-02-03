"""SmartKargo carrier tests fixtures."""

import karrio.sdk as karrio


gateway = karrio.gateway["smartkargo"].create(
    dict(
        id="123456789",
        test_mode=True,
        carrier_id="smartkargo",
        account_number="123456789",
        api_key="TEST_API_KEY",
    )
)