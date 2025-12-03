# type: ignore
import posthog
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from karrio.server.settings.base import *

# Try to import PostHog integration, fallback if not available
try:
    from posthog.sentry.posthog_integration import PostHogIntegration
except ImportError:
    try:
        from posthog.sentry import PostHogIntegration
    except ImportError:
        # PostHog Sentry integration not available in this version
        PostHogIntegration = None


# Health check apps settings
HEALTH_CHECK_APPS = [
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.contrib.migrations",
    "health_check.contrib.psutil",
]
INSTALLED_APPS += HEALTH_CHECK_APPS


# PostHog
POSTHOG_KEY = config("POSTHOG_KEY", default=None)
POSTHOG_HOST = config("POSTHOG_HOST", default="https://app.posthog.com")

if POSTHOG_KEY:
    posthog.project_api_key = POSTHOG_KEY
    posthog.host = POSTHOG_HOST


# =============================================================================
# Sentry Configuration
# =============================================================================
#
# Sentry provides error tracking, performance monitoring, and distributed
# tracing for Karrio. When SENTRY_DSN is configured, the following features
# are enabled:
#
# 1. Error Tracking: All unhandled exceptions are captured with full context
# 2. Performance Monitoring: API endpoints and gateway operations are traced
# 3. Distributed Tracing: Carrier API calls are linked to parent transactions
# 4. Metrics: Custom metrics for carrier operations (rates, shipments, etc.)
# 5. Logging Integration: ERROR/CRITICAL logs are sent to Sentry
#
# Environment Variables:
#   SENTRY_DSN                  - Sentry Data Source Name (required to enable)
#   SENTRY_ENVIRONMENT          - Environment name (default: from ENV or "production")
#   SENTRY_RELEASE              - Release version (default: VERSION)
#   SENTRY_TRACES_SAMPLE_RATE   - Transaction sampling rate 0.0-1.0 (default: 1.0)
#   SENTRY_PROFILES_SAMPLE_RATE - Profile sampling rate 0.0-1.0 (default: 1.0)
#   SENTRY_SEND_PII             - Send personally identifiable information (default: true)
#   SENTRY_DEBUG                - Enable Sentry debug mode (default: false)
#   SENTRY_TRACE_PROPAGATION_TARGETS - Regex patterns for distributed tracing (default: localhost)
#
# =============================================================================

sentry_sdk.utils.MAX_STRING_LENGTH = 4096
SENTRY_DSN = config("SENTRY_DSN", default=None)
SENTRY_ENVIRONMENT = config("SENTRY_ENVIRONMENT", default=config("ENV", default="production"))
SENTRY_RELEASE = config("SENTRY_RELEASE", default=config("VERSION", default=None))
# Lower default sample rates for better performance (was 1.0/100%)
SENTRY_TRACES_SAMPLE_RATE = config("SENTRY_TRACES_SAMPLE_RATE", default=0.1, cast=float)  # 10% of transactions
SENTRY_PROFILES_SAMPLE_RATE = config("SENTRY_PROFILES_SAMPLE_RATE", default=0.0, cast=float)  # Disabled by default
SENTRY_SEND_PII = config("SENTRY_SEND_PII", default=True, cast=bool)
SENTRY_DEBUG = config("SENTRY_DEBUG", default=False, cast=bool)
# Trace propagation targets for distributed tracing (internal services only)
# Comma-separated list of regex patterns; headers are NOT sent to carrier APIs
# Configure via env var for your domains (e.g., ".*\.yourdomain\.com,localhost")
SENTRY_TRACE_PROPAGATION_TARGETS = config(
    "SENTRY_TRACE_PROPAGATION_TARGETS",
    default=r"localhost",
)


def _sentry_before_send(event, hint):
    """Pre-process events before sending to Sentry.

    This hook allows us to:
    - Scrub sensitive data (API keys, tokens, passwords)
    - Add custom tags
    - Filter out certain events
    """
    # Scrub sensitive data from request bodies
    if "request" in event:
        request_data = event["request"]

        # Scrub headers
        if "headers" in request_data:
            sensitive_headers = ["authorization", "x-api-key", "cookie", "x-csrf-token"]
            for header in sensitive_headers:
                if header in request_data["headers"]:
                    request_data["headers"][header] = "[Filtered]"

        # Scrub POST data
        if "data" in request_data and isinstance(request_data["data"], dict):
            sensitive_fields = [
                "password", "secret", "token", "api_key", "apikey",
                "access_token", "refresh_token", "client_secret",
                "account_number", "meter_number", "license_key",
            ]
            for field in sensitive_fields:
                for key in list(request_data["data"].keys()):
                    if field.lower() in key.lower():
                        request_data["data"][key] = "[Filtered]"

    return event


def _sentry_before_send_transaction(event, hint):
    """Pre-process transactions before sending to Sentry.

    This hook allows us to:
    - Filter out noisy transactions (health checks, static files)
    - Add custom tags
    """
    transaction_name = event.get("transaction", "")

    # Filter out health check and monitoring endpoints
    noisy_endpoints = [
        "/health",
        "/ready",
        "/live",
        "/_health",
        "/favicon.ico",
        "/static/",
        "/robots.txt",
    ]

    for endpoint in noisy_endpoints:
        if transaction_name.startswith(endpoint):
            return None  # Drop this transaction

    return event


if SENTRY_DSN:
    # Build integrations list
    integrations = [
        DjangoIntegration(
            transaction_style="url",  # Use URL patterns for transaction names
            middleware_spans=False,   # Disabled for performance (was True)
            signals_spans=False,      # Disabled for performance (was True)
        ),
    ]

    # Add PostHog integration if available
    if POSTHOG_KEY and PostHogIntegration is not None:
        integrations.append(PostHogIntegration())

    # Try to add Redis integration if Redis is configured
    try:
        from sentry_sdk.integrations.redis import RedisIntegration
        if config("REDIS_URL", default=None) or config("REDIS_HOST", default=None):
            integrations.append(RedisIntegration())
    except ImportError:
        pass

    # Try to add Huey integration for background tasks
    try:
        from sentry_sdk.integrations.huey import HueyIntegration
        integrations.append(HueyIntegration())
    except ImportError:
        pass

    # Try to add httpx integration for async HTTP clients
    try:
        from sentry_sdk.integrations.httpx import HttpxIntegration
        integrations.append(HttpxIntegration())
    except Exception:
        pass  # httpx may not be installed

    # Try to add Strawberry GraphQL integration
    try:
        from sentry_sdk.integrations.strawberry import StrawberryIntegration
        integrations.append(StrawberryIntegration(async_execution=False))
    except Exception:
        pass  # strawberry integration may not be available

    # Parse trace propagation targets (comma-separated regex patterns)
    trace_targets = [
        pattern.strip()
        for pattern in SENTRY_TRACE_PROPAGATION_TARGETS.split(",")
        if pattern.strip()
    ]

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=integrations,

        # Environment and release tracking
        environment=SENTRY_ENVIRONMENT,
        release=SENTRY_RELEASE,

        # Performance monitoring (lower sample rates for better performance)
        traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
        # Only enable profiling if explicitly configured (disabled by default)
        **({"profile_session_sample_rate": SENTRY_PROFILES_SAMPLE_RATE, "profile_lifecycle": "trace"} if SENTRY_PROFILES_SAMPLE_RATE > 0 else {}),

        # Distributed tracing - propagate trace headers to internal services
        # Note: Headers are NOT sent to carrier APIs (they wouldn't understand them)
        trace_propagation_targets=trace_targets,

        # Privacy settings
        send_default_pii=SENTRY_SEND_PII,

        # Logging integration
        enable_logs=True,

        # Debug mode
        debug=SENTRY_DEBUG,

        # Event processing hooks
        before_send=_sentry_before_send,
        before_send_transaction=_sentry_before_send_transaction,

        # Additional options (reduced for performance)
        max_breadcrumbs=25,  # Reduced from 50 for lower memory usage
        attach_stacktrace=True,  # Attach stack traces to messages
        include_source_context=False,  # Disabled for performance (was True)
        include_local_variables=False,  # Disabled for performance (was True)
    )

    # Set default tags that will be applied to all events
    sentry_sdk.set_tag("service", "karrio-api")
    sentry_sdk.set_tag("framework", "django")

    import logging
    logger = logging.getLogger(__name__)
    logger.info(
        f"Sentry initialized: env={SENTRY_ENVIRONMENT}, "
        f"traces_sample_rate={SENTRY_TRACES_SAMPLE_RATE}"
    )


# OpenTelemetry Configuration
OTEL_ENABLED = config("OTEL_ENABLED", default=False, cast=bool)
OTEL_SERVICE_NAME = config("OTEL_SERVICE_NAME", default="karrio-api")
OTEL_EXPORTER_OTLP_ENDPOINT = config("OTEL_EXPORTER_OTLP_ENDPOINT", default=None)
OTEL_EXPORTER_OTLP_PROTOCOL = config("OTEL_EXPORTER_OTLP_PROTOCOL", default="grpc")
OTEL_EXPORTER_OTLP_HEADERS = config("OTEL_EXPORTER_OTLP_HEADERS", default="")
OTEL_TRACES_EXPORTER = config("OTEL_TRACES_EXPORTER", default="otlp")
OTEL_METRICS_EXPORTER = config("OTEL_METRICS_EXPORTER", default="otlp")
OTEL_LOGS_EXPORTER = config("OTEL_LOGS_EXPORTER", default="otlp")
OTEL_RESOURCE_ATTRIBUTES = config("OTEL_RESOURCE_ATTRIBUTES", default="")
OTEL_ENVIRONMENT = config("OTEL_ENVIRONMENT", default=config("ENV", default="production"))

# Only initialize OpenTelemetry if enabled and endpoint is configured
if OTEL_ENABLED and OTEL_EXPORTER_OTLP_ENDPOINT:
    import logging
    from opentelemetry import trace, metrics
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
    from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
    from opentelemetry.instrumentation.django import DjangoInstrumentor
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    from opentelemetry.instrumentation.logging import LoggingInstrumentor
    from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
    from opentelemetry.instrumentation.redis import RedisInstrumentor
    
    # Import appropriate exporter based on protocol
    if OTEL_EXPORTER_OTLP_PROTOCOL == "grpc":
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
        from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
    else:  # http/protobuf
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
    
    # Parse headers if provided
    headers = {}
    if OTEL_EXPORTER_OTLP_HEADERS:
        for header_pair in OTEL_EXPORTER_OTLP_HEADERS.split(","):
            if "=" in header_pair:
                key, value = header_pair.split("=", 1)
                headers[key.strip()] = value.strip()
    
    # Parse resource attributes
    resource_attributes = {
        SERVICE_NAME: OTEL_SERVICE_NAME,
        SERVICE_VERSION: config("VERSION", default="unknown"),
        "environment": OTEL_ENVIRONMENT,
        "deployment.environment": OTEL_ENVIRONMENT,
    }
    
    if OTEL_RESOURCE_ATTRIBUTES:
        for attr_pair in OTEL_RESOURCE_ATTRIBUTES.split(","):
            if "=" in attr_pair:
                key, value = attr_pair.split("=", 1)
                resource_attributes[key.strip()] = value.strip()
    
    # Create resource
    resource = Resource(attributes=resource_attributes)
    
    # Configure Trace Provider
    trace_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(trace_provider)
    
    # Configure span exporter
    span_exporter = OTLPSpanExporter(
        endpoint=OTEL_EXPORTER_OTLP_ENDPOINT,
        headers=headers if headers else None,
    )
    span_processor = BatchSpanProcessor(span_exporter)
    trace_provider.add_span_processor(span_processor)
    
    # Configure Metrics Provider
    metric_exporter = OTLPMetricExporter(
        endpoint=OTEL_EXPORTER_OTLP_ENDPOINT,
        headers=headers if headers else None,
    )
    metric_reader = PeriodicExportingMetricReader(
        exporter=metric_exporter,
        export_interval_millis=30000,  # Export metrics every 30 seconds
    )
    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[metric_reader],
    )
    metrics.set_meter_provider(meter_provider)
    
    # Instrument Django
    DjangoInstrumentor().instrument(
        is_sql_commentor_enabled=True,  # Add trace context to SQL queries
        request_hook=lambda span, request: span.set_attribute("http.client_ip", request.META.get("REMOTE_ADDR", "")),
        response_hook=lambda span, request, response: span.set_attribute("http.response.size", len(response.content) if hasattr(response, 'content') else 0),
    )
    
    # Instrument other libraries
    RequestsInstrumentor().instrument()  # HTTP client requests
    LoggingInstrumentor().instrument(set_logging_format=True)  # Add trace context to logs
    
    # Instrument database if PostgreSQL is used
    if config("DATABASE_ENGINE", default="").endswith("postgresql"):
        try:
            Psycopg2Instrumentor().instrument()
        except Exception:
            pass  # Psycopg2 might not be installed
    
    # Instrument Redis if configured
    if config("REDIS_URL", default=None) or config("REDIS_HOST", default=None):
        try:
            RedisInstrumentor().instrument()
        except Exception:
            pass  # Redis might not be installed

    # Instrument Huey task queue
    try:
        from huey.contrib.djhuey import HUEY as huey_instance
        from karrio.server.lib.otel_huey import HueyInstrumentor

        instrumentor = HueyInstrumentor()
        instrumentor.instrument(huey_instance)
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to instrument Huey: {e}")

    # Log that OpenTelemetry is enabled
    logger = logging.getLogger(__name__)
    logger.info(f"OpenTelemetry enabled: Service={OTEL_SERVICE_NAME}, Endpoint={OTEL_EXPORTER_OTLP_ENDPOINT}")


# =============================================================================
# Datadog Configuration
# =============================================================================
#
# Datadog provides full-stack observability including APM, infrastructure
# monitoring, logs, and more. When DD_TRACE_ENABLED is set, the following
# features are enabled:
#
# 1. APM Tracing: Distributed tracing for all requests and background tasks
# 2. Metrics: Custom metrics via DogStatsD
# 3. Logs: Automatic trace ID injection into logs
# 4. Profiling: Continuous profiling (optional)
#
# Environment Variables:
#   DD_TRACE_ENABLED        - Enable Datadog tracing (default: false)
#   DD_SERVICE              - Service name (default: karrio-api)
#   DD_ENV                  - Environment name (default: from ENV or "production")
#   DD_VERSION              - Application version (default: VERSION)
#   DD_AGENT_HOST           - Datadog agent host (default: localhost)
#   DD_TRACE_AGENT_PORT     - Datadog agent port (default: 8126)
#   DD_DOGSTATSD_PORT       - DogStatsD port for metrics (default: 8125)
#   DD_TRACE_SAMPLE_RATE    - Sampling rate 0.0-1.0 (default: 1.0)
#   DD_PROFILING_ENABLED    - Enable continuous profiling (default: false)
#   DD_LOGS_INJECTION       - Inject trace IDs into logs (default: true)
#
# =============================================================================

DD_TRACE_ENABLED = config("DD_TRACE_ENABLED", default=False, cast=bool)
DATADOG_ENABLED = config("DATADOG_ENABLED", default=False, cast=bool)  # Alias

# Use either DD_TRACE_ENABLED or DATADOG_ENABLED
_datadog_enabled = DD_TRACE_ENABLED or DATADOG_ENABLED

if _datadog_enabled:
    # Datadog configuration
    DD_SERVICE = config("DD_SERVICE", default="karrio-api")
    DD_ENV = config("DD_ENV", default=config("ENV", default="production"))
    DD_VERSION = config("DD_VERSION", default=config("VERSION", default="unknown"))
    DD_AGENT_HOST = config("DD_AGENT_HOST", default="localhost")
    DD_TRACE_AGENT_PORT = config("DD_TRACE_AGENT_PORT", default=8126, cast=int)
    DD_DOGSTATSD_PORT = config("DD_DOGSTATSD_PORT", default=8125, cast=int)
    DD_TRACE_SAMPLE_RATE = config("DD_TRACE_SAMPLE_RATE", default=1.0, cast=float)
    DD_PROFILING_ENABLED = config("DD_PROFILING_ENABLED", default=False, cast=bool)
    DD_LOGS_INJECTION = config("DD_LOGS_INJECTION", default=True, cast=bool)

    try:
        import ddtrace
        from ddtrace import config as dd_config, tracer, patch_all

        # Configure tracer
        ddtrace.config.service = DD_SERVICE
        ddtrace.config.env = DD_ENV
        ddtrace.config.version = DD_VERSION

        # Configure Django integration
        dd_config.django["service_name"] = DD_SERVICE
        dd_config.django["cache_service_name"] = f"{DD_SERVICE}-cache"
        dd_config.django["database_service_name"] = f"{DD_SERVICE}-db"
        dd_config.django["trace_query_string"] = True
        dd_config.django["analytics_enabled"] = True

        # Configure trace sampling
        tracer.configure(
            hostname=DD_AGENT_HOST,
            port=DD_TRACE_AGENT_PORT,
        )

        # Set global sample rate
        from ddtrace.sampler import DatadogSampler
        tracer.configure(sampler=DatadogSampler(default_sample_rate=DD_TRACE_SAMPLE_RATE))

        # Enable log injection
        if DD_LOGS_INJECTION:
            ddtrace.patch(logging=True)

        # Patch all supported libraries
        patch_all(
            django=True,
            redis=True,
            psycopg=True,
            requests=True,
            httpx=True,
            logging=DD_LOGS_INJECTION,
        )

        # Patch Huey for background task tracing
        try:
            from ddtrace import patch
            patch(huey=True)
        except Exception:
            pass  # Huey integration may not be available in all ddtrace versions

        # Enable profiling if configured
        if DD_PROFILING_ENABLED:
            try:
                import ddtrace.profiling.auto  # noqa: F401
            except ImportError:
                pass

        # Configure DogStatsD for metrics
        try:
            from datadog import initialize, statsd

            initialize(
                statsd_host=DD_AGENT_HOST,
                statsd_port=DD_DOGSTATSD_PORT,
            )

            # Set default tags for all metrics
            statsd.constant_tags = [
                f"service:{DD_SERVICE}",
                f"env:{DD_ENV}",
                f"version:{DD_VERSION}",
            ]

        except ImportError:
            pass  # datadog package not installed, metrics won't work

        import logging
        logger = logging.getLogger(__name__)
        logger.info(
            f"Datadog APM initialized: service={DD_SERVICE}, env={DD_ENV}, "
            f"agent={DD_AGENT_HOST}:{DD_TRACE_AGENT_PORT}"
        )

    except ImportError:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(
            "Datadog tracing enabled but ddtrace package not installed. "
            "Install with: pip install ddtrace"
        )
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to initialize Datadog APM: {e}")
