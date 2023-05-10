import logging
from django.db.models import signals

logger = logging.getLogger(__name__)


def register_signals():
    logger.info("karrio.admin signals registered...")
