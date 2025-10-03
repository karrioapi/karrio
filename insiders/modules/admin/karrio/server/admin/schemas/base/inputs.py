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
class AddonFilter(utils.Paginated):
    id: typing.Optional[str] = strawberry.UNSET
    name: typing.Optional[str] = strawberry.UNSET
    active: typing.Optional[bool] = strawberry.UNSET
    surcharge_type: typing.Optional[admin.SurchargeTypeEnum] = strawberry.UNSET


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
class CreateAddonMutationInput(utils.BaseInput):
    name: str
    amount: float
    surcharge_type: admin.SurchargeTypeEnum
    active: typing.Optional[bool] = strawberry.UNSET
    carriers: typing.Optional[typing.List[str]] = strawberry.UNSET
    services: typing.Optional[typing.List[str]] = strawberry.UNSET
    organizations: typing.Optional[typing.List[str]] = strawberry.UNSET
    carrier_accounts: typing.Optional[typing.List[str]] = strawberry.UNSET


@strawberry.input
class UpdateAddonMutationInput(CreateAddonMutationInput):
    id: str = strawberry.UNSET
    name: typing.Optional[str] = strawberry.UNSET
    amount: typing.Optional[float] = strawberry.UNSET
    surcharge_type: typing.Optional[admin.SurchargeTypeEnum] = strawberry.UNSET


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
    surcharge_id: typing.Optional[str] = strawberry.UNSET
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
