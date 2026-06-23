"""
Task Backend Abstraction Layer

Provides a backend-agnostic interface for background task dispatch and consumption.
Backends are selected via the TASK_BACKEND setting:

    "huey"       → HueyBackend (Redis-backed task queue, default)
    "servicebus" → ServiceBusBackend (Azure Service Bus)
    "immediate"  → ImmediateBackend (synchronous, for local dev without Redis)

Task definitions use the @background_task decorator which routes calls through
the active backend. The decorator preserves compatibility with the existing
TASK_DEFINITIONS discovery pattern used by karrio.server.events.tasks.

Periodic tasks use the @periodic_task decorator which registers a cron schedule
with the backend. The backend is responsible for executing the task on schedule.
"""

import abc
import contextlib
import functools
import logging
import typing

logger = logging.getLogger(__name__)

# Registry of task handlers — populated by @background_task decorators
TASK_HANDLERS: dict[str, typing.Callable] = {}

# Queue mapping — built dynamically from @background_task(queue=...) registrations
TASK_QUEUE_MAP: dict[str, str] = {}

# Registry of periodic tasks — populated by @periodic_task decorators,
# consumed by the backend during startup to register cron schedules.
PERIODIC_TASKS: list["PeriodicTask"] = []

# Singleton backend instance — set during Django startup via settings
_backend: typing.Optional["TaskBackend"] = None


class TaskLockError(Exception):
    """Raised when a task lock cannot be acquired (task already running)."""

    pass


class TaskBackend(abc.ABC):
    """Abstract interface for task queue backends."""

    @abc.abstractmethod
    def enqueue(
        self,
        task_name: str,
        args: tuple,
        kwargs: dict,
        *,
        queue: str | None = None,
        retries: int = 0,
        retry_delay: int = 60,
    ) -> str:
        """Enqueue a task for async processing.

        Args:
            task_name: Registered task function name.
            args: Positional arguments to pass to the handler.
            kwargs: Keyword arguments to pass to the handler.
            queue: Target queue name (used by Service Bus; ignored by Huey).
            retries: Max retry attempts on transient failure.
            retry_delay: Seconds between retries.

        Returns:
            Task/message ID string.
        """
        ...

    @abc.abstractmethod
    def start_consumer(self, queues: list[str] | None = None) -> None:
        """Start consuming messages (blocking). Called by the worker process."""
        ...

    @abc.abstractmethod
    def shutdown(self, timeout: int = 30) -> None:
        """Graceful shutdown — finish in-flight tasks within timeout."""
        ...

    def lock_task(self, name: str) -> contextlib.AbstractContextManager:
        """Return a context manager that acquires a named task lock.

        Raises TaskLockError if the lock is already held. The default
        implementation is a no-op (always succeeds) — backends with real
        locking (e.g. Huey/Redis) override this.
        """
        return contextlib.nullcontext()

    def register_periodic(
        self,
        func: typing.Callable,
        *,
        name: str | None = None,
        minute: str = "*",
        hour: str = "*",
        day: str = "*",
        month: str = "*",
        day_of_week: str = "*",
    ) -> typing.Callable:
        """Register a function as a periodic task with a cron schedule.

        Called by the framework after the backend is initialized, once for
        each @periodic_task in the PERIODIC_TASKS registry, and can also
        be called at runtime for dynamic schedule registration.

        Returns the wrapped task (backend-specific)."""
        return func


def get_backend() -> TaskBackend:
    """Return the active task backend singleton."""
    global _backend

    if _backend is None:
        raise RuntimeError(
            "Task backend not initialized. Ensure TASK_BACKEND is configured "
            "in Django settings and the backend is loaded during startup."
        )

    return _backend


def set_backend(backend: TaskBackend) -> None:
    """Set the active task backend singleton. Called from settings.

    Also materializes any @periodic_task decorators that were registered
    before the backend was available.
    """
    global _backend
    _backend = backend

    # Materialize pending periodic tasks with the now-available backend.
    for pt in PERIODIC_TASKS:
        if not pt._materialized:
            pt._materialize(backend)


def register_handler(name: str, handler: typing.Callable) -> None:
    """Register a task handler function by name."""
    TASK_HANDLERS[name] = handler


def get_handler(name: str) -> typing.Callable:
    """Look up a registered task handler by name."""
    handler = TASK_HANDLERS.get(name)

    if handler is None:
        raise KeyError(f"No handler registered for task '{name}'")

    return handler


class _TaskClass:
    """Shim that exposes __name__ for compatibility with the existing
    TASK_DEFINITIONS discovery pattern in karrio.server.events.tasks."""

    def __init__(self, name: str):
        self.__name__ = name


class BackgroundTask:
    """Wrapper returned by @background_task.

    Calling an instance enqueues the task through the active backend.
    Exposes `task_class` with `__name__` for compatibility with the
    existing `TASK_DEFINITIONS` registry consumed by `events/tasks.py`.
    """

    def __init__(
        self,
        func: typing.Callable,
        *,
        queue: str | None = None,
        retries: int = 0,
        retry_delay: int = 60,
    ):
        self._func = func
        self._name = func.__name__
        self._queue = queue or "karrio-default"
        self._retries = retries
        self._retry_delay = retry_delay

        # Compatibility shim for events/tasks.py `wrapper.task_class.__name__`
        self.task_class = _TaskClass(self._name)

        # Register the handler and queue mapping
        register_handler(self._name, func)
        if queue:
            TASK_QUEUE_MAP[self._name] = queue

        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs) -> str:
        """Enqueue the task via the active backend."""
        return get_backend().enqueue(
            task_name=self._name,
            args=args,
            kwargs=kwargs,
            queue=self._queue,
            retries=self._retries,
            retry_delay=self._retry_delay,
        )

    @property
    def name(self) -> str:
        return self._name

    def delay(self, *args, **kwargs) -> str:
        """Alias for __call__ — compatibility with Huey's .delay() API."""
        return self(*args, **kwargs)

    def call_local(self, *args, **kwargs):
        """Execute the handler synchronously (useful for tests)."""
        return self._func(*args, **kwargs)


def background_task(
    queue: str | None = None,
    retries: int = 0,
    retry_delay: int = 60,
):
    """Decorator that registers a function as a background task.

    Usage::

        @background_task(queue="karrio-webhooks", retries=5, retry_delay=60)
        @utils.tenant_aware
        @with_task_telemetry("notify_webhooks")
        def notify_webhooks(*args, **kwargs):
            webhook.notify_webhook_subscribers(*args, **kwargs)

    Calling the decorated function enqueues the task through the active backend.
    The function body executes in the worker process.
    """

    def decorator(func: typing.Callable) -> BackgroundTask:
        return BackgroundTask(func, queue=queue, retries=retries, retry_delay=retry_delay)

    return decorator


# ─────────────────────────────────────────────────────────────────
# Periodic tasks
# ─────────────────────────────────────────────────────────────────


class PeriodicTask:
    """Wrapper returned by @periodic_task.

    Stores the cron schedule and function. The backend materializes
    these into real scheduled tasks (e.g. Huey periodic tasks) when
    ``set_backend()`` is called.
    """

    def __init__(
        self,
        func: typing.Callable,
        *,
        minute: str = "*",
        hour: str = "*",
        day: str = "*",
        month: str = "*",
        day_of_week: str = "*",
    ):
        self._func = func
        self._name = func.__name__
        self.minute = minute
        self.hour = hour
        self.day = day
        self.month = month
        self.day_of_week = day_of_week
        self._materialized = False
        self._backend_task = None

        # Compatibility shim for events/tasks.py `wrapper.task_class.__name__`
        self.task_class = _TaskClass(self._name)

        functools.update_wrapper(self, func)

    def _materialize(self, backend: TaskBackend) -> None:
        """Register with the backend's periodic task scheduler."""
        self._backend_task = backend.register_periodic(
            self._func,
            name=self._name,
            minute=self.minute,
            hour=self.hour,
            day=self.day,
            month=self.month,
            day_of_week=self.day_of_week,
        )
        self._materialized = True

    def call_local(self, *args, **kwargs):
        """Execute the handler synchronously (useful for tests)."""
        return self._func(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """Execute the handler directly (periodic tasks are not enqueued on demand)."""
        return self._func(*args, **kwargs)

    @property
    def name(self) -> str:
        return self._name


def periodic_task(
    *,
    minute: str = "*",
    hour: str = "*",
    day: str = "*",
    month: str = "*",
    day_of_week: str = "*",
):
    """Decorator that registers a function as a periodic (cron-scheduled) task.

    Usage::

        @periodic_task(minute="*/7")
        @with_task_telemetry("background_trackers_update")
        def background_trackers_update():
            ...

    The backend materializes these into real scheduled tasks when
    ``set_backend()`` is called during Django startup.
    """

    def decorator(func: typing.Callable) -> PeriodicTask:
        pt = PeriodicTask(
            func,
            minute=minute,
            hour=hour,
            day=day,
            month=month,
            day_of_week=day_of_week,
        )
        PERIODIC_TASKS.append(pt)
        return pt

    return decorator


def lock_task(name: str) -> contextlib.AbstractContextManager:
    """Acquire a named task lock via the active backend.

    Raises TaskLockError if the lock is already held.
    Falls back to a no-op context manager if no backend is set
    (e.g. during tests without a backend).
    """
    if _backend is not None:
        return _backend.lock_task(name)
    return contextlib.nullcontext()
