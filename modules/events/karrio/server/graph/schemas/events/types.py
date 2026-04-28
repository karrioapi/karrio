import datetime
import typing

import karrio.lib as lib
import karrio.server.events.filters as filters
import karrio.server.events.models as models
import karrio.server.graph.schemas.base.types as base
import karrio.server.graph.schemas.events.inputs as inputs
import karrio.server.graph.utils as utils
import strawberry
from strawberry.types import Info


@strawberry.type
class WebhookType:
    object_type: str
    id: str
    url: str | None
    secret: str | None
    disabled: bool | None
    test_mode: bool | None
    description: str | None
    enabled_events: list[inputs.EventStatusEnum]
    last_event_at: datetime.datetime | None
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None
    created_by: base.UserType | None

    @staticmethod
    @utils.authentication_required
    def resolve(info: Info, id: str) -> typing.Optional["WebhookType"]:
        return models.Webhook.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info: Info,
        filter: inputs.WebhookFilter | None = strawberry.UNSET,
    ) -> utils.Connection["WebhookType"]:
        _filter = filter if filter is not strawberry.UNSET else inputs.WebhookFilter()
        queryset = filters.WebhookFilter(_filter.to_dict(), models.Webhook.access_by(info.context.request)).qs
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class EventType:
    object_type: str
    id: str
    test_mode: bool | None
    pending_webhooks: int | None
    type: inputs.EventStatusEnum | None
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None
    created_by: base.UserType | None

    @strawberry.field
    def request_id(self: models.Event) -> str | None:
        try:
            return (lib.to_dict(self.data) or {}).get("meta", {}).get("request_id")
        except (AttributeError, TypeError, ValueError):
            return (self.data or {}).get("meta", {}).get("request_id")

    @strawberry.field
    def data(self: models.Event) -> utils.JSON | None:
        try:
            return lib.to_dict(self.data)
        except (AttributeError, TypeError, ValueError):
            return self.data

    @staticmethod
    @utils.authentication_required
    def resolve(info: Info, id: str) -> typing.Optional["EventType"]:
        return models.Event.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info: Info,
        filter: inputs.EventFilter | None = strawberry.UNSET,
    ) -> utils.Connection["EventType"]:
        _filter = filter if filter is not strawberry.UNSET else inputs.EventFilter()
        queryset = filters.EventFilter(_filter.to_dict(), models.Event.access_by(info.context.request)).qs
        return utils.paginated_connection(queryset, **_filter.pagination())
