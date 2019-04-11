"""XPO logistics LTL rate quote request Datatype definition module."""

import attr
from typing import List, Union, Optional
from jstruct import JList, JStruct


@attr.s(auto_attribs=True)
class chargeAmt:
    amt: Optional[float] = None
    currencyCd: Optional[str] = None


@attr.s(auto_attribs=True)
class accessorials:
    accessorialCd: Optional[str] = None
    quantity: Optional[int] = None
    quantityUom: Optional[str] = None
    accessorialDesc: Optional[str] = None
    chargeAmt: chargeAmt = JStruct[chargeAmt]


@attr.s(auto_attribs=True)
class address:
    addressTypeCd: Optional[str] = None
    name: Optional[str] = None
    careOfName: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    postOfficeBox: Optional[str] = None
    cityName: Optional[str] = None
    stateCd: Optional[str] = None
    countryCd: Optional[str] = None
    postalCd: Optional[str] = None
    usZip4: Optional[str] = None


@attr.s(auto_attribs=True)
class weight:
    weight: Optional[float] = None
    weightUom: Optional[str] = None


@attr.s(auto_attribs=True)
class volume:
    volume: Optional[float] = None
    volumeUOM: Optional[str] = None


@attr.s(auto_attribs=True)
class dimensions:
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    dimensionsUom: Optional[str] = None


@attr.s(auto_attribs=True)
class commodity:
    pieceCnt: Optional[int] = None
    packageCode: Optional[str] = None
    grossWeight: weight = JStruct[weight]
    tareWeight: weight = JStruct[weight]
    volume: volume = JStruct[volume]
    desc: Optional[str] = None
    nmfcClass: Optional[str] = None
    nmfcItemCd: Optional[str] = None
    hazmatInd: Optional[bool] = None
    dimensions: dimensions = JStruct[dimensions]


@attr.s(auto_attribs=True)
class bill2Party:
    acctInstId: Optional[str] = None
    acctMadCd: Optional[str] = None
    address: address = JStruct[address]


@attr.s(auto_attribs=True)
class consignee:
    acctInstId: Optional[str] = None
    acctMadCd: Optional[str] = None
    address: address = JStruct[address]


@attr.s(auto_attribs=True)
class shipper:
    acctInstId: Optional[str] = None
    acctMadCd: Optional[str] = None
    address: address = JStruct[address]


@attr.s(auto_attribs=True)
class shipmentInfo:
    accessorials: accessorials = JStruct[accessorials]
    bill2Party: bill2Party = JStruct[bill2Party]
    commodity: commodity = JStruct[commodity]
    consignee: consignee = JStruct[consignee]
    freezableInd: Optional[bool]
    hazmatInd: Optional[bool]
    linealFt: Optional[float]
    paymentTermCd: Optional[str]
    shipmentDate: Optional[str]
    shipmentVolume: volume = JStruct[volume]
    shipper: shipper = JStruct[shipper]
    PalletCnt: Optional[int] = None
    comment: Optional[str]
    discountLevel: Optional[float]
