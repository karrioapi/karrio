import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class MetadataType:
    pass


@attr.s(auto_attribs=True)
class CancelResponseType:
    order_id: typing.Optional[str] = None
    state: typing.Optional[str] = None
    order_url: typing.Optional[str] = None
    sendle_reference: typing.Optional[str] = None
    tracking_url: typing.Optional[str] = None
    customer_reference: typing.Optional[str] = None
    metadata: typing.Optional[MetadataType] = jstruct.JStruct[MetadataType]
    cancelled_at: typing.Optional[str] = None
    cancellation_message: typing.Optional[str] = None
