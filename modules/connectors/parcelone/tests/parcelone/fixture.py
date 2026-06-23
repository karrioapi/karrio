"""ParcelOne test fixtures."""

import karrio.sdk as karrio

gateway = karrio.gateway["parcelone"].create(
    dict(
        username="test_user",
        password="test_password",
        api_key="test-api-key",
        mandator_id="TEST_MANDATOR",
        consigner_id="TEST_CONSIGNER",
        test_mode=True,
        config=dict(
            cep_id="DHL",
            product_id="PAKET",
        ),
    )
)
