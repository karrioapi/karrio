import typing
import datetime
import strawberry
from django.conf import settings

import karrio.server.graph.utils as utils
import karrio.server.admin.utils as admin
import karrio.server.graph.schemas.base.inputs as base


@strawberry.input
class UserFilter(utils.Paginated):
    id: typing.Optional[str] = strawberry.UNSET
    email: typing.Optional[str] = strawberry.UNSET
    is_staff: typing.Optional[bool] = strawberry.UNSET
    is_active: typing.Optional[bool] = strawberry.UNSET
    is_superuser: typing.Optional[bool] = strawberry.UNSET
    order_by: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class SurchargeFilter(utils.BaseInput):
    id: typing.Optional[str] = strawberry.UNSET
    name: typing.Optional[str] = strawberry.UNSET
    active: typing.Optional[bool] = strawberry.UNSET
    surcharge_type: typing.Optional[admin.SurchargeTypeEnum] = strawberry.UNSET


@strawberry.input
class CreateUserMutationInput(utils.BaseInput):
    email: str
    password1: str
    password2: str
    redirect_url: str
    full_name: typing.Optional[str] = strawberry.UNSET
    is_staff: typing.Optional[bool] = strawberry.UNSET
    is_active: typing.Optional[bool] = strawberry.UNSET
    is_superuser: typing.Optional[bool] = strawberry.UNSET
    organization_id: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class UpdateUserMutationInput(utils.BaseInput):
    email: str
    is_staff: typing.Optional[bool] = strawberry.UNSET
    is_active: typing.Optional[bool] = strawberry.UNSET
    is_superuser: typing.Optional[bool] = strawberry.UNSET


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
class CreateSurchargeMutationInput(utils.BaseInput):
    name: str
    amount: float
    surcharge_type: admin.SurchargeTypeEnum
    active: typing.Optional[bool] = strawberry.UNSET
    carriers: typing.Optional[typing.List[str]] = strawberry.UNSET
    services: typing.Optional[typing.List[str]] = strawberry.UNSET
    carrier_accounts: typing.Optional[typing.List[str]] = strawberry.UNSET


@strawberry.input
class UpdateSurchargeMutationInput(CreateSurchargeMutationInput):
    id: str = strawberry.UNSET
    name: typing.Optional[str] = strawberry.UNSET
    amount: typing.Optional[float] = strawberry.UNSET
    surcharge_type: typing.Optional[admin.SurchargeTypeEnum] = strawberry.UNSET


@strawberry.input
class UsageFilter(utils.BaseInput):
    date_after: typing.Optional[datetime.datetime] = strawberry.UNSET
    date_before: typing.Optional[datetime.datetime] = strawberry.UNSET
    omit: typing.Optional[typing.List[str]] = strawberry.UNSET


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
