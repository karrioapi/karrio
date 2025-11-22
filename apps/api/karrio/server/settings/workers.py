# type: ignore
import os
import sys
import socket
import huey
import redis
import decouple
from karrio.server.settings import base as settings


# Karrio Server Background jobs interval config
DEFAULT_SCHEDULER_RUN_INTERVAL = 3600  # value is seconds. so 3600 seconds = 1 Hour
DEFAULT_TRACKERS_UPDATE_INTERVAL = decouple.config(
    "TRACKING_PULSE", default=7200, cast=int
)  # value is seconds. so 10800 seconds = 3 Hours

# Check if worker is running in detached mode (separate from API server)
DETACHED_WORKER = decouple.config("DETACHED_WORKER", default=False, cast=bool)

WORKER_IMMEDIATE_MODE = decouple.config(
    "WORKER_IMMEDIATE_MODE", default=False, cast=bool
)

# Detect if running as a worker process (via run_huey command)
IS_WORKER_PROCESS = any("run_huey" in arg for arg in sys.argv)

# Always configure Huey for both API servers and workers
# API servers need to enqueue tasks even when DETACHED_WORKER=True
# Only the worker pods will consume tasks
# Redis configuration - REDIS_URL takes precedence and supersedes granular env vars
REDIS_URL = decouple.config("REDIS_URL", default=None)

# Parse REDIS_URL or construct from individual parameters
if REDIS_URL is not None:
    from urllib.parse import urlparse

    parsed = urlparse(REDIS_URL)

    # Extract values from REDIS_URL (these supersede granular env vars)
    REDIS_HOST = parsed.hostname
    REDIS_PORT = parsed.port or 6379
    REDIS_USERNAME = parsed.username or "default"
    REDIS_PASSWORD = parsed.password

    # Determine SSL from URL scheme (rediss:// means SSL is enabled)
    REDIS_SCHEME = (
        parsed.scheme if parsed.scheme in ("redis", "rediss") else "redis"
    )
    REDIS_SSL = REDIS_SCHEME == "rediss"

else:
    # Fall back to individual parameters
    REDIS_HOST = decouple.config("REDIS_HOST", default=None)
    REDIS_PORT = decouple.config("REDIS_PORT", default=None)
    REDIS_PASSWORD = decouple.config("REDIS_PASSWORD", default=None)
    REDIS_USERNAME = decouple.config("REDIS_USERNAME", default="default")
    REDIS_SSL = decouple.config("REDIS_SSL", default=False, cast=bool)

# Configure HUEY based on available Redis configuration
if REDIS_HOST is not None:
    # Calculate max connections based on environment
    # Each worker replica needs: (workers_per_replica + 1 scheduler) connections
    # Formula: (worker_replicas * (threads_per_worker + 1)) + api_connections + buffer
    # Example: 100 connections = (5 replicas * (8 workers + 1 scheduler)) + 40 API + 15 buffer
    REDIS_MAX_CONNECTIONS = decouple.config(
        "REDIS_MAX_CONNECTIONS", default=100, cast=int
    )

    # Connection pool configuration with timeouts
    # Use BlockingConnectionPool to wait for available connections instead of failing immediately
    pool_kwargs = {
        "host": REDIS_HOST,
        "port": REDIS_PORT,
        "max_connections": REDIS_MAX_CONNECTIONS,
        "timeout": 20,  # Wait up to 20 seconds for an available connection
        # Timeout settings to prevent hung connections
        "socket_timeout": 10,  # Command execution timeout (seconds)
        "socket_connect_timeout": 10,  # Connection establishment timeout (seconds)
        # Keep connections alive to prevent closure by firewalls/load balancers
        "socket_keepalive": True,
        # Retry on transient failures
        "retry_on_timeout": True,
    }

    # Add TCP keepalive options if available (Linux/Unix only)
    try:
        pool_kwargs["socket_keepalive_options"] = {
            socket.TCP_KEEPIDLE: 60,  # Start keepalive after 60s idle
            socket.TCP_KEEPINTVL: 10,  # Keepalive interval
            socket.TCP_KEEPCNT: 3,  # Keepalive probes before timeout
        }
    except AttributeError:
        # TCP keepalive constants not available on this platform
        pass

    # Add authentication if provided
    if REDIS_PASSWORD:
        pool_kwargs["password"] = REDIS_PASSWORD
    if REDIS_USERNAME:
        pool_kwargs["username"] = REDIS_USERNAME

    # Add SSL/TLS configuration if enabled
    if REDIS_SSL:
        # Use SSLConnection class for SSL/TLS connections
        pool_kwargs["connection_class"] = redis.SSLConnection
        pool_kwargs["ssl_cert_reqs"] = None  # For Azure Redis compatibility

    # Use BlockingConnectionPool to wait for connections instead of raising errors immediately
    pool = redis.BlockingConnectionPool(**pool_kwargs)

    HUEY = huey.RedisHuey(
        "default",
        connection_pool=pool,
        **({"immediate": WORKER_IMMEDIATE_MODE} if WORKER_IMMEDIATE_MODE else {}),
    )

else:
    # No Redis configured, use SQLite
    WORKER_DB_DIR = decouple.config("WORKER_DB_DIR", default=settings.WORK_DIR)
    WORKER_DB_FILE_NAME = os.path.join(WORKER_DB_DIR, "tasks.sqlite3")

    settings.DATABASES["workers"] = {
        "NAME": WORKER_DB_FILE_NAME,
        "ENGINE": "django.db.backends.sqlite3",
    }

    # SQLite-specific Huey configuration
    # WAL mode (Write-Ahead Logging) enables better concurrency for multiple workers
    # Increased timeout helps handle lock contention under concurrent access
    HUEY = huey.SqliteHuey(
        name="default",
        filename=WORKER_DB_FILE_NAME,
        # Storage-specific kwargs for better concurrent access handling
        journal_mode="wal",  # Enable Write-Ahead Logging for better concurrency
        timeout=30,  # Increase timeout to 30s to handle lock contention with multiple workers
        cache_mb=16,  # Increase cache size for better performance (default: 8MB)
        fsync=False,  # Disable forced fsync for better performance (default: False)
        **({"immediate": WORKER_IMMEDIATE_MODE} if WORKER_IMMEDIATE_MODE else {}),
    )
