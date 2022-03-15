import graphene

import karrio.server.graph.utils as utils
import karrio.server.graph.extension.orgs.types as types
import karrio.server.graph.extension.orgs.mutations as mutations
import karrio.server.orgs.models as models
from karrio.server.orgs.utils import admin_required


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
        return models.Organization.objects.get(
            users__id=info.context.user.id, is_active=True, **kwargs
        )

    @utils.login_required
    def resolve_organizations(self, info, **kwargs):
        return models.Organization.objects.filter(
            users__id=info.context.user.id, is_active=True, **kwargs
        )


class Mutation:
    create_organization = mutations.CreateOrganization.Field()
    update_organization = mutations.UpdateOrganization.Field()
    delete_organization = mutations.DeleteOrganization.Field()

    change_organization_owner = mutations.ChangeOrganizationOwner.Field()
    set_organization_user_roles = mutations.SetOrganizationUserRoles.Field()

    send_organization_invites = mutations.SendOrganizationInvites.Field()
    accept_organization_invitation = mutations.AcceptOrganizationInvitation.Field()
    delete_organization_invitation = utils.create_delete_mutation(
        "DeleteOrganizationInvitation",
        models.OrganizationInvitation,
        validator=admin_required,
    ).Field()
