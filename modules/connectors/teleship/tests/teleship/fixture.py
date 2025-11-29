"""Teleship carrier tests fixtures."""

import karrio.sdk as karrio
import karrio.lib as lib
import datetime

expiry = datetime.datetime.now() + datetime.timedelta(days=1)
client_id = "TEST_CLIENT_ID"
client_secret = "TEST_CLIENT_SECRET"

cached_auth = {
    f"teleship|{client_id}|{client_secret}": dict(
        accessToken="test_access_token",
        tokenType="bearer",
        expiresIn=3599,
        expiry=expiry.strftime("%Y-%m-%d %H:%M:%S"),
    ),
}

gateway = karrio.gateway["teleship"].create(
    dict(
        client_id=client_id,
        client_secret=client_secret,
        test_mode=True,
    ),
    cache=lib.Cache(**cached_auth),
)
