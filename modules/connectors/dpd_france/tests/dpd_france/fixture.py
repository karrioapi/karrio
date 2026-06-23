"""Test fixture for DPD France — instantiates a gateway with sandbox-style settings."""

import karrio.sdk as karrio


gateway = karrio.gateway["dpd_france"].create(
    dict(
        id="carrier_id_test",
        test_mode=True,
        carrier_id="dpd_france",
        userid="test",
        password="test",
        customer_center_number="123",
        customer_number="456789",
        language="EN",
    )
)
