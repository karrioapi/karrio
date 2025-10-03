import logging
from django.db.models import signals

import karrio.references as ref
import karrio.server.core.utils as utils
import karrio.server.providers.models as models

logger = logging.getLogger(__name__)


def register_signals():
    signals.post_save.connect(carrier_changed, sender=models.Carrier)

    logger.info("karrio.providers signals registered...")


@utils.disable_for_loaddata
def carrier_changed(
    sender, instance, created, raw, using, update_fields, *args, **kwargs
):
    """Setup default capabilities when carrier are created."""
    if not created:
        return

    if len(instance.capabilities or []) == 0:
        instance.capabilities = ref.get_carrier_capabilities(instance.carrier_code)
        instance.save()
