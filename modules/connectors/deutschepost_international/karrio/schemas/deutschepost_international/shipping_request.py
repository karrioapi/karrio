from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class ContentType:
    contentPieceHsCode: Optional[int] = None
    contentPieceDescription: Optional[str] = None
    contentPieceValue: Optional[str] = None
    contentPieceNetweight: Optional[int] = None
    contentPieceOrigin: Optional[str] = None
    contentPieceAmount: Optional[int] = None
    contentPieceIndexNumber: Optional[int] = None


@s(auto_attribs=True)
class ItemType:
    product: Optional[str] = None
    serviceLevel: Optional[str] = None
    recipient: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    addressLine3: Optional[str] = None
    postalCode: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    destinationCountry: Optional[str] = None
    custRef: Optional[str] = None
    recipientPhone: Optional[str] = None
    recipientFax: Optional[str] = None
    recipientEmail: Optional[str] = None
    senderTaxId: Optional[str] = None
    importerTaxId: Optional[str] = None
    shipmentAmount: Optional[int] = None
    shipmentCurrency: Optional[str] = None
    shipmentGrossWeight: Optional[int] = None
    returnItemWanted: Optional[bool] = None
    shipmentNaturetype: Optional[str] = None
    contents: List[ContentType] = JList[ContentType]
    custRef2: Optional[str] = None
    custRef3: Optional[str] = None


@s(auto_attribs=True)
class PaperworkType:
    contactName: Optional[str] = None
    awbCopyCount: Optional[int] = None
    jobReference: Optional[str] = None
    pickupType: Optional[str] = None
    telephoneNumber: Optional[str] = None


@s(auto_attribs=True)
class ShippingRequestType:
    customerEkp: Optional[str] = None
    orderStatus: Optional[str] = None
    paperwork: Optional[PaperworkType] = JStruct[PaperworkType]
    items: List[ItemType] = JList[ItemType]
