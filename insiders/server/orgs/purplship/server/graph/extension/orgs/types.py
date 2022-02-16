import graphene
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model

import purplship.server.graph.utils as utils
from purplship.server.serializers import SerializerDecorator, Context
from purplship.server.user.serializers import TokenSerializer
import purplship.server.orgs.models as models


class OrganizationUserType(utils.BaseObjectType):
    is_admin = graphene.Boolean(required=True)
    is_owner = graphene.Boolean()

    class Meta:
        model = get_user_model()
        fields = ("email", "full_name", "is_staff", "last_login", "date_joined")


class OrganizationInvitationType(utils.BaseObjectType):
    organization_name = graphene.String(required=True)

    class Meta:
        model = models.OrganizationInvitation
        fields = (
            "id",
            "guid",
            "invitee_identifier",
            "created",
            "modified",
            "invited_by",
            "invitee",
        )

    def resolve_organization_name(self, info, **kwargs):
        return self.organization.name


class OrganizationMemberType(graphene.ObjectType):
    email = graphene.String(required=True)
    full_name = graphene.String(required=False)
    is_admin = graphene.Boolean(required=True)
    is_owner = graphene.Boolean()
    invitation = graphene.Field(OrganizationInvitationType)
    last_login = graphene.DateTime(required=False)


class OrganizationType(utils.BaseObjectType):
    token = graphene.String(required=True)
    current_user = graphene.Field(OrganizationUserType, required=True)
    members = graphene.List(
        graphene.NonNull(OrganizationMemberType), default_value=[], required=True
    )

    class Meta:
        model = models.Organization
        exclude = (
            "tokens",
            "users",
        )

    def resolve_token(self, info, **kwargs):
        return (
            SerializerDecorator[TokenSerializer](
                data=dict(user=info.context.user),
                context=Context(user=info.context.user, org=self),
            )
            .save()
            .instance
        )

    def resolve_current_user(self, info):
        owner = getattr(self, "owner", None)
        user = info.context.user
        return OrganizationUserType(
            **{
                k: v
                for k, v in model_to_dict(user).items()
                if k in OrganizationUserType._meta.fields.keys()
            },
            is_admin=self.organization_users.get(user=user).is_admin,
            is_owner=owner and self.is_owner(user),
        )

    def resolve_members(self, info):
        owner = getattr(self, "owner", None)
        users = [
            OrganizationMemberType(
                email=user.email,
                full_name=user.full_name,
                is_admin=self.organization_users.get(user=user).is_admin,
                is_owner=owner and self.is_owner(user),
                last_login=user.last_login,
            )
            for user in self.users.filter(is_active=True)
        ]
        invites = [
            OrganizationMemberType(
                email=getattr(invite.invitee, "email", invite.invitee_identifier),
                full_name=getattr(invite.invitee, "full_name", ""),
                is_admin=False,
                is_owner=False,
                invitation=invite,
            )
            for invite in self.organization_invites.all()
        ]

        return users + invites
