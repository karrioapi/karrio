import unittest
from unittest.mock import patch

import karrio.sdk as karrio
import karrio.lib as lib


class TestUPSAuthentication(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.fresh_gateway = karrio.gateway["ups"].create(
            dict(
                client_id="client_id",
                client_secret="client_secret",
                account_number="account_number",
                test_mode=True,
            ),
        )

    def test_authenticate(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            result = self.fresh_gateway.proxy.authenticate()
            parsed_response = result.deserialize()
            print(parsed_response)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{self.fresh_gateway.settings.server_url}/security/v1/oauth/token",
            )
            self.assertEqual(parsed_response, "access_token")

    def test_authenticate_uses_error_decoder(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            self.fresh_gateway.proxy.authenticate()

            self.assertEqual(
                mock.call_args[1].get("on_error"),
                lib.error_decoder,
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse

            with self.assertRaises(Exception):
                self.fresh_gateway.proxy.authenticate()

    def test_non_json_auth_error(self):
        """Test that non-JSON auth errors (e.g. HTML 401 pages) are handled gracefully."""
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.side_effect = Exception("HTTP 401: Unauthorized")

            with self.assertRaises(Exception) as ctx:
                self.fresh_gateway.proxy.authenticate()

            print(ctx.exception)
            self.assertIn("401", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()


LoginResponse = {
    "token_type": "Bearer",
    "issued_at": "1685542319575",
    "client_id": "client_id",
    "access_token": "access_token",
    "scope": "",
    "expires_in": "14399",
    "refresh_count": "0",
    "status": "approved",
}

ErrorResponse = {
    "response": {
        "errors": [
            {
                "code": "250003",
                "message": "Invalid Access License number",
            }
        ]
    }
}
