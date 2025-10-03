import datetime
import karrio.sdk as karrio
import karrio.core.utils as lib

expiry = datetime.datetime.now() + datetime.timedelta(days=1)
cached_auth = {
    f"dtdc|dtdc|TEST_API_KEY": dict(
        access_token="access_token",
        expiry=expiry.strftime("%Y-%m-%d %H:%M:%S"),
    ),
}

gateway = karrio.gateway["dtdc"].create(
    dict(
        api_key="TEST_API_KEY",
        customer_code="TESTCUST001",
        username="TESTUSER001",
        password="TESTPASS001",
        test_mode=True,
    ),
    cache=lib.Cache(**cached_auth),
)
