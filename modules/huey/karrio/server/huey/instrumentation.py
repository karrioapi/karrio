"""
OpenTelemetry instrumentation for Huey task queue.

Provides tracing support for Huey tasks, enabling distributed tracing
across API requests and background tasks.
"""

import functools
import logging
from collections.abc import Callable
from typing import Any

from opentelemetry import context, propagate, trace
from opentelemetry.trace import Status, StatusCode

logger = logging.getLogger(__name__)


class HueyInstrumentor:
    """Instrumentation for Huey task queue."""

    _instance = None
    _instrumented = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def instrument(self, huey_instance=None):
        if self._instrumented:
            logger.debug("Huey already instrumented")
            return

        try:
            if huey_instance is None:
                from django.conf import settings

                huey_instance = settings.HUEY

            original_task = huey_instance.task
            huey_instance.task = self._wrap_task_decorator(original_task, huey_instance)

            if hasattr(huey_instance, "periodic_task"):
                original_periodic = huey_instance.periodic_task
                huey_instance.periodic_task = self._wrap_task_decorator(original_periodic, huey_instance)

            self._instrumented = True
            logger.info("Huey instrumented for OpenTelemetry")

        except Exception as e:
            logger.warning("Failed to instrument Huey: %s", e)

    def _wrap_task_decorator(self, original_decorator: Callable, huey_instance) -> Callable:
        @functools.wraps(original_decorator)
        def wrapped_decorator(*args, **kwargs):
            decorated = original_decorator(*args, **kwargs)

            def task_wrapper(fn):
                task_fn = decorated(fn)

                @functools.wraps(task_fn)
                def traced_task(*task_args, **task_kwargs):
                    tracer = trace.get_tracer(__name__)

                    trace_context = task_kwargs.pop("_otel_context", None)
                    if trace_context:
                        ctx = propagate.extract(trace_context)
                        token = context.attach(ctx)
                    else:
                        token = None

                    task_name = fn.__name__
                    with tracer.start_as_current_span(
                        f"huey.task.{task_name}",
                        kind=trace.SpanKind.CONSUMER,
                    ) as span:
                        try:
                            span.set_attribute("messaging.system", "huey")
                            span.set_attribute("messaging.destination", task_name)
                            span.set_attribute("messaging.operation", "process")
                            span.set_attribute("task.name", task_name)

                            result = task_fn(*task_args, **task_kwargs)
                            span.set_status(Status(StatusCode.OK))
                            return result

                        except Exception as e:
                            span.set_status(Status(StatusCode.ERROR, str(e)))
                            span.record_exception(e)
                            raise
                        finally:
                            if token:
                                context.detach(token)

                traced_task.task = task_fn.task if hasattr(task_fn, "task") else task_fn
                if hasattr(task_fn, "__name__"):
                    traced_task.__name__ = task_fn.__name__
                if hasattr(task_fn, "__module__"):
                    traced_task.__module__ = task_fn.__module__

                return traced_task

            return task_wrapper

        return wrapped_decorator


def inject_trace_context(task_kwargs: dict[str, Any]) -> dict[str, Any]:
    """Inject current trace context into task kwargs for propagation."""
    carrier = {}
    propagate.inject(carrier)
    if carrier:
        task_kwargs["_otel_context"] = carrier
    return task_kwargs
