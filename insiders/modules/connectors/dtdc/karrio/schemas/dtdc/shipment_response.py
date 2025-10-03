import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PieceType:
    reference_number: typing.Optional[str] = None
    product_code: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DatumType:
    success: typing.Optional[bool] = None
    reference_number: typing.Optional[str] = None
    courier_partner: typing.Optional[str] = None
    courier_account: typing.Optional[str] = None
    courier_partner_reference_number: typing.Optional[str] = None
    chargeable_weight: typing.Optional[float] = None
    self_pickup_enabled: typing.Optional[bool] = None
    customer_reference_number: typing.Optional[str] = None
    pieces: typing.Optional[typing.List[PieceType]] = jstruct.JList[PieceType]
    bar_code_data: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    status: typing.Optional[str] = None
    data: typing.Optional[typing.List[DatumType]] = jstruct.JList[DatumType]
