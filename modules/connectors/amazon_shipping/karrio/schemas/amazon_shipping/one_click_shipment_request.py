import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ChannelDetails:
    channelType: typing.Optional[str] = None
    amazonOrderDetails: typing.Any = None
    amazonShipmentDetails: typing.Any = None


@attr.s(auto_attribs=True)
class Size:
    length: typing.Optional[float] = None
    width: typing.Optional[float] = None
    unit: typing.Optional[str] = None
    height: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class LabelSpecifications:
    format: typing.Optional[str] = None
    size: typing.Optional[Size] = jstruct.JStruct[Size]
    dpi: typing.Optional[int] = None
    pageLayout: typing.Optional[str] = None
    needFileJoining: typing.Optional[bool] = None
    requestedDocumentTypes: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class InsuredValue:
    value: typing.Optional[float] = None
    unit: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Package:
    dimensions: typing.Optional[Size] = jstruct.JStruct[Size]
    weight: typing.Optional[InsuredValue] = jstruct.JStruct[InsuredValue]
    insuredValue: typing.Optional[InsuredValue] = jstruct.JStruct[InsuredValue]
    packageClientReferenceId: typing.Optional[str] = None
    items: typing.Any = None


@attr.s(auto_attribs=True)
class ServiceSelection:
    serviceId: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class OneClickShipmentRequest:
    shipFrom: typing.Optional[typing.Dict[str, typing.Optional[str]]] = None
    shipTo: typing.Optional[typing.Dict[str, typing.Optional[str]]] = None
    returnTo: typing.Any = None
    shipDate: typing.Optional[str] = None
    packages: typing.Optional[typing.List[Package]] = jstruct.JList[Package]
    channelDetails: typing.Optional[ChannelDetails] = jstruct.JStruct[ChannelDetails]
    labelSpecifications: typing.Optional[LabelSpecifications] = jstruct.JStruct[LabelSpecifications]
    serviceSelection: typing.Optional[ServiceSelection] = jstruct.JStruct[ServiceSelection]
    shipperInstruction: typing.Any = None
