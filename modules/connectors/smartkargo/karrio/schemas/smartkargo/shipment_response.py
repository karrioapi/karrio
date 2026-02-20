import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DimensionType:
    pieceReference: typing.Optional[str] = None
    pieces: typing.Optional[float] = None
    grossWeight: typing.Optional[float] = None
    height: typing.Optional[float] = None
    width: typing.Optional[float] = None
    length: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class OtherChargeType:
    charge: typing.Optional[float] = None
    name: typing.Any = None


@attr.s(auto_attribs=True)
class ShipmentType:
    issueDate: typing.Optional[str] = None
    siteId: typing.Optional[str] = None
    headerReference: typing.Optional[str] = None
    packageReference: typing.Optional[str] = None
    prefix: typing.Optional[str] = None
    airWaybill: typing.Optional[str] = None
    estimatedDeliveryDate: typing.Optional[str] = None
    commodityType: typing.Optional[str] = None
    serviceType: typing.Optional[str] = None
    origin: typing.Optional[str] = None
    destination: typing.Any = None
    packageDescription: typing.Optional[str] = None
    totalGrossWeight: typing.Optional[float] = None
    totalPackages: typing.Optional[float] = None
    totalPieces: typing.Optional[float] = None
    currency: typing.Optional[str] = None
    insuranceRequired: typing.Optional[bool] = None
    declaredValue: typing.Optional[float] = None
    specialHandlingType: typing.Optional[str] = None
    deliveryRequestTime: typing.Optional[str] = None
    pickupRequestTime: typing.Optional[str] = None
    expectedSLAInHours: typing.Any = None
    paymentMode: typing.Optional[str] = None
    grossVolumeUnitMeasure: typing.Optional[str] = None
    grossWeightUnitMeasure: typing.Optional[str] = None
    additionalInfo01: typing.Any = None
    additionalInfo02: typing.Any = None
    additionalInfo03: typing.Any = None
    additionalInfo04: typing.Any = None
    status: typing.Optional[str] = None
    createdOn: typing.Optional[str] = None
    labelUrl: typing.Optional[str] = None
    shippingFee: typing.Optional[float] = None
    insurance: typing.Optional[float] = None
    totalCharges: typing.Optional[float] = None
    total: typing.Optional[float] = None
    totalTax: typing.Optional[float] = None
    otherCharges: typing.Optional[typing.List[OtherChargeType]] = jstruct.JList[OtherChargeType]
    validations: typing.Optional[typing.List[typing.Any]] = None
    dimensions: typing.Optional[typing.List[DimensionType]] = jstruct.JList[DimensionType]
    participants: typing.Optional[typing.List[typing.Dict[str, typing.Optional[str]]]] = None


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    exchangeId: typing.Optional[str] = None
    fileIdentifier: typing.Any = None
    siteId: typing.Optional[str] = None
    inputType: typing.Optional[str] = None
    status: typing.Optional[str] = None
    valid: typing.Optional[str] = None
    createdOn: typing.Optional[str] = None
    shipments: typing.Optional[typing.List[ShipmentType]] = jstruct.JList[ShipmentType]
    validations: typing.Optional[typing.List[typing.Any]] = None
