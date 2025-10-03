import typing
import datetime
import strawberry

import karrio.lib as lib
import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.base.types as base
import karrio.server.graph.schemas.events.inputs as inputs
import karrio.server.events.models as models
import karrio.server.events.filters as filters


@strawberry.type
class WebhookType:
    object_type: str
    id: str
    url: typing.Optional[str]
    secret: typing.Optional[str]
    disabled: typing.Optional[bool]
    test_mode: typing.Optional[bool]
    description: typing.Optional[str]
    enabled_events: typing.List[inputs.EventStatusEnum]
    last_event_at: typing.Optional[datetime.datetime]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]
    created_by: typing.Optional[base.UserType]

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["WebhookType"]:
        return models.Webhook.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.WebhookFilter] = strawberry.UNSET,
    ) -> utils.Connection["WebhookType"]:
        _filter = filter if filter is not strawberry.UNSET else inputs.WebhookFilter()
        queryset = filters.WebhookFilter(
            _filter.to_dict(), models.Webhook.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class EventType:
    object_type: str
    id: str
    test_mode: typing.Optional[bool]
    pending_webhooks: typing.Optional[int]
    type: typing.Optional[inputs.EventStatusEnum]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]
    created_by: typing.Optional[base.UserType]

    @strawberry.field
    def data(self: models.Event) -> typing.Optional[utils.JSON]:
        try:
            return lib.to_dict(self.data)
        except:
            return self.data

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["EventType"]:
        return models.Event.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.EventFilter] = strawberry.UNSET,
    ) -> utils.Connection["EventType"]:
        _filter = filter if filter is not strawberry.UNSET else inputs.EventFilter()
        queryset = filters.EventFilter(
            _filter.to_dict(), models.Event.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())
