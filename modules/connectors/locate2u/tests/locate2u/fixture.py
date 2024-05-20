import karrio
import datetime
import karrio.lib as lib

expiry = datetime.datetime.now() + datetime.timedelta(days=1)
client_id = "client_id"
client_secret = "client_secret"
cached_auth = {
    f"locate2u|{client_id}|{client_secret}": dict(
        access_token="access_token",
        token_type="Bearer",
        scope="locate2u.api",
        expires_in="3600",
        expiry=expiry.strftime("%Y-%m-%d %H:%M:%S"),
    )
}

gateway = karrio.gateway["locate2u"].create(
    dict(
        client_id=client_id,
        client_secret=client_secret,
    ),
    cache=lib.Cache(**cached_auth),
)
