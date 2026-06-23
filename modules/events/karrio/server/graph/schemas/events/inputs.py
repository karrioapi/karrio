import datetime
import typing

import karrio.server.events.serializers as serializers
import karrio.server.graph.utils as utils
import strawberry

EventStatusEnum: typing.Any = strawberry.enum(serializers.EventTypes)


@strawberry.input
class CreateWebhookMutationInput(utils.BaseInput):
    url: str
    enabled_events: list[EventStatusEnum]
    description: str | None = strawberry.UNSET
    disabled: bool | None = False


@strawberry.input
class WebhookFilter(utils.Paginated):
    url: str | None = strawberry.UNSET
    disabled: bool | None = strawberry.UNSET
    test_mode: bool | None = strawberry.UNSET
    events: list[EventStatusEnum] | None = strawberry.UNSET
    date_after: datetime.datetime | None = strawberry.UNSET
    date_before: datetime.datetime | None = strawberry.UNSET


@strawberry.input
class UpdateWebhookMutationInput(utils.BaseInput):
    id: str
    url: str | None = strawberry.UNSET
    enabled_events: list[EventStatusEnum] = strawberry.UNSET
    description: str | None = strawberry.UNSET
    disabled: bool | None = strawberry.UNSET


@strawberry.input
class EventFilter(utils.Paginated):
    entity_id: str | None = strawberry.UNSET
    type: list[EventStatusEnum] | None = strawberry.UNSET
    date_after: datetime.datetime | None = strawberry.UNSET
    date_before: datetime.datetime | None = strawberry.UNSET
    keyword: str | None = strawberry.UNSET
