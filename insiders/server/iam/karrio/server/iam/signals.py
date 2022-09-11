import logging
from django.conf import settings
from django.dispatch import receiver
from django.db.models import signals

import karrio.server.core.utils as utils
import karrio.server.orgs.models as orgs
import karrio.server.user.models as user
import karrio.server.iam.models as models
import karrio.server.iam.permissions as permissions

logger = logging.getLogger(__name__)


def register_all():
    signals.post_save.connect(organization_owner_changed, sender=orgs.OrganizationOwner)
    signals.post_save.connect(organization_user_changed, sender=orgs.OrganizationUser)
    signals.post_delete.connect(context_object_deleted, sender=orgs.OrganizationUser)
    signals.post_delete.connect(context_object_deleted, sender=user.Token)

    logger.info("karrio.iam signals registered...")


@utils.disable_for_loaddata
def context_object_deleted(sender, instance, *args, **kwargs):
    # clean up permission contexts when related objects are removed.
    models.ContextPermission.objects.filter(object_pk=instance.pk).delete()


@utils.disable_for_loaddata
def organization_user_changed(sender, instance, created, *args, **kwargs):
    # sync organization user permissions based on roles updates
    permissions.sync_permissions(instance)


@utils.disable_for_loaddata
def organization_owner_changed(sender, instance, created, *args, **kwargs):
    # sync organization user permissions based on roles updates
    roles = getattr(instance.organization_user, "roles", [])

    if "admin" not in roles:
        instance.organization_user.roles += ["admin"]
        instance.organization_user.save()

if settings.MULTI_TENANTS:
    from django_tenants.signals import post_schema_sync
    from django_tenants.models import TenantMixin

    @receiver(post_schema_sync, sender=TenantMixin)
    def check_post_schema_sync(**kwargs):
        client = kwargs['tenant']

        permissions.setup_groups(
            run_synchronous=True,
            schema=client.schema_name,
        )

        logger.debug(f"default group permissions created for tenant {client.id}")
