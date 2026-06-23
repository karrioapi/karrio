"""Amazon Shipping test fixtures."""

import datetime

import karrio.lib as lib
import karrio.sdk as karrio

# Test SP-API credentials
client_id = "amzn1.application-oa2-client.test123"
client_secret = "test-client-secret"
refresh_token = "Atzr|test-refresh-token"

# Pre-cached auth token to avoid authentication in tests
expiry = datetime.datetime.now() + datetime.timedelta(days=1)
cached_auth = {
    f"amazon_shipping|{client_id}": dict(
        access_token="Atza|test-access-token",
        expiry=lib.fdatetime(expiry),
    )
}

gateway = karrio.gateway["amazon_shipping"].create(
    dict(
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token,
        aws_region="us-east-1",
        shipping_business_id="AmazonShipping_US",
    ),
    cache=lib.Cache(**cached_auth),
)
