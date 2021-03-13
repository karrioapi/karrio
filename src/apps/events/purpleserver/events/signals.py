import logging
from django.db.models import signals

import purpleserver.manager.models as models

logger = logging.getLogger(__name__)


def register_signals():
    signals.post_save.connect(shipment_updated, sender=models.Shipment)
    signals.post_delete.connect(shipment_updated, sender=models.Shipment)
    signals.post_save.connect(tracker_updated, sender=models.Tracking)

    logger.info("webhooks signals registered...")


def shipment_updated(sender, *args, **kwargs):
    """Shipment related events:
        - shipment purchased (label purchased)
        - shipment fulfilled (shipped)
        - shipment cancelled/deleted (label voided)
    """
    pass


def tracker_updated(sender, *args, **kwargs):
    """Tracking related events:
        - tracker created (in-transit)
        - tracker status changed (delivered or blocked)
    """
    pass


