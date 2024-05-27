import karrio
import datetime
import karrio.lib as lib

expiry = datetime.datetime.now() + datetime.timedelta(days=1)
principal = "principal"
credential = "credential"
cached_auth = {
    f"eshipper|{principal}|{credential}": dict(
        token="string",
        expires_in="string",
        token_type="string",
        refresh_token="string",
        refresh_expires_in="string",
        expiry=expiry.strftime("%Y-%m-%d %H:%M:%S"),
    )
}

gateway = karrio.gateway["eshipper"].create(
    dict(
        principal="principal",
        credential="credential",
    ),
    cache=lib.Cache(**cached_auth),
)
