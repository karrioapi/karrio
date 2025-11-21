import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class MetadataType:
    voidedAt: typing.Optional[str] = None
    voidedBy: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentCancelResponseType:
    shipmentId: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None
    status: typing.Optional[str] = None
    metadata: typing.Optional[MetadataType] = jstruct.JStruct[MetadataType]
