import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class CancelRequestType:
    accountNumber: typing.Optional[str] = None
    subAccountNumber: typing.Optional[str] = None
    packageID: typing.Optional[str] = None
