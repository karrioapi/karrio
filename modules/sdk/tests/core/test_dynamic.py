"""Tests for karrio.core.dynamic (opt-in dynamic carrier metadata)."""

import datetime
import time
import unittest
from unittest import mock

import attr
import karrio.core.dynamic as dynamic
import karrio.lib as lib

# Expected shape for an error/empty DynamicMetadata after a failed fetch.
# Using a full-dict expected value here (instead of per-field assertions)
# catches accidental field additions/typos — see .claude/rules/testing.md.
ERROR_METADATA_DICT = {
    "services": [],
    "options": [],
    "service_availability": {},
    "connection_config_defaults": {},
    "raw": mock.ANY,  # "timeout" or "<exception str>"
    "source": "error",
    "fetched_at": mock.ANY,
    "ttl_seconds": 1,  # _FakeSettings.dynamic_negative_ttl_seconds
    "exclusive": False,
}


def _payload(name: str = "x") -> dynamic.DynamicMetadata:
    return dynamic.DynamicMetadata(
        connection_config_defaults={"default_consigner_id": name},
        source="profile",
        fetched_at=datetime.datetime.now(datetime.UTC),
        ttl_seconds=3600,
    )


class _FakeSettings(dynamic.DynamicMetadataMixin):
    """Minimal stand-in for a real connector Settings used by tests."""

    carrier_name = "fake"
    carrier_id = "fake"
    id = "test-connection-1"
    username = None

    dynamic_ttl_seconds = 60
    dynamic_timeout_seconds = 0.2
    dynamic_negative_ttl_seconds = 1

    def __init__(self):
        self._fetch_calls = 0
        self._fetch_result = _payload()
        self._fetch_raises = None
        self._fetch_sleep = 0.0
        self.connection_cache = lib.Cache()

    def fetch_dynamic_metadata(self) -> dynamic.DynamicMetadata:
        self._fetch_calls += 1
        if self._fetch_sleep:
            time.sleep(self._fetch_sleep)
        if self._fetch_raises is not None:
            raise self._fetch_raises
        return self._fetch_result


class TestDynamicMetadataValueObject(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_empty_is_empty(self):
        empty = dynamic.DynamicMetadata.empty()
        self.assertTrue(empty.is_empty)
        self.assertEqual(empty.source, "static")
        self.assertIsNotNone(empty.fetched_at)

    def test_non_empty_when_any_field_populated(self):
        m = dynamic.DynamicMetadata(connection_config_defaults={"k": "v"})
        self.assertFalse(m.is_empty)


class TestDynamicMetadataMixin(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.settings = _FakeSettings()

    def test_cache_key_includes_carrier_and_connection(self):
        self.assertEqual(
            self.settings.dynamic_cache_key(),
            "karrio.dynamic.fake.test-connection-1",
        )

    def test_first_call_fetches_then_caches(self):
        first = self.settings.get_dynamic_metadata()
        second = self.settings.get_dynamic_metadata()

        self.assertEqual(self.settings._fetch_calls, 1)
        self.assertEqual(first.connection_config_defaults["default_consigner_id"], "x")
        self.assertIs(first, second)

    def test_invalidate_forces_refetch(self):
        self.settings.get_dynamic_metadata()
        self.settings.invalidate_dynamic_metadata()
        self.settings.get_dynamic_metadata()
        self.assertEqual(self.settings._fetch_calls, 2)

    def test_timeout_returns_error_source_and_short_cache(self):
        self.settings._fetch_sleep = 0.5  # > 0.2s timeout
        metadata = self.settings.get_dynamic_metadata()

        self.assertDictEqual(
            attr.asdict(metadata),
            {**ERROR_METADATA_DICT, "raw": {"error": "timeout"}},
        )

    def test_exception_returns_error_source(self):
        self.settings._fetch_raises = RuntimeError("vendor 500")
        metadata = self.settings.get_dynamic_metadata()

        self.assertDictEqual(
            attr.asdict(metadata),
            {**ERROR_METADATA_DICT, "raw": {"error": "vendor 500"}},
        )

    def test_negative_cache_short_circuits_subsequent_calls(self):
        self.settings._fetch_raises = RuntimeError("down")
        self.settings.get_dynamic_metadata()
        self.settings.get_dynamic_metadata()

        # Negative-cached: only one fetch despite two calls.
        self.assertEqual(self.settings._fetch_calls, 1)

    def test_cache_expiry_refetches(self):
        # Force an "old" cached entry by lying about fetched_at.
        stale = _payload("old")
        stale.fetched_at = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=2)
        stale.ttl_seconds = 60
        self.settings.connection_cache.set(self.settings.dynamic_cache_key(), stale)

        fresh = self.settings.get_dynamic_metadata()

        self.assertEqual(self.settings._fetch_calls, 1)
        self.assertEqual(fresh.connection_config_defaults["default_consigner_id"], "x")

    def test_subclass_without_fetch_raises_not_implemented(self):
        class _Bare(dynamic.DynamicMetadataMixin):
            carrier_name = "bare"
            carrier_id = "bare"
            id = "1"
            connection_cache = lib.Cache()

        bare = _Bare()
        result = bare.get_dynamic_metadata()
        # NotImplementedError is caught by the same handler as any other exception
        # → returns the "error" sentinel rather than blowing up the request path.
        self.assertEqual(result.source, "error")
        self.assertTrue(result.is_empty)

    def test_subclass_can_isinstance_check_from_outside(self):
        # Server-side code uses this to decide whether to call the hydrator.
        self.assertIsInstance(self.settings, dynamic.DynamicMetadataMixin)


if __name__ == "__main__":
    unittest.main()
