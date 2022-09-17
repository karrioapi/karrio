import typing
import datetime
import strawberry

import karrio.server.graph.utils as utils


@strawberry.input
class CreateAppMutationInput(utils.BaseInput):
    display_name: str
    developer_name: str
    features: typing.List[str]
    launch_url: str
    is_embedded: bool
    redirect_uris: str = None
    is_public: typing.Optional[bool] = False
    metadata: typing.Optional[utils.JSON] = None


@strawberry.input
class AppFilter(utils.Paginated):
    features: typing.List[str] = strawberry.UNSET
    metadata_key: typing.Optional[str] = strawberry.UNSET
    metadata_value: typing.Optional[str] = strawberry.UNSET
    created_after: typing.Optional[datetime.datetime] = strawberry.UNSET
    created_before: typing.Optional[datetime.datetime] = strawberry.UNSET


@strawberry.input
class UpdateAppMutationInput(utils.BaseInput):
    id: str
    display_name: typing.Optional[str] = None
    developer_name: typing.Optional[str] = None
    features: typing.List[str] = None
    launch_url: typing.Optional[str] = None
    is_embedded: typing.Optional[bool] = None
    redirect_uris: typing.Optional[str] = None
    is_public: typing.Optional[bool] = False
    metadata: typing.Optional[utils.JSON] = None


@strawberry.input
class AppInstallationFilter(utils.Paginated):
    metadata_key: typing.Optional[str] = strawberry.UNSET
    metadata_value: typing.Optional[str] = strawberry.UNSET
    created_after: typing.Optional[datetime.datetime] = strawberry.UNSET
    created_before: typing.Optional[datetime.datetime] = strawberry.UNSET


@strawberry.input
class InstallAppMutationInput(utils.BaseInput):
    app_id: str
    access_scopes = typing.List[str]
    metadata: typing.Optional[utils.JSON] = None


@strawberry.input
class UninstallAppMutationInput(utils.BaseInput):
    app_id: str
