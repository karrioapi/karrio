import logging
from django.db.models import signals
from django.contrib.auth import get_user_model

from karrio.server.core import utils
from karrio.server.conf import settings
import karrio.server.orgs.models as models

logger = logging.getLogger(__name__)


def register_all():
    signals.post_save.connect(user_updated, sender=get_user_model())

    logger.info("orgs webhooks signals registered...")


@utils.disable_for_loaddata
def user_updated(sender, instance, *args, **kwargs):
    """User related events:
    - user created (if signup create org when no invites are available)
    - user updated (if user set back to active, ensure orgs where owner are active)
    """
    created = kwargs.get("created", False)
    changes = kwargs.get("update_fields") or []

    if settings.MULTI_TENANTS and settings.schema == "public":
        return

    # user created
    if created:
        org_name = instance.full_name.split(" ")[0]
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
            name=f"{org_name.capitalize()}'s Org",
            slug=f"{org_name.lower()}_org".replace(" ", "").lower(),
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
