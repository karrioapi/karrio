from karrio.server.core.logging import logger


def register_signals():
    try:
        from karrio.server.huey.signals import register_huey_signals

        register_huey_signals()
    except ImportError:
        logger.debug("Huey module not installed, skipping signal registration")

    logger.info("Signal registration complete", module="karrio.admin")
