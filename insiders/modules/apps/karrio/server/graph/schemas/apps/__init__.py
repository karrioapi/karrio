import strawberry
from strawberry.types import Info

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.apps.mutations as mutations
import karrio.server.graph.schemas.apps.inputs as inputs
import karrio.server.graph.schemas.apps.types as types

extra_types: list = []


@strawberry.type
class Query:
    # OAuth App queries
    oauth_app: types.OAuthAppType = strawberry.field(resolver=types.OAuthAppType.resolve)
    oauth_apps: utils.Connection[types.OAuthAppType] = strawberry.field(
        resolver=types.OAuthAppType.resolve_list
    )

    # App Installation queries
    app_installation: types.AppInstallationType = strawberry.field(
        resolver=types.AppInstallationType.resolve
    )
    app_installations: utils.Connection[types.AppInstallationType] = strawberry.field(
        resolver=types.AppInstallationType.resolve_list
    )
    app_installation_by_app_id: types.AppInstallationType = strawberry.field(
        resolver=types.AppInstallationType.resolve_by_app_id
    )


@strawberry.type
class Mutation:
    # OAuth App mutations
    @strawberry.mutation
    def create_oauth_app(
        self, info: Info, input: inputs.CreateOAuthAppMutationInput
    ) -> mutations.CreateOAuthAppMutation:
        return mutations.CreateOAuthAppMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_oauth_app(
        self, info: Info, input: inputs.UpdateOAuthAppMutationInput
    ) -> mutations.UpdateOAuthAppMutation:
        return mutations.UpdateOAuthAppMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_oauth_app(
        self, info: Info, input: inputs.DeleteOAuthAppMutationInput
    ) -> mutations.DeleteOAuthAppMutation:
        return mutations.DeleteOAuthAppMutation.mutate(info, **input.to_dict())

    # App Installation mutations
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

    @strawberry.mutation
    def update_app_installation(
        self, info: Info, input: inputs.UpdateAppInstallationMutationInput
    ) -> mutations.UpdateAppInstallationMutation:
        return mutations.UpdateAppInstallationMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def rotate_app_api_key(
        self, info: Info, input: inputs.RotateAppApiKeyMutationInput
    ) -> mutations.RotateAppApiKeyMutation:
        return mutations.RotateAppApiKeyMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def ensure_app_api_key(
        self, info: Info, input: inputs.EnsureAppApiKeyMutationInput
    ) -> mutations.EnsureAppApiKeyMutation:
        return mutations.EnsureAppApiKeyMutation.mutate(info, **input.to_dict())
