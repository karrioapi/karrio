"""Backwards-compatible re-export. Canonical location: karrio.server.huey.signals"""

import logging

logger = logging.getLogger(__name__)


def register_huey_signals():
    try:
        from karrio.server.huey.signals import register_huey_signals as _register

        _register()
    except ImportError:
        logger.debug("Huey module not installed, skipping signal registration")
