import graphene
from graphene_django.rest_framework import mutation

from purplship.server.serializers import make_fields_optional
import purplship.server.graph.utils as utils
import purplship.server.graph.extension.orgs.types as types
import purplship.server.orgs.serializers as serializers
import purplship.server.orgs.models as models
from purplship.server.orgs.utils import send_invitation_emails
from pyparsing import empty


class SerializerMutation(mutation.SerializerMutation):
    class Meta:
        abstract = True

    @classmethod
    def get_serializer_kwargs(cls, root, info, **input):
        data = input.copy()

        if "id" in input:
            org = cls._meta.model_class.objects.get(id=data.pop("id"))

            return {
                "instance": org,
                "data": data,
                "partial": True,
                "context": info.context,
            }

        return {"data": data, "partial": False, "context": info.context}


class CreateOrganization(SerializerMutation):
    class Meta:
        model_operations = ("create",)
        convert_choices_to_enum = False
        serializer_class = serializers.OrganizationModelSerializer


class UpdateOrganization(SerializerMutation):
    class Meta:
        model_operations = ("update",)
        convert_choices_to_enum = False
        serializer_class = make_fields_optional(serializers.OrganizationModelSerializer)


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
