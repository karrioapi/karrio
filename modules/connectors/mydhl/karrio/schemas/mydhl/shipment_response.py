import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DocumentType:
    imageFormat: typing.Optional[str] = None
    content: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageType:
    referenceNumber: typing.Optional[int] = None
    trackingNumber: typing.Optional[str] = None
    trackingUrl: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    shipmentTrackingNumber: typing.Optional[int] = None
    trackingUrl: typing.Optional[str] = None
    packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
    documents: typing.Optional[typing.List[DocumentType]] = jstruct.JList[DocumentType]
