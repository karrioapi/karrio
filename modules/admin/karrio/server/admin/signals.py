from karrio.server.core.logging import logger


def register_signals():
    from karrio.server.admin.worker.signals import register_huey_signals

    register_huey_signals()
    logger.info("Signal registration complete", module="karrio.admin")
