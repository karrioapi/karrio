"""DHL Freight authentication — client_credentials OAuth flow."""

import unittest
from unittest.mock import patch

import karrio.lib as lib
import karrio.sdk as karrio


class TestDHLFreightAuthentication(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.fresh_gateway = karrio.gateway["dhl_freight"].create(
            dict(
                client_id="client_id",
                client_secret="client_secret",
                test_mode=True,
            ),
        )

    def test_authenticate_returns_access_token(self):
        with patch("karrio.mappers.dhl_freight.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            result = self.fresh_gateway.proxy.authenticate()
            parsed = result.deserialize()

            self.assertEqual(parsed, "access_token")

    def test_authenticate_targets_sandbox_token_url(self):
        with patch("karrio.mappers.dhl_freight.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            self.fresh_gateway.proxy.authenticate()

            url = mock.call_args[1]["url"]
            self.assertIn("api-sandbox.dhl.com/auth/v1/token", url)
            # client_credentials grant: grant_type + response_type as query string
            self.assertIn("grant_type=client_credentials", url)
            self.assertIn("response_type=access_token", url)

    def test_authenticate_targets_production_token_url(self):
        prod_gateway = karrio.gateway["dhl_freight"].create(
            dict(client_id="cid", client_secret="csec", test_mode=False),
        )
        with patch("karrio.mappers.dhl_freight.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            prod_gateway.proxy.authenticate()
            self.assertIn("api.dhl.com/auth/v1/token", mock.call_args[1]["url"])

    def test_authenticate_uses_error_decoder(self):
        with patch("karrio.mappers.dhl_freight.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            self.fresh_gateway.proxy.authenticate()

            self.assertEqual(
                mock.call_args[1].get("on_error"),
                lib.error_decoder,
            )

    def test_authenticate_sends_basic_auth_header(self):
        """Credentials ride in an ``Authorization: Basic <b64>`` header — not in the body.

        Empirically validated against the sandbox: when credentials are sent
        in the body, the DHL gateway returns 401 even with valid keys.
        """
        with patch("karrio.mappers.dhl_freight.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            self.fresh_gateway.proxy.authenticate()

            headers = mock.call_args[1]["headers"]
            self.assertTrue(headers["Authorization"].startswith("Basic "))
            # base64("client_id:client_secret") = "Y2xpZW50X2lkOmNsaWVudF9zZWNyZXQ="
            self.assertEqual(
                headers["Authorization"],
                "Basic Y2xpZW50X2lkOmNsaWVudF9zZWNyZXQ=",
            )

    def test_authenticate_does_not_send_credentials_in_body(self):
        """Regression guard — body must be empty so the gateway routes on Basic Auth."""
        with patch("karrio.mappers.dhl_freight.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            self.fresh_gateway.proxy.authenticate()

            body = mock.call_args[1]["data"]
            self.assertNotIn("client_id=", body)
            self.assertNotIn("client_secret=", body)


if __name__ == "__main__":
    unittest.main()


LoginResponse = {
    "access_token": "access_token",
    "token_type": "Bearer",
    "expires_in": 1799,
}
