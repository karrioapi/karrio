import logging
from django.db.models import signals

import karrio.server.core.utils as utils
import karrio.server.shipping.models as models

logger = logging.getLogger(__name__)


def register_all():
    signals.post_save.connect(shipping_method_updated, sender=models.ShippingMethod)

    logger.info("jtl:karrio.shipping signals registered...")


@utils.disable_for_loaddata
def shipping_method_updated(sender, instance, **kwargs):
    pass
