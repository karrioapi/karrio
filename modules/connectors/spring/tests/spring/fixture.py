"""Spring carrier tests fixtures."""

import karrio.sdk as karrio
import karrio.lib as lib

gateway = karrio.gateway["spring"].create(
    dict(
        carrier_id="spring",
        test_mode=True,
        api_key="TEST_API_KEY",
    )
)
