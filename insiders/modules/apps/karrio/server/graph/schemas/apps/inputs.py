import typing
import datetime
import strawberry

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.base.inputs as base


# OAuth App Inputs
@strawberry.input
class OAuthAppFilter(utils.Paginated):
    display_name: typing.Optional[str] = strawberry.UNSET
    features: typing.Optional[typing.List[str]] = strawberry.UNSET
    metadata_key: typing.Optional[str] = strawberry.UNSET
    metadata_value: typing.Optional[str] = strawberry.UNSET
    created_after: typing.Optional[datetime.datetime] = strawberry.UNSET
    created_before: typing.Optional[datetime.datetime] = strawberry.UNSET


@strawberry.input
class CreateOAuthAppMutationInput(utils.BaseInput):
    display_name: str
    description: typing.Optional[str] = strawberry.UNSET
    launch_url: str
    redirect_uris: str
    features: typing.Optional[typing.List[str]] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET


@strawberry.input
class UpdateOAuthAppMutationInput(utils.BaseInput):
    id: str
    display_name: typing.Optional[str] = strawberry.UNSET
    description: typing.Optional[str] = strawberry.UNSET
    launch_url: typing.Optional[str] = strawberry.UNSET
    redirect_uris: typing.Optional[str] = strawberry.UNSET
    features: typing.Optional[typing.List[str]] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET


@strawberry.input
class DeleteOAuthAppMutationInput(utils.BaseInput):
    id: str


# App Installation Inputs
@strawberry.input
class AppInstallationFilter(utils.Paginated):
    app_id: typing.Optional[str] = strawberry.UNSET
    app_type: typing.Optional[str] = strawberry.UNSET
    is_active: typing.Optional[bool] = strawberry.UNSET
    metadata_key: typing.Optional[str] = strawberry.UNSET
    metadata_value: typing.Optional[str] = strawberry.UNSET
    created_after: typing.Optional[datetime.datetime] = strawberry.UNSET
    created_before: typing.Optional[datetime.datetime] = strawberry.UNSET


@strawberry.input
class InstallAppMutationInput(utils.BaseInput):
    app_id: str
    app_type: typing.Optional[str] = "marketplace"  # builtin, marketplace, private
    access_scopes: typing.Optional[typing.List[str]] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
    metafields: typing.Optional[
        typing.List[base.CreateMetafieldInput]
    ] = strawberry.UNSET
    # For private apps that need OAuth
    requires_oauth: typing.Optional[bool] = False
    oauth_app_data: typing.Optional[CreateOAuthAppMutationInput] = strawberry.UNSET


@strawberry.input
class UninstallAppMutationInput(utils.BaseInput):
    app_id: typing.Optional[str] = strawberry.UNSET
    installation_id: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class UpdateAppInstallationMutationInput(utils.BaseInput):
    id: str
    access_scopes: typing.Optional[typing.List[str]] = strawberry.UNSET
    is_active: typing.Optional[bool] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
    metafields: typing.Optional[typing.List[base.MetafieldInput]] = strawberry.UNSET


@strawberry.input
class RotateAppApiKeyMutationInput(utils.BaseInput):
    id: str


@strawberry.input
class EnsureAppApiKeyMutationInput(utils.BaseInput):
    id: str
