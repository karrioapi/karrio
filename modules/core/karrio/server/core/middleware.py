import json
import threading
from django.db.models import Q
from django.http import HttpResponse
from karrio.core.utils import Tracer
from karrio.server.conf import settings


class CreatorAccess:
    def __call__(self, context, key: str = "created_by", **kwargs) -> Q:
        user_key = f"{key}_id"
        user = getattr(context, "user", None)

        return Q(**{user_key: getattr(user, "id", None)})


class WideAccess:
    def __call__(self, *args, **kwargs) -> Q:
        return Q()


class UserToken:
    def __call__(self, context, **kwargs) -> dict:
        return dict(user=getattr(context, "user", context))


class SessionContext:
    """Middleware that manages request context, tracing, and telemetry.

    This middleware:
    1. Creates a Tracer instance for each request
    2. Injects telemetry (Sentry) if configured
    3. Stores the request in thread-local storage for access throughout the request lifecycle
    4. Saves tracing records after the response is generated
    5. Sets up user context for telemetry
    """

    _threadmap: dict = {}

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        import time

        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Create tracer with telemetry injection
        tracer = Tracer()
        self._inject_telemetry(tracer, request)
        request.tracer = tracer

        self._threadmap[threading.get_ident()] = request

        # Track request timing
        start_time = time.time()

        response = self.get_response(request)

        # Record request metrics
        self._record_request_metrics(request, response, start_time)

        # Code to be executed for each request/response after
        # the view is called.
        try:
            self._save_tracing_records(request, schema=settings.schema)
            del self._threadmap[threading.get_ident()]
        except KeyError:
            pass

        return response

    def _inject_telemetry(self, tracer: Tracer, request):
        """Inject telemetry into tracer if Sentry is configured.

        This method conditionally imports and sets up SentryTelemetry
        only when SENTRY_DSN is configured, ensuring zero overhead
        when Sentry is not in use.
        """
        try:
            from karrio.server.core.telemetry import get_telemetry_for_request

            telemetry = get_telemetry_for_request()
            tracer.set_telemetry(telemetry)

            # Set user context if authenticated
            user = getattr(request, "user", None)
            if user and getattr(user, "is_authenticated", False):
                tracer.set_user(
                    user_id=str(user.id) if hasattr(user, "id") else None,
                    email=getattr(user, "email", None),
                    username=getattr(user, "username", None),
                )

            # Set request context tags
            tracer.set_tag("http.method", request.method)
            tracer.set_tag("http.path", request.path)

            # Set test_mode tag if available
            test_mode = getattr(request, "test_mode", None)
            if test_mode is not None:
                tracer.set_tag("test_mode", str(test_mode).lower())

            # Set org context for multi-tenant deployments
            org = getattr(request, "org", None)
            if org:
                tracer.set_tag("org_id", str(org.id) if hasattr(org, "id") else str(org))

        except ImportError:
            # Telemetry module not available, continue with NoOpTelemetry
            pass
        except Exception:
            # Any other error, continue with NoOpTelemetry
            pass

    def _record_request_metrics(self, request, response, start_time):
        """Record HTTP request metrics to telemetry."""
        import time

        try:
            from karrio.server.core.telemetry import get_telemetry_for_request

            telemetry = get_telemetry_for_request()
            duration_ms = (time.time() - start_time) * 1000

            # Common tags for all metrics
            tags = {
                "method": request.method,
                "path": request.path,
                "status_code": str(response.status_code),
            }

            # Add test_mode tag if available
            test_mode = getattr(request, "test_mode", None)
            if test_mode is not None:
                tags["test_mode"] = str(test_mode).lower()

            # Record request count
            telemetry.record_metric("karrio.http.request", 1, tags=tags, metric_type="counter")

            # Record response time distribution
            telemetry.record_metric("karrio.http.duration", duration_ms, unit="millisecond", tags=tags, metric_type="distribution")

            # Record error count for 4xx/5xx responses
            if response.status_code >= 400:
                error_tags = {**tags, "error_class": "client" if response.status_code < 500 else "server"}
                telemetry.record_metric("karrio.http.error", 1, tags=error_tags, metric_type="counter")

        except Exception:
            pass  # Don't let metrics recording break the request

    def _save_tracing_records(self, request, schema: str = None):
        from karrio.server.tracing.utils import save_tracing_records

        save_tracing_records(request, schema=schema)

    @classmethod
    def get_current_request(cls):
        return cls._threadmap.get(threading.get_ident())


class NonHtmlDebugToolbarMiddleware:
    """
    The Django Debug Toolbar usually only works for views that return HTML.
    This middleware wraps any non-HTML response in HTML if the request
    has a 'debug' query parameter (e.g. https://api.karrio.io/foo?debug)
    Special handling for json (pretty printing) and
    binary data (only show data length)
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.GET.get("debug") == "":
            if response["Content-Type"] == "application/octet-stream":
                new_content = (
                    "<html><body>Binary Data, "
                    "Length: {}</body></html>".format(len(response.content))
                )
                response = HttpResponse(new_content)
            elif response["Content-Type"] != "text/html":
                content = response.content
                try:
                    json_ = json.loads(content)
                    content = json.dumps(json_, sort_keys=True, indent=2)
                except ValueError:
                    pass
                response = HttpResponse(
                    "<html><body><pre>{}" "</pre></body></html>".format(content)
                )

        return response
