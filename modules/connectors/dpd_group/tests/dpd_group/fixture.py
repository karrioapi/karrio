"""DPD Group carrier tests fixtures."""

import karrio.sdk as karrio


gateway = karrio.gateway["dpd_group"].create(
    dict(
        id="123456789",
        test_mode=True,
        carrier_id="dpd_group",
        account_number="123456789",
        api_key="TEST_API_KEY",
    )
)