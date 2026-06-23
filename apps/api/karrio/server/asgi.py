"""
ASGI config for karrio.server project.

Exposes the ASGI callable as a module-level variable named ``application``.

The callable is a thin async wrapper around Django's ASGI app that
captures the worker's running event loop on the first http/websocket
request. The captured loop is handed to the ``karrio.server.servicebus``
publisher (if installed) so its async producer can schedule publishes
on the worker's event loop via ``asyncio.run_coroutine_threadsafe``.

Why first-request capture and not the ASGI lifespan protocol: our
custom ``UvicornWorker`` (karrio/apps/api/karrio/server/workers.py) sets
``"lifespan": "off"`` explicitly because Django's stock ASGI app does
not handle lifespan messages. First-request capture is one global +
a handful of lines, no worker config change needed.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import asyncio
import logging
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "karrio.server.settings")
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

logger = logging.getLogger(__name__)

_django_app = get_asgi_application()
_loop_captured = False


async def application(scope, receive, send):
    """ASGI application with first-request event-loop capture.

    Non-http/websocket scopes pass straight through to Django. The
    capture happens once per worker; subsequent requests are zero-cost
    fast-path (a single boolean check).
    """
    global _loop_captured
    if not _loop_captured and scope.get("type") in ("http", "websocket"):
        _loop_captured = True
        try:
            from karrio.server.servicebus import set_async_loop

            set_async_loop(asyncio.get_running_loop())
            logger.debug("ASGI: captured event loop for servicebus async publisher")
        except ImportError:
            # servicebus extension not installed in this deployment; that's
            # fine — bridge dual-publish will use the sync path.
            pass
        except Exception:
            logger.warning(
                "ASGI: failed to capture event loop for servicebus async publisher",
                exc_info=True,
            )
    await _django_app(scope, receive, send)
