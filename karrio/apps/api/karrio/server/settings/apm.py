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


#  Sentry
sentry_sdk.utils.MAX_STRING_LENGTH = 4096
SENTRY_DSN = config("SENTRY_DSN", default=None)

if SENTRY_DSN:
    # Build integrations list
    integrations = [DjangoIntegration()]
    if POSTHOG_KEY and PostHogIntegration is not None:
        integrations.append(PostHogIntegration())

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=integrations,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
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
    if config("REDIS_HOST", default=None):
        try:
            RedisInstrumentor().instrument()
        except Exception:
            pass  # Redis might not be installed
    
    # Instrument Huey task queue (temporarily disabled due to compatibility issues)
    # try:
    #     from karrio.server.lib.otel_huey import instrument_huey
    #     instrument_huey()
    # except Exception as e:
    #     logger = logging.getLogger(__name__)
    #     logger.warning(f"Failed to instrument Huey: {e}")
    
    # Log that OpenTelemetry is enabled
    logger = logging.getLogger(__name__)
    logger.info(f"OpenTelemetry enabled: Service={OTEL_SERVICE_NAME}, Endpoint={OTEL_EXPORTER_OTLP_ENDPOINT}")
