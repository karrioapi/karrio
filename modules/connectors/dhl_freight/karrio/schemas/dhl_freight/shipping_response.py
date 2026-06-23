import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class LicensePlateType:
    licensePlate: typing.Optional[str] = None
    sscc: typing.Optional[str] = None
    pieceId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingResponseType:
    shipmentId: typing.Optional[str] = None
    transportInstructionId: typing.Optional[str] = None
    status: typing.Optional[str] = None
    licensePlates: typing.Optional[typing.List[LicensePlateType]] = jstruct.JList[LicensePlateType]
