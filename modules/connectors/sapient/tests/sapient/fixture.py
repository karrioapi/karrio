import karrio
import datetime
import karrio.lib as lib

expiry = datetime.datetime.now() + datetime.timedelta(days=1)
client_id = "client_id"
client_secret = "client_secret"
cached_auth = {
    f"sapient|{client_id}|{client_secret}": dict(
        access_token="access_token",
        token_type="Bearer",
        issued_at="1685542319575",
        scope="mscapi.all",
        expires_in="14399",
        expiry=expiry.strftime("%Y-%m-%d %H:%M:%S"),
    )
}

gateway = karrio.gateway["sapient"].create(
    dict(
        client_id="client_id",
        client_secret="client_secret",
        shipping_account_id="shipping_account_id",
    ),
    cache=lib.Cache(**cached_auth),
)
