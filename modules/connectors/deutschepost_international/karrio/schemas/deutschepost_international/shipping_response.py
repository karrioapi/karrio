from attr import s
from typing import Optional, Any, List
from jstruct import JStruct


@s(auto_attribs=True)
class ItemsType:
    id: Optional[int] = None
    barcode: Optional[str] = None
    product: Optional[str] = None
    serviceLevel: Optional[str] = None
    custRef: Optional[str] = None
    recipient: Optional[str] = None
    recipientPhone: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    addressLine3: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    destinationCountry: Optional[str] = None
    shipmentGrossWeight: Optional[int] = None
    senderTaxID: Optional[str] = None
    importerTaxId: Optional[str] = None
    returnItemWanted: Optional[bool] = None
    contents: List[Any] = []


@s(auto_attribs=True)
class ShipmentsType:
    awb: Optional[int] = None
    items: Optional[ItemsType] = JStruct[ItemsType]


@s(auto_attribs=True)
class ShippingResponseType:
    customerEkp: Optional[str] = None
    orderId: Optional[int] = None
    orderStatus: Optional[str] = None
    shipments: Optional[ShipmentsType] = JStruct[ShipmentsType]
