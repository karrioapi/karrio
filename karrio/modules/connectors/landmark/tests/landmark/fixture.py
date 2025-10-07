"""Landmark Global carrier tests fixtures."""

import karrio.sdk as karrio


gateway = karrio.gateway["landmark"].create(
    dict(
        id="landmark_test",
        test_mode=True,
        carrier_id="landmark",
        username="test_username",
        password="test_password",
        client_id="2437",
        account_number="TEST123",
        region="Landmark CMH",
        config=dict(
            account_currency="EUR",
        ),
    )
)
