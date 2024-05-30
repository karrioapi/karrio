import karrio
import datetime
import karrio.lib as lib

expiry = datetime.datetime.now() + datetime.timedelta(days=1)
api_key = "api_key"
secret_key = "secret_key"
track_api_key = "api_key"
track_secret_key = "secret_key"

cached_auth = {
    f"fedex|{api_key}|{secret_key}": dict(
        access_token="access_token",
        token_type="bearer",
        expires_in=3599,
        scope="CXS-TP",
        expiry=expiry.strftime("%Y-%m-%d %H:%M:%S"),
    ),
    f"fedex|{track_api_key}|{track_secret_key}": dict(
        access_token="access_token",
        token_type="bearer",
        expires_in=3599,
        scope="CXS-TP",
        expiry=expiry.strftime("%Y-%m-%d %H:%M:%S"),
    ),
}

gateway = karrio.gateway["fedex"].create(
    dict(
        api_key=api_key,
        secret_key=secret_key,
        track_api_key=track_api_key,
        track_secret_key=track_secret_key,
        account_number="2349857",
    ),
    cache=lib.Cache(**cached_auth),
)
