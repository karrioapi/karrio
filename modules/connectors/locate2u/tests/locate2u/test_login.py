import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.lib as lib
import karrio.providers.locate2u.utils as utils


class TestLocate2uLogin(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_login(self):
        with patch("karrio.mappers.locate2u.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            parsed_response = utils.login(gateway.settings)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.auth_server_url}/connect/token",
            )
            self.assertDictEqual(
                lib.to_dict(parsed_response),
                ParsedLoginResponse,
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.locate2u.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse

            with self.assertRaises(Exception):
                utils.login(gateway.settings)


if __name__ == "__main__":
    unittest.main()


ParsedLoginResponse = {
    "expiry": ANY,
    "token_type": "Bearer",
    "access_token": "access_token",
    "scope": "locate2u.api",
    "expires_in": 3600,
}

LoginResponse = """{
  "access_token": "access_token",
  "expires_in": 3600,
  "token_type": "Bearer",
  "scope": "locate2u.api"
}
"""

ErrorResponse = """{
    "error": "invalid_client"
}
"""
