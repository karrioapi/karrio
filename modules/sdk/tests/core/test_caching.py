import unittest
import datetime

from karrio.core.utils.caching import Cache, ThreadSafeTokenManager


class TestCacheVersion(unittest.TestCase):
    """Tests for Cache version-based cache invalidation."""

    def setUp(self):
        self.maxDiff = None

    def test_cache_stores_version(self):
        cache = Cache(version="1234")
        self.assertEqual(cache._version, "1234")

    def test_cache_default_version_is_empty(self):
        cache = Cache()
        self.assertEqual(cache._version, "")

    def test_thread_safe_appends_version_to_cache_key(self):
        cache = Cache(version="1700000000.0")
        manager = cache.thread_safe(
            refresh_func=lambda: {},
            cache_key="carrier|client_id|client_secret",
        )
        self.assertEqual(
            manager.cache_key,
            "carrier|client_id|client_secret|v:1700000000.0",
        )

    def test_thread_safe_no_version_leaves_key_unchanged(self):
        cache = Cache()
        manager = cache.thread_safe(
            refresh_func=lambda: {},
            cache_key="carrier|client_id|client_secret",
        )
        self.assertEqual(
            manager.cache_key,
            "carrier|client_id|client_secret",
        )

    def test_different_versions_produce_different_keys(self):
        cache_v1 = Cache(version="1")
        cache_v2 = Cache(version="2")

        manager_v1 = cache_v1.thread_safe(
            refresh_func=lambda: {},
            cache_key="carrier|id|secret",
        )
        manager_v2 = cache_v2.thread_safe(
            refresh_func=lambda: {},
            cache_key="carrier|id|secret",
        )

        self.assertNotEqual(manager_v1.cache_key, manager_v2.cache_key)
        self.assertEqual(manager_v1.cache_key, "carrier|id|secret|v:1")
        self.assertEqual(manager_v2.cache_key, "carrier|id|secret|v:2")


class TestCacheGetSet(unittest.TestCase):
    """Tests for Cache basic get/set operations."""

    def test_set_and_get_value(self):
        cache = Cache()
        cache.set("key", "value")
        self.assertEqual(cache.get("key"), "value")

    def test_get_returns_none_for_missing_key(self):
        cache = Cache()
        self.assertIsNone(cache.get("nonexistent"))

    def test_init_kwargs_populate_cache(self):
        cache = Cache(token="abc123")
        self.assertEqual(cache.get("token"), "abc123")


class TestThreadSafeTokenManager(unittest.TestCase):
    """Tests for ThreadSafeTokenManager token lifecycle."""

    def setUp(self):
        self.maxDiff = None
        self.future_expiry = (
            datetime.datetime.now() + datetime.timedelta(hours=2)
        ).strftime("%Y-%m-%d %H:%M:%S")
        self.past_expiry = (
            datetime.datetime.now() - datetime.timedelta(hours=1)
        ).strftime("%Y-%m-%d %H:%M:%S")

    def test_get_token_calls_refresh_when_no_cached_token(self):
        cache = Cache()
        refresh_called = {"count": 0}

        def mock_refresh():
            refresh_called["count"] += 1
            return {
                "access_token": "fresh_token",
                "expiry": self.future_expiry,
            }

        manager = cache.thread_safe(
            refresh_func=mock_refresh,
            cache_key="test|key",
        )

        token = manager.get_token()
        self.assertEqual(token, "fresh_token")
        self.assertEqual(refresh_called["count"], 1)

    def test_get_token_returns_cached_token_when_valid(self):
        cache = Cache()
        refresh_called = {"count": 0}

        def mock_refresh():
            refresh_called["count"] += 1
            return {
                "access_token": "fresh_token",
                "expiry": self.future_expiry,
            }

        manager = cache.thread_safe(
            refresh_func=mock_refresh,
            cache_key="test|key",
        )

        # First call triggers refresh
        manager.get_token()
        self.assertEqual(refresh_called["count"], 1)

        # Second call should use cached token
        token = manager.get_token()
        self.assertEqual(token, "fresh_token")
        self.assertEqual(refresh_called["count"], 1)

    def test_get_token_refreshes_when_expired(self):
        cache = Cache()
        call_count = {"n": 0}

        def mock_refresh():
            call_count["n"] += 1
            return {
                "access_token": f"token_{call_count['n']}",
                "expiry": self.future_expiry,
            }

        manager = cache.thread_safe(
            refresh_func=mock_refresh,
            cache_key="test|key",
            buffer_minutes=0,
        )

        # First call triggers refresh
        token = manager.get_token()
        self.assertEqual(token, "token_1")
        self.assertEqual(call_count["n"], 1)

        # Simulate expiry by setting an expired token in cache
        cache.set(manager.cache_key, {
            "access_token": "token_1",
            "expiry": self.past_expiry,
        })

        # Next call should trigger a new refresh
        token = manager.get_token()
        self.assertEqual(token, "token_2")
        self.assertEqual(call_count["n"], 2)

    def test_get_token_raises_value_error_when_refresh_returns_no_token(self):
        cache = Cache()
        manager = cache.thread_safe(
            refresh_func=lambda: {"expiry": self.future_expiry},
            cache_key="test|key",
        )

        with self.assertRaises(ValueError):
            manager.get_token()

    def test_get_token_propagates_refresh_errors(self):
        cache = Cache()
        manager = cache.thread_safe(
            refresh_func=lambda: (_ for _ in ()).throw(
                ConnectionError("network down")
            ),
            cache_key="test|key",
        )

        with self.assertRaises(ConnectionError):
            manager.get_token()

    def test_version_change_invalidates_cached_token(self):
        """Core test: version change forces token refresh."""
        cache_v1 = Cache(version="1")
        cache_v2 = Cache(version="2")

        # Populate v1 cache
        manager_v1 = cache_v1.thread_safe(
            refresh_func=lambda: {
                "access_token": "token_v1",
                "expiry": self.future_expiry,
            },
            cache_key="carrier|id|secret",
        )
        self.assertEqual(manager_v1.get_token(), "token_v1")

        # v2 cache has a different versioned key — won't see v1's token
        manager_v2 = cache_v2.thread_safe(
            refresh_func=lambda: {
                "access_token": "token_v2",
                "expiry": self.future_expiry,
            },
            cache_key="carrier|id|secret",
        )
        self.assertEqual(manager_v2.get_token(), "token_v2")

    def test_get_state_delegates_to_get_token(self):
        cache = Cache()
        manager = cache.thread_safe(
            refresh_func=lambda: {
                "access_token": "state_token",
                "expiry": self.future_expiry,
            },
            cache_key="test|key",
        )

        self.assertEqual(manager.get_state(), "state_token")

    def test_custom_token_field(self):
        cache = Cache()
        manager = cache.thread_safe(
            refresh_func=lambda: {
                "paymentAuthorizationToken": "payment_token",
                "expiry": self.future_expiry,
            },
            cache_key="test|key",
            token_field="paymentAuthorizationToken",
        )

        self.assertEqual(manager.get_token(), "payment_token")


class TestThreadSafeTokenManagerExpiry(unittest.TestCase):
    """Tests for expiry parsing and buffer logic."""

    def test_parse_expiry_valid(self):
        manager = ThreadSafeTokenManager(
            cache=Cache(),
            refresh_func=lambda: {},
            cache_key="test",
        )
        result = manager._parse_expiry("2025-06-15 14:30:00")
        self.assertEqual(result, datetime.datetime(2025, 6, 15, 14, 30, 0))

    def test_parse_expiry_returns_none_for_empty(self):
        manager = ThreadSafeTokenManager(
            cache=Cache(),
            refresh_func=lambda: {},
            cache_key="test",
        )
        self.assertIsNone(manager._parse_expiry(""))
        self.assertIsNone(manager._parse_expiry(None))

    def test_parse_expiry_returns_none_for_invalid_format(self):
        manager = ThreadSafeTokenManager(
            cache=Cache(),
            refresh_func=lambda: {},
            cache_key="test",
        )
        self.assertIsNone(manager._parse_expiry("not-a-date"))

    def test_is_token_valid_returns_false_for_missing_token(self):
        manager = ThreadSafeTokenManager(
            cache=Cache(),
            refresh_func=lambda: {},
            cache_key="test",
        )
        future = datetime.datetime.now() + datetime.timedelta(hours=2)
        self.assertFalse(manager._is_token_valid(None, future))
        self.assertFalse(manager._is_token_valid("", future))

    def test_is_token_valid_returns_false_for_missing_expiry(self):
        manager = ThreadSafeTokenManager(
            cache=Cache(),
            refresh_func=lambda: {},
            cache_key="test",
        )
        self.assertFalse(manager._is_token_valid("token", None))

    def test_is_token_valid_with_buffer(self):
        manager = ThreadSafeTokenManager(
            cache=Cache(),
            refresh_func=lambda: {},
            cache_key="test",
            buffer_minutes=60,
        )
        # Expiry 30 minutes from now, but buffer is 60 — should be invalid
        soon_expiry = datetime.datetime.now() + datetime.timedelta(minutes=30)
        self.assertFalse(manager._is_token_valid("token", soon_expiry))

        # Expiry 2 hours from now — should be valid
        far_expiry = datetime.datetime.now() + datetime.timedelta(hours=2)
        self.assertTrue(manager._is_token_valid("token", far_expiry))


if __name__ == "__main__":
    unittest.main()
