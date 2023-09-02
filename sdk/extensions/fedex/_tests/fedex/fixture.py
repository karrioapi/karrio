import karrio
import datetime
import karrio.lib as lib

expiry = datetime.datetime.now() + datetime.timedelta(days=1)
api_key = "api_key"
secret_key = "secret_key"
cached_auth = {
    f"fedex|{api_key}|{secret_key}": dict(
        token_type="bearer",
        access_token="access_token",
        expires_in=3599,
        scope="CXS",
        expiry=expiry.strftime("%Y-%m-%d %H:%M:%S"),
    )
}

gateway = karrio.gateway["fedex"].create(
    dict(
        api_key=api_key,
        secret_key=secret_key,
        account_number="Your Account Number",
        cache=lib.Cache(**cached_auth),
    )
)
