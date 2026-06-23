import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AdditionalInformationType:
    code: typing.Optional[str] = None
    stringValue: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CashOnDeliveryType:
    amount: typing.Optional[int] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class InsuranceType:
    value: typing.Optional[int] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TemperatureControlledType:
    type: typing.Optional[str] = None
    min: typing.Optional[int] = None
    max: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class AdditionalServicesType:
    after12Delivery: typing.Optional[bool] = None
    availablePickupTime: typing.Optional[str] = None
    availableDeliveryTime: typing.Optional[str] = None
    cashOnDelivery: typing.Optional[CashOnDeliveryType] = jstruct.JStruct[CashOnDeliveryType]
    dangerousGoods: typing.Optional[bool] = None
    dropOffByConsignor: typing.Optional[bool] = None
    insurance: typing.Optional[InsuranceType] = jstruct.JStruct[InsuranceType]
    preAdvice: typing.Optional[bool] = None
    sideLoadingPickup: typing.Optional[bool] = None
    sideUnloadingDelivery: typing.Optional[bool] = None
    temperatureControlled: typing.Optional[TemperatureControlledType] = jstruct.JStruct[TemperatureControlledType]
    tailLiftLoading: typing.Optional[bool] = None
    tailLiftUnloading: typing.Optional[bool] = None
    timeSlotBookingPickup: typing.Optional[bool] = None
    timeSlotBookingDelivery: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class AddressType:
    street: typing.Optional[str] = None
    additionalAddressInfo: typing.Optional[str] = None
    cityName: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PartyType:
    id: typing.Optional[str] = None
    type: typing.Optional[str] = None
    name: typing.Optional[str] = None
    vat: typing.Optional[str] = None
    vatEoriSocialSecurityNumber: typing.Optional[str] = None
    contactName: typing.Optional[str] = None
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    phone: typing.Optional[str] = None
    email: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PayerCodeType:
    code: typing.Optional[str] = None
    location: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DangerousGoodsType:
    dgmId: typing.Optional[int] = None
    properShippingName: typing.Optional[str] = None
    adrClass: typing.Optional[str] = None
    unNumber: typing.Optional[int] = None
    flashpointValue: typing.Optional[int] = None
    packageGroup: typing.Optional[str] = None
    tunnelCode: typing.Optional[str] = None
    grossWeight: typing.Optional[int] = None
    quantityMeasurementUnitQualifier: typing.Optional[str] = None
    quantityMeasurementValue: typing.Optional[int] = None
    numberOfPieces: typing.Optional[int] = None
    packageType: typing.Optional[str] = None
    officialNameTechDescription: typing.Optional[str] = None
    marinePollutant: typing.Optional[bool] = None
    marinePollutantName: typing.Optional[str] = None
    exceptedQuantity: typing.Optional[bool] = None
    limitedQuantity: typing.Optional[bool] = None
    emptyContainer: typing.Optional[bool] = None
    environmentHazardous: typing.Optional[bool] = None
    waste: typing.Optional[bool] = None
    netExplosiveMass: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PieceType:
    id: typing.Optional[typing.List[str]] = None
    goodsType: typing.Optional[str] = None
    packageType: typing.Optional[str] = None
    marksAndNumbers: typing.Optional[str] = None
    numberOfPieces: typing.Optional[int] = None
    weight: typing.Optional[int] = None
    volume: typing.Optional[float] = None
    loadingMeters: typing.Optional[int] = None
    palletPlaces: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    length: typing.Optional[int] = None
    stackable: typing.Optional[bool] = None
    dangerousGoods: typing.Optional[DangerousGoodsType] = jstruct.JStruct[DangerousGoodsType]


@attr.s(auto_attribs=True)
class ReferenceType:
    qualifier: typing.Optional[str] = None
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingRequestType:
    id: typing.Optional[str] = None
    productCode: typing.Optional[str] = None
    pickupDate: typing.Optional[str] = None
    requestedDeliveryDate: typing.Optional[str] = None
    pickupInstruction: typing.Optional[str] = None
    deliveryInstruction: typing.Optional[str] = None
    totalNumberOfPieces: typing.Optional[int] = None
    totalWeight: typing.Optional[int] = None
    totalVolume: typing.Optional[float] = None
    totalLoadingMeters: typing.Optional[int] = None
    totalPalletPlaces: typing.Optional[int] = None
    goodsDescription: typing.Optional[str] = None
    goodsValue: typing.Optional[int] = None
    goodsValueCurrency: typing.Optional[str] = None
    references: typing.Optional[typing.List[ReferenceType]] = jstruct.JList[ReferenceType]
    payerCode: typing.Optional[PayerCodeType] = jstruct.JStruct[PayerCodeType]
    parties: typing.Optional[typing.List[PartyType]] = jstruct.JList[PartyType]
    additionalServices: typing.Optional[AdditionalServicesType] = jstruct.JStruct[AdditionalServicesType]
    pieces: typing.Optional[typing.List[PieceType]] = jstruct.JList[PieceType]
    additionalInformation: typing.Optional[typing.List[AdditionalInformationType]] = jstruct.JList[AdditionalInformationType]
