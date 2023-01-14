import typing
import strawberry

import karrio.server.graph.utils as utils
import karrio.server.orgs.utils as orgs


@strawberry.input
class CreateOrganizationMutationInput(utils.BaseInput):
    name: str


@strawberry.input
class UpdateOrganizationMutationInput(utils.BaseInput):
    id: str
    name: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class DeleteOrganizationMutationInput(utils.BaseInput):
    id: str
    password: str


@strawberry.input
class SetOrganizationUserRolesMutationInput(utils.BaseInput):
    org_id: str
    user_id: str
    roles: typing.List[orgs.OrganizationUserRole]


@strawberry.input
class ChangeOrganizationOwnerMutationInput(utils.BaseInput):
    org_id: str
    email: str
    password: str


@strawberry.input
class SendOrganizationInvitesMutationInput(utils.BaseInput):
    org_id: str
    emails: typing.List[str]
    redirect_url: str


@strawberry.input
class AcceptOrganizationInvitationMutationInput(utils.BaseInput):
    guid: str
