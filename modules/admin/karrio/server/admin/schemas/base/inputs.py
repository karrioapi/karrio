import typing
import strawberry
from django.conf import settings

import karrio.server.graph.utils as utils
import karrio.server.admin.utils as admin
import karrio.server.orgs.utils as orgs_utils
import karrio.server.graph.schemas.base.inputs as base
import karrio.server.graph.schemas.orgs.inputs as orgs_inputs
import karrio.server.graph.schemas.orders.inputs as orders_inputs


@strawberry.input
class UserFilter(utils.Paginated):
    id: typing.Optional[str] = strawberry.UNSET
    email: typing.Optional[str] = strawberry.UNSET
    is_staff: typing.Optional[bool] = strawberry.UNSET
    is_active: typing.Optional[bool] = strawberry.UNSET
    is_superuser: typing.Optional[bool] = strawberry.UNSET
    order_by: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class AccountFilter(orgs_inputs.OrgFilter):
    pass


@strawberry.input
class CreateOrganizationAccountMutationInput(utils.BaseInput):
    name: str
    slug: typing.Optional[str] = strawberry.UNSET
    is_active: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class UpdateOrganizationAccountMutationInput(utils.BaseInput):
    id: str
    name: typing.Optional[str] = strawberry.UNSET
    slug: typing.Optional[str] = strawberry.UNSET
    is_active: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class DeleteOrganizationAccountMutationInput(utils.BaseInput):
    id: str


@strawberry.input
class DisableOrganizationAccountMutationInput(utils.BaseInput):
    id: str


@strawberry.input
class InviteOrganizationUserMutationInput(utils.BaseInput):
    email: str
    roles: typing.List[orgs_utils.OrganizationUserRole] = strawberry.UNSET
    is_owner: bool = strawberry.UNSET


@strawberry.input
class AccountCarrierConnectionFilter(base.CarrierFilter):
    account_id: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class MarkupFilter(utils.Paginated):
    """Filter for Markup model queries."""
    id: typing.Optional[str] = strawberry.UNSET
    name: typing.Optional[str] = strawberry.UNSET
    active: typing.Optional[bool] = strawberry.UNSET
    markup_type: typing.Optional[admin.MarkupTypeEnum] = strawberry.UNSET
    account_id: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class FeeFilter(utils.Paginated):
    """Filter for Fee model queries."""
    id: typing.Optional[str] = strawberry.UNSET
    markup_id: typing.Optional[str] = strawberry.UNSET
    shipment_id: typing.Optional[str] = strawberry.UNSET
    account_id: typing.Optional[str] = strawberry.UNSET
    carrier_code: typing.Optional[str] = strawberry.UNSET
    date_after: typing.Optional[str] = strawberry.UNSET
    date_before: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class TaskExecutionFilter(utils.Paginated):
    """Filter for task execution records."""
    status: typing.Optional[str] = strawberry.UNSET
    task_name: typing.Optional[str] = strawberry.UNSET
    date_after: typing.Optional[str] = strawberry.UNSET
    date_before: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class CreateUserMutationInput(utils.BaseInput):
    email: str
    password1: str
    password2: str
    redirect_url: typing.Optional[str] = strawberry.UNSET
    full_name: typing.Optional[str] = strawberry.UNSET
    is_staff: typing.Optional[bool] = strawberry.UNSET
    is_active: typing.Optional[bool] = strawberry.UNSET
    is_superuser: typing.Optional[bool] = strawberry.UNSET
    organization_id: typing.Optional[str] = strawberry.UNSET
    permissions: typing.Optional[typing.List[str]] = strawberry.UNSET


@strawberry.input
class UpdateUserMutationInput(utils.BaseInput):
    id: int
    email: typing.Optional[str] = strawberry.UNSET
    full_name: typing.Optional[str] = strawberry.UNSET
    is_staff: typing.Optional[bool] = strawberry.UNSET
    is_active: typing.Optional[bool] = strawberry.UNSET
    is_superuser: typing.Optional[bool] = strawberry.UNSET
    permissions: typing.Optional[typing.List[str]] = strawberry.UNSET


@strawberry.input
class PermissionGroupFilter(utils.Paginated):
    pass


@strawberry.input
class DeleteUserMutationInput(utils.BaseInput):
    id: int


@strawberry.input
class CreateConnectionMutationInput(base.CreateCarrierConnectionMutationInput):
    pass


@strawberry.input
class UpdateConnectionMutationInput(base.UpdateCarrierConnectionMutationInput):
    pass


@strawberry.input
class DeleteConnectionMutationInput(utils.BaseInput):
    id: str


@strawberry.input
class CreateMarkupMutationInput(utils.BaseInput):
    """Input for creating a new Markup."""
    name: str
    amount: float
    markup_type: admin.MarkupTypeEnum
    active: typing.Optional[bool] = strawberry.UNSET
    is_visible: typing.Optional[bool] = strawberry.UNSET
    carrier_codes: typing.Optional[typing.List[str]] = strawberry.UNSET
    service_codes: typing.Optional[typing.List[str]] = strawberry.UNSET
    connection_ids: typing.Optional[typing.List[str]] = strawberry.UNSET
    organizations: typing.Optional[typing.List[str]] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET


@strawberry.input
class UpdateMarkupMutationInput(utils.BaseInput):
    """Input for updating an existing Markup."""
    id: str
    name: typing.Optional[str] = strawberry.UNSET
    amount: typing.Optional[float] = strawberry.UNSET
    markup_type: typing.Optional[admin.MarkupTypeEnum] = strawberry.UNSET
    active: typing.Optional[bool] = strawberry.UNSET
    is_visible: typing.Optional[bool] = strawberry.UNSET
    carrier_codes: typing.Optional[typing.List[str]] = strawberry.UNSET
    service_codes: typing.Optional[typing.List[str]] = strawberry.UNSET
    connection_ids: typing.Optional[typing.List[str]] = strawberry.UNSET
    organizations: typing.Optional[typing.List[str]] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET


InstanceConfigMutationInput = strawberry.input(
    type(
        "InstanceConfigMutationInput",
        (utils.BaseInput,),
        {
            **{k: strawberry.UNSET for k, _ in settings.CONSTANCE_CONFIG.items()},
            "__annotations__": {
                k: typing.Optional[_def[2]]
                for k, _def in settings.CONSTANCE_CONFIG.items()
            },
        },
    )
)

# Admin-specific filter inputs

@strawberry.input
class ResourceUsageFilter(utils.UsageFilter):
    carrier_connection_id: typing.Optional[str] = strawberry.UNSET
    markup_id: typing.Optional[str] = strawberry.UNSET
    account_id: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class SystemShipmentFilter(base.ShipmentFilter):
    """Admin-specific shipment filter with additional account filtering"""
    account_id: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class SystemTrackerFilter(base.TrackerFilter):
    """Admin-specific tracker filter with additional account filtering"""
    account_id: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class SystemOrderFilter(orders_inputs.OrderFilter):
    """Admin-specific order filter with additional account filtering"""
    account_id: typing.Optional[str] = strawberry.UNSET
