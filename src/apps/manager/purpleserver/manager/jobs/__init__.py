import logging
import schedule
from django.conf import settings
from purpleserver.manager.jobs import helpers, tracking

logger = logging.getLogger(__name__)
DEFAULT_TRACKERS_UPDATE_INTERVAL = getattr(settings, 'DEFAULT_TRACKERS_UPDATE_INTERVAL', 10800)


def start_schedulers():
    schedule.every(DEFAULT_TRACKERS_UPDATE_INTERVAL).seconds.do(tracking.update_trackers)

    logger.info("manager background jobs scheduled...")
    helpers.run_continuously()
