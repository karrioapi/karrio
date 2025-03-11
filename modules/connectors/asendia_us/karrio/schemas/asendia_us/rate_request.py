import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class RateRequestType:
    accountNumber: typing.Optional[str] = None
    subAccountNumber: typing.Optional[str] = None
    processingLocation: typing.Optional[str] = None
    recipientPostalCode: typing.Optional[str] = None
    recipientCountryCode: typing.Optional[str] = None
    totalPackageWeight: typing.Optional[float] = None
    weightUnit: typing.Optional[str] = None
    dimLength: typing.Optional[float] = None
    dimWidth: typing.Optional[float] = None
    dimHeight: typing.Optional[float] = None
    dimUnit: typing.Optional[str] = None
    productCode: typing.Optional[str] = None
