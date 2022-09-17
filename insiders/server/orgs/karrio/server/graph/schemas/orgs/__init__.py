import strawberry
from strawberry.types import Info

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.base as base
import karrio.server.graph.schemas.orgs.mutations as mutations
import karrio.server.graph.schemas.orgs.inputs as inputs
import karrio.server.graph.schemas.orgs.types as types
import karrio.server.orgs.models as models
from karrio.server.orgs.utils import admin_required

extra_types: list = []


@strawberry.type
class Query:
    organization: types.OrganizationType = strawberry.field(
        resolver=types.OrganizationType.resolve
    )
    organizations: utils.Connection[types.OrganizationType] = strawberry.field(
        resolver=types.OrganizationType.resolve_list
    )
    organization_invitation: types.OrganizationInvitationType = strawberry.field(
        resolver=types.OrganizationInvitationType.resolve
    )


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_organization(
        self, info: Info, input: inputs.CreateOrganizationMutationInput
    ) -> mutations.CreateOrganizationMutation:
        return mutations.CreateOrganizationMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_organization(
        self, info: Info, input: inputs.UpdateOrganizationMutationInput
    ) -> mutations.UpdateOrganizationMutation:
        return mutations.UpdateOrganizationMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_organization(
        self, info: Info, input: inputs.DeleteOrganizationMutationInput
    ) -> mutations.DeleteOrganizationMutation:
        return mutations.DeleteOrganizationMutation.mutate(
            info,
            **input.to_dict()
        )

    @strawberry.mutation
    def change_organization_owner(
        self, info: Info, input: inputs.ChangeOrganizationOwnerMutationInput
    ) -> mutations.ChangeOrganizationOwnerMutation:
        return mutations.ChangeOrganizationOwnerMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def set_organization_user_roles(
        self, info: Info, input: inputs.SetOrganizationUserRolesMutationInput
    ) -> mutations.SetOrganizationUserRolesMutation:
        return mutations.SetOrganizationUserRolesMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def send_organization_invites(
        self, info: Info, input: inputs.SendOrganizationInvitesMutationInput
    ) -> mutations.SendOrganizationInvitesMutation:
        return mutations.SendOrganizationInvitesMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def accept_organization_invitation(
        self, info: Info, input: inputs.AcceptOrganizationInvitationMutationInput
    ) -> mutations.AcceptOrganizationInvitationMutation:
        return mutations.AcceptOrganizationInvitationMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_organization_invitation(
        self, info: Info, input: base.inputs.DeleteMutationInput
    ) -> base.mutations.DeleteMutation:
        return base.mutations.DeleteMutation.mutate(
            info,
            models.OrganizationInvitation,
            validator=admin_required,
            **input.to_dict()
        )
