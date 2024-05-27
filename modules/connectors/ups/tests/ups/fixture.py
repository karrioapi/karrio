import karrio
import datetime
import karrio.lib as lib

expiry = datetime.datetime.now() + datetime.timedelta(days=1)
client_id = "client_id"
client_secret = "client_secret"
cached_auth = {
    f"ups|{client_id}|{client_secret}": dict(
        token_type="Bearer",
        issued_at="1685542319575",
        client_id=client_id,
        access_token="access_token",
        scope="",
        expires_in="14399",
        refresh_count="0",
        status="approved",
        expiry=expiry.strftime("%Y-%m-%d %H:%M:%S"),
    )
}

gateway = karrio.gateway["ups"].create(
    dict(
        client_id="client_id",
        client_secret="client_secret",
        account_number="Your Account Number",
    ),
    cache=lib.Cache(**cached_auth),
)
