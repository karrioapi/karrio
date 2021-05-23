import graphene
import graphene_django

from purpleserver.serializers import SerializerDecorator, Context
from purpleserver.user.serializers import TokenSerializer
import purpleserver.orgs.models as models


class OrganizationType(graphene_django.DjangoObjectType):
    token = graphene.String(required=True)

    class Meta:
        model = models.Organization
        exclude = ('tokens', )

    def resolve_token(self, info, **kwargs):
        return SerializerDecorator[TokenSerializer](
            data=dict(user=info.context.user),
            context=Context(user=info.context.user, org=self)).save().instance
