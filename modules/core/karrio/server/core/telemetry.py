"""
Telemetry implementations for Karrio Server.

This module provides telemetry implementations for multiple APM providers:
- Sentry: Error tracking and performance monitoring
- OpenTelemetry (OTEL): Vendor-neutral observability standard
- Datadog: Full-stack observability platform

Provider Priority (first enabled wins):
1. SENTRY_DSN -> SentryTelemetry
2. OTEL_ENABLED=true -> OpenTelemetryTelemetry
3. DD_TRACE_ENABLED=true -> DatadogTelemetry
4. None -> NoOpTelemetry (zero overhead)
"""

import typing
import functools
from functools import lru_cache
from enum import Enum

import karrio.lib as lib


T = typing.TypeVar("T")


def failsafe(callable: typing.Callable[[], T]) -> T:
    """Execute callable and return None on any exception."""
    try:
        return callable()
    except Exception:
        return None


class TelemetryProvider(Enum):
    NONE = "none"
    SENTRY = "sentry"
    OPENTELEMETRY = "opentelemetry"
    DATADOG = "datadog"


# =============================================================================
# Provider Detection
# =============================================================================


def is_sentry_enabled() -> bool:
    return failsafe(lambda: bool(__import__("django.conf", fromlist=["settings"]).settings.SENTRY_DSN)) or False


def is_otel_enabled() -> bool:
    return failsafe(lambda: bool(getattr(__import__("django.conf", fromlist=["settings"]).settings, "OTEL_ENABLED", False))) or False


def is_datadog_enabled() -> bool:
    def _check():
        settings = __import__("django.conf", fromlist=["settings"]).settings
        return bool(getattr(settings, "DD_TRACE_ENABLED", False) or getattr(settings, "DATADOG_ENABLED", False))
    return failsafe(_check) or False


def get_active_provider() -> TelemetryProvider:
    if is_sentry_enabled():
        return TelemetryProvider.SENTRY
    if is_otel_enabled():
        return TelemetryProvider.OPENTELEMETRY
    if is_datadog_enabled():
        return TelemetryProvider.DATADOG
    return TelemetryProvider.NONE


# =============================================================================
# Telemetry Factory
# =============================================================================


@lru_cache(maxsize=1)
def get_telemetry_instance() -> lib.Telemetry:
    provider = get_active_provider()
    return {
        TelemetryProvider.SENTRY: lambda: SentryTelemetry(),
        TelemetryProvider.OPENTELEMETRY: lambda: OpenTelemetryTelemetry(),
        TelemetryProvider.DATADOG: lambda: DatadogTelemetry(),
    }.get(provider, lambda: lib.NoOpTelemetry())()


def get_telemetry_for_request() -> lib.Telemetry:
    return get_telemetry_instance()


# =============================================================================
# Sentry Implementation
# =============================================================================


class SentrySpanContext(lib.SpanContext):
    def __init__(self, span):
        self._span = span

    def __enter__(self) -> "SentrySpanContext":
        self._span and self._span.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if not self._span:
            return
        if exc_val:
            self._span.set_status("error")
            self._span.set_data("error.message", str(exc_val))
        self._span.__exit__(exc_type, exc_val, exc_tb)

    def set_attribute(self, key: str, value: typing.Any) -> None:
        self._span and key and self._span.set_data(key, value)

    def set_status(self, status: str, message: str = None) -> None:
        if not self._span:
            return
        self._span.set_status(status or "ok")
        message and self._span.set_data("status.message", message)

    def record_exception(self, exception: Exception) -> None:
        if self._span and exception:
            self._span.set_data("exception.type", type(exception).__name__)
            self._span.set_data("exception.message", str(exception))

    def add_event(self, name: str, attributes: typing.Dict[str, typing.Any] = None) -> None:
        self._span and name and self._span.set_data(f"event.{name}", attributes or {})


class SentryTelemetry(lib.Telemetry):
    """Sentry-backed telemetry. Requires: sentry-sdk >= 2.0.0"""

    def start_span(self, name: str, attributes: typing.Dict[str, typing.Any] = None, kind: str = None) -> lib.SpanContext:
        try:
            import sentry_sdk
            current = sentry_sdk.get_current_span()
            span = (
                current.start_child(op=kind or "function", name=name)
                if current else
                sentry_sdk.start_span(op=kind or "function", name=name)
            )
            [span.set_data(k, v) for k, v in (attributes or {}).items()]
            return SentrySpanContext(span)
        except Exception:
            return lib.NoOpSpanContext()

    def add_breadcrumb(self, message: str, category: str, data: typing.Dict[str, typing.Any] = None, level: str = "info") -> None:
        failsafe(lambda: __import__("sentry_sdk").add_breadcrumb(
            message=message, category=category or "default", data=data or {}, level=level or "info"
        ))

    def record_metric(self, name: str, value: float, unit: str = None, tags: typing.Dict[str, str] = None, metric_type: str = "counter") -> None:
        def _record():
            from sentry_sdk import metrics
            metric_tags = tags or {}
            # Use metrics.count for counters (newer API), metrics.gauge for gauges, metrics.distribution for histograms
            if metric_type == "counter":
                metrics.count(name, value, tags=metric_tags, unit=unit)
            elif metric_type == "gauge":
                metrics.gauge(name, value, tags=metric_tags, unit=unit)
            elif metric_type == "distribution":
                metrics.distribution(name, value, tags=metric_tags, unit=unit)
            else:
                metrics.count(name, value, tags=metric_tags, unit=unit)
        failsafe(_record)

    def capture_exception(self, exception: Exception, context: typing.Dict[str, typing.Any] = None, tags: typing.Dict[str, str] = None) -> None:
        def _capture():
            import sentry_sdk
            with sentry_sdk.push_scope() as scope:
                context and scope.set_context("karrio", context)
                [scope.set_tag(k, v) for k, v in (tags or {}).items()]
                sentry_sdk.capture_exception(exception)
        failsafe(_capture)

    def set_context(self, name: str, data: typing.Dict[str, typing.Any]) -> None:
        failsafe(lambda: __import__("sentry_sdk").set_context(name, data or {}))

    def set_tag(self, key: str, value: str) -> None:
        failsafe(lambda: __import__("sentry_sdk").set_tag(key, str(value) if value is not None else ""))

    def set_user(self, user_id: str = None, email: str = None, username: str = None, ip_address: str = None, data: typing.Dict[str, typing.Any] = None) -> None:
        def _set_user():
            import sentry_sdk
            user_data = {
                **({"id": user_id} if user_id else {}),
                **({"email": email} if email else {}),
                **({"username": username} if username else {}),
                **({"ip_address": ip_address} if ip_address else {}),
                **(data or {}),
            }
            user_data and sentry_sdk.set_user(user_data)
        failsafe(_set_user)

    def start_transaction(self, name: str, op: str = None, attributes: typing.Dict[str, typing.Any] = None) -> lib.SpanContext:
        try:
            import sentry_sdk
            transaction = sentry_sdk.start_transaction(name=name, op=op or "http.server")
            [transaction.set_data(k, v) for k, v in (attributes or {}).items()]
            return SentrySpanContext(transaction)
        except Exception:
            return lib.NoOpSpanContext()


# =============================================================================
# OpenTelemetry Implementation
# =============================================================================


class OTELSpanContext(lib.SpanContext):
    def __init__(self, span, token=None):
        self._span = span
        self._token = token

    def __enter__(self) -> "OTELSpanContext":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if not self._span:
            return
        try:
            from opentelemetry.trace import StatusCode
            if exc_val:
                self._span.set_status(StatusCode.ERROR, str(exc_val))
                self._span.record_exception(exc_val)
            else:
                self._span.set_status(StatusCode.OK)
            self._span.end()
        except Exception:
            pass
        finally:
            self._token and failsafe(lambda: __import__("opentelemetry").context.detach(self._token))

    def _safe_value(self, value: typing.Any) -> typing.Any:
        if value is None:
            return ""
        if isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, (list, tuple)):
            return [str(v) for v in value]
        return str(value)

    def set_attribute(self, key: str, value: typing.Any) -> None:
        self._span and key and self._span.set_attribute(key, self._safe_value(value))

    def set_status(self, status: str, message: str = None) -> None:
        def _set():
            from opentelemetry.trace import StatusCode
            code = {"ok": StatusCode.OK, "error": StatusCode.ERROR}.get((status or "ok").lower(), StatusCode.UNSET)
            self._span.set_status(code, message)
        self._span and failsafe(_set)

    def record_exception(self, exception: Exception) -> None:
        self._span and exception and self._span.record_exception(exception)

    def add_event(self, name: str, attributes: typing.Dict[str, typing.Any] = None) -> None:
        if self._span and name:
            safe_attrs = {k: self._safe_value(v) for k, v in (attributes or {}).items()}
            self._span.add_event(name, attributes=safe_attrs or None)


class OpenTelemetryTelemetry(lib.Telemetry):
    """OpenTelemetry-backed telemetry. Requires: opentelemetry-api >= 1.20.0"""

    def __init__(self):
        self._tracer = None
        self._meter = None

    def _get_tracer(self):
        if not self._tracer:
            self._tracer = failsafe(lambda: __import__("opentelemetry").trace.get_tracer("karrio"))
        return self._tracer

    def _get_meter(self):
        if not self._meter:
            self._meter = failsafe(lambda: __import__("opentelemetry").metrics.get_meter("karrio"))
        return self._meter

    def _safe_value(self, value: typing.Any) -> typing.Any:
        if value is None:
            return ""
        if isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, (list, tuple)):
            return [str(v) for v in value]
        return str(value)

    def start_span(self, name: str, attributes: typing.Dict[str, typing.Any] = None, kind: str = None) -> lib.SpanContext:
        try:
            from opentelemetry import trace, context
            from opentelemetry.trace import SpanKind

            tracer = self._get_tracer()
            if not tracer:
                return lib.NoOpSpanContext()

            kind_map = {"client": SpanKind.CLIENT, "server": SpanKind.SERVER, "producer": SpanKind.PRODUCER, "consumer": SpanKind.CONSUMER}
            span_kind = kind_map.get((kind or "").lower(), SpanKind.INTERNAL)
            safe_attrs = {k: self._safe_value(v) for k, v in (attributes or {}).items()} or None

            span = tracer.start_span(name, kind=span_kind, attributes=safe_attrs)
            ctx = trace.set_span_in_context(span)
            token = context.attach(ctx)

            return OTELSpanContext(span, token)
        except Exception:
            return lib.NoOpSpanContext()

    def add_breadcrumb(self, message: str, category: str, data: typing.Dict[str, typing.Any] = None, level: str = "info") -> None:
        def _add():
            from opentelemetry import trace
            span = trace.get_current_span()
            if span and span.is_recording():
                attrs = {"category": category or "default", "level": level or "info", **{k: self._safe_value(v) for k, v in (data or {}).items()}}
                span.add_event(message, attributes=attrs)
        failsafe(_add)

    def record_metric(self, name: str, value: float, unit: str = None, tags: typing.Dict[str, str] = None, metric_type: str = "counter") -> None:
        def _record():
            meter = self._get_meter()
            if not meter:
                return
            attrs = {k: str(v) for k, v in (tags or {}).items()}
            if metric_type == "counter":
                meter.create_counter(name, unit=unit or "1").add(max(0, int(value)), attributes=attrs)
            elif metric_type == "gauge":
                meter.create_up_down_counter(name, unit=unit or "1").add(int(value), attributes=attrs)
            elif metric_type == "distribution":
                meter.create_histogram(name, unit=unit or "ms").record(value, attributes=attrs)
        failsafe(_record)

    def capture_exception(self, exception: Exception, context: typing.Dict[str, typing.Any] = None, tags: typing.Dict[str, str] = None) -> None:
        def _capture():
            from opentelemetry import trace
            span = trace.get_current_span()
            if span and span.is_recording():
                span.record_exception(exception)
                [span.set_attribute(f"context.{k}", self._safe_value(v)) for k, v in (context or {}).items()]
                [span.set_attribute(k, v) for k, v in (tags or {}).items()]
        failsafe(_capture)

    def set_context(self, name: str, data: typing.Dict[str, typing.Any]) -> None:
        def _set():
            from opentelemetry import trace
            span = trace.get_current_span()
            if span and span.is_recording():
                [span.set_attribute(f"{name}.{k}", self._safe_value(v)) for k, v in (data or {}).items()]
        failsafe(_set)

    def set_tag(self, key: str, value: str) -> None:
        def _set():
            from opentelemetry import trace
            span = trace.get_current_span()
            span and span.is_recording() and span.set_attribute(key, str(value) if value is not None else "")
        failsafe(_set)

    def set_user(self, user_id: str = None, email: str = None, username: str = None, ip_address: str = None, data: typing.Dict[str, typing.Any] = None) -> None:
        def _set():
            from opentelemetry import trace
            span = trace.get_current_span()
            if span and span.is_recording():
                user_id and span.set_attribute("enduser.id", user_id)
                email and span.set_attribute("enduser.email", email)
                username and span.set_attribute("enduser.username", username)
                ip_address and span.set_attribute("client.address", ip_address)
                [span.set_attribute(f"enduser.{k}", self._safe_value(v)) for k, v in (data or {}).items()]
        failsafe(_set)

    def start_transaction(self, name: str, op: str = None, attributes: typing.Dict[str, typing.Any] = None) -> lib.SpanContext:
        attrs = {**(attributes or {}), **({"operation": op} if op else {})}
        return self.start_span(name, attributes=attrs or None, kind="server")


# =============================================================================
# Datadog Implementation
# =============================================================================


class DatadogSpanContext(lib.SpanContext):
    def __init__(self, span):
        self._span = span

    def __enter__(self) -> "DatadogSpanContext":
        self._span and failsafe(lambda: self._span.__enter__())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if not self._span:
            return
        exc_val and failsafe(lambda: self._span.set_exc_info(exc_type, exc_val, exc_tb))
        failsafe(lambda: self._span.__exit__(exc_type, exc_val, exc_tb))

    def _safe_value(self, value: typing.Any) -> typing.Any:
        return value if isinstance(value, (str, int, float, bool)) else str(value) if value is not None else ""

    def set_attribute(self, key: str, value: typing.Any) -> None:
        self._span and key and failsafe(lambda: self._span.set_tag(key, self._safe_value(value)))

    def set_status(self, status: str, message: str = None) -> None:
        def _set():
            if (status or "ok").lower() == "error":
                self._span.error = 1
                message and self._span.set_tag("error.message", message)
            else:
                self._span.error = 0
        self._span and failsafe(_set)

    def record_exception(self, exception: Exception) -> None:
        def _record():
            import sys
            info = sys.exc_info()
            self._span.set_exc_info(info[0], info[1], info[2]) if info[1] is exception else self._span.set_exc_info(type(exception), exception, None)
        self._span and exception and failsafe(_record)

    def add_event(self, name: str, attributes: typing.Dict[str, typing.Any] = None) -> None:
        self._span and name and failsafe(lambda: self._span.set_tag(f"event.{name}", str(attributes or {})))


class DatadogTelemetry(lib.Telemetry):
    """Datadog-backed telemetry. Requires: ddtrace >= 2.0.0"""

    def __init__(self):
        self._tracer = None

    def _get_tracer(self):
        if not self._tracer:
            self._tracer = failsafe(lambda: __import__("ddtrace").tracer)
        return self._tracer

    def _safe_value(self, value: typing.Any) -> typing.Any:
        return value if isinstance(value, (str, int, float, bool)) else str(value) if value is not None else ""

    def start_span(self, name: str, attributes: typing.Dict[str, typing.Any] = None, kind: str = None) -> lib.SpanContext:
        try:
            tracer = self._get_tracer()
            if not tracer:
                return lib.NoOpSpanContext()

            kind_map = {"client": "http", "server": "web", "consumer": "worker", "producer": "worker", "internal": "custom"}
            span = tracer.trace(name, service="karrio", span_type=kind_map.get((kind or "").lower()))
            [span.set_tag(k, self._safe_value(v)) for k, v in (attributes or {}).items()]

            return DatadogSpanContext(span)
        except Exception:
            return lib.NoOpSpanContext()

    def add_breadcrumb(self, message: str, category: str, data: typing.Dict[str, typing.Any] = None, level: str = "info") -> None:
        def _add():
            tracer = self._get_tracer()
            span = tracer and tracer.current_span()
            if span:
                cat = category or "default"
                span.set_tag(f"breadcrumb.{cat}", message)
                [span.set_tag(f"breadcrumb.{cat}.{k}", str(v)) for k, v in (data or {}).items()]
        failsafe(_add)

    def record_metric(self, name: str, value: float, unit: str = None, tags: typing.Dict[str, str] = None, metric_type: str = "counter") -> None:
        def _record():
            try:
                from datadog import statsd
                dd_tags = [f"{k}:{v}" for k, v in (tags or {}).items()]
                {"counter": statsd.increment, "gauge": statsd.gauge, "distribution": statsd.distribution}.get(
                    metric_type, statsd.increment
                )(name, value, tags=dd_tags)
            except ImportError:
                tracer = self._get_tracer()
                span = tracer and tracer.current_span()
                span and span.set_metric(name, value)
        failsafe(_record)

    def capture_exception(self, exception: Exception, context: typing.Dict[str, typing.Any] = None, tags: typing.Dict[str, str] = None) -> None:
        def _capture():
            import sys
            tracer = self._get_tracer()
            span = tracer and tracer.current_span()
            if span:
                info = sys.exc_info()
                span.set_exc_info(info[0], info[1], info[2]) if info[1] is exception else span.set_exc_info(type(exception), exception, None)
                [span.set_tag(f"context.{k}", str(v)) for k, v in (context or {}).items()]
                [span.set_tag(k, v) for k, v in (tags or {}).items()]
        failsafe(_capture)

    def set_context(self, name: str, data: typing.Dict[str, typing.Any]) -> None:
        def _set():
            tracer = self._get_tracer()
            span = tracer and tracer.current_span()
            span and [span.set_tag(f"{name}.{k}", str(v)) for k, v in (data or {}).items()]
        failsafe(_set)

    def set_tag(self, key: str, value: str) -> None:
        def _set():
            tracer = self._get_tracer()
            span = tracer and tracer.current_span()
            span and span.set_tag(key, str(value) if value is not None else "")
        failsafe(_set)

    def set_user(self, user_id: str = None, email: str = None, username: str = None, ip_address: str = None, data: typing.Dict[str, typing.Any] = None) -> None:
        def _set():
            try:
                from ddtrace import tracer
                from ddtrace.contrib.trace_utils import set_user
                if any([user_id, email, username]):
                    set_user(tracer, user_id=user_id, email=email, name=username)
                    return
            except (ImportError, AttributeError):
                pass
            tracer = self._get_tracer()
            span = tracer and tracer.current_span()
            if span:
                user_id and span.set_tag("usr.id", user_id)
                email and span.set_tag("usr.email", email)
                username and span.set_tag("usr.name", username)
                ip_address and span.set_tag("http.client_ip", ip_address)
                [span.set_tag(f"usr.{k}", str(v)) for k, v in (data or {}).items()]
        failsafe(_set)

    def start_transaction(self, name: str, op: str = None, attributes: typing.Dict[str, typing.Any] = None) -> lib.SpanContext:
        attrs = {**(attributes or {}), **({"operation": op} if op else {})}
        return self.start_span(name, attributes=attrs or None, kind="server")


# =============================================================================
# Background Task Utilities
# =============================================================================


def create_task_tracer(task_name: str = None, context: typing.Dict[str, typing.Any] = None) -> lib.Tracer:
    """Create a Tracer with telemetry for background tasks (Huey/Celery).

    Works correctly without Django HTTP request context.
    """
    tracer = lib.Tracer()
    tracer.set_telemetry(get_telemetry_instance())
    tracer.set_tag("execution.type", "background_task")
    task_name and tracer.set_tag("task.name", task_name)

    ctx = context or {}
    ctx.get("user_id") and tracer.set_user(user_id=str(ctx["user_id"]))
    ctx.get("org_id") and tracer.set_tag("org.id", str(ctx["org_id"]))
    ctx.get("test_mode") is not None and tracer.set_tag("test_mode", str(ctx["test_mode"]).lower())

    return tracer


def with_task_telemetry(task_name: str = None):
    """Decorator that adds telemetry instrumentation to background tasks."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            op_name = task_name or func.__name__
            telemetry = get_telemetry_instance()

            telemetry.add_breadcrumb(f"Starting background task: {op_name}", "task", {"task_name": op_name}, "info")

            with telemetry.start_span(f"task.{op_name}", kind="consumer") as span:
                span.set_attribute("task.name", op_name)
                span.set_attribute("task.type", "background")

                try:
                    result = func(*args, **kwargs)
                    span.set_status("ok")
                    telemetry.record_metric(f"karrio_task_{op_name}_success", 1, tags={"task_name": op_name})
                    return result

                except Exception as e:
                    span.set_status("error", str(e))
                    span.record_exception(e)
                    telemetry.record_metric(f"karrio_task_{op_name}_error", 1, tags={"task_name": op_name, "error_type": type(e).__name__})
                    telemetry.capture_exception(e, context={"task_name": op_name}, tags={"task_name": op_name})
                    raise

        return wrapper
    return decorator
