import graphene
from graphene_django.types import ErrorType

from purplship.server.orgs.utils import send_invitation_emails
import purplship.server.graph.extension.orgs.types as types
import purplship.server.orgs.serializers as serializers
import purplship.server.orgs.models as models
import purplship.server.graph.utils as utils


class CreateOrganization(utils.ClientMutation):
    organization = graphene.Field(types.OrganizationType)

    class Input:
        name = graphene.String(required=True)
        slug = graphene.String()

    @classmethod
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
        slug = graphene.String()

    @classmethod
    @utils.login_required
    def mutate_and_get_payload(cls, root, info, id, **data):
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

        return cls(organization=instance)


class SendOrganizationInvites(utils.ClientMutation):
    organization = graphene.Field(types.OrganizationType)

    class Input:
        org_id = graphene.String(required=True)
        emails = graphene.List(graphene.String, required=True, empty=False)
        redirect_url = graphene.String(required=True)

    @classmethod
    @utils.login_required
    def mutate_and_get_payload(cls, root, info, org_id, emails, redirect_url, **kwargs):
        organization = serializers.admin_required(
            models.Organization.objects.get(id=org_id, users__id=info.context.user.id),
            info.context,
        )

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
