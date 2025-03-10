import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ContentType:
    itemDescription: typing.Optional[str] = None
    itemQuantity: typing.Optional[int] = None
    itemValue: typing.Optional[int] = None
    itemTotalValue: typing.Optional[int] = None
    weightUOM: typing.Optional[str] = None
    itemWeight: typing.Optional[float] = None
    itemTotalWeight: typing.Optional[float] = None
    HSTariffNumber: typing.Optional[str] = None
    countryofOrigin: typing.Optional[str] = None
    itemCategory: typing.Optional[str] = None
    itemSubcategory: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomsFormType:
    contentComments: typing.Optional[str] = None
    restrictionType: typing.Optional[str] = None
    restrictionComments: typing.Optional[str] = None
    AESITN: typing.Optional[str] = None
    invoiceNumber: typing.Optional[str] = None
    licenseNumber: typing.Optional[str] = None
    certificateNumber: typing.Optional[str] = None
    customsContentType: typing.Optional[str] = None
    importersReference: typing.Optional[str] = None
    importersContact: typing.Optional[str] = None
    exportersReference: typing.Optional[str] = None
    exportersContact: typing.Optional[str] = None
    contents: typing.Optional[typing.List[ContentType]] = jstruct.JList[ContentType]


@attr.s(auto_attribs=True)
class AddressType:
    streetAddress: typing.Optional[str] = None
    secondaryAddress: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    ZIPCode: typing.Optional[str] = None
    ZIPPlus4: typing.Optional[str] = None
    urbanization: typing.Optional[str] = None
    firstName: typing.Optional[str] = None
    lastName: typing.Optional[str] = None
    firm: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    email: typing.Optional[str] = None
    ignoreBadAddress: typing.Optional[bool] = None
    platformUserId: typing.Optional[str] = None
    parcelLockerDelivery: typing.Optional[bool] = None
    holdForPickup: typing.Optional[bool] = None
    facilityId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ImageInfoType:
    imageType: typing.Optional[str] = None
    labelType: typing.Optional[str] = None
    shipInfo: typing.Optional[bool] = None
    receiptOption: typing.Optional[str] = None
    suppressPostage: typing.Optional[bool] = None
    suppressMailDate: typing.Optional[bool] = None
    returnLabel: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class CustomerReferenceType:
    referenceNumber: typing.Optional[str] = None
    printReferenceNumber: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class DestinationEntryFacilityAddressType:
    streetAddress: typing.Optional[str] = None
    secondaryAddress: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    ZIPCode: typing.Optional[str] = None
    ZIPPlus4: typing.Optional[str] = None
    urbanization: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ContainerType:
    containerID: typing.Optional[str] = None
    sortType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OriginalPackageType:
    originalTrackingNumber: typing.Optional[str] = None
    originalConstructCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageOptionsType:
    packageValue: typing.Optional[int] = None
    nonDeliveryOption: typing.Optional[str] = None
    redirectAddress: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    contentType: typing.Optional[str] = None
    generateGXEvent: typing.Optional[bool] = None
    containers: typing.Optional[typing.List[ContainerType]] = jstruct.JList[ContainerType]
    ancillaryServiceEndorsements: typing.Optional[str] = None
    originalPackage: typing.Optional[OriginalPackageType] = jstruct.JStruct[OriginalPackageType]


@attr.s(auto_attribs=True)
class PackageDescriptionType:
    weightUOM: typing.Optional[str] = None
    weight: typing.Optional[int] = None
    dimensionsUOM: typing.Optional[str] = None
    length: typing.Optional[int] = None
    height: typing.Optional[int] = None
    width: typing.Optional[int] = None
    girth: typing.Optional[int] = None
    mailClass: typing.Optional[str] = None
    rateIndicator: typing.Optional[str] = None
    processingCategory: typing.Optional[str] = None
    destinationEntryFacilityType: typing.Optional[str] = None
    destinationEntryFacilityAddress: typing.Optional[DestinationEntryFacilityAddressType] = jstruct.JStruct[DestinationEntryFacilityAddressType]
    packageOptions: typing.Optional[PackageOptionsType] = jstruct.JStruct[PackageOptionsType]
    customerReference: typing.Optional[typing.List[CustomerReferenceType]] = jstruct.JList[CustomerReferenceType]
    extraServices: typing.Optional[typing.List[int]] = None
    mailingDate: typing.Optional[str] = None
    carrierRelease: typing.Optional[bool] = None
    physicalSignatureRequired: typing.Optional[bool] = None
    inductionZIPCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LabelRequestType:
    imageInfo: typing.Optional[ImageInfoType] = jstruct.JStruct[ImageInfoType]
    toAddress: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    fromAddress: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    senderAddress: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    returnAddress: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    packageDescription: typing.Optional[PackageDescriptionType] = jstruct.JStruct[PackageDescriptionType]
    customsForm: typing.Optional[CustomsFormType] = jstruct.JStruct[CustomsFormType]
