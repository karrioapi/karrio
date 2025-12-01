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
        billing_number="33333333330102",
        config={
            "label_type": "ZPL2_910_300_700_oz",
        },
    ),
    cache=lib.Cache(**cached_auth),
)
