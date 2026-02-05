import unittest
from unittest.mock import patch

import karrio.sdk as karrio
import karrio.lib as lib


class TestDHLParcelDEAuthentication(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.fresh_gateway = karrio.gateway["dhl_parcel_de"].create(
            dict(
                username="username",
                password="password",
                client_id="client_id",
                client_secret="client_secret",
                test_mode=True,
            ),
        )

    def test_authenticate(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            result = self.fresh_gateway.proxy.authenticate()
            parsed_response = result.deserialize()
            print(parsed_response)

            self.assertEqual(parsed_response, "access_token")

    def test_authenticate_uses_error_decoder(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            self.fresh_gateway.proxy.authenticate()

            self.assertEqual(
                mock.call_args[1].get("on_error"),
                lib.error_decoder,
            )

    def test_non_json_auth_error(self):
        """Test that non-JSON auth errors (e.g. HTML 401 pages) are handled gracefully."""
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.side_effect = Exception("HTTP 401: Unauthorized")

            with self.assertRaises(Exception) as ctx:
                self.fresh_gateway.proxy.authenticate()

            print(ctx.exception)
            self.assertIn("401", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()


LoginResponse = {
    "access_token": "access_token",
    "token_type": "Bearer",
    "expires_in": 1799,
}
