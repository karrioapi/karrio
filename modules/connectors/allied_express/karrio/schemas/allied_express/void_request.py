import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class VoidRequestType:
    shipmentno: typing.Optional[int] = None
    postalcode: typing.Optional[int] = None
