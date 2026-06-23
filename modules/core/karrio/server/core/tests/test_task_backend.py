"""
Tests for the task backend abstraction layer.

Run with:
    karrio test --failfast karrio.server.core.tests.test_task_backend
  or:
    LOG_LEVEL=30 python -m unittest karrio.server.core.tests.test_task_backend -v
"""

import unittest

from karrio.server.core.backends.immediate import ImmediateBackend
from karrio.server.core.task_backend import (
    PERIODIC_TASKS,
    TASK_HANDLERS,
    TASK_QUEUE_MAP,
    TaskLockError,
    _backend,
    background_task,
    get_backend,
    get_handler,
    lock_task,
    periodic_task,
    register_handler,
    set_backend,
)


class TestTaskHandlerRegistry(unittest.TestCase):
    """Tests for task handler registration and lookup."""

    def setUp(self):
        self.maxDiff = None
        # Save and clear registry state
        self._saved_handlers = dict(TASK_HANDLERS)
        self._saved_queue_map = dict(TASK_QUEUE_MAP)

    def tearDown(self):
        TASK_HANDLERS.clear()
        TASK_HANDLERS.update(self._saved_handlers)
        TASK_QUEUE_MAP.clear()
        TASK_QUEUE_MAP.update(self._saved_queue_map)

    def test_register_handler(self):
        """register_handler adds a callable to TASK_HANDLERS."""

        def my_handler():
            pass

        register_handler("test_task", my_handler)
        self.assertIs(TASK_HANDLERS["test_task"], my_handler)

    def test_get_handler_found(self):
        """get_handler returns the registered callable."""

        def my_handler():
            pass

        register_handler("test_task", my_handler)
        self.assertIs(get_handler("test_task"), my_handler)

    def test_get_handler_not_found(self):
        """get_handler raises KeyError for unregistered tasks."""
        with self.assertRaises(KeyError):
            get_handler("nonexistent_task")


class TestBackgroundTaskDecorator(unittest.TestCase):
    """Tests for the @background_task decorator and BackgroundTask wrapper."""

    def setUp(self):
        self.maxDiff = None
        self._saved_handlers = dict(TASK_HANDLERS)
        self._saved_queue_map = dict(TASK_QUEUE_MAP)
        self._saved_backend = _backend

    def tearDown(self):
        TASK_HANDLERS.clear()
        TASK_HANDLERS.update(self._saved_handlers)
        TASK_QUEUE_MAP.clear()
        TASK_QUEUE_MAP.update(self._saved_queue_map)

    def test_decorator_registers_handler(self):
        """@background_task registers the function in TASK_HANDLERS."""

        @background_task(queue="karrio-test")
        def my_task(x, y):
            return x + y

        self.assertIn("my_task", TASK_HANDLERS)

    def test_decorator_registers_queue_mapping(self):
        """@background_task with queue= populates TASK_QUEUE_MAP."""

        @background_task(queue="karrio-test-queue")
        def my_queued_task():
            pass

        self.assertEqual(TASK_QUEUE_MAP["my_queued_task"], "karrio-test-queue")

    def test_decorator_no_queue_uses_default(self):
        """@background_task without queue= uses karrio-default."""

        @background_task()
        def my_default_task():
            pass

        self.assertEqual(my_default_task._queue, "karrio-default")
        self.assertNotIn("my_default_task", TASK_QUEUE_MAP)

    def test_task_class_compat(self):
        """BackgroundTask.task_class.__name__ matches the function name."""

        @background_task(queue="karrio-test")
        def my_task():
            pass

        self.assertEqual(my_task.task_class.__name__, "my_task")

    def test_call_local_executes_synchronously(self):
        """call_local() runs the handler directly without enqueuing."""
        results = []

        @background_task(queue="karrio-test")
        def accumulator(value):
            results.append(value)

        accumulator.call_local("hello")
        self.assertEqual(results, ["hello"])

    def test_name_property(self):
        """BackgroundTask.name returns the function name."""

        @background_task(queue="karrio-test")
        def my_named_task():
            pass

        self.assertEqual(my_named_task.name, "my_named_task")

    def test_call_enqueues_via_backend(self):
        """Calling a BackgroundTask dispatches through the active backend."""
        backend = ImmediateBackend()
        set_backend(backend)

        results = []

        @background_task(queue="karrio-test")
        def enqueue_test(value):
            results.append(value)

        enqueue_test("dispatched")

        # ImmediateBackend executes synchronously
        self.assertEqual(results, ["dispatched"])


class TestImmediateBackend(unittest.TestCase):
    """Tests for the ImmediateBackend."""

    def setUp(self):
        self.maxDiff = None
        self._saved_handlers = dict(TASK_HANDLERS)
        self._saved_backend = _backend

    def tearDown(self):
        TASK_HANDLERS.clear()
        TASK_HANDLERS.update(self._saved_handlers)

    def test_enqueue_calls_handler_synchronously(self):
        """ImmediateBackend.enqueue executes the handler inline."""
        results = []

        def handler(x):
            results.append(x)

        register_handler("sync_task", handler)

        backend = ImmediateBackend()
        task_id = backend.enqueue("sync_task", (42,), {})

        self.assertEqual(results, [42])
        self.assertTrue(len(task_id) > 0)

    def test_enqueue_catches_handler_errors(self):
        """ImmediateBackend catches handler exceptions (fail-open like Huey immediate)."""

        def failing_handler():
            raise ValueError("boom")

        register_handler("fail_task", failing_handler)

        backend = ImmediateBackend()
        # Should not raise
        task_id = backend.enqueue("fail_task", (), {})
        self.assertTrue(len(task_id) > 0)

    def test_enqueue_returns_unique_ids(self):
        """Each enqueue call returns a unique task ID."""

        def noop():
            pass

        register_handler("noop", noop)

        backend = ImmediateBackend()
        id1 = backend.enqueue("noop", (), {})
        id2 = backend.enqueue("noop", (), {})
        self.assertNotEqual(id1, id2)

    def test_start_consumer_is_noop(self):
        """start_consumer does nothing (no worker needed)."""
        backend = ImmediateBackend()
        backend.start_consumer()  # should not raise

    def test_shutdown_is_noop(self):
        """shutdown does nothing."""
        backend = ImmediateBackend()
        backend.shutdown()  # should not raise


class TestGetSetBackend(unittest.TestCase):
    """Tests for get_backend / set_backend singleton management."""

    def test_set_and_get_backend(self):
        """set_backend stores, get_backend retrieves."""
        backend = ImmediateBackend()
        set_backend(backend)
        self.assertIs(get_backend(), backend)

    def test_get_backend_raises_when_none(self):
        """get_backend raises RuntimeError if no backend is set."""
        import karrio.server.core.task_backend as tb

        saved = tb._backend
        try:
            tb._backend = None
            with self.assertRaises(RuntimeError):
                get_backend()
        finally:
            tb._backend = saved


class TestPeriodicTaskDecorator(unittest.TestCase):
    """Tests for the @periodic_task decorator and PeriodicTask wrapper."""

    def setUp(self):
        self.maxDiff = None
        self._saved_periodic = list(PERIODIC_TASKS)

    def tearDown(self):
        PERIODIC_TASKS.clear()
        PERIODIC_TASKS.extend(self._saved_periodic)

    def test_decorator_appends_to_registry(self):
        """@periodic_task adds a PeriodicTask to PERIODIC_TASKS."""
        initial_count = len(PERIODIC_TASKS)

        @periodic_task(minute="*/5")
        def my_periodic():
            pass

        self.assertEqual(len(PERIODIC_TASKS), initial_count + 1)
        self.assertIs(PERIODIC_TASKS[-1], my_periodic)

    def test_stores_cron_params(self):
        """PeriodicTask stores all cron schedule parameters."""

        @periodic_task(minute="30", hour="2", day="1", month="*/3", day_of_week="1")
        def scheduled_task():
            pass

        self.assertEqual(scheduled_task.minute, "30")
        self.assertEqual(scheduled_task.hour, "2")
        self.assertEqual(scheduled_task.day, "1")
        self.assertEqual(scheduled_task.month, "*/3")
        self.assertEqual(scheduled_task.day_of_week, "1")

    def test_defaults_to_wildcard(self):
        """Unspecified cron params default to '*'."""

        @periodic_task(minute="0")
        def hourly_task():
            pass

        self.assertEqual(hourly_task.minute, "0")
        self.assertEqual(hourly_task.hour, "*")
        self.assertEqual(hourly_task.day, "*")
        self.assertEqual(hourly_task.month, "*")
        self.assertEqual(hourly_task.day_of_week, "*")

    def test_call_local_executes_synchronously(self):
        """call_local() runs the handler directly."""
        results = []

        @periodic_task(minute="*/10")
        def accumulator():
            results.append("ran")

        accumulator.call_local()
        self.assertEqual(results, ["ran"])

    def test_call_executes_directly(self):
        """Calling a PeriodicTask invokes the handler (not enqueued)."""
        results = []

        @periodic_task(minute="0", hour="0")
        def direct_call():
            results.append("called")

        direct_call()
        self.assertEqual(results, ["called"])

    def test_task_class_compat(self):
        """PeriodicTask.task_class.__name__ matches the function name."""

        @periodic_task(minute="0")
        def compat_task():
            pass

        self.assertEqual(compat_task.task_class.__name__, "compat_task")

    def test_name_property(self):
        """PeriodicTask.name returns the function name."""

        @periodic_task(minute="0")
        def named_periodic():
            pass

        self.assertEqual(named_periodic.name, "named_periodic")

    def test_not_materialized_before_set_backend(self):
        """PeriodicTask._materialized is False before set_backend is called."""

        @periodic_task(minute="*/5")
        def pending_task():
            pass

        self.assertFalse(pending_task._materialized)


class TestSetBackendMaterializesPeriodicTasks(unittest.TestCase):
    """Tests that set_backend() materializes pending periodic tasks."""

    def setUp(self):
        self.maxDiff = None
        self._saved_periodic = list(PERIODIC_TASKS)
        self._saved_backend = _backend

    def tearDown(self):
        PERIODIC_TASKS.clear()
        PERIODIC_TASKS.extend(self._saved_periodic)
        import karrio.server.core.task_backend as tb

        tb._backend = self._saved_backend

    def test_set_backend_materializes_pending(self):
        """set_backend() calls _materialize on each unmaterialized PeriodicTask."""

        @periodic_task(minute="*/5")
        def mat_test():
            pass

        self.assertFalse(mat_test._materialized)

        backend = ImmediateBackend()
        set_backend(backend)

        self.assertTrue(mat_test._materialized)

    def test_set_backend_skips_already_materialized(self):
        """set_backend() does not re-materialize tasks already materialized."""

        @periodic_task(minute="0")
        def already_done():
            pass

        already_done._materialized = True
        original_backend_task = already_done._backend_task

        backend = ImmediateBackend()
        set_backend(backend)

        # Should not have changed
        self.assertIs(already_done._backend_task, original_backend_task)

    def test_immediate_register_periodic_is_noop(self):
        """ImmediateBackend.register_periodic returns the func unchanged."""
        backend = ImmediateBackend()

        def my_func():
            pass

        result = backend.register_periodic(my_func, minute="*/5", hour="2")
        self.assertIs(result, my_func)


class TestLockTask(unittest.TestCase):
    """Tests for lock_task() and TaskLockError."""

    def setUp(self):
        self.maxDiff = None
        self._saved_backend = _backend

    def tearDown(self):
        import karrio.server.core.task_backend as tb

        tb._backend = self._saved_backend

    def test_lock_task_noop_without_backend(self):
        """lock_task() returns a no-op context manager when no backend is set."""
        import karrio.server.core.task_backend as tb

        tb._backend = None

        with lock_task("test_lock"):
            pass  # should not raise

    def test_lock_task_noop_with_immediate_backend(self):
        """ImmediateBackend.lock_task is a no-op (always succeeds)."""
        backend = ImmediateBackend()
        set_backend(backend)

        with lock_task("test_lock"):
            pass  # should not raise

        # Nested locks also succeed (no real locking)
        with lock_task("test_lock"), lock_task("test_lock"):
            pass  # should not raise

    def test_task_lock_error_is_exception(self):
        """TaskLockError can be raised and caught."""
        with self.assertRaises(TaskLockError):
            raise TaskLockError("test lock held")

    def test_task_lock_error_message(self):
        """TaskLockError preserves the error message."""
        try:
            raise TaskLockError("lock 'my_task' is held")
        except TaskLockError as e:
            self.assertIn("my_task", str(e))


if __name__ == "__main__":
    unittest.main()
