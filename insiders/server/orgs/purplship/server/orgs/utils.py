import typing
import logging
from django.db import transaction
from django.contrib.auth import get_user_model
from django_email_verification.confirm import (
    _get_validated_field,
    EmailMultiAlternatives,
    render_to_string,
)

from purplship.core.utils import exec_parrallel
from purplship.server.conf import settings
import purplship.server.orgs.models as models

logger = logging.getLogger(__name__)
User = get_user_model()


def admin_required(instance, context) -> models.Organization:
    organization = (
        instance.organization if hasattr(instance, "organization") else instance
    )
    if not organization.organization_users.filter(
        is_admin=True, user__id=context.user.id
    ).exists():
        raise Exception("User Not Authorized")

    return instance


def send_invitation_emails(
    organization: models.Organization,
    emails: typing.List[str],
    redirect_url: str,
    invited_by: User,
):
    @transaction.atomic
    def action(email: str):
        invitation = models.OrganizationInvitation.objects.create(
            invitee_identifier=email,
            invited_by=invited_by,
            invitee=User.objects.filter(email=email).first(),
            organization_id=organization.id,
        )
        send_invitation(invitation, organization, redirect_url)
        organization.organization_invites.add(invitation)

    exclusion = [
        *organization.users.all().values_list("email", flat=True),
        *organization.organization_invites.all().values_list(
            "invitee_identifier", flat=True
        ),
    ]
    return exec_parrallel(action, [email for email in emails if email not in exclusion])


def send_invitation(
    invitation: models.OrganizationInvitation,
    organization: models.Organization,
    redirect_url: str,
):
    owner = getattr(organization, "owner", None)
    sender = _get_validated_field("EMAIL_FROM_ADDRESS")
    invited_by = invitation.invited_by.full_name or "You are"
    redirect_link = f"{redirect_url}?token={invitation.guid}"
    subject = f"{invited_by} invited you to join the {organization.name} team on {settings.APP_NAME}"
    context = {
        "redirect_link": redirect_link,
        "app_name": settings.APP_NAME,
        "organization_name": organization.name,
        "owner_email": getattr(owner, "email", invitation.invited_by.email),
    }

    text = render_to_string("purplship/invitation_email.html", context)
    html = render_to_string("purplship/invitation_email.html", context)

    logger.info(f"Sending invitation email to {invitation.invitee_identifier}")

    msg = EmailMultiAlternatives(subject, text, sender, [invitation.invitee_identifier])
    msg.attach_alternative(html, "text/html")
    msg.send()
