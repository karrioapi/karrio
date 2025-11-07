from django.db.models import signals

from karrio.server.core.logging import logger
import karrio.server.core.utils as utils
import karrio.server.user.models as user
import karrio.server.iam.models as models


def register_all():
    signals.post_delete.connect(context_object_deleted, sender=user.Token)

    logger.info("Signal registration complete", module="karrio.iam")


@utils.disable_for_loaddata
def context_object_deleted(sender, instance, *args, **kwargs):
    # clean up permission contexts when related objects are removed.
    models.ContextPermission.objects.filter(object_pk=instance.pk).delete()
