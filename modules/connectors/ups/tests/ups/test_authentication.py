import unittest
from unittest.mock import patch, ANY

import karrio.sdk as karrio
import karrio.lib as lib


class TestUPSAuthentication(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_authenticate(self):
        # Create a fresh gateway without cached auth to test the login flow
        fresh_gateway = karrio.gateway["ups"].create(
            dict(
                client_id="client_id",
                client_secret="client_secret",
                account_number="account_number",
                test_mode=True,
            ),
        )

        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            # Call authenticate directly on the proxy
            result = fresh_gateway.proxy.authenticate()
            parsed_response = result.deserialize()

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{fresh_gateway.settings.server_url}/security/v1/oauth/token",
            )
            # Compare token returned
            self.assertEqual(parsed_response, "access_token")

    def test_parse_error_response(self):
        # Create a fresh gateway without cached auth to test the login flow
        fresh_gateway = karrio.gateway["ups"].create(
            dict(
                client_id="client_id",
                client_secret="client_secret",
                account_number="account_number",
                test_mode=True,
            ),
        )

        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse

            with self.assertRaises(Exception):
                fresh_gateway.proxy.authenticate()


if __name__ == "__main__":
    unittest.main()


LoginResponse = """{
    "token_type": "Bearer",
    "issued_at": "1685542319575",
    "client_id": "client_id",
    "access_token": "access_token",
    "scope": "",
    "expires_in": "14399",
    "refresh_count": "0",
    "status": "approved"
}
"""

ErrorResponse = """{
  "response": {
    "errors": [
      {
        "code": "250003",
        "message": "Invalid Access License number"
      }
    ]
  }
}
"""
