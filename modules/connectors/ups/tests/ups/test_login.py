import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.lib as lib
import karrio.providers.ups.utils as utils


class TestUPSLogin(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_login(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            parsed_response = utils.login(gateway.settings)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/security/v1/oauth/token",
            )
            self.assertDictEqual(
                lib.to_dict(parsed_response),
                ParsedLoginResponse,
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse

            with self.assertRaises(Exception):
                utils.login(gateway.settings)


if __name__ == "__main__":
    unittest.main()


ParsedLoginResponse = {
    "expiry": ANY,
    "token_type": "Bearer",
    "issued_at": "1685542319575",
    "client_id": "client_id",
    "access_token": "access_token",
    "expires_in": "14399",
    "refresh_count": "0",
    "status": "approved",
}

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
