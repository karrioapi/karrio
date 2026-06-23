"""Tests for the _sentry_before_send_transaction hook wiring in apm.py."""

import logging
import unittest
from unittest import mock

from karrio.server.core.tests._logging_helpers import capture_records


def _import_hook():
    with mock.patch.dict("os.environ", {"SENTRY_DSN": ""}):
        from karrio.server.settings.apm import _sentry_before_send_transaction

        return _sentry_before_send_transaction


class TestSentryBeforeSendTransaction(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.hook = _import_hook()

    def _event(self, transaction="/api/v1/shipments/", spans=None):
        return {"transaction": transaction, "spans": spans or []}

    def test_leaky_span_body_is_scrubbed(self):
        body = (
            '{"recipient": {"name": "Klaus Wagner", "email": "k.wagner@gmx.de", '
            '"phone": "+49 172 9876543"}, "service": "V01PAK"}'
        )
        event = self._event(spans=[{"data": {"http.request.body": body, "http.status_code": 200}}])
        result = self.hook(event, {})
        self.assertIsNotNone(result)
        scrubbed_body = result["spans"][0]["data"]["http.request.body"]
        self.assertNotIn("Klaus Wagner", scrubbed_body)
        self.assertNotIn("k.wagner@gmx.de", scrubbed_body)
        self.assertNotIn("+49 172 9876543", scrubbed_body)
        self.assertIn("V01PAK", scrubbed_body)
        self.assertEqual(result["spans"][0]["data"]["http.status_code"], 200)

    def test_no_spans_returns_event_unchanged(self):
        event = self._event(spans=[])
        result = self.hook(event, {})
        self.assertIs(result, event)

    def test_engine_error_returns_event_not_none(self):
        import karrio.server.core.telemetry_scrubbing as mod

        body = '{"recipient": {"name": "Anna Müller"}}'
        event = self._event(spans=[{"data": {"http.request.body": body}}])
        with mock.patch.object(mod, "scrub_span_data", side_effect=RuntimeError("boom")):
            result = self.hook(event, {})
        # Must return event unchanged, NEVER None (None drops the transaction)
        self.assertIs(result, event)

    def test_noisy_endpoint_still_dropped(self):
        event = self._event(transaction="/health")
        result = self.hook(event, {})
        self.assertIsNone(result)

    def test_non_target_span_keys_unchanged(self):
        event = self._event(spans=[{"data": {"db.statement": "SELECT 1", "http.status_code": 200}}])
        result = self.hook(event, {})
        self.assertEqual(result["spans"][0]["data"]["db.statement"], "SELECT 1")
        self.assertEqual(result["spans"][0]["data"]["http.status_code"], 200)


class TestWawiDiagnosticLogging(unittest.TestCase):
    """SHIP2-1185 commit 4 — _sentry_before_send_transaction emits
    `sentry.before_send_transaction.ok` / `.raised` log lines for
    transactions whose name starts with `/v1/wawi/`, and nothing for
    other transactions. Gives STG pod-log observability.

    NOTE: cannot use `self.assertLogs(...)` because the project routes
    stdlib logging through Loguru's `InterceptHandler` on the root logger
    (see karrio.server.core.logging.setup_django_loguru). A direct
    handler on the named logger captures records reliably whether
    Loguru is active or not."""

    APM_LOGGER = "karrio.server.settings.apm"

    def setUp(self):
        self.maxDiff = None
        self.hook = _import_hook()

    def _event(self, transaction, spans=None):
        return {"transaction": transaction, "spans": spans or []}

    def _carrier_span(self):
        return {
            "op": "http.carrier",
            "data": {"http.url": "https://api-sandbox.dhl.com/x", "http.request.body": "Hans Müller"},
        }

    def _capture_records(self, logger_name, level=logging.DEBUG):
        return capture_records(self, logger_name, level=level)

    def test_wawi_success_emits_info(self):
        records = self._capture_records(self.APM_LOGGER, level=logging.INFO)
        event = self._event(
            "/v1/wawi/shipment",
            spans=[self._carrier_span(), {"op": "db", "data": {"db.statement": "SELECT 1"}}],
        )
        result = self.hook(event, {})
        self.assertIsNotNone(result)
        ok = [r.getMessage() for r in records if "sentry.before_send_transaction.ok" in r.getMessage()]
        self.assertEqual(len(ok), 1, f"expected exactly one .ok line, got {[r.getMessage() for r in records]!r}")
        line = ok[0]
        self.assertIn("txn=/v1/wawi/shipment", line)
        self.assertIn("spans=2", line)
        self.assertIn("carrier=1", line)
        self.assertIn("dur_ms=", line)

    def test_non_wawi_transaction_emits_no_diagnostic(self):
        records = self._capture_records(self.APM_LOGGER)
        event = self._event("/api/v1/shipments/", spans=[self._carrier_span()])
        self.hook(event, {})
        diagnostic = [r.getMessage() for r in records if "sentry.before_send_transaction." in r.getMessage()]
        self.assertEqual(
            diagnostic,
            [],
            f"non-wawi transactions must not emit diagnostic; got {diagnostic!r}",
        )

    def test_noisy_endpoint_emits_no_diagnostic(self):
        records = self._capture_records(self.APM_LOGGER)
        event = self._event("/health", spans=[self._carrier_span()])
        result = self.hook(event, {})
        self.assertIsNone(result)
        diagnostic = [r.getMessage() for r in records if "sentry.before_send_transaction." in r.getMessage()]
        self.assertEqual(diagnostic, [])

    def test_wawi_failure_path_emits_warning_with_exc_info(self):
        import karrio.server.core.telemetry_scrubbing as mod

        records = self._capture_records(self.APM_LOGGER, level=logging.WARNING)
        event = self._event("/v1/wawi/shipment", spans=[self._carrier_span()])
        with mock.patch.object(mod, "scrub_span_data", side_effect=RuntimeError("induced")):
            result = self.hook(event, {})
        # Hook must return the event (never None) so the transaction isn't dropped.
        self.assertIsNotNone(result)
        raised = [r for r in records if "sentry.before_send_transaction.raised" in r.getMessage()]
        self.assertEqual(
            len(raised), 1, f"expected exactly one .raised line, got {[r.getMessage() for r in records]!r}"
        )
        rec = raised[0]
        self.assertIn("txn=/v1/wawi/shipment", rec.getMessage())
        # exc_info=True attaches the original exception info to the record.
        self.assertIsNotNone(rec.exc_info, "warning must include exc_info traceback")
        self.assertIs(rec.exc_info[0], RuntimeError)
        self.assertEqual(str(rec.exc_info[1]), "induced")


if __name__ == "__main__":
    unittest.main()
