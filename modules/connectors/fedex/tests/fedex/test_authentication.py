import unittest
from unittest.mock import patch

import karrio.sdk as karrio
import karrio.lib as lib


class TestFedExAuthentication(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.fresh_gateway = karrio.gateway["fedex"].create(
            dict(
                api_key="api_key",
                secret_key="secret_key",
                track_api_key="track_api_key",
                track_secret_key="track_secret_key",
                account_number="2349857",
                test_mode=True,
            ),
        )
        self.test_request = lib.Serializable({}, ctx={"auth_type": "shipping_auth"})

    def test_authenticate(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            result = self.fresh_gateway.proxy.authenticate(self.test_request)
            parsed_response = result.deserialize()
            print(parsed_response)

            self.assertEqual(parsed_response, "access_token")

    def test_authenticate_uses_error_decoder(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            self.fresh_gateway.proxy.authenticate(self.test_request)

            self.assertEqual(
                mock.call_args[1].get("on_error"),
                lib.error_decoder,
            )

    def test_non_json_auth_error(self):
        """Test that non-JSON auth errors (e.g. HTML 401 pages) are handled gracefully."""
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.side_effect = Exception("HTTP 401: Unauthorized")

            with self.assertRaises(Exception) as ctx:
                self.fresh_gateway.proxy.authenticate(self.test_request)

            print(ctx.exception)
            self.assertIn("401", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()


LoginResponse = {
    "access_token": "access_token",
    "token_type": "bearer",
    "expires_in": 3599,
    "scope": "CXS-TP",
}
