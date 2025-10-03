import typing
import strawberry

import karrio.server.graph.utils as utils
import karrio.server.orgs.utils as orgs


@strawberry.input
class OrgFilter(utils.Paginated):
    id: typing.Optional[str] = strawberry.UNSET
    name: typing.Optional[str] = strawberry.UNSET
    slug: typing.Optional[str] = strawberry.UNSET
    is_active: typing.Optional[bool] = strawberry.UNSET
    order_by: typing.Optional[str] = strawberry.UNSET


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
    roles: typing.Optional[typing.List[orgs.OrganizationUserRole]] = strawberry.UNSET


@strawberry.input
class AcceptOrganizationInvitationMutationInput(utils.BaseInput):
    guid: str


@strawberry.input
class RemoveOrganizationMemberMutationInput(utils.BaseInput):
    org_id: str
    user_id: str


@strawberry.input
class UpdateMemberStatusMutationInput(utils.BaseInput):
    org_id: str
    user_id: str
    is_active: bool


@strawberry.input
class ResendOrganizationInviteMutationInput(utils.BaseInput):
    invitation_id: str
    redirect_url: str


@strawberry.input
class OrgUsageFilter(utils.UsageFilter):
    id: str = strawberry.UNSET
