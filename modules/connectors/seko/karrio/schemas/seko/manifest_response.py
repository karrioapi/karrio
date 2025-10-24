import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class OutboundManifestType:
    ManifestNumber: typing.Optional[str] = None
    ManifestedConnotes: typing.Optional[typing.List[str]] = None
    ManifestContent: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ManifestResponseType:
    OutboundManifest: typing.Optional[typing.List[OutboundManifestType]] = jstruct.JList[OutboundManifestType]
    InboundManifest: typing.Optional[typing.List[typing.Any]] = None
    Error: typing.Optional[typing.List[typing.Any]] = None
    StatusCode: typing.Optional[int] = None
    UnManifestedConnotes: typing.Optional[typing.List[typing.Any]] = None
