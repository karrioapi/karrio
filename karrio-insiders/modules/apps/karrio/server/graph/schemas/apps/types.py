import typing
import datetime
import strawberry

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.base.types as base
import karrio.server.graph.schemas.apps.inputs as inputs
import karrio.server.apps.filters as filters
import karrio.server.apps.models as models


@strawberry.type
class OAuthAppType:
    """OAuth applications created by developers for API access"""
    object_type: str
    id: str
    display_name: str
    description: typing.Optional[str]
    launch_url: str
    redirect_uris: str
    features: typing.List[str]
    client_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: base.UserType
    metadata: typing.Optional[utils.JSON] = None

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["OAuthAppType"]:
        return models.OAuthApp.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.OAuthAppFilter] = strawberry.UNSET,
    ) -> utils.Connection["OAuthAppType"]:
        _filter = filter if filter is not strawberry.UNSET else inputs.OAuthAppFilter()
        queryset = filters.OAuthAppFilter(
            _filter.to_dict(), models.OAuthApp.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class OAuthAppWithCredentialsType:
    """OAuth app with client credentials - only returned during creation"""
    object_type: str
    id: str
    display_name: str
    description: typing.Optional[str]
    launch_url: str
    redirect_uris: str
    features: typing.List[str]
    client_id: str
    client_secret: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: base.UserType
    metadata: typing.Optional[utils.JSON] = None


@strawberry.type
class AppInstallationType:
    """Installation records for physical apps from the app store"""
    object_type: str
    id: str
    app_id: str
    app_type: str
    access_scopes: typing.List[str]
    api_key: typing.Optional[str]
    is_active: bool
    requires_oauth: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: base.UserType
    metadata: typing.Optional[utils.JSON] = None
    oauth_app: typing.Optional[OAuthAppType] = None

    @strawberry.field
    def metafields(self: models.AppInstallation) -> typing.List[base.MetafieldType]:
        return self.metafields.all()

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

    @staticmethod
    @utils.authentication_required
    def resolve_by_app_id(info, app_id: str) -> typing.Optional["AppInstallationType"]:
        """Check if a specific app is installed for the current user"""
        return models.AppInstallation.access_by(info.context.request).filter(
            app_id=app_id, is_active=True
        ).first()
