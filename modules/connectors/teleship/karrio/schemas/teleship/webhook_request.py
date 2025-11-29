import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class MetadataType:
    shopId: typing.Optional[str] = None
    environment: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class WebhookRequestType:
    url: typing.Optional[str] = None
    description: typing.Optional[str] = None
    enabled: typing.Optional[bool] = None
    enabledEvents: typing.Optional[typing.List[str]] = None
    metadata: typing.Optional[MetadataType] = jstruct.JStruct[MetadataType]
