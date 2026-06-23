import decouple

KARRIO_HOST = decouple.config("KARRIO_HTTP_HOST", default="0.0.0.0")  # noqa: S104
KARRIO_PORT = decouple.config("KARRIO_HTTP_PORT", default=5002)

bind = f"{KARRIO_HOST}:{KARRIO_PORT}"
accesslog = "-"
loglevel = "debug"
capture_output = True
enable_stdio_inheritance = True
workers = decouple.config("KARRIO_WORKERS", default=2, cast=int)

# NOTE: preload_app is intentionally NOT set here.
# With UvicornWorker (ASGI), preload_app=True causes:
#   1. asyncio.CancelledError in django-health-check (stale event loop from master)
#   2. psycopg "BAD" connections (DB pool forked from master)
# UvicornWorker manages its own lifecycle and ignores gunicorn's post_fork,
# so these issues cannot be fixed via post_fork hooks.
# Cold-start CPU optimization should be addressed at the k8s level
# (resource requests/limits, startup probes) instead.
