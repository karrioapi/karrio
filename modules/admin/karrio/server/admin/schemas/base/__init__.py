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

extra_types = [*types.SystemCarrierSettings.values()]


@strawberry.type
class Query:
    me: types.UserType = strawberry.field(resolver=types.UserType.me)
    user: typing.Optional[types.UserType] = strawberry.field(
        resolver=types.UserType.resolve
    )
    users: utils.Connection[types.UserType] = strawberry.field(
        resolver=types.UserType.resolve_list
    )

    configs: types.InstanceConfigType = strawberry.field(
        resolver=types.InstanceConfigType.resolve
    )
    system_usage: types.SystemUsageType = strawberry.field(
        resolver=types.SystemUsageType.resolve
    )
    surcharge: typing.Optional[types.SurchargeType] = strawberry.field(
        resolver=types.SurchargeType.resolve
    )
    surcharges: typing.List[types.SurchargeType] = strawberry.field(
        resolver=types.SurchargeType.resolve_list
    )
    system_connection: typing.Optional[
        types.SystemCarrierConnectionType
    ] = strawberry.field(resolver=types.SystemConnectionType.resolve)
    system_connections: typing.List[
        types.SystemCarrierConnectionType
    ] = strawberry.field(resolver=types.SystemConnectionType.resolve_list)

    rate_sheet: typing.Optional[types.SystemRateSheetType] = strawberry.field(
        resolver=types.SystemRateSheetType.resolve
    )
    rate_sheets: utils.Connection[types.SystemRateSheetType] = strawberry.field(
        resolver=types.SystemRateSheetType.resolve_list
    )

    permission_groups: utils.Connection[types.PermissionGroupType] = strawberry.field(
        resolver=types.PermissionGroupType.resolve_list
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
    def create_carrier_connection(
        self, info: Info, input: inputs.CreateConnectionMutationInput
    ) -> mutations.CreateConnectionMutation:
        return mutations.CreateConnectionMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_carrier_connection(
        self, info: Info, input: inputs.UpdateConnectionMutationInput
    ) -> mutations.UpdateConnectionMutation:
        return mutations.UpdateConnectionMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_carrier_connection(
        self, info: Info, input: inputs.DeleteConnectionMutationInput
    ) -> mutations.DeleteConnectionMutation:
        return mutations.DeleteConnectionMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def create_surcharge(
        self, info: Info, input: inputs.CreateSurchargeMutationInput
    ) -> mutations.CreateSurchargeMutation:
        return mutations.CreateSurchargeMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_surcharge(
        self, info: Info, input: inputs.UpdateSurchargeMutationInput
    ) -> mutations.UpdateSurchargeMutation:
        return mutations.UpdateSurchargeMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_surcharge(
        self, info: Info, input: inputs.base.DeleteMutationInput
    ) -> mutations.base.DeleteMutation:
        return mutations.base.DeleteMutation.mutate(
            info, model=pricing.Surcharge, **input.to_dict()
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
    def delete_rate_sheet(
        self, info: Info, input: inputs.base.DeleteMutationInput
    ) -> mutations.base.DeleteMutation:
        return mutations.base.DeleteMutation.mutate(
            info, model=providers.RateSheet, **input.to_dict()
        )
