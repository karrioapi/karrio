"""Hermes carrier tests fixtures."""

import karrio.sdk as karrio


gateway = karrio.gateway["hermes"].create(
    dict(
        id="hermes_test",
        test_mode=True,
        carrier_id="hermes",
        username="test_user",
        password="test_password",
        client_id="test_client_id",
        client_secret="test_client_secret",
    )
)