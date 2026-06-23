"""Regression tests for karrio.server.tracing.utils.set_tracing_context.

Covers the fix for the AttributeError crash when set_tracing_context is called
from a background task (e.g. karrio-data-import / buy_shipment_label) where
SessionContext.get_current_request() returns None and there is no tracer on the
thread-local request.
"""

import unittest
from unittest import mock


class TestSetTracingContextNoRequest(unittest.TestCase):
    """set_tracing_context must not raise when there is no current request."""

    def setUp(self):
        self.maxDiff = None

    def _call(self, **kwargs):
        """Import and call set_tracing_context with the given kwargs."""
        from karrio.server.tracing.utils import set_tracing_context

        set_tracing_context(**kwargs)

    @mock.patch("karrio.server.tracing.utils._propagate_to_sentry")
    @mock.patch("karrio.server.core.middleware.SessionContext.get_current_request", return_value=None)
    def test_does_not_raise_when_no_request(self, _mock_get_request, mock_sentry):
        """No AttributeError when get_current_request() returns None."""
        # Should complete without raising
        self._call(tracking_number="trk_test")
        mock_sentry.assert_called_once_with({"tracking_number": "trk_test"})

    @mock.patch("karrio.server.tracing.utils._propagate_to_sentry")
    @mock.patch("karrio.server.core.middleware.SessionContext.get_current_request", return_value=None)
    def test_sentry_still_called_when_no_request(self, _mock_get_request, mock_sentry):
        """_propagate_to_sentry is called unconditionally even without a request."""
        self._call(shipment_id="shp_abc", tracking_number="trk_xyz")
        mock_sentry.assert_called_once_with({"shipment_id": "shp_abc", "tracking_number": "trk_xyz"})

    @mock.patch("karrio.server.tracing.utils._propagate_to_sentry")
    def test_adds_context_when_request_has_tracer(self, mock_sentry):
        """When a request with a tracer is present, add_context receives the kwargs."""
        mock_tracer = mock.Mock()
        mock_request = mock.Mock()
        mock_request.tracer = mock_tracer

        with mock.patch(
            "karrio.server.core.middleware.SessionContext.get_current_request",
            return_value=mock_request,
        ):
            self._call(tracking_number="trk_with_tracer")

        mock_tracer.add_context.assert_called_once_with({"tracking_number": "trk_with_tracer"})
        mock_sentry.assert_called_once_with({"tracking_number": "trk_with_tracer"})

    @mock.patch("karrio.server.tracing.utils._propagate_to_sentry")
    def test_skips_tracer_when_request_has_no_tracer_attr(self, mock_sentry):
        """If request exists but has no .tracer attribute, add_context is not called."""
        mock_request = object()  # plain object — no .tracer attribute

        with mock.patch(
            "karrio.server.core.middleware.SessionContext.get_current_request",
            return_value=mock_request,
        ):
            self._call(object_id="obj_123")

        mock_sentry.assert_called_once_with({"object_id": "obj_123"})


if __name__ == "__main__":
    unittest.main()
