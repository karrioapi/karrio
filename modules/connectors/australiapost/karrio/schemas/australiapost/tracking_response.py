import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class EventType:
    location: typing.Optional[str] = None
    description: typing.Optional[str] = None
    date: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ConsignmentType:
    events: typing.Optional[typing.List[EventType]] = jstruct.JList[EventType]
    status: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorType:
    code: typing.Optional[str] = None
    name: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ItemType:
    article_id: typing.Optional[str] = None
    product_type: typing.Optional[str] = None
    events: typing.Optional[typing.List[EventType]] = jstruct.JList[EventType]
    status: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackableItemType:
    article_id: typing.Optional[str] = None
    product_type: typing.Optional[str] = None
    events: typing.Optional[typing.List[EventType]] = jstruct.JList[EventType]
    status: typing.Optional[str] = None
    consignment_id: typing.Optional[str] = None
    number_of_items: typing.Optional[int] = None
    items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]


@attr.s(auto_attribs=True)
class TrackingResultType:
    tracking_id: typing.Optional[str] = None
    errors: typing.Optional[typing.List[ErrorType]] = jstruct.JList[ErrorType]
    status: typing.Optional[str] = None
    trackable_items: typing.Optional[typing.List[TrackableItemType]] = jstruct.JList[TrackableItemType]
    consignment: typing.Optional[typing.List[ConsignmentType]] = jstruct.JList[ConsignmentType]


@attr.s(auto_attribs=True)
class TrackingResponseType:
    tracking_results: typing.Optional[typing.List[TrackingResultType]] = jstruct.JList[TrackingResultType]
