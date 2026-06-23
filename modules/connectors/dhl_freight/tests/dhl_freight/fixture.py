import datetime

import karrio.lib as lib
import karrio.sdk as karrio

expiry = datetime.datetime.now() + datetime.timedelta(days=1)
client_id = "client_id"
client_secret = "client_secret"
cached_auth = {
    f"dhl_freight|{client_id}|{client_secret}": dict(
        access_token="access_token",
        token_type="Bearer",
        expires_in="1799",
        expiry=expiry.strftime("%Y-%m-%d %H:%M:%S"),
    )
}

gateway = karrio.gateway["dhl_freight"].create(
    dict(
        client_id=client_id,
        client_secret=client_secret,
        account_number="62085855350106",  # consignor account → Parties[Consignor].Id
        test_mode=True,
        # The Postman sandbox sample is NL → RO; align the account country
        # with the shipper origin so the SDK's gateway origin check passes.
        # (DHL Freight customers are billed per origin country.)
        account_country_code="NL",
    ),
    cache=lib.Cache(**cached_auth),
)
