"""Amazon Shipping authentication tests."""

import unittest
from unittest.mock import patch

import karrio.sdk as karrio


class TestAmazonShippingAuthentication(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_authenticate(self):
        # Create a fresh gateway without cached auth to test the OAuth2 flow
        fresh_gateway = karrio.gateway["amazon_shipping"].create(
            dict(
                client_id="amzn1.application-oa2-client.test123",
                client_secret="test-client-secret",
                refresh_token="Atzr|test-refresh-token",
                aws_region="us-east-1",
            ),
        )

        with patch("karrio.mappers.amazon_shipping.proxy.lib.request") as mock:
            mock.return_value = TokenResponse
            result = fresh_gateway.proxy.authenticate()
            parsed_response = result.deserialize()

            self.assertEqual(
                mock.call_args[1]["url"],
                "https://api.amazon.com/auth/o2/token",
            )
            self.assertEqual(mock.call_args[1]["method"], "POST")
            self.assertEqual(
                mock.call_args[1]["headers"]["Content-Type"],
                "application/x-www-form-urlencoded",
            )
            self.assertEqual(parsed_response, "Atza|test-access-token")


if __name__ == "__main__":
    unittest.main()


TokenResponse = """{
    "access_token": "Atza|test-access-token",
    "token_type": "bearer",
    "expires_in": 3600,
    "refresh_token": "Atzr|test-refresh-token"
}
"""
