import graphene

import purpleserver.graph.extension.orgs.types as types
import purpleserver.graph.extension.orgs.mutations as mutations
import purpleserver.orgs.models as models


class Query:
    organizations = graphene.List(types.OrganizationType, is_active=graphene.Boolean(required=False))
    organization = graphene.Field(types.OrganizationType, id=graphene.String(required=True))

    @types.login_required
    def resolve_organization(self, info, **kwargs):
        return models.Organization.objects.get(users__id=info.context.user.id, **kwargs)

    @types.login_required
    def resolve_organizations(self, info, **kwargs):
        return models.Organization.objects.filter(users__id=info.context.user.id, **kwargs)


class Mutation:
    create_organization = mutations.CreateOrganization.Field()
    update_organization = mutations.UpdateOrganization.Field()
