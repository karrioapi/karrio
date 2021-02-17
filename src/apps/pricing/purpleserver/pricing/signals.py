import logging
from django.db.models.signals import post_save, post_delete

from purpleserver.core.gateway import Rates
import purpleserver.pricing.models as models

logger = logging.getLogger(__name__)


def register_rate_post_processing(*_, **__):
    logger.debug("register custom surcharge  processing")
    try:
        Rates.post_process_functions = [
            charge.apply_charge for charge in models.Surcharge.objects.all()
        ]
    except:
        logger.warning("Failed to register custom charge processing")


post_save.connect(register_rate_post_processing, sender=models.Surcharge)
post_delete.connect(register_rate_post_processing, sender=models.Surcharge)
