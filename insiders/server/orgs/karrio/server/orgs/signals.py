import logging
from django.db.models import signals
from django.contrib.auth import get_user_model

from karrio.server.conf import settings
import karrio.server.core.utils as utils
import karrio.server.events.tasks as tasks
import karrio.server.orgs.models as models
import karrio.server.orgs.serializers as serializers

logger = logging.getLogger(__name__)


def register_all():
    signals.post_save.connect(user_updated, sender=get_user_model())
    signals.post_delete.connect(owner_deleted, sender=models.OrganizationOwner)

    logger.info("karrio.orgs signals registered...")


@utils.disable_for_loaddata
def user_updated(sender, instance, *args, **kwargs):
    """User related events:
    - user created (if signup create org when no invites are available)
    - user updated (if user set back to active, ensure orgs where owner are active)
    """
    if settings.MULTI_TENANTS and settings.schema == "public":
        return

    changes = kwargs.get("update_fields") or []
    has_org = models.Organization.objects.filter(users__id=instance.id).exists()

    # user made active
    if instance.is_active and not has_org:
        _user_name = instance.full_name.split(" ")[0]
        _org_name = _user_name if any(_user_name) else instance.email.split("@")[0].split(".")[0]
        invitation = models.OrganizationInvitation.objects.filter(
            invitee_identifier=instance.email
        ).first()

        # has invitation from an active organization
        if invitation and invitation.organization.is_active:
            invitation.organization.add_user(instance)
            invitation.organization.save()
            invitation.delete()
            return

        # no invitation: create a new organization for the user
        organization = models.Organization.objects.create(
            name=f"{_org_name.capitalize()}",
            slug=f"{_org_name.lower()}_org".replace(" ", "").lower(),
            is_active=instance.is_active,
        )

        owner = organization.add_user(instance, is_admin=True)
        organization.change_owner(owner)
        organization.save()
        return

    # user active state updated
    if "is_active" in changes:
        models.Organization.objects.filter(
            is_active=not instance.is_active,
            owner__organization_user__user__id=instance.id,
        ).update(is_active=instance.is_active)


@utils.disable_for_loaddata
def owner_deleted(sender, instance, **kwargs):
    tasks.cleanup_orgs(schema=settings.schema)
