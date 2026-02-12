"""DPD Group carrier tests fixtures."""

import datetime
import karrio.sdk as karrio
import karrio.lib as lib


# Pre-populate token cache to avoid real API calls during tests
dpd_login = "TEST_USERNAME"
dpd_bucode = "001"  # DE business unit code
expiry = datetime.datetime.now() + datetime.timedelta(days=1)

cached_auth = {
    f"dpd_meta|u:{dpd_login}|{dpd_bucode}|test": dict(
        access_token="fake_access_token_for_testing",
        expiry=expiry.strftime("%Y-%m-%d %H:%M:%S"),
    )
}

gateway = karrio.gateway["dpd_meta"].create(
    dict(
        id="dpd_meta_test",
        test_mode=True,
        carrier_id="dpd_meta",
        dpd_login=dpd_login,
        dpd_password="TEST_PASSWORD",
        dpd_bucode=dpd_bucode,
        customer_id="123456789",
        customer_account_number="ACC123456",
        account_country_code="DE",
    ),
    cache=lib.Cache(**cached_auth),
)
