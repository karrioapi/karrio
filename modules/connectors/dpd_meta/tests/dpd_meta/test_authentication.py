"""DPD Meta auth-token expiry tests.

Regression for the `now + 24h` fabricated expiry: the META `/login` token is a
JWT, so `get_token` must store the token's real `exp`, and fall back to a short
window (never 24h) when the token is not a decodable JWT.
"""

import base64
import datetime
import json
import unittest
from unittest import mock
from urllib.error import HTTPError

import karrio.lib as lib
import karrio.providers.dpd_meta.utils as provider_utils
import karrio.sdk as karrio
from karrio.core.models import ShipmentRequest


def _b64url(data: dict) -> str:
    return base64.urlsafe_b64encode(json.dumps(data).encode()).rstrip(b"=").decode()


def _unsigned_jwt(exp: int) -> str:
    return f"{_b64url({'alg': 'none', 'typ': 'JWT'})}.{_b64url({'exp': exp})}.sig"


class TestDecodeTokenExpiry(unittest.TestCase):
    def test_valid_jwt_returns_local_datetime(self):
        exp = int((datetime.datetime.now() + datetime.timedelta(hours=8)).timestamp())

        self.assertEqual(
            provider_utils.decode_token_expiry(_unsigned_jwt(exp)),
            datetime.datetime.fromtimestamp(exp),
        )

    def test_non_jwt_returns_none(self):
        self.assertIsNone(provider_utils.decode_token_expiry("not-a-jwt"))


class _LoginResponse:
    is_error = False

    def __init__(self, token: str):
        self._token = token

    def get_header(self, _name: str) -> str:
        return self._token


CACHE_KEY = "dpd_meta|u:TEST_USERNAME|001|test"


class TestDPDMetaTokenExpiry(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.gateway = karrio.gateway["dpd_meta"].create(
            dict(
                id="dpd_meta_auth_test",
                test_mode=True,
                carrier_id="dpd_meta",
                dpd_login="TEST_USERNAME",
                dpd_password="TEST_PASSWORD",
                dpd_bucode="001",
                customer_id="123456789",
                customer_account_number="ACC123456",
                account_country_code="DE",
            ),
            cache=lib.Cache(),
        )

    def _authenticate(self, token: str) -> dict:
        with mock.patch(
            "karrio.mappers.dpd_meta.proxy.lib.request_with_response",
            return_value=_LoginResponse(token),
        ):
            self.gateway.proxy.authenticate()
        return self.gateway.proxy.settings.connection_cache.get(CACHE_KEY)

    def test_get_token_stores_jwt_exp(self):
        exp = int((datetime.datetime.now() + datetime.timedelta(hours=8)).timestamp())
        token = _unsigned_jwt(exp)

        record = self._authenticate(token)

        self.assertDictEqual(
            record,
            {
                "access_token": token,
                "token_type": "Bearer",
                "expires_in": mock.ANY,
                "expiry": datetime.datetime.fromtimestamp(exp).strftime("%Y-%m-%d %H:%M:%S"),
            },
        )

    def test_non_jwt_token_falls_back_to_short_window(self):
        before = datetime.datetime.now()

        record = self._authenticate("fake_access_token_for_testing")

        stored = datetime.datetime.strptime(record["expiry"], "%Y-%m-%d %H:%M:%S")
        self.assertGreater(stored, before + datetime.timedelta(minutes=14))
        self.assertLess(stored, before + datetime.timedelta(minutes=16))


class TestDPDMetaTokenRetryOn401(unittest.TestCase):
    """When DPD rejects a cached META JWT (HTTP 401, per the vendor OpenAPI),
    create_shipment / schedule_pickup must invalidate the token and retry once
    with a fresh one, so a stale-but-recorded-valid token can't block a label.
    """

    def setUp(self):
        self.maxDiff = None
        self.gateway = karrio.gateway["dpd_meta"].create(
            dict(
                id="dpd_meta_retry_test",
                test_mode=True,
                carrier_id="dpd_meta",
                dpd_login="TEST_USERNAME",
                dpd_password="TEST_PASSWORD",
                dpd_bucode="001",
                customer_id="123456789",
                customer_account_number="ACC123456",
                account_country_code="DE",
            ),
            cache=lib.Cache(),
        )
        self.request = lib.Serializable(
            ShipmentRequest(
                service="dpd_meta_classic",
                shipper={"country_code": "DE", "postal_code": "10115", "city": "Berlin"},
                recipient={"country_code": "DE", "postal_code": "20095", "city": "Hamburg"},
                parcels=[{"weight": 1.0}],
            ),
            lambda _: {},
        )

    def _make_401(self):
        return HTTPError(url="x", code=401, msg="Unauthorized", hdrs=None, fp=mock.MagicMock(read=lambda: b"unauth"))

    def _manager(self, *tokens):
        manager = mock.MagicMock()
        manager.get_state.side_effect = list(tokens) if len(tokens) > 1 else None
        if len(tokens) == 1:
            manager.get_state.return_value = tokens[0]
        return manager

    def test_invalidates_and_retries_once_on_401(self):
        proxy = self.gateway.proxy
        manager = self._manager("stale_token", "fresh_token")

        def fake_request(headers=None, on_error=None, **kwargs):
            if "stale_token" in (headers or {}).get("Authorization", ""):
                return on_error(self._make_401())
            return '{"shipmentId": "1"}'

        with (
            mock.patch.object(proxy, "_token_manager", return_value=manager),
            mock.patch("karrio.mappers.dpd_meta.proxy.lib.request", side_effect=fake_request),
        ):
            proxy.create_shipment(self.request)

        self.assertEqual(manager.get_state.call_count, 2)
        manager.invalidate.assert_called_once()

    def test_no_retry_when_first_call_succeeds(self):
        proxy = self.gateway.proxy
        manager = self._manager("good_token")

        with (
            mock.patch.object(proxy, "_token_manager", return_value=manager),
            mock.patch("karrio.mappers.dpd_meta.proxy.lib.request", return_value='{"shipmentId": "1"}'),
        ):
            proxy.create_shipment(self.request)

        manager.invalidate.assert_not_called()
        self.assertEqual(manager.get_state.call_count, 1)

    def test_two_consecutive_401s_stop_after_one_retry(self):
        proxy = self.gateway.proxy
        manager = self._manager("t1", "t2")
        calls = {"n": 0}

        def always_401(headers=None, on_error=None, **kwargs):
            calls["n"] += 1
            return on_error(self._make_401())

        with (
            mock.patch.object(proxy, "_token_manager", return_value=manager),
            mock.patch("karrio.mappers.dpd_meta.proxy.lib.request", side_effect=always_401),
        ):
            proxy.create_shipment(self.request)

        self.assertEqual(calls["n"], 2)
        manager.invalidate.assert_called_once()

    def test_schedule_pickup_invalidates_and_retries_once_on_401(self):
        proxy = self.gateway.proxy
        manager = self._manager("stale_token", "fresh_token")

        def fake_request(headers=None, on_error=None, **kwargs):
            if "stale_token" in (headers or {}).get("Authorization", ""):
                return on_error(self._make_401())
            return '{"pickup": {}}'

        with (
            mock.patch.object(proxy, "_token_manager", return_value=manager),
            mock.patch("karrio.mappers.dpd_meta.proxy.lib.request", side_effect=fake_request),
        ):
            proxy.schedule_pickup(self.request)

        self.assertEqual(manager.get_state.call_count, 2)
        manager.invalidate.assert_called_once()


SOAP_AUTH_RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ns2:getAuthResponse xmlns:ns2="http://dpd.com/common/service/types/LoginService/2.0">
      <return>
        <delisId>TEST_USERNAME</delisId>
        <authToken>ws-token-abc123</authToken>
        <depot>0163</depot>
      </return>
    </ns2:getAuthResponse>
  </soap:Body>
</soap:Envelope>"""

SOAP_CACHE_KEY = "dpd_meta|ws|TEST_USERNAME|test"


class TestDPDMetaSoapTokenExpiry(unittest.TestCase):
    """The V2_0 LoginService response carries no real expiry, so the SOAP
    authToken must be cached for a SHORT window (correctness comes from the
    LOGIN_5/6 reactive refresh), never the old fabricated 24h.
    """

    def setUp(self):
        self.maxDiff = None
        self.gateway = karrio.gateway["dpd_meta"].create(
            dict(
                id="dpd_meta_soap_test",
                test_mode=True,
                carrier_id="dpd_meta",
                dpd_login="TEST_USERNAME",
                dpd_password="TEST_PASSWORD",
                dpd_bucode="001",
                customer_id="123456789",
                customer_account_number="ACC123456",
                account_country_code="DE",
            ),
            cache=lib.Cache(),
        )

    def test_public_ws_login_stores_short_window(self):
        before = datetime.datetime.now()

        with mock.patch(
            "karrio.mappers.dpd_meta.proxy.lib.request",
            return_value=SOAP_AUTH_RESPONSE,
        ):
            token, messages = self.gateway.proxy.authenticate_public_ws()

        self.assertEqual(token, "ws-token-abc123")
        self.assertEqual(messages, [])
        record = self.gateway.proxy.settings.connection_cache.get(SOAP_CACHE_KEY)
        stored = datetime.datetime.strptime(record["expiry"], "%Y-%m-%d %H:%M:%S")
        self.assertGreater(stored, before + datetime.timedelta(hours=1))
        self.assertLess(stored, before + datetime.timedelta(hours=4))


def _ws_login_fault(code: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <soap:Fault>
      <faultcode>soap:Server</faultcode>
      <faultstring>Fault occured</faultstring>
      <detail>
        <ns:authenticationFault xmlns:ns="http://dpd.com/common/service/types/Authentication/2.0">
          <errorCode>{code}</errorCode>
          <errorMessage>auth expired</errorMessage>
        </ns:authenticationFault>
      </detail>
    </soap:Fault>
  </soap:Body>
</soap:Envelope>"""


DEPOT_SUCCESS = """<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ns2:getDepotDataResponse xmlns:ns2="http://dpd.com/common/service/types/DepotDataService/1.0">
      <DepotData><depot>0163</depot><country>DE</country><zipCode>10115</zipCode></DepotData>
    </ns2:getDepotDataResponse>
  </soap:Body>
</soap:Envelope>"""


class TestDPDMetaSoapReactiveRefresh(unittest.TestCase):
    """An expired public-WS authToken surfaces as a SOAP LOGIN_5/LOGIN_6 fault
    (a body error, not an HTTP status), so get_locations must detect it, drop the
    cached authToken, re-login, and retry the depot call once.
    """

    def setUp(self):
        self.maxDiff = None
        self.gateway = karrio.gateway["dpd_meta"].create(
            dict(
                id="dpd_meta_ws_retry_test",
                test_mode=True,
                carrier_id="dpd_meta",
                dpd_login="TEST_USERNAME",
                dpd_password="TEST_PASSWORD",
                dpd_bucode="001",
                customer_id="123456789",
                customer_account_number="ACC123456",
                account_country_code="DE",
            ),
            cache=lib.Cache(),
        )
        self.request = lib.Serializable(None, lambda _: "<q>[AUTH_TOKEN]</q>", {"country": "DE", "zip_code": "10115"})

    def _run(self, depot_responses):
        proxy = self.gateway.proxy
        calls = {"login": 0, "depot": 0}

        def fake_request(url=None, **kwargs):
            if "LoginService" in url:
                calls["login"] += 1
                return SOAP_AUTH_RESPONSE
            depot = depot_responses[min(calls["depot"], len(depot_responses) - 1)]
            calls["depot"] += 1
            return depot

        with (
            mock.patch.object(
                proxy.settings.connection_cache,
                "delete",
                wraps=proxy.settings.connection_cache.delete,
            ) as spy_delete,
            mock.patch("karrio.mappers.dpd_meta.proxy.lib.request", side_effect=fake_request),
        ):
            result = proxy.get_locations(self.request).deserialize()
        return calls, spy_delete, result

    def test_login_5_triggers_one_reauth_and_retry(self):
        calls, spy_delete, result = self._run([_ws_login_fault("LOGIN_5"), DEPOT_SUCCESS])

        self.assertEqual(calls, {"login": 2, "depot": 2})
        spy_delete.assert_called_once_with(self.gateway.proxy._ws_auth_cache_key)
        self.assertIn("<depot>0163</depot>", result)

    def test_login_6_triggers_one_reauth_and_retry(self):
        calls, spy_delete, result = self._run([_ws_login_fault("LOGIN_6"), DEPOT_SUCCESS])

        self.assertEqual(calls, {"login": 2, "depot": 2})
        spy_delete.assert_called_once()
        self.assertIn("<depot>0163</depot>", result)

    def test_success_does_not_retry(self):
        calls, spy_delete, result = self._run([DEPOT_SUCCESS])

        self.assertEqual(calls, {"login": 1, "depot": 1})
        spy_delete.assert_not_called()
        self.assertIn("<depot>0163</depot>", result)

    def test_two_consecutive_login_5_stop_after_one_retry(self):
        calls, spy_delete, result = self._run([_ws_login_fault("LOGIN_5"), _ws_login_fault("LOGIN_5")])

        self.assertEqual(calls, {"login": 2, "depot": 2})
        spy_delete.assert_called_once()
        self.assertIn("LOGIN_5", result)

    def test_non_xml_depot_error_does_not_raise_or_retry(self):
        # RH-I7: a malformed/non-XML body must fall through, not raise in the loop.
        calls, spy_delete, result = self._run(["this is not xml <<<"])

        self.assertEqual(calls, {"login": 1, "depot": 1})
        spy_delete.assert_not_called()
        self.assertIn("not xml", result)


class TestDPDMetaBufferMinutes(unittest.TestCase):
    """buffer_minutes=5 keeps a short-lived (SEUR) token usable instead of
    forcing a re-login on every request, while still refreshing near expiry.
    """

    def setUp(self):
        self.maxDiff = None

    def _gateway(self, minutes_to_expiry):
        expiry = (datetime.datetime.now() + datetime.timedelta(minutes=minutes_to_expiry)).strftime("%Y-%m-%d %H:%M:%S")
        primed = {CACHE_KEY: {"access_token": "primed_token", "token_type": "Bearer", "expiry": expiry}}
        return karrio.gateway["dpd_meta"].create(
            dict(
                id="dpd_meta_buffer_test",
                test_mode=True,
                carrier_id="dpd_meta",
                dpd_login="TEST_USERNAME",
                dpd_password="TEST_PASSWORD",
                dpd_bucode="001",
                customer_id="123456789",
                customer_account_number="ACC123456",
                account_country_code="DE",
            ),
            cache=lib.Cache(**primed),
        )

    def test_token_with_20min_left_is_valid_no_relogin(self):
        gateway = self._gateway(20)

        with mock.patch("karrio.mappers.dpd_meta.proxy.lib.request_with_response") as mock_login:
            token = gateway.proxy._token_manager().get_state()

        self.assertEqual(token, "primed_token")
        mock_login.assert_not_called()

    def test_token_with_3min_left_triggers_refresh(self):
        gateway = self._gateway(3)
        fresh = _unsigned_jwt(int((datetime.datetime.now() + datetime.timedelta(hours=8)).timestamp()))

        with mock.patch(
            "karrio.mappers.dpd_meta.proxy.lib.request_with_response",
            return_value=_LoginResponse(fresh),
        ) as mock_login:
            token = gateway.proxy._token_manager().get_state()

        self.assertEqual(token, fresh)
        mock_login.assert_called_once()


if __name__ == "__main__":
    unittest.main()
