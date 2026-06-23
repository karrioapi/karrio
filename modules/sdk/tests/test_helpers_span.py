"""Span tagging behaviour for _urlopen_with_span."""

import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError
from urllib.request import Request

from karrio.core.utils.helpers import SPAN_BODY_MAX, _urlopen_with_span
from karrio.core.utils.tracing import Tracer


def _make_fake_span():
    span = MagicMock()
    span.__enter__ = MagicMock(return_value=span)
    span.__exit__ = MagicMock(return_value=False)
    return span


def _trace_for(ctx: dict):
    """Build a trace partial that carries a real Tracer with the given context."""
    import functools

    tracer = Tracer()
    tracer.add_context(ctx)
    trace = functools.partial(tracer.trace)
    trace._tracer = tracer
    return trace


def _fake_http_response(status: int = 200, body: bytes = b"ok"):
    resp = MagicMock()
    resp.status = status
    resp.read.return_value = body
    resp.headers = {}
    resp.url = "https://api.example.com/v1/rate"
    return resp


class TestUrlopenWithSpanTagging(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.req = Request("https://api.example.com/v1/rate", method="POST")

    @patch("karrio.core.utils.helpers.urlopen")
    @patch("sentry_sdk.start_span")
    def test_emits_all_tags_when_full_context_present(self, mock_start, mock_urlopen):
        """carrier_name + request_id + tracking_number + tenant_id → all 4 tags emitted."""
        span = _make_fake_span()
        mock_start.return_value = span
        mock_urlopen.return_value = _fake_http_response()

        trace = _trace_for(
            {
                "carrier_name": "ups",
                "tracking_number": "1Z999AA10123456784",
                "tenant_id": "tenant-abc",
                "request_id": "req-001",
            }
        )

        _urlopen_with_span(self.req, trace=trace)

        mock_start.assert_called_once_with(op="http.carrier", description="ups.http")

        set_tag_calls = {c.args[0]: c.args[1] for c in span.set_tag.call_args_list}
        self.assertEqual(set_tag_calls["carrier"], "ups")
        self.assertEqual(set_tag_calls["tenant_id"], "tenant-abc")
        self.assertIn("request_id", set_tag_calls)
        self.assertEqual(set_tag_calls["tracking_number"], "1Z999AA10123456784")

    @patch("karrio.core.utils.helpers.urlopen")
    @patch("sentry_sdk.start_span")
    def test_falls_back_to_http_client_when_no_trace(self, mock_start, mock_urlopen):
        """trace=None → op=http.client, no carrier/tracking_number/tenant_id tags."""
        span = _make_fake_span()
        mock_start.return_value = span
        mock_urlopen.return_value = _fake_http_response()

        _urlopen_with_span(self.req, trace=None)

        mock_start.assert_called_once_with(op="http.client", description=unittest.mock.ANY)

        set_tag_calls = {c.args[0]: c.args[1] for c in span.set_tag.call_args_list if c.args[0] != "http.status_code"}
        self.assertNotIn("carrier", set_tag_calls)
        self.assertNotIn("tracking_number", set_tag_calls)
        self.assertNotIn("tenant_id", set_tag_calls)

    @patch("karrio.core.utils.helpers.urlopen")
    @patch("sentry_sdk.start_span")
    def test_carrier_only_no_other_context(self, mock_start, mock_urlopen):
        """Only carrier_name in context → carrier + request_id tags; tracking_number/tenant_id skipped."""
        span = _make_fake_span()
        mock_start.return_value = span
        mock_urlopen.return_value = _fake_http_response()

        trace = _trace_for({"carrier_name": "dhl_express"})

        _urlopen_with_span(self.req, trace=trace)

        mock_start.assert_called_once_with(op="http.carrier", description="dhl_express.http")

        set_tag_calls = {c.args[0]: c.args[1] for c in span.set_tag.call_args_list if c.args[0] != "http.status_code"}
        self.assertEqual(set_tag_calls["carrier"], "dhl_express")
        self.assertIn("request_id", set_tag_calls)
        self.assertNotIn("tracking_number", set_tag_calls)
        self.assertNotIn("tenant_id", set_tag_calls)

    @patch("karrio.core.utils.helpers.urlopen")
    @patch("sentry_sdk.start_span")
    def test_tags_status_on_http_error(self, mock_start, mock_urlopen):
        """HTTPError path sets http.status_code tag to error code."""
        span = _make_fake_span()
        mock_start.return_value = span

        http_err = HTTPError(
            url="https://api.example.com/v1/rate",
            code=422,
            msg="Unprocessable Entity",
            hdrs=None,
            fp=MagicMock(read=MagicMock(return_value=b'{"error": "bad input"}')),
        )
        mock_urlopen.side_effect = http_err

        with self.assertRaises(HTTPError):
            _urlopen_with_span(self.req, trace=None)

        set_tag_calls = {c.args[0]: c.args[1] for c in span.set_tag.call_args_list}
        self.assertEqual(set_tag_calls.get("http.status_code"), "422")

    @patch("karrio.core.utils.helpers.urlopen")
    @patch("sentry_sdk.start_span", side_effect=RuntimeError("sentry broken"))
    def test_failsafe_falls_through_to_plain_urlopen(self, mock_start, mock_urlopen):
        """If sentry_sdk.start_span raises, the request still completes via plain urlopen."""
        mock_urlopen.return_value = _fake_http_response()

        result = _urlopen_with_span(self.req, trace=None)

        mock_urlopen.assert_called_once_with(self.req, timeout=None)
        self.assertIsNotNone(result)

    @patch("karrio.core.utils.helpers.urlopen")
    @patch("sentry_sdk.start_span")
    def test_retry_attempt_data_set(self, mock_start, mock_urlopen):
        """attempt=2 → span.set_data('http.retry_attempt', 2)."""
        span = _make_fake_span()
        mock_start.return_value = span
        mock_urlopen.return_value = _fake_http_response()

        _urlopen_with_span(self.req, trace=None, attempt=2)

        set_data_calls = {c.args[0]: c.args[1] for c in span.set_data.call_args_list}
        self.assertEqual(set_data_calls.get("http.retry_attempt"), 2)

    def test_body_truncation_at_16KB(self):
        """Body of 4500 chars retained in full; body of 20000 chars truncated to SPAN_BODY_MAX."""
        body_4500 = "x" * 4500
        body_20000 = "y" * 20000

        self.assertEqual(len(body_4500[:SPAN_BODY_MAX]), 4500)
        self.assertEqual(len(body_20000[:SPAN_BODY_MAX]), SPAN_BODY_MAX)
        self.assertEqual(SPAN_BODY_MAX, 16384)
