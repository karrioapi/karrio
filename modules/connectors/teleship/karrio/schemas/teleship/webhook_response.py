import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class MetadataType:
    shopId: typing.Optional[str] = None
    environment: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class WebhookResponseType:
    id: typing.Optional[str] = None
    url: typing.Optional[str] = None
    description: typing.Optional[str] = None
    enabledEvents: typing.Optional[typing.List[str]] = None
    secret: typing.Optional[str] = None
    enabled: typing.Optional[bool] = None
    metadata: typing.Optional[MetadataType] = jstruct.JStruct[MetadataType]
