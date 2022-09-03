import graphene
from rest_framework import exceptions
from graphene_django.types import ErrorType

from karrio.server.conf import settings
from karrio.server.core.utils import failsafe, send_email
from karrio.server.orgs.utils import (
    OrganizationUserRole,
    roles_required,
    send_invitation_emails,
)
import karrio.server.orgs.serializers.organization as serializers
import karrio.server.graph.extension.orgs.types as types
import karrio.server.orgs.models as models
import karrio.server.graph.utils as utils


class CreateOrganization(utils.ClientMutation):
    organization = graphene.Field(types.OrganizationType)

    class Input:
        name = graphene.String(required=True)

    @classmethod
    @utils.permisions_required(["ALLOW_MULTI_ACCOUNT"])
    @utils.login_required
    def mutate_and_get_payload(cls, root, info, **data):
        serializer = serializers.OrganizationModelSerializer(
            data=data,
            context=info.context,
        )

        if not serializer.is_valid():
            return cls(errors=ErrorType.from_errors(serializer.errors))

        return cls(organization=serializer.save())


class UpdateOrganization(utils.ClientMutation):
    organization = graphene.Field(types.OrganizationType)

    class Input:
        id = graphene.String(required=True)
        name = graphene.String()

    @classmethod
    @roles_required(["admin"])
    def mutate_and_get_payload(cls, root, info, id, **data):
        try:
            instance = models.Organization.objects.get(
                id=id, users__id=info.context.user.id
            )
            serializer = serializers.OrganizationModelSerializer(
                instance,
                data=data,
                partial=True,
                context=info.context,
            )

            if not serializer.is_valid():
                return cls(errors=ErrorType.from_errors(serializer.errors))

            return cls(organization=serializer.save())
        except Exception as e:
            raise e


class DeleteOrganization(utils.ClientMutation):
    organization = graphene.Field(types.OrganizationType)

    class Input:
        id = graphene.String(required=True)
        password = graphene.String(required=True)

    @classmethod
    @utils.password_required
    @roles_required(["owner"])
    def mutate_and_get_payload(cls, **kwargs):
        org = kwargs.get("org")

        org.is_active = False
        org.save()

        # TODO: send email to all users

        return cls(organization=org)


class SetOrganizationUserRoles(utils.ClientMutation):
    organization = graphene.Field(types.OrganizationType)

    class Input:
        org_id = graphene.String(required=True)
        user_id = graphene.String(required=True)
        roles = graphene.List(graphene.NonNull(graphene.String), required=True)

    @classmethod
    @roles_required(["owner"])
    def mutate_and_get_payload(cls, root, info, org_id, user_id, roles, **kwargs):
        changes = ["roles"]
        org = kwargs.get("org")
        org_user = org.organization_users.get(user__id=user_id)

        org_user.roles = roles
        org.save(update_fields=changes)

        return cls(organization=models.Organization.objects.get(id=org_id))


class ChangeOrganizationOwner(utils.ClientMutation):
    organization = graphene.Field(types.OrganizationType)

    class Input:
        org_id = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    @classmethod
    @roles_required(["owner"])
    def mutate_and_get_payload(
        cls, root, info, org_id: str, email: str = None, password: str = None, **kwargs
    ):
        org = kwargs.get("org")
        new_owner = org.organization_users.get(user__email=email)

        if not info.context.user.check_password(password):
            raise exceptions.ValidationError({"password": "Invalid password"})

        org.change_owner(new_owner)
        org.save(update_fields=["owner"])

        failsafe(
            lambda: send_email(
                emails=[email],
                subject=f"{settings.APP_NAME} organization ownership successfully transferred to you",
                email_template="karrio/organization_ownership_email.html",
                context=dict(
                    organization_name=org.name,
                    current_owner_email=info.context.user.email,
                ),
            ),
            warning="Failed to send email to new owner",
        )

        return cls(organization=models.Organization.objects.get(id=org_id))


class SendOrganizationInvites(utils.ClientMutation):
    organization = graphene.Field(types.OrganizationType)

    class Input:
        org_id = graphene.String(required=True)
        emails = graphene.List(graphene.String, required=True, empty=False)
        redirect_url = graphene.String(required=True)

    @classmethod
    @roles_required(["admin"])
    def mutate_and_get_payload(cls, root, info, org_id, emails, redirect_url, **kwargs):
        organization = kwargs.get("org")

        send_invitation_emails(organization, emails, redirect_url, info.context.user)

        return cls(organization=models.Organization.objects.get(id=org_id))


class AcceptOrganizationInvitation(utils.ClientMutation):
    organization = graphene.Field(types.OrganizationType)

    class Input:
        guid = graphene.String(required=True)

    @classmethod
    @utils.login_required
    def mutate_and_get_payload(cls, root, info, guid, **kwargs):
        invitation = models.OrganizationInvitation.objects.get(
            guid=guid,
            invitee__email=info.context.user.email,
        )

        invitation.organization.add_user(invitation.invitee)
        invitation.organization.save()
        organization = models.Organization.objects.get(id=invitation.organization.id)
        invitation.delete(keep_parents=True)

        return cls(organization=organization)
