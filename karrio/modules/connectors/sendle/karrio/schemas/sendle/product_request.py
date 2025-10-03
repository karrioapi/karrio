import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ProductRequestType:
    sender_address_line1: typing.Optional[str] = None
    sender_address_line2: typing.Optional[str] = None
    sender_suburb: typing.Optional[str] = None
    sender_postcode: typing.Optional[str] = None
    sender_country: typing.Optional[str] = None
    receiver_address_line1: typing.Optional[str] = None
    receiver_address_line2: typing.Optional[str] = None
    receiver_suburb: typing.Optional[str] = None
    receiver_postcode: typing.Optional[str] = None
    receiver_country: typing.Optional[str] = None
    weight_value: typing.Optional[float] = None
    weight_units: typing.Optional[str] = None
    volume_value: typing.Optional[str] = None
    volume_units: typing.Optional[str] = None
    length_value: typing.Optional[float] = None
    width_value: typing.Optional[float] = None
    height_value: typing.Optional[float] = None
    dimension_units: typing.Optional[str] = None
