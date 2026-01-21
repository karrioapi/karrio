"""Asendia carrier tests fixtures."""

import karrio.sdk as karrio


gateway = karrio.gateway["asendia"].create(
    dict(
        id="asendia",
        test_mode=True,
        carrier_id="asendia",
        username="test_user",
        password="test_pass",
        customer_id="CUST123",
    )
)
