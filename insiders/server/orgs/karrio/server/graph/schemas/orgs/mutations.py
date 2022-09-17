import typing
import strawberry
from strawberry.types import Info
from rest_framework import exceptions

import karrio.server.conf as conf
import karrio.server.core.utils as core
import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.orgs.types as types
import karrio.server.graph.schemas.orgs.inputs as inputs
import karrio.server.orgs.serializers.organization as serializers
import karrio.server.orgs.models as models
import karrio.server.orgs.utils as orgs


@strawberry.type
class CreateOrganizationMutation(utils.BaseMutation):
    organization: typing.Optional[types.OrganizationType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["ALLOW_MULTI_ACCOUNT"])
    def mutate(
        info: Info, **input: inputs.CreateOrganizationMutationInput
    ) -> "CreateOrganizationMutation":
        serializer = serializers.OrganizationModelSerializer(
            data=input,
            context=info.context,
        )

        if not serializer.is_valid():
            return CreateOrganizationMutation(errors=utils.ErrorType.from_errors(serializer.errors))

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
        serializer = serializers.OrganizationModelSerializer(
            instance,
            data=input,
            partial=True,
            context=info.context,
        )

        if not serializer.is_valid():
            return UpdateOrganizationMutation( # type:ignore
                errors=utils.ErrorType.from_errors(serializer.errors)
            )

        return UpdateOrganizationMutation(organization=serializer.save()) # type:ignore


class DeleteOrganizationMutation(utils.BaseMutation):
    organization: typing.Optional[types.OrganizationType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_org_owner"])
    def mutate(
        info: Info, **input: inputs.DeleteOrganizationMutationInput
    ) -> "DeleteOrganizationMutation":
        org = input.get("org")

        org.is_active = False
        org.save()

        return DeleteOrganizationMutation(organization=org) # type:ignore


@strawberry.type
class SetOrganizationUserRolesMutation(utils.BaseMutation):
    organization: typing.Optional[types.OrganizationType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_team"])
    def mutate(
        info: Info, **input: inputs.SetOrganizationUserRolesMutationInput
    ) -> "SetOrganizationUserRolesMutation":
        changes = ["roles"]
        org = input.get("org")
        roles = input.get("roles")
        org_id = input.get("org_id")
        user_id = input.get("user_id")

        org_user = org.organization_users.get(user__id=user_id)
        org_user.roles = roles
        org.save(update_fields=changes)

        return SetOrganizationUserRolesMutation( # type:ignore
            organization=models.Organization.objects.get(id=org_id)
        )


@strawberry.type
class ChangeOrganizationOwnerMutation(utils.BaseMutation):
    organization: typing.Optional[types.OrganizationType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_org_owner"])
    def mutate(
        info: Info, **input: inputs.ChangeOrganizationOwnerMutationInput
    ) -> "ChangeOrganizationOwnerMutation":
        org = input.get("org")
        email = input.get("email")
        org_id = input.get("org_id")
        password = input.get("password")
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

        return ChangeOrganizationOwnerMutation( # type: ignore
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
        orgs.send_invitation_emails(
            input.get("org"),
            input.get("emails"),
            input.get("redirect_url"),
            info.context.request.user,
        )

        return SendOrganizationInvitesMutation(organization=organization) # type: ignore


@strawberry.type
class AcceptOrganizationInvitationMutation(utils.BaseMutation):
    organization: typing.Optional[types.OrganizationType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required()
    def mutate(
        info: Info, **input: inputs.AcceptOrganizationInvitationMutationInput
    ) -> "AcceptOrganizationInvitationMutation":
        invitation = models.OrganizationInvitation.objects.get(
            guid=input.get("guid"),
            invitee__email=info.context.user.email,
        )

        invitation.organization.add_user(invitation.invitee)
        invitation.organization.save()
        organization = models.Organization.objects.get(id=invitation.organization.id)
        invitation.delete(keep_parents=True)

        return AcceptOrganizationInvitationMutation(organization=organization) # type: ignore
