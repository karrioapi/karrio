import uuid
import typing
import strawberry
from strawberry.types import Info
from rest_framework import exceptions

import karrio.lib as lib
import karrio.server.conf as conf
import karrio.server.orgs.utils as orgs
import karrio.server.core.utils as core
import karrio.server.graph.utils as utils
import karrio.server.orgs.models as models
import karrio.server.graph.schemas.orgs.types as types
import karrio.server.graph.schemas.orgs.inputs as inputs
import karrio.server.orgs.serializers.organization as serializers


@strawberry.type
class CreateOrganizationMutation(utils.BaseMutation):
    organization: typing.Optional[types.OrganizationType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["ALLOW_MULTI_ACCOUNT"])
    def mutate(
        info: Info, **input: inputs.CreateOrganizationMutationInput
    ) -> "CreateOrganizationMutation":
        slug = f"org_{lib.to_slug(input.get('name'))}_{uuid.uuid4().hex}"
        serializer = serializers.OrganizationModelSerializer(
            data={**input, "slug": slug},
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)

        return CreateOrganizationMutation(organization=serializer.save())  # type:ignore


@strawberry.type
class UpdateOrganizationMutation(utils.BaseMutation):
    organization: typing.Optional[types.OrganizationType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_team"])
    def mutate(
        info: Info, **input: inputs.UpdateOrganizationMutationInput
    ) -> "UpdateOrganizationMutation":
        instance = models.Organization.objects.get(
            id=input.get("id"),
            users__id=info.context.request.user.id,
        )

        if input.get("name"):
            input.update({ "slug": f"org_{lib.to_slug(input.get('name'))}_{uuid.uuid4().hex}" })

        serializer = serializers.OrganizationModelSerializer(
            instance,
            data=input,
            partial=True,
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)

        return UpdateOrganizationMutation(organization=serializer.save())  # type:ignore


@strawberry.type
class DeleteOrganizationMutation(utils.BaseMutation):
    organization: typing.Optional[types.OrganizationType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_org_owner"])
    def mutate(
        info: Info, **input: inputs.DeleteOrganizationMutationInput
    ) -> "DeleteOrganizationMutation":
        # Get the organization by ID and verify user has access
        org = models.Organization.objects.get(
            id=input.get("id"),
            users__id=info.context.request.user.id,
        )

        # Validate password
        if not info.context.request.user.check_password(input.get("password")):
            raise exceptions.ValidationError({"password": "Invalid password"})

        # Deactivate the organization
        org.is_active = False
        org.save()

        return DeleteOrganizationMutation(organization=org)  # type:ignore


@strawberry.type
class SetOrganizationUserRolesMutation(utils.BaseMutation):
    organization: typing.Optional[types.OrganizationType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_team"])
    def mutate(
        info: Info, org=None, org_id=None, user_id=None, roles=[], **kwargs
    ) -> "SetOrganizationUserRolesMutation":
        # Get organization by ID and verify user has access
        org = models.Organization.objects.get(
            id=org_id,
            users__id=info.context.request.user.id,
        )

        # Support both user ID and email as user identifier
        if "@" in str(user_id):
            # If user_id contains @, treat it as email
            org_user = org.organization_users.get(user__email=user_id)
        else:
            # Otherwise treat it as user ID
            org_user = org.organization_users.get(user__id=user_id)

        org_user.roles = roles
        org_user.save(update_fields=["roles"])

        return SetOrganizationUserRolesMutation(  # type:ignore
            organization=org
        )


@strawberry.type
class ChangeOrganizationOwnerMutation(utils.BaseMutation):
    organization: typing.Optional[types.OrganizationType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_org_owner"])
    def mutate(
        info: Info, org=None, email=None, org_id=None, password=None, **kwargs
    ) -> "ChangeOrganizationOwnerMutation":
        new_owner = org.organization_users.get(user__email=email)

        if not info.context.request.user.check_password(password):
            raise exceptions.ValidationError({"password": "Invalid password"})

        org.change_owner(new_owner)
        org.save(update_fields=["owner"])

        core.failsafe(
            lambda: core.send_email(
                emails=[email],
                subject=f"{conf.settings.APP_NAME} organization ownership successfully transferred to you",
                email_template="karrio/organization_ownership_email.html",
                context=dict(
                    organization_name=org.name,
                    current_owner_email=info.context.request.user.email,
                ),
            ),
            warning="Failed to send email to new owner",
        )

        return ChangeOrganizationOwnerMutation(  # type: ignore
            organization=models.Organization.objects.get(id=org_id)
        )


@strawberry.type
class SendOrganizationInvitesMutation(utils.BaseMutation):
    organization: typing.Optional[types.OrganizationType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_team"])
    def mutate(
        info: Info, **input: inputs.SendOrganizationInvitesMutationInput
    ) -> "SendOrganizationInvitesMutation":
        # Get organization by ID and verify user has access
        organization = models.Organization.objects.get(
            id=input.get("org_id"),
            users__id=info.context.request.user.id,
        )

        orgs.send_invitation_emails(
            organization,
            input.get("emails"),
            input.get("redirect_url"),
            info.context.request.user,
            input.get("roles", []),
            False,  # is_owner not supported in this input
        )

        return SendOrganizationInvitesMutation(organization=organization)  # type: ignore


@strawberry.type
class AcceptOrganizationInvitationMutation(utils.BaseMutation):
    organization: typing.Optional[types.OrganizationType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required()
    def mutate(
        info: Info, guid=None, **kwargs
    ) -> "AcceptOrganizationInvitationMutation":
        invitation = models.OrganizationInvitation.objects.get(
            guid=guid,
            invitee__email=info.context.request.user.email,
        )

        org_user = invitation.organization.add_user(invitation.invitee)
        invitation.organization.save()

        if invitation.roles and org_user.roles != invitation.roles:
            org_user.roles = invitation.roles
            org_user.save()

        if invitation.is_owner:
            invitation.organization.change_owner(org_user)

        # cleanup invitation
        invitation.delete(keep_parents=True)

        return AcceptOrganizationInvitationMutation(
            organization=models.Organization.objects.get(id=invitation.organization.id)
        )  # type: ignore


@strawberry.type
class RemoveOrganizationMemberMutation(utils.BaseMutation):
    organization: typing.Optional[types.OrganizationType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_team"])
    def mutate(
        info: Info, **input: inputs.RemoveOrganizationMemberMutationInput
    ) -> "RemoveOrganizationMemberMutation":
        org = models.Organization.objects.get(
            id=input.get("org_id"),
            users__id=info.context.request.user.id,
        )

        # Get the organization user to remove
        # Support both user ID and email as user identifier
        user_id = input.get("user_id")
        if "@" in str(user_id):
            # If user_id contains @, treat it as email
            org_user = org.organization_users.get(user__email=user_id)
        else:
            # Otherwise treat it as user ID
            org_user = org.organization_users.get(user__id=user_id)

        # Check if trying to remove the owner
        if org.is_owner(org_user.user):
            raise exceptions.ValidationError(
                {
                    "user_id": "Cannot remove the organization owner. Transfer ownership first."
                }
            )

        # Check if trying to remove self
        if org_user.user.id == info.context.request.user.id:
            raise exceptions.ValidationError(
                {"user_id": "Cannot remove yourself from the organization."}
            )

        # Remove the user from organization
        org_user.delete()

        return RemoveOrganizationMemberMutation(organization=org)  # type: ignore


@strawberry.type
class UpdateMemberStatusMutation(utils.BaseMutation):
    organization: typing.Optional[types.OrganizationType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_team"])
    def mutate(
        info: Info, **input: inputs.UpdateMemberStatusMutationInput
    ) -> "UpdateMemberStatusMutation":
        org = models.Organization.objects.get(
            id=input.get("org_id"),
            users__id=info.context.request.user.id,
        )

        # Get the organization user to update
        # Support both user ID and email as user identifier
        user_id = input.get("user_id")
        if "@" in str(user_id):
            # If user_id contains @, treat it as email
            org_user = org.organization_users.get(user__email=user_id)
        else:
            # Otherwise treat it as user ID
            org_user = org.organization_users.get(user__id=user_id)

        # Check if trying to suspend the owner
        if org.is_owner(org_user.user) and not input.get("is_active"):
            raise exceptions.ValidationError(
                {"user_id": "Cannot suspend the organization owner."}
            )

        # Check if trying to suspend self
        if org_user.user.id == info.context.request.user.id and not input.get(
            "is_active"
        ):
            raise exceptions.ValidationError({"user_id": "Cannot suspend yourself."})

        # Update the user's active status
        org_user.user.is_active = input.get("is_active")
        org_user.user.save(update_fields=["is_active"])

        return UpdateMemberStatusMutation(organization=org)  # type: ignore


@strawberry.type
class ResendOrganizationInviteMutation(utils.BaseMutation):
    invitation: typing.Optional[types.OrganizationInvitationType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_team"])
    def mutate(
        info: Info, **input: inputs.ResendOrganizationInviteMutationInput
    ) -> "ResendOrganizationInviteMutation":
        # Get the invitation
        invitation = models.OrganizationInvitation.objects.get(
            id=input.get("invitation_id"),
            organization__users__id=info.context.request.user.id,
        )

        # Resend the invitation email
        orgs.send_invitation_emails(
            invitation.organization,
            [invitation.invitee_identifier],
            input.get("redirect_url"),
            info.context.request.user,
            invitation.roles,
            invitation.is_owner,
        )

        return ResendOrganizationInviteMutation(invitation=invitation)  # type: ignore
