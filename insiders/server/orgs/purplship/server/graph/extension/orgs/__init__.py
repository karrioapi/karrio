import graphene

from purplship.server.graph.extension.base.types import login_required
import purplship.server.graph.extension.orgs.types as types
import purplship.server.graph.extension.orgs.mutations as mutations
import purplship.server.orgs.models as models


class Query:
    organizations = graphene.List(
        types.OrganizationType,
        required=True,
        is_active=graphene.Boolean(required=False),
        default_value=[],
    )
    organization = graphene.Field(
        types.OrganizationType, id=graphene.String(required=True)
    )

    @login_required
    def resolve_organization(self, info, **kwargs):
        return models.Organization.objects.get(users__id=info.context.user.id, **kwargs)

    @login_required
    def resolve_organizations(self, info, **kwargs):
        return models.Organization.objects.filter(
            users__id=info.context.user.id, **kwargs
        )


class Mutation:
    create_organization = mutations.CreateOrganization.Field()
    update_organization = mutations.UpdateOrganization.Field()
