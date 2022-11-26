import typing
import datetime
import strawberry

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.base.types as base
import karrio.server.graph.schemas.apps.inputs as inputs
import karrio.server.apps.filters as filters
import karrio.server.apps.models as models


@strawberry.type
class AppType:
    object_type: str
    id: str
    display_name: str
    developer_name: str
    is_public: bool
    is_builtin: bool
    is_embedded: bool
    is_published: bool
    launch_url: str
    features: typing.List[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: base.UserType
    metadata: typing.Optional[utils.JSON] = None
    installation: typing.Optional["AppInstallationType"] = None

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["AppType"]:
        return models.App.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.AppFilter] = strawberry.UNSET,
    ) -> utils.Connection["AppType"]:
        _filter = filter if filter is not strawberry.UNSET else inputs.AppFilter()
        queryset = filters.AppFilter(
            _filter.to_dict(), models.App.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class PrivateAppType:
    object_type: str
    id: str
    display_name: str
    developer_name: str
    is_public: bool
    is_builtin: bool
    is_embedded: bool
    is_published: bool
    launch_url: str
    features: typing.List[str]
    client_id: str
    redirect_uris: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: base.UserType
    metadata: typing.Optional[utils.JSON] = None
    installation: typing.Optional["AppInstallationType"] = None

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["PrivateAppType"]:
        return models.App.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.AppFilter] = strawberry.UNSET,
    ) -> utils.Connection["PrivateAppType"]:
        _filter = filter if filter is not strawberry.UNSET else inputs.AppFilter()
        queryset = filters.AppFilter(
            _filter.to_dict(), models.App.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())



@strawberry.type
class AppInstallationType:
    object_type: str
    id: int
    access_scopes: typing.List[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: base.UserType
    metadata: typing.Optional[utils.JSON] = None

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["AppInstallationType"]:
        return models.AppInstallation.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.AppInstallationFilter] = strawberry.UNSET,
    ) -> utils.Connection["AppInstallationType"]:
        _filter = filter if filter is not strawberry.UNSET else inputs.AppInstallationFilter()
        queryset = filters.AppInstallationFilter(
            _filter.to_dict(), models.AppInstallation.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())
