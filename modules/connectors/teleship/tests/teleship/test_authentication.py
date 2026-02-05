import unittest
from unittest.mock import patch

import karrio.sdk as karrio
import karrio.lib as lib


class TestTeleshipAuthentication(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.fresh_gateway = karrio.gateway["teleship"].create(
            dict(
                client_id="TEST_CLIENT_ID",
                client_secret="TEST_CLIENT_SECRET",
                test_mode=True,
            ),
        )
        self.test_request = lib.Serializable({})

    def test_authenticate(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            result = self.fresh_gateway.proxy.authenticate(self.test_request)
            parsed_response = result.deserialize()
            print(parsed_response)

            self.assertEqual(parsed_response, "test_access_token")

    def test_authenticate_uses_error_decoder(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            self.fresh_gateway.proxy.authenticate(self.test_request)

            self.assertEqual(
                mock.call_args[1].get("on_error"),
                lib.error_decoder,
            )

    def test_non_json_auth_error(self):
        """Test that non-JSON auth errors (e.g. HTML 401 pages) are handled gracefully."""
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.side_effect = Exception("HTTP 401: Unauthorized")

            with self.assertRaises(Exception) as ctx:
                self.fresh_gateway.proxy.authenticate(self.test_request)

            print(ctx.exception)
            self.assertIn("401", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()


LoginResponse = {
    "accessToken": "test_access_token",
    "tokenType": "bearer",
    "expiresIn": 3599,
}
