import karrio
import datetime
import karrio.lib as lib

expiry = datetime.datetime.now() + datetime.timedelta(days=1)
client_id = "client_id"
client_secret = "client_secret"
cached_auth = {
    f"usps_international|{client_id}|{client_secret}": dict(
        token_type="Bearer",
        issued_at="1685542319575",
        client_id=client_id,
        access_token="access_token",
        scope="addresses international-prices subscriptions payments pickup tracking labels scan-forms companies service-delivery-standards locations international-labels prices",
        expires_in="14399",
        refresh_count="0",
        status="approved",
        expiry=expiry.strftime("%Y-%m-%d %H:%M:%S"),
        issuer="api.usps_international.com",
        application_name="Silver Shipper Developer",
        api_products="[Shipping-Silver]",
        public_key="LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUF4QWxwZjNSNEE1S0lwZnhJVWk1bgpMTFByZjZVZTV3MktzeGxSVzE1UWV0UzBjWGVxaW9OT2hXbDNaaVhEWEdKT3ZuK3RoY0NWVVQ3WC9JZWYvTENZCkhUWk1kYUJOdW55VHEwT2RNZmVkUU8zYUNKZmwvUnJPTHYyaG9TRDR4U1YxRzFuTTc1RTlRYitFZ1p0cmFEUXoKNW42SXRpMUMzOHFGMjU5NVRHUWVUemx3Wk1LQng1VTY2bGwzNzlkZ2plTUJxS3ppVHZHWEpOdVg5ZzRrRlBIaApTLzNERm9FNkVFSW8zUHExeDlXTnRaSm93VkRwQUVZZTQ3SU1UdXJDN2NGcXp2d3M1b1BDRHQ4c083N2lUdDN0Cm1vK3NrM2ExWnZSaGs2WUQ3Zkt1UldQVzFEYUM4dC9pazlnWnhqQndYNlZsSUhDRzRZSHlYejZteWdGV09jMmEKOVFJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0t",
    )
}

gateway = karrio.gateway["usps_international"].create(
    dict(
        client_id="client_id",
        client_secret="client_secret",
        account_number="Your Account Number",
    ),
    cache=lib.Cache(**cached_auth),
)
