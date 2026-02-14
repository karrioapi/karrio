import typing
import strawberry
from strawberry.types import Info

import karrio.server.iam.models as iam
import karrio.server.graph.utils as utils
import karrio.server.pricing.models as pricing
import karrio.server.providers.models as providers
import karrio.server.admin.schemas.base.types as types
import karrio.server.admin.schemas.base.inputs as inputs
import karrio.server.admin.schemas.base.mutations as mutations

extra_types = []


@strawberry.type
class Query:
    me: types.SystemUserType = strawberry.field(resolver=types.SystemUserType.me)
    user: typing.Optional[types.SystemUserType] = strawberry.field(
        resolver=types.SystemUserType.resolve
    )
    users: utils.Connection[types.SystemUserType] = strawberry.field(
        resolver=types.SystemUserType.resolve_list
    )

    configs: types.InstanceConfigType = strawberry.field(
        resolver=types.InstanceConfigType.resolve
    )
    usage: types.AdminSystemUsageType = strawberry.field(
        resolver=types.AdminSystemUsageType.resolve
    )

    markup: typing.Optional[types.MarkupType] = strawberry.field(
        resolver=types.MarkupType.resolve
    )
    markups: utils.Connection[types.MarkupType] = strawberry.field(
        resolver=types.MarkupType.resolve_list
    )
    fee: typing.Optional[types.FeeType] = strawberry.field(
        resolver=types.FeeType.resolve
    )
    fees: utils.Connection[types.FeeType] = strawberry.field(
        resolver=types.FeeType.resolve_list
    )

    system_carrier_connection: typing.Optional[types.SystemCarrierConnectionType] = (
        strawberry.field(resolver=types.SystemCarrierConnectionType.resolve)
    )
    system_carrier_connections: utils.Connection[types.SystemCarrierConnectionType] = (
        strawberry.field(resolver=types.SystemCarrierConnectionType.resolve_list)
    )

    rate_sheet: typing.Optional[types.SystemRateSheetType] = strawberry.field(
        resolver=types.SystemRateSheetType.resolve
    )
    rate_sheets: utils.Connection[types.SystemRateSheetType] = strawberry.field(
        resolver=types.SystemRateSheetType.resolve_list
    )

    permission_groups: utils.Connection[types.PermissionGroupType] = strawberry.field(
        resolver=types.PermissionGroupType.resolve_list
    )

    carrier_connections: utils.Connection[types.AccountCarrierConnectionType] = strawberry.field(
        resolver=types.AccountCarrierConnectionType.resolve_list
    )
    carrier_connection: typing.Optional[types.AccountCarrierConnectionType] = strawberry.field(
        resolver=types.AccountCarrierConnectionType.resolve
    )

    shipments: utils.Connection[types.SystemShipmentType] = strawberry.field(
        resolver=types.SystemShipmentType.resolve_list
    )
    shipment: typing.Optional[types.SystemShipmentType] = strawberry.field(
        resolver=types.SystemShipmentType.resolve
    )

    trackers: utils.Connection[types.SystemTrackerType] = strawberry.field(
        resolver=types.SystemTrackerType.resolve_list
    )
    tracker: typing.Optional[types.SystemTrackerType] = strawberry.field(
        resolver=types.SystemTrackerType.resolve
    )

    orders: utils.Connection[types.SystemOrderType] = strawberry.field(
        resolver=types.SystemOrderType.resolve_list
    )
    order: typing.Optional[types.SystemOrderType] = strawberry.field(
        resolver=types.SystemOrderType.resolve
    )

    account: typing.Optional[types.OrganizationAccountType] = strawberry.field(
        resolver=types.OrganizationAccountType.resolve
    )
    accounts: utils.Connection[types.OrganizationAccountType] = strawberry.field(
        resolver=types.OrganizationAccountType.resolve_list
    )

    task_executions: utils.Connection[types.TaskExecutionType] = strawberry.field(
        resolver=types.TaskExecutionType.resolve_list
    )
    worker_health: types.WorkerHealthType = strawberry.field(
        resolver=types.WorkerHealthType.resolve
    )


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(
        self, info: Info, input: inputs.CreateUserMutationInput
    ) -> mutations.CreateUserMutation:
        return mutations.CreateUserMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_user(
        self, info: Info, input: inputs.UpdateUserMutationInput
    ) -> mutations.UpdateUserMutation:
        return mutations.UpdateUserMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def remove_user(
        self, info: Info, input: inputs.DeleteUserMutationInput
    ) -> mutations.DeleteUserMutation:
        def validator(instance, **kwargs):
            if instance.id == info.context.request.user.id:
                raise Exception("You can't remove yourself")

        return mutations.DeleteUserMutation.mutate(
            info,
            model=iam.User,
            validator=validator,
            **input.to_dict(),
        )

    @strawberry.mutation
    def update_configs(
        self, info: Info, input: inputs.InstanceConfigMutationInput
    ) -> mutations.InstanceConfigMutation:
        return mutations.InstanceConfigMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def create_system_carrier_connection(
        self, info: Info, input: inputs.CreateConnectionMutationInput
    ) -> mutations.CreateSystemCarrierConnectionMutation:
        return mutations.CreateSystemCarrierConnectionMutation.mutate(
            info, **input.to_dict()
        )

    @strawberry.mutation
    def update_system_carrier_connection(
        self, info: Info, input: inputs.UpdateConnectionMutationInput
    ) -> mutations.UpdateSystemCarrierConnectionMutation:
        return mutations.UpdateSystemCarrierConnectionMutation.mutate(
            info, **input.to_dict()
        )

    @strawberry.mutation
    def delete_system_carrier_connection(
        self, info: Info, input: inputs.DeleteConnectionMutationInput
    ) -> mutations.DeleteConnectionMutation:
        return mutations.DeleteConnectionMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def create_markup(
        self, info: Info, input: inputs.CreateMarkupMutationInput
    ) -> mutations.CreateMarkupMutation:
        return mutations.CreateMarkupMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_markup(
        self, info: Info, input: inputs.UpdateMarkupMutationInput
    ) -> mutations.UpdateMarkupMutation:
        return mutations.UpdateMarkupMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_markup(
        self, info: Info, input: inputs.base.DeleteMutationInput
    ) -> mutations.base.DeleteMutation:
        return mutations.base.DeleteMutation.mutate(
            info, model=pricing.Markup, **input.to_dict()
        )

    @strawberry.mutation
    def create_rate_sheet(
        self, info: Info, input: inputs.base.CreateRateSheetMutationInput
    ) -> mutations.CreateRateSheetMutation:
        return mutations.CreateRateSheetMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_rate_sheet(
        self, info: Info, input: inputs.base.UpdateRateSheetMutationInput
    ) -> mutations.UpdateRateSheetMutation:
        return mutations.UpdateRateSheetMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_rate_sheet_service(
        self, info: Info, input: inputs.base.DeleteRateSheetServiceMutationInput
    ) -> mutations.DeleteRateSheetServiceMutation:
        return mutations.DeleteRateSheetServiceMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_rate_sheet(
        self, info: Info, input: inputs.base.DeleteMutationInput
    ) -> mutations.base.DeleteMutation:
        return mutations.base.DeleteMutation.mutate(
            info, model=providers.RateSheet, **input.to_dict()
        )

    # ─────────────────────────────────────────────────────────────────────────
    # SHARED ZONE MUTATIONS
    # ─────────────────────────────────────────────────────────────────────────

    @strawberry.mutation
    def add_shared_zone(
        self, info: Info, input: inputs.base.AddSharedZoneMutationInput
    ) -> mutations.AddSharedZoneMutation:
        return mutations.AddSharedZoneMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_shared_zone(
        self, info: Info, input: inputs.base.UpdateSharedZoneMutationInput
    ) -> mutations.UpdateSharedZoneMutation:
        return mutations.UpdateSharedZoneMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_shared_zone(
        self, info: Info, input: inputs.base.DeleteSharedZoneMutationInput
    ) -> mutations.DeleteSharedZoneMutation:
        return mutations.DeleteSharedZoneMutation.mutate(info, **input.to_dict())

    # ─────────────────────────────────────────────────────────────────────────
    # SHARED SURCHARGE MUTATIONS
    # ─────────────────────────────────────────────────────────────────────────

    @strawberry.mutation
    def add_shared_surcharge(
        self, info: Info, input: inputs.base.AddSharedSurchargeMutationInput
    ) -> mutations.AddSharedSurchargeMutation:
        return mutations.AddSharedSurchargeMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_shared_surcharge(
        self, info: Info, input: inputs.base.UpdateSharedSurchargeMutationInput
    ) -> mutations.UpdateSharedSurchargeMutation:
        return mutations.UpdateSharedSurchargeMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_shared_surcharge(
        self, info: Info, input: inputs.base.DeleteSharedSurchargeMutationInput
    ) -> mutations.DeleteSharedSurchargeMutation:
        return mutations.DeleteSharedSurchargeMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def batch_update_surcharges(
        self, info: Info, input: inputs.base.BatchUpdateSurchargesMutationInput
    ) -> mutations.BatchUpdateSurchargesMutation:
        return mutations.BatchUpdateSurchargesMutation.mutate(info, **input.to_dict())

    # ─────────────────────────────────────────────────────────────────────────
    # SERVICE RATE MUTATIONS
    # ─────────────────────────────────────────────────────────────────────────

    @strawberry.mutation
    def update_service_rate(
        self, info: Info, input: inputs.base.UpdateServiceRateMutationInput
    ) -> mutations.UpdateServiceRateMutation:
        return mutations.UpdateServiceRateMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def batch_update_service_rates(
        self, info: Info, input: inputs.base.BatchUpdateServiceRatesMutationInput
    ) -> mutations.BatchUpdateServiceRatesMutation:
        return mutations.BatchUpdateServiceRatesMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_service_rate(
        self, info: Info, input: inputs.base.DeleteServiceRateMutationInput
    ) -> mutations.DeleteServiceRateMutation:
        return mutations.DeleteServiceRateMutation.mutate(info, **input.to_dict())

    # ─────────────────────────────────────────────────────────────────────────
    # WEIGHT RANGE MUTATIONS
    # ─────────────────────────────────────────────────────────────────────────

    @strawberry.mutation
    def add_weight_range(
        self, info: Info, input: inputs.base.AddWeightRangeMutationInput
    ) -> mutations.AddWeightRangeMutation:
        return mutations.AddWeightRangeMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def remove_weight_range(
        self, info: Info, input: inputs.base.RemoveWeightRangeMutationInput
    ) -> mutations.RemoveWeightRangeMutation:
        return mutations.RemoveWeightRangeMutation.mutate(info, **input.to_dict())

    # ─────────────────────────────────────────────────────────────────────────
    # SERVICE ZONE/SURCHARGE ASSIGNMENT MUTATIONS
    # ─────────────────────────────────────────────────────────────────────────

    @strawberry.mutation
    def update_service_zone_ids(
        self, info: Info, input: inputs.base.UpdateServiceZoneIdsMutationInput
    ) -> mutations.UpdateServiceZoneIdsMutation:
        return mutations.UpdateServiceZoneIdsMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_service_surcharge_ids(
        self, info: Info, input: inputs.base.UpdateServiceSurchargeIdsMutationInput
    ) -> mutations.UpdateServiceSurchargeIdsMutation:
        return mutations.UpdateServiceSurchargeIdsMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def create_organization_account(
        self, info: Info, input: inputs.CreateOrganizationAccountMutationInput
    ) -> mutations.CreateOrganizationAccountMutation:
        return mutations.CreateOrganizationAccountMutation.mutate(
            info, **input.to_dict()
        )

    @strawberry.mutation
    def update_organization_account(
        self, info: Info, input: inputs.UpdateOrganizationAccountMutationInput
    ) -> mutations.UpdateOrganizationAccountMutation:
        return mutations.UpdateOrganizationAccountMutation.mutate(
            info, **input.to_dict()
        )

    @strawberry.mutation
    def disable_organization_account(
        self, info: Info, input: inputs.DisableOrganizationAccountMutationInput
    ) -> mutations.DisableOrganizationAccountMutation:
        return mutations.DisableOrganizationAccountMutation.mutate(
            info, **input.to_dict()
        )

    @strawberry.mutation
    def delete_organization_account(
        self, info: Info, input: inputs.DeleteOrganizationAccountMutationInput
    ) -> mutations.DeleteOrganizationAccountMutation:
        return mutations.DeleteOrganizationAccountMutation.mutate(
            info, **input.to_dict()
        )

    @strawberry.mutation
    def invite_organization_user(
        self, info: Info, input: inputs.InviteOrganizationUserMutationInput
    ) -> mutations.InviteOrganizationUserMutation:
        return mutations.InviteOrganizationUserMutation.mutate(info, **input.to_dict())
