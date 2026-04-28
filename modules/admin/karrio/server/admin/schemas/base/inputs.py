import karrio.server.admin.utils as admin
import karrio.server.graph.schemas.base.inputs as base
import karrio.server.graph.utils as utils
import strawberry


@strawberry.input
class UserFilter(utils.Paginated):
    id: str | None = strawberry.UNSET
    email: str | None = strawberry.UNSET
    is_staff: bool | None = strawberry.UNSET
    is_active: bool | None = strawberry.UNSET
    is_superuser: bool | None = strawberry.UNSET
    order_by: str | None = strawberry.UNSET


@strawberry.input
class MarkupFilter(utils.Paginated):
    """Filter for Markup model queries."""

    id: str | None = strawberry.UNSET
    name: str | None = strawberry.UNSET
    active: bool | None = strawberry.UNSET
    markup_type: admin.MarkupTypeEnum | None = strawberry.UNSET
    account_id: str | None = strawberry.UNSET
    meta_key: str | None = strawberry.UNSET
    meta_value: str | None = strawberry.UNSET
    metadata_key: str | None = strawberry.UNSET
    metadata_value: str | None = strawberry.UNSET


@strawberry.input
class FeeFilter(utils.Paginated):
    """Filter for Fee model queries."""

    id: str | None = strawberry.UNSET
    markup_id: str | None = strawberry.UNSET
    shipment_id: str | None = strawberry.UNSET
    account_id: str | None = strawberry.UNSET
    carrier_code: str | None = strawberry.UNSET
    date_after: str | None = strawberry.UNSET
    date_before: str | None = strawberry.UNSET


@strawberry.input
class CreateUserMutationInput(utils.BaseInput):
    email: str
    password1: str
    password2: str
    redirect_url: str | None = strawberry.UNSET
    full_name: str | None = strawberry.UNSET
    is_staff: bool | None = strawberry.UNSET
    is_active: bool | None = strawberry.UNSET
    is_superuser: bool | None = strawberry.UNSET
    organization_id: str | None = strawberry.UNSET
    permissions: list[str] | None = strawberry.UNSET


@strawberry.input
class UpdateUserMutationInput(utils.BaseInput):
    id: int
    email: str | None = strawberry.UNSET
    full_name: str | None = strawberry.UNSET
    is_staff: bool | None = strawberry.UNSET
    is_active: bool | None = strawberry.UNSET
    is_superuser: bool | None = strawberry.UNSET
    permissions: list[str] | None = strawberry.UNSET


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
    active: bool | None = strawberry.UNSET
    is_visible: bool | None = strawberry.UNSET
    carrier_codes: list[str] | None = strawberry.UNSET
    service_codes: list[str] | None = strawberry.UNSET
    connection_ids: list[str] | None = strawberry.UNSET
    organizations: list[str] | None = strawberry.UNSET
    meta: utils.JSON | None = strawberry.UNSET
    metadata: utils.JSON | None = strawberry.UNSET


@strawberry.input
class UpdateMarkupMutationInput(utils.BaseInput):
    """Input for updating an existing Markup."""

    id: str
    name: str | None = strawberry.UNSET
    amount: float | None = strawberry.UNSET
    markup_type: admin.MarkupTypeEnum | None = strawberry.UNSET
    active: bool | None = strawberry.UNSET
    is_visible: bool | None = strawberry.UNSET
    carrier_codes: list[str] | None = strawberry.UNSET
    service_codes: list[str] | None = strawberry.UNSET
    connection_ids: list[str] | None = strawberry.UNSET
    organizations: list[str] | None = strawberry.UNSET
    meta: utils.JSON | None = strawberry.UNSET
    metadata: utils.JSON | None = strawberry.UNSET


@strawberry.input
class InstanceConfigMutationInput(utils.BaseInput):
    configs: utils.JSON | None = strawberry.UNSET


# Admin-specific filter inputs


@strawberry.input
class ResourceUsageFilter(utils.UsageFilter):
    carrier_connection_id: str | None = strawberry.UNSET
    markup_id: str | None = strawberry.UNSET
    account_id: str | None = strawberry.UNSET


# -----------------------------------------------------------
# Worker Management Mutation Inputs
# -----------------------------------------------------------


@strawberry.input
class TriggerTrackerUpdateInput(utils.BaseInput):
    tracker_ids: list[str] | None = strawberry.UNSET


@strawberry.input
class RetryWebhookInput(utils.BaseInput):
    event_id: str
