"""
Tracing and Telemetry module for Karrio SDK.

This module provides:
1. SDK Tracing: Records request/response data for persistence (TracingRecord model)
2. APM Telemetry: Optional integration with external APM tools (e.g., Sentry)

The telemetry abstraction follows the same injection pattern as Cache and SystemConfig:
- SDK defines abstract interface with NoOp default
- Server layer injects concrete implementation (e.g., SentryTelemetry)
- Zero overhead when no APM is configured
"""

import abc
import uuid
import attr
import time
import typing
import functools
import concurrent.futures as futures

Trace = typing.Callable[[typing.Any, str], typing.Any]

# Shared thread pool executor for trace recording
# Using a single executor avoids the overhead of creating new thread pools per trace
_trace_executor: typing.Optional[futures.ThreadPoolExecutor] = None
_trace_executor_lock = __import__("threading").Lock()


def _get_trace_executor() -> futures.ThreadPoolExecutor:
    """Get or create the shared trace executor (lazy initialization, thread-safe)."""
    global _trace_executor
    if _trace_executor is None:
        with _trace_executor_lock:
            if _trace_executor is None:
                _trace_executor = futures.ThreadPoolExecutor(
                    max_workers=4,
                    thread_name_prefix="karrio_trace",
                )
    return _trace_executor


# =============================================================================
# Telemetry Abstraction Layer
# =============================================================================


class SpanContext:
    """Abstract span context for timing operations.

    Implementations should support context manager protocol for automatic
    span lifecycle management.
    """

    def __enter__(self) -> "SpanContext":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    def set_attribute(self, key: str, value: typing.Any) -> None:
        """Set an attribute on this span."""
        pass

    def set_attributes(self, attributes: typing.Dict[str, typing.Any]) -> None:
        """Set multiple attributes on this span."""
        for k, v in (attributes or {}).items():
            self.set_attribute(k, v)

    def set_status(self, status: str, message: str = None) -> None:
        """Set the status of this span (ok, error)."""
        pass

    def record_exception(self, exception: Exception) -> None:
        """Record an exception on this span."""
        pass

    def add_event(self, name: str, attributes: typing.Dict[str, typing.Any] = None) -> None:
        """Add an event to this span."""
        pass


class NoOpSpanContext(SpanContext):
    """No-operation span context - zero overhead when telemetry is disabled."""
    pass


class Telemetry(abc.ABC):
    """Abstract telemetry interface for APM integration.

    This interface defines the contract for observability features without
    coupling to any specific APM provider. The SDK uses this interface,
    and concrete implementations (e.g., SentryTelemetry) are injected
    at runtime by the server layer.

    Default behavior (NoOpTelemetry) has zero overhead and no external dependencies.
    """

    @abc.abstractmethod
    def start_span(
        self,
        name: str,
        attributes: typing.Dict[str, typing.Any] = None,
        kind: str = None,
    ) -> SpanContext:
        """Start a new span for an operation."""
        pass

    @abc.abstractmethod
    def add_breadcrumb(
        self,
        message: str,
        category: str,
        data: typing.Dict[str, typing.Any] = None,
        level: str = "info",
    ) -> None:
        """Add a breadcrumb for debugging context."""
        pass

    @abc.abstractmethod
    def record_metric(
        self,
        name: str,
        value: float,
        unit: str = None,
        tags: typing.Dict[str, str] = None,
        metric_type: str = "counter",
    ) -> None:
        """Record a metric value."""
        pass

    @abc.abstractmethod
    def capture_exception(
        self,
        exception: Exception,
        context: typing.Dict[str, typing.Any] = None,
        tags: typing.Dict[str, str] = None,
    ) -> None:
        """Capture an exception for error tracking."""
        pass

    @abc.abstractmethod
    def set_context(
        self,
        name: str,
        data: typing.Dict[str, typing.Any],
    ) -> None:
        """Set contextual data for the current scope."""
        pass

    @abc.abstractmethod
    def set_tag(self, key: str, value: str) -> None:
        """Set a tag on the current scope."""
        pass

    @abc.abstractmethod
    def set_user(
        self,
        user_id: str = None,
        email: str = None,
        username: str = None,
        ip_address: str = None,
        data: typing.Dict[str, typing.Any] = None,
    ) -> None:
        """Set user information for the current scope."""
        pass

    def start_transaction(
        self,
        name: str,
        op: str = None,
        attributes: typing.Dict[str, typing.Any] = None,
    ) -> SpanContext:
        """Start a new transaction (top-level span)."""
        return self.start_span(name, attributes=attributes, kind=op)

    def instrument_function(
        self,
        name: str = None,
        attributes: typing.Dict[str, typing.Any] = None,
    ):
        """Decorator to instrument a function with a span."""
        def decorator(func):
            span_name = name or f"{func.__module__}.{func.__name__}"

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                with self.start_span(span_name, attributes=attributes) as span:
                    try:
                        result = func(*args, **kwargs)
                        span.set_status("ok")
                        return result
                    except Exception as e:
                        span.set_status("error", str(e))
                        span.record_exception(e)
                        raise

            return wrapper
        return decorator


class NoOpTelemetry(Telemetry):
    """No-operation telemetry implementation.

    This is the default telemetry used when no APM is configured.
    All methods are no-ops with minimal overhead.
    """

    def start_span(
        self,
        name: str,
        attributes: typing.Dict[str, typing.Any] = None,
        kind: str = None,
    ) -> SpanContext:
        return NoOpSpanContext()

    def add_breadcrumb(
        self,
        message: str,
        category: str,
        data: typing.Dict[str, typing.Any] = None,
        level: str = "info",
    ) -> None:
        pass

    def record_metric(
        self,
        name: str,
        value: float,
        unit: str = None,
        tags: typing.Dict[str, str] = None,
        metric_type: str = "counter",
    ) -> None:
        pass

    def capture_exception(
        self,
        exception: Exception,
        context: typing.Dict[str, typing.Any] = None,
        tags: typing.Dict[str, str] = None,
    ) -> None:
        pass

    def set_context(
        self,
        name: str,
        data: typing.Dict[str, typing.Any],
    ) -> None:
        pass

    def set_tag(self, key: str, value: str) -> None:
        pass

    def set_user(
        self,
        user_id: str = None,
        email: str = None,
        username: str = None,
        ip_address: str = None,
        data: typing.Dict[str, typing.Any] = None,
    ) -> None:
        pass


class TimingSpanContext(SpanContext):
    """A span context that captures timing and attributes for custom processing."""

    def __init__(
        self,
        name: str,
        on_finish: typing.Callable[["TimingSpanContext"], None] = None,
    ):
        self.name = name
        self.start_time = time.time()
        self.end_time: typing.Optional[float] = None
        self.attributes: typing.Dict[str, typing.Any] = {}
        self.status: str = "ok"
        self.status_message: typing.Optional[str] = None
        self.exception: typing.Optional[Exception] = None
        self.events: typing.List[typing.Dict[str, typing.Any]] = []
        self._on_finish = on_finish

    def __enter__(self) -> "TimingSpanContext":
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.end_time = time.time()
        if exc_val is not None:
            self.set_status("error", str(exc_val))
            self.record_exception(exc_val)
        if self._on_finish:
            self._on_finish(self)

    def set_attribute(self, key: str, value: typing.Any) -> None:
        self.attributes[key] = value

    def set_status(self, status: str, message: str = None) -> None:
        self.status = status
        self.status_message = message

    def record_exception(self, exception: Exception) -> None:
        self.exception = exception

    def add_event(self, name: str, attributes: typing.Dict[str, typing.Any] = None) -> None:
        self.events.append({
            "name": name,
            "timestamp": time.time(),
            "attributes": attributes or {},
        })

    @property
    def duration_ms(self) -> float:
        """Get the span duration in milliseconds."""
        end = self.end_time or time.time()
        return (end - self.start_time) * 1000


# Default telemetry instance (no-op)
_default_telemetry = NoOpTelemetry()


def get_default_telemetry() -> Telemetry:
    """Get the default telemetry instance (NoOpTelemetry)."""
    return _default_telemetry


# =============================================================================
# SDK Tracing Layer
# =============================================================================


@attr.s(auto_attribs=True)
class Record:
    """A trace record capturing SDK operation data."""
    key: str
    data: typing.Any
    timestamp: float
    metadata: dict = {}


class Tracer:
    """Tracer for recording SDK operations with optional APM telemetry integration.

    The Tracer provides two layers of observability:
    1. SDK Tracing: Records request/response data for persistence (TracingRecord model)
    2. APM Telemetry: Optional integration with external APM tools (e.g., Sentry)

    Telemetry is injected at runtime by the server layer, following the same pattern
    as Cache and SystemConfig. When no telemetry is configured, NoOpTelemetry is used
    with zero overhead.

    Usage:
        # Basic tracing (always available)
        tracer.trace({"url": url, "data": payload}, "request")

        # APM telemetry (when configured)
        with tracer.start_span("karrio_rates_fetch") as span:
            span.set_attribute("carrier_count", len(carriers))
            result = fetch_rates()

        # Breadcrumbs for debugging context
        tracer.add_breadcrumb("Fetching rates", "carrier", {"carrier": "fedex"})
    """

    def __init__(
        self,
        id: str = None,
        telemetry: Telemetry = None,
    ) -> None:
        self.id = id or str(uuid.uuid4())
        self.inner_context: typing.Dict[str, typing.Any] = {}
        self.inner_recordings: typing.Dict[futures.Future, dict] = {}
        self._telemetry = telemetry or get_default_telemetry()

    @property
    def telemetry(self) -> Telemetry:
        """Access the telemetry instance for APM operations."""
        return self._telemetry

    def set_telemetry(self, telemetry: Telemetry) -> None:
        """Set the telemetry instance (typically called by server layer)."""
        self._telemetry = telemetry or get_default_telemetry()

    def trace(
        self, data: typing.Any, key: str, metadata: dict = {}, format: str = None
    ) -> typing.Any:
        """Record trace data for SDK operations.

        This method records request/response data that can be persisted
        to the TracingRecord model for debugging and auditing.
        """
        def _save():
            return Record(
                key=key,
                data={"format": format, **data},
                timestamp=time.time(),
                metadata=metadata,
            )

        # Use shared executor to avoid creating new thread pools per trace
        executor = _get_trace_executor()
        self.inner_recordings.update({executor.submit(_save): data})

        # Add telemetry breadcrumb for APM context
        self._telemetry.add_breadcrumb(
            message=f"SDK trace: {key}",
            category="karrio.sdk",
            data={
                "key": key,
                "format": format,
                "has_data": data is not None,
                **({"carrier": metadata.get("connection", {}).get("carrier_name")} if metadata else {}),
            },
            level="debug",
        )

        return data

    def with_metadata(self, metadata: dict):
        """Create a partial trace function with preset metadata."""
        return functools.partial(self.trace, metadata=metadata)

    @property
    def records(self) -> typing.List[Record]:
        """Get all recorded trace records."""
        return [rec.result() for rec in futures.as_completed(self.inner_recordings)]

    @property
    def context(self) -> typing.Dict[str, typing.Any]:
        """Get the tracer context dictionary."""
        return self.inner_context

    def add_context(self, data: typing.Dict[str, typing.Any]):
        """Add data to the tracer context."""
        self.inner_context.update(data)

        # Also set telemetry context for APM correlation
        if data:
            self._telemetry.set_context("karrio_trace", {
                "tracer_id": self.id,
                **data,
            })

    # -------------------------------------------------------------------------
    # Telemetry convenience methods
    # -------------------------------------------------------------------------

    def start_span(
        self,
        name: str,
        attributes: typing.Dict[str, typing.Any] = None,
        kind: str = None,
    ) -> SpanContext:
        """Start a new telemetry span for timing and tracing operations."""
        return self._telemetry.start_span(name, attributes=attributes, kind=kind)

    def add_breadcrumb(
        self,
        message: str,
        category: str,
        data: typing.Dict[str, typing.Any] = None,
        level: str = "info",
    ) -> None:
        """Add a breadcrumb for debugging context."""
        self._telemetry.add_breadcrumb(message, category, data, level)

    def record_metric(
        self,
        name: str,
        value: float,
        unit: str = None,
        tags: typing.Dict[str, str] = None,
        metric_type: str = "counter",
    ) -> None:
        """Record a metric value."""
        self._telemetry.record_metric(name, value, unit, tags, metric_type)

    def capture_exception(
        self,
        exception: Exception,
        context: typing.Dict[str, typing.Any] = None,
        tags: typing.Dict[str, str] = None,
    ) -> None:
        """Capture an exception for error tracking."""
        self._telemetry.capture_exception(exception, context, tags)

    def set_tag(self, key: str, value: str) -> None:
        """Set a tag on the current telemetry scope."""
        self._telemetry.set_tag(key, value)

    def set_user(
        self,
        user_id: str = None,
        email: str = None,
        username: str = None,
        ip_address: str = None,
        data: typing.Dict[str, typing.Any] = None,
    ) -> None:
        """Set user information for the current telemetry scope."""
        self._telemetry.set_user(user_id, email, username, ip_address, data)
