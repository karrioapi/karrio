"""DPD Group carrier tests fixtures."""

import karrio.sdk as karrio


gateway = karrio.gateway["dpd_group"].create(
    dict(
        id="dpd_group_test",
        test_mode=True,
        carrier_id="dpd_group",
        bucode="TEST_BUCODE",
        username="TEST_USERNAME",
        password="TEST_PASSWORD",
        customer_id="123456789",
        customer_account_number="ACC123456",
    )
)
