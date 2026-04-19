"""
Tests for the Huey task backend.

Verifies that:
- _huey_generic_dispatch is registered in Huey's TaskRegistry at import time
- HueyBackend dispatches migrated @background_task tasks through the generic dispatcher
- HueyBackend delegates unmigrated @db_task wrappers to their native Huey TaskWrapper
- Round-trip: enqueue → deserialize → execute works in immediate mode

Run with:
    karrio test --failfast karrio.server.huey.tests.test_huey_backend
"""

from unittest.mock import patch

from django.test import TestCase
from karrio.server.core.task_backend import (
    TASK_HANDLERS,
    TASK_QUEUE_MAP,
    background_task,
    register_handler,
)


class TestGenericDispatcherRegistration(TestCase):
    """_huey_generic_dispatch must be in Huey's TaskRegistry at import time."""

    def setUp(self):
        self.maxDiff = None

    def test_generic_dispatcher_in_task_registry(self):
        """Importing backend.py registers _huey_generic_dispatch in the Huey TaskRegistry."""
        from huey.contrib.djhuey import HUEY

        # The task must be registered in Huey's registry so the worker can
        # deserialize it. This was the root cause of KARRIO-SHIPPING-API-PROD-1N.
        registry = HUEY._registry
        registered_names = list(registry._registry.keys())
        expected = "karrio.server.huey.backend._huey_generic_dispatch"

        self.assertIn(
            expected,
            registered_names,
            f"_huey_generic_dispatch not found in TaskRegistry. Registered: {registered_names}",
        )

    def test_generic_dispatcher_is_module_level(self):
        """_huey_generic_dispatch is a module-level attribute, not lazily created."""
        import karrio.server.huey.backend as backend_module

        self.assertTrue(
            hasattr(backend_module, "_huey_generic_dispatch"),
            "_huey_generic_dispatch should be a module-level attribute",
        )


class TestHueyBackendEnqueue(TestCase):
    """HueyBackend.enqueue routes tasks correctly."""

    def setUp(self):
        self.maxDiff = None
        self._saved_handlers = dict(TASK_HANDLERS)
        self._saved_queue_map = dict(TASK_QUEUE_MAP)

    def tearDown(self):
        TASK_HANDLERS.clear()
        TASK_HANDLERS.update(self._saved_handlers)
        TASK_QUEUE_MAP.clear()
        TASK_QUEUE_MAP.update(self._saved_queue_map)

    def test_enqueue_calls_generic_dispatcher(self):
        """Migrated tasks are routed through _huey_generic_dispatch."""
        from karrio.server.huey.backend import HueyBackend

        register_handler("test_migrated_task", lambda v: None)

        backend = HueyBackend()
        with patch("karrio.server.huey.backend._huey_generic_dispatch") as mock_dispatch:
            mock_dispatch.return_value = type("R", (), {"id": "test-123"})()
            task_id = backend.enqueue("test_migrated_task", ("hello",), {})

            mock_dispatch.assert_called_once_with("test_migrated_task", ["hello"], {})
            self.assertEqual(task_id, "test-123")

    def test_enqueue_with_kwargs(self):
        """Generic dispatcher receives kwargs correctly."""
        from karrio.server.huey.backend import HueyBackend

        register_handler("test_kwargs_task", lambda a, b, key=None: None)

        backend = HueyBackend()
        with patch("karrio.server.huey.backend._huey_generic_dispatch") as mock_dispatch:
            mock_dispatch.return_value = type("R", (), {"id": "test-456"})()
            backend.enqueue("test_kwargs_task", (1, 2), {"key": "value"})

            mock_dispatch.assert_called_once_with("test_kwargs_task", [1, 2], {"key": "value"})

    def test_enqueue_returns_task_id(self):
        """enqueue returns a non-empty task ID string."""
        from karrio.server.huey.backend import HueyBackend

        register_handler("test_id_task", lambda: None)

        backend = HueyBackend()
        with patch("karrio.server.huey.backend._huey_generic_dispatch") as mock_dispatch:
            mock_dispatch.return_value = type("R", (), {"id": "abc-789"})()
            task_id = backend.enqueue("test_id_task", (), {})

            self.assertEqual(task_id, "abc-789")


class TestGenericDispatchExecution(TestCase):
    """Tests for _huey_generic_dispatch executing handlers directly (simulates worker)."""

    def setUp(self):
        self.maxDiff = None
        self._saved_handlers = dict(TASK_HANDLERS)
        self._saved_queue_map = dict(TASK_QUEUE_MAP)

    def tearDown(self):
        TASK_HANDLERS.clear()
        TASK_HANDLERS.update(self._saved_handlers)
        TASK_QUEUE_MAP.clear()
        TASK_QUEUE_MAP.update(self._saved_queue_map)

    def test_dispatch_executes_handler(self):
        """_huey_generic_dispatch looks up and calls the registered handler."""
        from karrio.server.huey.backend import _huey_generic_dispatch

        results = []
        register_handler("exec_task", lambda v: results.append(v))

        # call_local bypasses Huey queue/signals — directly invokes the function
        _huey_generic_dispatch.call_local("exec_task", ["hello"], {})

        self.assertEqual(results, ["hello"])

    def test_dispatch_passes_args_and_kwargs(self):
        """Handler receives both positional and keyword arguments."""
        from karrio.server.huey.backend import _huey_generic_dispatch

        results = []
        register_handler("args_task", lambda a, b, key=None: results.append((a, b, key)))

        _huey_generic_dispatch.call_local("args_task", [1, 2], {"key": "val"})

        self.assertEqual(results, [(1, 2, "val")])

    def test_dispatch_error_propagation(self):
        """Errors in the handler propagate through the generic dispatcher."""
        from karrio.server.huey.backend import _huey_generic_dispatch

        def failing():
            raise ValueError("boom")

        register_handler("failing_task", failing)

        with self.assertRaises(ValueError) as ctx:
            _huey_generic_dispatch.call_local("failing_task", [], {})

        self.assertIn("boom", str(ctx.exception))

    def test_dispatch_unknown_handler_raises(self):
        """Generic dispatcher raises KeyError for unregistered task names."""
        from karrio.server.huey.backend import _huey_generic_dispatch

        with self.assertRaises(KeyError):
            _huey_generic_dispatch.call_local("nonexistent_task_xyz", [], {})

    def test_background_task_round_trip_via_call_local(self):
        """@background_task handler is discoverable and executable via generic dispatch."""
        from karrio.server.huey.backend import _huey_generic_dispatch

        results = []

        @background_task(queue="karrio-test")
        def round_trip_task(x, y):
            results.append(x + y)

        # Simulate what the worker does: look up handler by name and execute
        _huey_generic_dispatch.call_local("round_trip_task", [3, 4], {})

        self.assertEqual(results, [7])


class TestHueyBackendRegisterPeriodic(TestCase):
    """HueyBackend.register_periodic wraps functions with Huey's crontab scheduler."""

    def setUp(self):
        self.maxDiff = None

    def test_register_periodic_returns_callable(self):
        """register_periodic returns a Huey-wrapped callable."""
        from karrio.server.huey.backend import HueyBackend

        backend = HueyBackend()

        def my_cron_job():
            pass

        result = backend.register_periodic(my_cron_job, name="test_cron", minute="*/5")

        self.assertTrue(callable(result))

    def test_register_periodic_adds_to_huey_registry(self):
        """Registered periodic tasks appear in Huey's TaskRegistry."""
        from karrio.server.huey.backend import HueyBackend

        from huey.contrib.djhuey import HUEY

        backend = HueyBackend()

        def discoverable_cron():
            pass

        backend.register_periodic(
            discoverable_cron,
            name="test_discoverable_cron",
            minute="0",
            hour="3",
        )

        registered_names = list(HUEY._registry._registry.keys())
        self.assertTrue(
            any("test_discoverable_cron" in name for name in registered_names),
            f"test_discoverable_cron not found in TaskRegistry. Registered: {registered_names}",
        )

    def test_register_periodic_with_full_cron(self):
        """register_periodic accepts all five cron fields."""
        from karrio.server.huey.backend import HueyBackend

        backend = HueyBackend()

        def full_cron():
            pass

        # Should not raise — all fields valid
        result = backend.register_periodic(
            full_cron,
            name="test_full_cron",
            minute="30",
            hour="2",
            day="15",
            month="*/3",
            day_of_week="1",
        )

        self.assertTrue(callable(result))


class TestHueyBackendLockTask(TestCase):
    """HueyBackend.lock_task translates Huey's lock into TaskLockError.

    These tests use the real Huey lock. When the backing storage (Redis)
    is not reachable (e.g. CI without a Redis service), the tests are
    skipped — the translation layer is still covered by the unit-level
    TaskLockError tests in test_task_backend.py.
    """

    def setUp(self):
        self.maxDiff = None

    def _skip_if_storage_unavailable(self):
        """Skip the test if Huey's storage backend is not reachable."""
        from karrio.server.huey.backend import HueyBackend

        backend = HueyBackend()
        try:
            with backend.lock_task("__connectivity_probe__"):
                pass
        except Exception:
            self.skipTest("Huey storage not reachable (no Redis in this environment)")
        return backend

    def test_lock_task_returns_context_manager(self):
        """lock_task returns an object with __enter__ and __exit__."""
        from karrio.server.huey.backend import HueyBackend

        backend = HueyBackend()
        lock = backend.lock_task("test_lock_cm")

        self.assertTrue(hasattr(lock, "__enter__"))
        self.assertTrue(hasattr(lock, "__exit__"))

    def test_lock_task_succeeds_when_unlocked(self):
        """lock_task context manager succeeds on first acquisition."""
        backend = self._skip_if_storage_unavailable()

        with backend.lock_task("test_unheld_lock"):
            pass  # should not raise

    def test_lock_task_raises_task_lock_error(self):
        """Nested lock acquisition raises TaskLockError."""
        from karrio.server.core.task_backend import TaskLockError

        backend = self._skip_if_storage_unavailable()

        with backend.lock_task("test_double_lock"):
            # Second acquisition of the same lock must fail
            self.assertRaises(TaskLockError, backend.lock_task("test_double_lock").__enter__)
