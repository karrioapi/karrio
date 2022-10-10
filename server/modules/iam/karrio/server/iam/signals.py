import logging
from django.db.models import signals

import karrio.server.core.utils as utils
import karrio.server.user.models as user
import karrio.server.iam.models as models

logger = logging.getLogger(__name__)


def register_all():
    signals.post_delete.connect(context_object_deleted, sender=user.Token)

    logger.info("karrio.iam signals registered...")


@utils.disable_for_loaddata
def context_object_deleted(sender, instance, *args, **kwargs):
    # clean up permission contexts when related objects are removed.
    models.ContextPermission.objects.filter(object_pk=instance.pk).delete()
