import graphene

import purplship.server.graph.utils as utils
import purplship.server.graph.extension.orgs.types as types
import purplship.server.graph.extension.orgs.mutations as mutations
import purplship.server.orgs.models as models
from purplship.server.orgs.utils import admin_required


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
    organization_invitation = graphene.Field(
        types.OrganizationInvitationType,
        id=graphene.String(required=False),
        guid=graphene.String(required=False),
    )

    def resolve_organization_invitation(self, info, **kwargs):
        return models.OrganizationInvitation.objects.get(**kwargs)

    @utils.login_required
    def resolve_organization(self, info, **kwargs):
        return models.Organization.objects.get(users__id=info.context.user.id, **kwargs)

    @utils.login_required
    def resolve_organizations(self, info, **kwargs):
        return models.Organization.objects.filter(
            users__id=info.context.user.id, **kwargs
        )


class Mutation:
    create_organization = mutations.CreateOrganization.Field()
    update_organization = mutations.UpdateOrganization.Field()

    send_organization_invites = mutations.SendOrganizationInvites.Field()
    accept_organization_invitation = mutations.AcceptOrganizationInvitation.Field()
    delete_organization_invitation = utils.create_delete_mutation(
        "DeleteOrganizationInvitation",
        models.OrganizationInvitation,
        validator=admin_required,
    ).Field()
