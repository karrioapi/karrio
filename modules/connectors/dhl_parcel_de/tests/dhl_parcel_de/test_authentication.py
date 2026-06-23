import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError

import karrio.lib as lib
import karrio.sdk as karrio
from karrio.core.models import ShipmentRequest


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


class TestDHLParcelDETokenRetryOn401(unittest.TestCase):
    """Regression for #622: when the upstream rejects a cached token (401/403),
    the proxy must invalidate the cache and retry once with a fresh token,
    so a stale-but-not-yet-expired token can never block a customer's label.
    """

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
        # Minimal request object; we only care about HTTP-call behaviour.
        self.shipment_request = ShipmentRequest(
            service="dhl_paket",
            shipper={"country_code": "DE", "postal_code": "10115", "city": "Berlin"},
            recipient={"country_code": "DE", "postal_code": "20095", "city": "Hamburg"},
            parcels=[{"weight": 1.0}],
        )

    def _make_401(self):
        return HTTPError(url="x", code=401, msg="Unauthorized", hdrs=None, fp=MagicMock(read=lambda: b"unauth"))

    def test_invalidates_cache_on_401_and_retries_once(self):
        """First call → 401, manager.invalidate() called, second call → 200."""
        proxy = self.fresh_gateway.proxy
        manager = MagicMock()
        manager.get_state.side_effect = ["stale_token", "fresh_token"]

        with (
            patch.object(proxy, "_token_manager", return_value=manager),
            patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock_request,
        ):

            def fake_request(headers=None, on_error=None, **kwargs):
                if headers and "stale_token" in headers.get("Authorization", ""):
                    # Simulate 401 — call on_error like lib.request would.
                    return on_error(self._make_401())
                return '{"items":[]}'

            mock_request.side_effect = fake_request
            proxy.create_shipment(lib.Serializable(self.shipment_request, lambda r: {}))

        self.assertEqual(manager.get_state.call_count, 2, "expected one retry after 401")
        manager.invalidate.assert_called_once()

    def test_does_not_retry_when_first_call_succeeds(self):
        """No 401 → no invalidate, no second auth call."""
        proxy = self.fresh_gateway.proxy
        manager = MagicMock()
        manager.get_state.return_value = "good_token"

        with (
            patch.object(proxy, "_token_manager", return_value=manager),
            patch("karrio.mappers.dhl_parcel_de.proxy.lib.request", return_value='{"items":[]}'),
        ):
            proxy.create_shipment(lib.Serializable(self.shipment_request, lambda r: {}))

        manager.invalidate.assert_not_called()
        self.assertEqual(manager.get_state.call_count, 1)

    def test_two_consecutive_401s_return_body_for_downstream_parse(self):
        """If both attempts 401 we hand the body to downstream parsers (no
        infinite loop)."""
        proxy = self.fresh_gateway.proxy
        manager = MagicMock()
        manager.get_state.side_effect = ["t1", "t2"]
        call_count = {"n": 0}

        def always_401(headers=None, on_error=None, **kwargs):
            call_count["n"] += 1
            return on_error(self._make_401())

        with (
            patch.object(proxy, "_token_manager", return_value=manager),
            patch("karrio.mappers.dhl_parcel_de.proxy.lib.request", side_effect=always_401),
        ):
            proxy.create_shipment(lib.Serializable(self.shipment_request, lambda r: {}))

        self.assertEqual(call_count["n"], 2, "exactly one retry, not an infinite loop")
        manager.invalidate.assert_called_once()


if __name__ == "__main__":
    unittest.main()


LoginResponse = {
    "access_token": "access_token",
    "token_type": "Bearer",
    "expires_in": 1799,
}
