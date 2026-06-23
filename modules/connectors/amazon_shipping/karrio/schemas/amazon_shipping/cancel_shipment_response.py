import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Payload:
    pass


@attr.s(auto_attribs=True)
class CancelShipmentResponse:
    payload: typing.Optional[Payload] = jstruct.JStruct[Payload]
