import karrio.sdk as karrio
import datetime
import karrio.lib as lib

expiry = datetime.datetime.now() + datetime.timedelta(days=1)
client_id = "client_id"
client_secret = "client_secret"
cached_auth = {
    f"dhl_parcel_de|{client_id}|{client_secret}": dict(
        access_token="access_token",
        token_type="Bearer",
        expires_in="1799",
        expiry=expiry.strftime("%Y-%m-%d %H:%M:%S"),
    )
}

gateway = karrio.gateway["dhl_parcel_de"].create(
    dict(
        username="username",
        password="password",
        client_id=client_id,
        client_secret=client_secret,
        test_mode=True,  # Test mode uses default sandbox billing numbers automatically
        config={
            "label_type": "ZPL2_910_300_700_oz",
            # billing numbers are auto-populated from DEFAULT_TEST_BILLING_NUMBERS in test mode
        },
    ),
    cache=lib.Cache(**cached_auth),
)
