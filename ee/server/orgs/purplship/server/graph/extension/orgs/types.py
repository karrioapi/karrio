import graphene
import graphene_django
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model

from purplship.server.serializers import SerializerDecorator, Context
from purplship.server.user.serializers import TokenSerializer
import purplship.server.orgs.models as models


class OrganizationUserType(graphene_django.DjangoObjectType):
    is_admin = graphene.Boolean(required=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'full_name', 'is_staff', 'last_login', 'date_joined')


class OrganizationType(graphene_django.DjangoObjectType):
    token = graphene.String(required=True)
    user = graphene.Field(OrganizationUserType, required=True)

    class Meta:
        model = models.Organization
        exclude = ('tokens', )

    def resolve_token(self, info, **kwargs):
        return SerializerDecorator[TokenSerializer](
            data=dict(user=info.context.user),
            context=Context(user=info.context.user, org=self)).save().instance

    def resolve_user(self, info):
        user = info.context.user
        return OrganizationUserType(
            **{
                k: v for k, v in model_to_dict(user).items()
                if k in OrganizationUserType._meta.fields.keys()
            },
            is_admin=self.organization_users.get(user=user).is_admin
        )

    def resolve_users(self, info):
        return [
            OrganizationUserType(
                **{
                    k: v for k,v in model_to_dict(user).items()
                    if k in OrganizationUserType._meta.fields.keys()
                },
                is_admin=self.organization_users.get(user=user)
            )
            for user in self.users.all()
        ]
