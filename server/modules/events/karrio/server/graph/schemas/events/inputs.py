import datetime
import typing
import strawberry

import karrio.server.graph.utils as utils
import karrio.server.events.serializers as serializers

EventStatusEnum: typing.Any = strawberry.enum(serializers.EventTypes)


@strawberry.input
class CreateWebhookMutationInput(utils.BaseInput):
    url: str
    enabled_events: typing.List[EventStatusEnum]
    description: typing.Optional[str] = None
    disabled: typing.Optional[bool] = False
    test_mode: typing.Optional[bool] = False


@strawberry.input
class WebhookFilter(utils.Paginated):
    url: typing.Optional[str] = strawberry.UNSET
    disabled: typing.Optional[bool] = strawberry.UNSET
    test_mode: typing.Optional[bool] = strawberry.UNSET
    events: typing.List[EventStatusEnum] = strawberry.UNSET
    date_after: typing.Optional[datetime.datetime] = strawberry.UNSET
    date_before: typing.Optional[datetime.datetime] = strawberry.UNSET


@strawberry.input
class UpdateWebhookMutationInput(utils.BaseInput):
    id: str
    url: typing.Optional[str] = None
    enabled_events: typing.List[EventStatusEnum] = None
    description: typing.Optional[str] = None
    disabled: typing.Optional[bool] = None
    test_mode: typing.Optional[bool] = None


@strawberry.input
class EventFilter(utils.Paginated):
    entity_id: typing.Optional[str] = strawberry.UNSET
    type: typing.List[EventStatusEnum] = strawberry.UNSET
    date_after: typing.Optional[datetime.datetime] = strawberry.UNSET
    date_before: typing.Optional[datetime.datetime] = strawberry.UNSET
