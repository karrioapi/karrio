import karrio
import datetime
import karrio.lib as lib

expiry = datetime.datetime.now() + datetime.timedelta(days=1)
seller_id = "SELLER_ID"
developer_id = "DEVELOPER_ID"
cached_auth = {
    f"amazon_shipping|{seller_id}|{developer_id}": dict(
        authorizationCode="authorizationCode",
        expiry=expiry.strftime("%Y-%m-%d %H:%M:%S"),
    )
}

gateway = karrio.gateway["amazon_shipping"].create(
    dict(
        seller_id=seller_id,
        developer_id=developer_id,
        mws_auth_token="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    ),
    cache=lib.Cache(**cached_auth),
)
