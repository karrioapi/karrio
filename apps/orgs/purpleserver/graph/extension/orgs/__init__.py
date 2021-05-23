import graphene

import purpleserver.graph.extension.orgs.types as types
import purpleserver.orgs.models as models


class Query:
    organization = graphene.Field(types.OrganizationType, id=graphene.Int(required=True))
    organizations = graphene.List(types.OrganizationType)

    def resolve_organization(self, info, **kwargs):
        return models.Organization.objects.get(users__id=info.context.user.id, **kwargs)

    def resolve_organizations(self, info, **kwargs):
        return models.Organization.objects.filter(users__id=info.context.user.id, **kwargs)


class Mutation:
    pass
