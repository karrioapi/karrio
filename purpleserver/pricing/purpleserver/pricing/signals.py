import logging
from django.db.models.signals import post_save, post_delete

from purpleserver.core.gateway import Rates
import purpleserver.pricing.models as models

logger = logging.getLogger(__name__)


def register_rate_post_processing(*_, **__):
    logger.debug("register custom charge  processing")
    try:
        Rates.post_process_functions = [
            charge.apply_charge for charge in models.PricingCharge.objects.all()
        ]
    except Exception as e:
        logger.warning(f"Failed to register custom charge processing: {e}")


post_save.connect(register_rate_post_processing, sender=models.PricingCharge)
post_delete.connect(register_rate_post_processing, sender=models.PricingCharge)
