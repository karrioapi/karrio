import strawberry
from strawberry.types import Info

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.base as base
import karrio.server.graph.schemas.apps.mutations as mutations
import karrio.server.graph.schemas.apps.inputs as inputs
import karrio.server.graph.schemas.apps.types as types
import karrio.server.apps.models as models

extra_types: list = []


@strawberry.type
class Query:
    app: types.AppType = strawberry.field(resolver=types.AppType.resolve)
    apps: utils.Connection[types.AppType] = strawberry.field(
        resolver=types.AppType.resolve_list
    )
    private_app: types.PrivateAppType = strawberry.field(
        resolver=types.PrivateAppType.resolve
    )
    private_apps: utils.Connection[types.PrivateAppType] = strawberry.field(
        resolver=types.PrivateAppType.resolve_list
    )
    installations: utils.Connection[types.AppInstallationType] = strawberry.field(
        resolver=types.AppInstallationType.resolve_list
    )


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_app(
        self, info: Info, input: inputs.CreateAppMutationInput
    ) -> mutations.CreateAppMutation:
        return mutations.CreateAppMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_app(
        self, info: Info, input: inputs.UpdateAppMutationInput
    ) -> mutations.UpdateAppMutation:
        return mutations.UpdateAppMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_app(
        self, info: Info, input: base.inputs.DeleteMutationInput
    ) -> base.mutations.DeleteMutation:
        return base.mutations.DeleteMutation.mutate(
            info, model=models.App, **input.to_dict()
        )

    @strawberry.mutation
    def install_app(
        self, info: Info, input: inputs.InstallAppMutationInput
    ) -> mutations.InstallAppMutation:
        return mutations.InstallAppMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def uninstall_app(
        self, info: Info, input: inputs.UninstallAppMutationInput
    ) -> mutations.UninstallAppMutation:
        return mutations.UninstallAppMutation.mutate(info, **input.to_dict())
