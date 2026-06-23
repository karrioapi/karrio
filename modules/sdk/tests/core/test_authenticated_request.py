import datetime
import io
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from karrio.core.utils.caching import Cache
from karrio.lib import authenticated_request


def _make_http_error(code: int, body: bytes = b"") -> HTTPError:
    """Construct a real HTTPError instance for on_error path testing."""
    return HTTPError(
        url="https://example.test/api",
        code=code,
        msg=f"HTTP {code}",
        hdrs={},  # type: ignore[arg-type]
        fp=io.BytesIO(body),
    )


def _future_expiry() -> str:
    return (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")


class TestAuthenticatedRequest(unittest.TestCase):
    """Tests for ``lib.authenticated_request`` — the SDK helper that wraps
    ``lib.request`` with bearer-token auth and a single retry on auth
    rejection. Carrier proxies should call this directly instead of
    re-implementing the invalidate-and-retry dance per carrier.
    """

    def setUp(self):
        self.maxDiff = None
        self.cache = Cache()
        self.refresh_calls: list[int] = []

        def refresh():
            self.refresh_calls.append(len(self.refresh_calls) + 1)
            return {
                "access_token": f"tok-{len(self.refresh_calls)}",
                "expiry": _future_expiry(),
            }

        self.refresh = refresh
        self.manager = self.cache.thread_safe(refresh_func=refresh, cache_key="carrier|cid|csecret")

    # ------------------------------------------------------------------
    # Happy path
    # ------------------------------------------------------------------

    def test_success_on_first_attempt_calls_request_once(self):
        captured_calls: list[dict] = []

        def fake_request(*, headers, on_error, **kwargs):
            captured_calls.append({"headers": dict(headers), "kwargs": kwargs})
            return "OK"

        with patch("karrio.lib.request", side_effect=fake_request):
            result = authenticated_request(
                self.manager,
                url="https://example.test/api/orders",
                method="POST",
                data="{}",
            )

        self.assertEqual(result, "OK")
        self.assertEqual(len(captured_calls), 1, "no retry on success")
        self.assertEqual(len(self.refresh_calls), 1, "token issued once")
        self.assertEqual(captured_calls[0]["headers"]["Authorization"], "Bearer tok-1")

    def test_caller_headers_are_preserved_and_merged(self):
        """The Authorization header must not clobber caller-supplied headers."""
        seen_headers: list[dict] = []

        def fake_request(*, headers, on_error, **kwargs):
            seen_headers.append(dict(headers))
            return "OK"

        with patch("karrio.lib.request", side_effect=fake_request):
            authenticated_request(
                self.manager,
                url="https://example.test/api",
                method="POST",
                headers={"content-type": "application/json", "Accept-Language": "de"},
            )

        self.assertEqual(seen_headers[0]["content-type"], "application/json")
        self.assertEqual(seen_headers[0]["Accept-Language"], "de")
        self.assertEqual(seen_headers[0]["Authorization"], "Bearer tok-1")

    # ------------------------------------------------------------------
    # 401/403 retry
    # ------------------------------------------------------------------

    def test_401_invalidates_token_and_retries_once(self):
        attempts: list[str] = []

        def fake_request(*, headers, on_error, **kwargs):
            attempts.append(headers["Authorization"])
            if len(attempts) == 1:
                return on_error(_make_http_error(401, b'{"error":"invalid_token"}'))
            return '{"ok":true}'

        with patch("karrio.lib.request", side_effect=fake_request):
            result = authenticated_request(
                self.manager,
                url="https://example.test/api",
                method="POST",
            )

        self.assertEqual(result, '{"ok":true}')
        self.assertEqual(len(attempts), 2, "expected one retry")
        self.assertEqual(attempts[0], "Bearer tok-1")
        self.assertEqual(attempts[1], "Bearer tok-2", "fresh token after invalidate")
        self.assertEqual(len(self.refresh_calls), 2, "token refreshed exactly twice")

    def test_403_also_triggers_retry(self):
        attempts: list[str] = []

        def fake_request(*, headers, on_error, **kwargs):
            attempts.append(headers["Authorization"])
            if len(attempts) == 1:
                return on_error(_make_http_error(403))
            return "OK"

        with patch("karrio.lib.request", side_effect=fake_request):
            result = authenticated_request(self.manager, url="https://example.test/api", method="GET")

        self.assertEqual(result, "OK")
        self.assertEqual(len(attempts), 2)

    def test_double_401_returns_error_body_without_third_attempt(self):
        attempts: list[int] = []

        def fake_request(*, headers, on_error, **kwargs):
            attempts.append(1)
            return on_error(_make_http_error(401, b'{"error":"still_invalid"}'))

        with patch("karrio.lib.request", side_effect=fake_request):
            result = authenticated_request(self.manager, url="https://example.test/api", method="POST")

        # Default error decoder returns the decoded body so the existing
        # parse_*_response parsers handle the carrier's error envelope.
        self.assertEqual(result, '{"error":"still_invalid"}')
        self.assertEqual(len(attempts), 2, "exactly two attempts, no third")

    # ------------------------------------------------------------------
    # Non-auth errors are not retried
    # ------------------------------------------------------------------

    def test_500_is_not_retried(self):
        attempts: list[int] = []

        def fake_request(*, headers, on_error, **kwargs):
            attempts.append(1)
            return on_error(_make_http_error(500, b"internal server error"))

        with patch("karrio.lib.request", side_effect=fake_request):
            result = authenticated_request(self.manager, url="https://example.test/api", method="POST")

        self.assertEqual(result, "internal server error")
        self.assertEqual(len(attempts), 1, "500 must not trigger token invalidate")
        self.assertEqual(len(self.refresh_calls), 1)

    def test_400_is_not_retried(self):
        attempts: list[int] = []

        def fake_request(*, headers, on_error, **kwargs):
            attempts.append(1)
            return on_error(_make_http_error(400, b'{"error":"bad request"}'))

        with patch("karrio.lib.request", side_effect=fake_request):
            result = authenticated_request(self.manager, url="https://example.test/api", method="POST")

        self.assertEqual(result, '{"error":"bad request"}')
        self.assertEqual(len(attempts), 1)

    # ------------------------------------------------------------------
    # Caller customisation
    # ------------------------------------------------------------------

    def test_custom_auth_header_for_non_bearer_schemes(self):
        """Carriers using ``X-Token`` or HTTP Basic can supply a callable."""
        seen_headers: list[dict] = []

        def fake_request(*, headers, on_error, **kwargs):
            seen_headers.append(dict(headers))
            return "OK"

        with patch("karrio.lib.request", side_effect=fake_request):
            authenticated_request(
                self.manager,
                auth_header=lambda tok: {"X-API-Token": tok},
                url="https://example.test/api",
                method="GET",
            )

        self.assertNotIn("Authorization", seen_headers[0])
        self.assertEqual(seen_headers[0]["X-API-Token"], "tok-1")

    def test_callers_on_error_is_invoked_on_each_attempt(self):
        """If the caller passes ``on_error`` it must still receive the error
        from both attempts; the SDK helper sniffs the status independently."""
        delegate_calls: list[int] = []

        def caller_on_error(err):
            delegate_calls.append(err.code)
            return f"<decoded {err.code}>"

        attempts: list[int] = []

        def fake_request(*, headers, on_error, **kwargs):
            attempts.append(1)
            # Always 401 — verify caller's on_error is invoked both times
            # and that the final return value comes from caller_on_error,
            # not the default decoder.
            return on_error(_make_http_error(401, b"ignored"))

        with patch("karrio.lib.request", side_effect=fake_request):
            result = authenticated_request(
                self.manager,
                on_error=caller_on_error,
                url="https://example.test/api",
                method="POST",
            )

        self.assertEqual(result, "<decoded 401>")
        self.assertEqual(delegate_calls, [401, 401])
        self.assertEqual(len(attempts), 2)

    def test_custom_retry_on_statuses_widens_retry_set(self):
        attempts: list[int] = []

        def fake_request(*, headers, on_error, **kwargs):
            attempts.append(1)
            if len(attempts) == 1:
                return on_error(_make_http_error(419))
            return "OK"

        with patch("karrio.lib.request", side_effect=fake_request):
            result = authenticated_request(
                self.manager,
                retry_on_statuses=(419, 401),
                url="https://example.test/api",
                method="POST",
            )

        self.assertEqual(result, "OK")
        self.assertEqual(len(attempts), 2)


if __name__ == "__main__":
    unittest.main()
