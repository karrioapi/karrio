"""
Huey Instance Factory

Creates and configures the Huey instance (Redis or SQLite) based on
environment variables. Extracted from settings/workers.py.
"""

import logging
import os
import socket

import decouple
import redis

import huey

logger = logging.getLogger(__name__)


def create_huey_instance(
    *,
    work_dir: str = "",
    databases: dict = None,
    worker_immediate_mode: bool = False,
    detached_worker: bool = False,
    is_worker_process: bool = False,
):
    """Build a Huey instance from environment configuration.

    Returns:
        A configured huey.RedisHuey or huey.SqliteHuey instance.
    """
    redis_url = decouple.config("REDIS_URL", default=None)

    if redis_url is not None:
        from urllib.parse import urlparse

        parsed = urlparse(redis_url)
        redis_host = parsed.hostname
        redis_port = parsed.port or 10000
        redis_username = parsed.username or "default"
        redis_password = parsed.password
        redis_scheme = parsed.scheme if parsed.scheme in ("redis", "rediss") else "redis"
        redis_ssl = redis_scheme == "rediss"
    else:
        redis_host = decouple.config("REDIS_HOST", default=None)
        redis_port = decouple.config("REDIS_PORT", default=None)
        redis_password = decouple.config("REDIS_PASSWORD", default=None)
        redis_username = decouple.config("REDIS_USERNAME", default="default")
        redis_ssl = decouple.config("REDIS_SSL", default=False, cast=bool)

    if redis_host is not None:
        redis_max_connections = decouple.config("REDIS_MAX_CONNECTIONS", default=100, cast=int)

        pool_kwargs = {
            "host": redis_host,
            "port": redis_port,
            "max_connections": redis_max_connections,
            "timeout": 20,
            "socket_timeout": 10,
            "socket_connect_timeout": 10,
            "socket_keepalive": True,
            "retry_on_timeout": True,
        }

        try:
            pool_kwargs["socket_keepalive_options"] = {
                socket.TCP_KEEPIDLE: 60,
                socket.TCP_KEEPINTVL: 10,
                socket.TCP_KEEPCNT: 3,
            }
        except AttributeError:
            pass

        if redis_password:
            pool_kwargs["password"] = redis_password
        if redis_username:
            pool_kwargs["username"] = redis_username

        if redis_ssl:
            pool_kwargs["connection_class"] = redis.SSLConnection
            pool_kwargs["ssl_cert_reqs"] = None

        pool = redis.BlockingConnectionPool(**pool_kwargs)

        instance = huey.RedisHuey(
            "default",
            connection_pool=pool,
            **({"immediate": worker_immediate_mode} if worker_immediate_mode else {}),
        )

    else:
        worker_db_dir = decouple.config("WORKER_DB_DIR", default=work_dir)
        worker_db_file = os.path.join(worker_db_dir, "tasks.sqlite3")

        if databases is not None:
            databases["workers"] = {
                "NAME": worker_db_file,
                "ENGINE": "django.db.backends.sqlite3",
            }

        instance = huey.SqliteHuey(
            name="default",
            filename=worker_db_file,
            journal_mode="wal",
            timeout=30,
            cache_mb=16,
            fsync=False,
            **({"immediate": worker_immediate_mode} if worker_immediate_mode else {}),
        )

        if detached_worker and not is_worker_process and not worker_immediate_mode:
            instance.immediate = True

    return instance
