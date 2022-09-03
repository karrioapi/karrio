import logging
from django.db.models import signals

import karrio.server.core.utils as utils
import karrio.server.orgs.models as orgs
import karrio.server.user.models as user
import karrio.server.iam.models as models
import karrio.server.iam.permissions as permissions

logger = logging.getLogger(__name__)


def register_all():
    signals.post_save.connect(api_token_changed, sender=user.Token)
    signals.post_save.connect(organization_user_changed, sender=orgs.OrganizationUser)
    signals.post_delete.connect(organization_user_deleted, sender=orgs.OrganizationUser)

    logger.info("karrio.iam signals registered...")


@utils.disable_for_loaddata
def api_token_changed(sender, instance, created, *args, **kwargs):
    # sync organization user permissions based on roles updates
    pass


@utils.disable_for_loaddata
def organization_user_changed(sender, instance, created, *args, **kwargs):
    # sync organization user permissions based on roles updates
    permissions.sync_permissions(instance)


@utils.disable_for_loaddata
def organization_user_deleted(sender, instance,  *args, **kwargs):
    models.ContextPermission.objects.filter(object_pk=instance.pk).delete()
