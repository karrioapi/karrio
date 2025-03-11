import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class OrderCreateResponseType:
    id: typing.Optional[int] = None
    barcode: typing.Optional[str] = None
    revertOrderId: typing.Optional[int] = None
    revertBarcode: typing.Optional[str] = None
    postalcode: typing.Any = None
