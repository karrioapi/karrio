import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AccountType:
    typeCode: typing.Optional[str] = None
    number: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AdditionalChargeType:
    value: typing.Optional[float] = None
    caption: typing.Optional[str] = None
    typeCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DeclarationNoteType:
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ExporterType:
    id: typing.Optional[str] = None
    code: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class InvoiceType:
    number: typing.Optional[str] = None
    date: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class SpecialInstructionType:
    value: typing.Optional[str] = None
    typeCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class QuantityType:
    value: typing.Optional[int] = None
    unitOfMeasurement: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class WeightType:
    netValue: typing.Optional[float] = None
    grossValue: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class LineItemType:
    number: typing.Optional[int] = None
    description: typing.Optional[str] = None
    price: typing.Optional[int] = None
    quantity: typing.Optional[QuantityType] = jstruct.JStruct[QuantityType]
    commodityCodes: typing.Optional[typing.List[SpecialInstructionType]] = jstruct.JList[SpecialInstructionType]
    exportReasonType: typing.Optional[str] = None
    manufacturerCountry: typing.Optional[str] = None
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]


@attr.s(auto_attribs=True)
class ExportDeclarationType:
    lineItems: typing.Optional[typing.List[LineItemType]] = jstruct.JList[LineItemType]
    invoice: typing.Optional[InvoiceType] = jstruct.JStruct[InvoiceType]
    remarks: typing.Optional[typing.List[DeclarationNoteType]] = jstruct.JList[DeclarationNoteType]
    additionalCharges: typing.Optional[typing.List[AdditionalChargeType]] = jstruct.JList[AdditionalChargeType]
    destinationPortName: typing.Optional[str] = None
    placeOfIncoterm: typing.Optional[str] = None
    payerVATNumber: typing.Optional[str] = None
    recipientReference: typing.Optional[str] = None
    exporter: typing.Optional[ExporterType] = jstruct.JStruct[ExporterType]
    packageMarks: typing.Optional[str] = None
    declarationNotes: typing.Optional[typing.List[DeclarationNoteType]] = jstruct.JList[DeclarationNoteType]
    exportReference: typing.Optional[str] = None
    exportReason: typing.Optional[str] = None
    exportReasonType: typing.Optional[str] = None
    licenses: typing.Optional[typing.List[SpecialInstructionType]] = jstruct.JList[SpecialInstructionType]
    shipmentType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DimensionsType:
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PackageType:
    typeCode: typing.Optional[str] = None
    weight: typing.Optional[float] = None
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    customerReferences: typing.Optional[typing.List[SpecialInstructionType]] = jstruct.JList[SpecialInstructionType]
    description: typing.Optional[str] = None
    labelDescription: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ContentType:
    packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
    isCustomsDeclarable: typing.Optional[bool] = None
    declaredValue: typing.Optional[float] = None
    declaredValueCurrency: typing.Optional[str] = None
    exportDeclaration: typing.Optional[ExportDeclarationType] = jstruct.JStruct[ExportDeclarationType]
    description: typing.Optional[str] = None
    USFilingTypeValue: typing.Optional[str] = None
    incoterm: typing.Optional[str] = None
    unitOfMeasurement: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ContactInformationType:
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    mobilePhone: typing.Optional[str] = None
    companyName: typing.Optional[str] = None
    fullName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PostalAddressType:
    postalCode: typing.Optional[int] = None
    cityName: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None
    provinceCode: typing.Optional[str] = None
    addressLine1: typing.Optional[str] = None
    addressLine2: typing.Optional[str] = None
    addressLine3: typing.Optional[str] = None
    countyName: typing.Optional[str] = None
    provinceName: typing.Optional[str] = None
    countryName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DetailsType:
    postalAddress: typing.Optional[PostalAddressType] = jstruct.JStruct[PostalAddressType]
    contactInformation: typing.Optional[ContactInformationType] = jstruct.JStruct[ContactInformationType]
    typeCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomerDetailsType:
    shipperDetails: typing.Optional[DetailsType] = jstruct.JStruct[DetailsType]
    receiverDetails: typing.Optional[DetailsType] = jstruct.JStruct[DetailsType]
    buyerDetails: typing.Optional[DetailsType] = jstruct.JStruct[DetailsType]
    importerDetails: typing.Optional[DetailsType] = jstruct.JStruct[DetailsType]
    exporterDetails: typing.Optional[DetailsType] = jstruct.JStruct[DetailsType]


@attr.s(auto_attribs=True)
class DocumentImageType:
    typeCode: typing.Optional[str] = None
    imageFormat: typing.Optional[str] = None
    content: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EstimatedDeliveryDateType:
    isRequested: typing.Optional[bool] = None
    typeCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OnDemandDeliveryType:
    deliveryOption: typing.Optional[str] = None
    location: typing.Optional[str] = None
    specialInstructions: typing.Optional[str] = None
    gateCode: typing.Optional[int] = None
    whereToLeave: typing.Optional[str] = None
    neighbourName: typing.Optional[str] = None
    neighbourHouseNumber: typing.Optional[int] = None
    authorizerName: typing.Optional[str] = None
    servicePointId: typing.Optional[str] = None
    requestedDeliveryDate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomerBarcodeType:
    content: typing.Optional[str] = None
    textBelowBarcode: typing.Optional[str] = None
    symbologyCode: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class CustomerLogoType:
    fileFormat: typing.Optional[str] = None
    content: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ImageOptionType:
    typeCode: typing.Optional[str] = None
    templateName: typing.Optional[str] = None
    isRequested: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class OutputImagePropertiesType:
    printerDPI: typing.Optional[int] = None
    customerBarcodes: typing.Optional[typing.List[CustomerBarcodeType]] = jstruct.JList[CustomerBarcodeType]
    customerLogos: typing.Optional[typing.List[CustomerLogoType]] = jstruct.JList[CustomerLogoType]
    encodingFormat: typing.Optional[str] = None
    imageOptions: typing.Optional[typing.List[ImageOptionType]] = jstruct.JList[ImageOptionType]


@attr.s(auto_attribs=True)
class ParentShipmentType:
    productCode: typing.Optional[str] = None
    packagesCount: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PickupType:
    isRequested: typing.Optional[bool] = None
    closeTime: typing.Optional[str] = None
    location: typing.Optional[str] = None
    specialInstructions: typing.Optional[typing.List[SpecialInstructionType]] = jstruct.JList[SpecialInstructionType]
    pickupDetails: typing.Optional[DetailsType] = jstruct.JStruct[DetailsType]


@attr.s(auto_attribs=True)
class PrepaidChargeType:
    typeCode: typing.Optional[str] = None
    currency: typing.Optional[str] = None
    value: typing.Optional[float] = None
    method: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentNotificationType:
    typeCode: typing.Optional[str] = None
    receiverId: typing.Optional[str] = None
    languageCode: typing.Optional[str] = None
    languageCountryCode: typing.Optional[str] = None
    bespokeMessage: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ValueAddedServiceType:
    serviceCode: typing.Optional[str] = None
    value: typing.Optional[float] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    plannedShippingDateAndTime: typing.Optional[str] = None
    pickup: typing.Optional[PickupType] = jstruct.JStruct[PickupType]
    productCode: typing.Optional[str] = None
    localProductCode: typing.Optional[str] = None
    getRateEstimates: typing.Optional[bool] = None
    accounts: typing.Optional[typing.List[AccountType]] = jstruct.JList[AccountType]
    valueAddedServices: typing.Optional[typing.List[ValueAddedServiceType]] = jstruct.JList[ValueAddedServiceType]
    outputImageProperties: typing.Optional[OutputImagePropertiesType] = jstruct.JStruct[OutputImagePropertiesType]
    customerDetails: typing.Optional[CustomerDetailsType] = jstruct.JStruct[CustomerDetailsType]
    content: typing.Optional[ContentType] = jstruct.JStruct[ContentType]
    documentImages: typing.Optional[typing.List[DocumentImageType]] = jstruct.JList[DocumentImageType]
    onDemandDelivery: typing.Optional[OnDemandDeliveryType] = jstruct.JStruct[OnDemandDeliveryType]
    requestOndemandDeliveryURL: typing.Optional[bool] = None
    shipmentNotification: typing.Optional[typing.List[ShipmentNotificationType]] = jstruct.JList[ShipmentNotificationType]
    prepaidCharges: typing.Optional[typing.List[PrepaidChargeType]] = jstruct.JList[PrepaidChargeType]
    getTransliteratedResponse: typing.Optional[bool] = None
    estimatedDeliveryDate: typing.Optional[EstimatedDeliveryDateType] = jstruct.JStruct[EstimatedDeliveryDateType]
    getAdditionalInformation: typing.Optional[typing.List[EstimatedDeliveryDateType]] = jstruct.JList[EstimatedDeliveryDateType]
    parentShipment: typing.Optional[ParentShipmentType] = jstruct.JStruct[ParentShipmentType]
