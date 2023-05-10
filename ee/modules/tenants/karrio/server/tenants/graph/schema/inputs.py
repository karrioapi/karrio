import typing
import strawberry

import karrio.server.graph.utils as utils


@strawberry.input
class CreateTenantMutationInput(utils.BaseInput):
    name: str
    domain: str
    schema_name: str
    admin_email: str
    feature_flags: typing.Optional[utils.JSON] = strawberry.UNSET
    app_domains: typing.Optional[typing.List[str]] = strawberry.UNSET


@strawberry.input
class UpdateTenantMutationInput(utils.BaseInput):
    schema_name: str
    name: typing.Optional[str] = strawberry.UNSET
    feature_flags: typing.Optional[utils.JSON] = strawberry.UNSET
    app_domains: typing.Optional[typing.List[str]] = strawberry.UNSET


@strawberry.input
class DeleteTenantMutationInput(utils.BaseInput):
    schema_name: str


@strawberry.input
class AddCustomDomainMutationInput(utils.BaseInput):
    domain: str
    schema_name: str


@strawberry.input
class UpdateCustomDomainMutationInput(utils.BaseInput):
    schema_name: str
    domain: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class DeleteCustomDomainMutationInput(utils.BaseInput):
    schema_name: str


@strawberry.input
class TenantFilter(utils.Paginated):
    app_domain: typing.Optional[str] = strawberry.UNSET
    api_domain: typing.Optional[str] = strawberry.UNSET
    schema_name: typing.Optional[str] = strawberry.UNSET
