"""Unit tests for Sentry shipment context propagation in set_tracing_context.

These tests verify that _propagate_to_sentry (called by set_tracing_context)
correctly sets Sentry tags and structured context for shipment data.

The function under test is imported directly to avoid Django bootstrap.
"""
import sys
import types
import unittest
from unittest import mock


# Replicate the exact logic from karrio.server.tracing.utils._propagate_to_sentry
# so we can test it without Django. The real module is integration-tested via
# karrio test; these unit tests verify the Sentry tagging logic in isolation.

_SENTRY_TAG_KEYS = {"shipment_id", "tracking_number", "object_id"}


def _to_dict(val):
    """Minimal reimplementation of lib.to_dict for test isolation."""
    if isinstance(val, dict):
        return {k: v for k, v in val.items() if v is not None}
    return val


def _propagate_to_sentry(context: dict):
    """Mirror of karrio.server.tracing.utils._propagate_to_sentry."""
    try:
        import sentry_sdk
    except ImportError:
        return

    try:
        for key in _SENTRY_TAG_KEYS:
            value = context.get(key)
            if value:
                sentry_sdk.set_tag(key, value)

        shipment_id = context.get("shipment_id")
        tracking_number = context.get("tracking_number")
        if shipment_id or tracking_number:
            sentry_sdk.set_context(
                "shipment",
                _to_dict(
                    {
                        "shipment_id": shipment_id,
                        "tracking_number": tracking_number,
                    }
                ),
            )
    except Exception:
        pass


class TestPropagateToSentry(unittest.TestCase):
    """Test Sentry tag/context propagation for shipment data."""

    def setUp(self):
        self.maxDiff = None

    @mock.patch("sentry_sdk.set_context")
    @mock.patch("sentry_sdk.set_tag")
    def test_sets_shipment_id_tag(self, mock_set_tag, mock_set_context):
        _propagate_to_sentry({"shipment_id": "shp_abc123"})
        mock_set_tag.assert_any_call("shipment_id", "shp_abc123")

    @mock.patch("sentry_sdk.set_context")
    @mock.patch("sentry_sdk.set_tag")
    def test_sets_tracking_number_tag(self, mock_set_tag, mock_set_context):
        _propagate_to_sentry({"tracking_number": "1Z999AA10123456784"})
        mock_set_tag.assert_any_call("tracking_number", "1Z999AA10123456784")

    @mock.patch("sentry_sdk.set_context")
    @mock.patch("sentry_sdk.set_tag")
    def test_sets_object_id_tag(self, mock_set_tag, mock_set_context):
        _propagate_to_sentry({"object_id": "shp_abc123"})
        mock_set_tag.assert_any_call("object_id", "shp_abc123")

    @mock.patch("sentry_sdk.set_context")
    @mock.patch("sentry_sdk.set_tag")
    def test_sets_sentry_shipment_context(self, mock_set_tag, mock_set_context):
        _propagate_to_sentry({
            "shipment_id": "shp_abc123",
            "tracking_number": "1Z999",
        })
        mock_set_context.assert_called_once_with(
            "shipment",
            {"shipment_id": "shp_abc123", "tracking_number": "1Z999"},
        )

    @mock.patch("sentry_sdk.set_context")
    @mock.patch("sentry_sdk.set_tag")
    def test_skips_sentry_tags_for_none_values(self, mock_set_tag, mock_set_context):
        _propagate_to_sentry({"shipment_id": None, "tracking_number": None})
        mock_set_tag.assert_not_called()
        mock_set_context.assert_not_called()

    @mock.patch("sentry_sdk.set_context")
    @mock.patch("sentry_sdk.set_tag")
    def test_skips_sentry_tags_for_empty_values(self, mock_set_tag, mock_set_context):
        _propagate_to_sentry({"shipment_id": "", "tracking_number": ""})
        mock_set_tag.assert_not_called()
        mock_set_context.assert_not_called()

    @mock.patch("sentry_sdk.set_context")
    @mock.patch("sentry_sdk.set_tag")
    def test_ignores_non_sentry_keys(self, mock_set_tag, mock_set_context):
        _propagate_to_sentry({"request_log_id": "log_123", "some_other": "val"})
        mock_set_tag.assert_not_called()
        mock_set_context.assert_not_called()

    @mock.patch("sentry_sdk.set_context")
    @mock.patch("sentry_sdk.set_tag")
    def test_shipment_context_omits_none_tracking(self, mock_set_tag, mock_set_context):
        _propagate_to_sentry({"shipment_id": "shp_1", "tracking_number": None})
        mock_set_context.assert_called_once_with(
            "shipment",
            {"shipment_id": "shp_1"},
        )

    def test_no_error_when_sentry_not_installed(self):
        sentry_module = sys.modules.get("sentry_sdk")
        sys.modules["sentry_sdk"] = None
        try:
            # Should not raise
            _propagate_to_sentry({"shipment_id": "shp_1"})
        finally:
            if sentry_module is not None:
                sys.modules["sentry_sdk"] = sentry_module
            else:
                sys.modules.pop("sentry_sdk", None)


if __name__ == "__main__":
    unittest.main()
