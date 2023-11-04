from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class FieldType:
    key: Optional[str] = None
    value: Optional[str] = None


@s(auto_attribs=True)
class FieldsType:
    field: List[FieldType] = JList[FieldType]
    customField: List[FieldType] = JList[FieldType]


@s(auto_attribs=True)
class AddressType:
    companyName: Optional[str] = None
    lastName: Optional[str] = None
    firstName: Optional[str] = None
    line0: Optional[str] = None
    line1: Optional[str] = None
    line2: Optional[str] = None
    line3: Optional[str] = None
    countryCode: Optional[str] = None
    countryLabel: Optional[str] = None
    city: Optional[str] = None
    zipCode: Optional[str] = None
    phoneNumber: Optional[str] = None
    mobileNumber: Optional[str] = None
    doorCode1: Optional[str] = None
    doorCode2: Optional[str] = None
    intercom: Optional[str] = None
    email: Optional[str] = None
    language: Optional[str] = None
    stateOrProvinceCode: Optional[str] = None


@s(auto_attribs=True)
class AddresseeType:
    addresseeParcelRef: Optional[str] = None
    codeBarForReference: Optional[bool] = None
    serviceInfo: Optional[str] = None
    promotionCode: Optional[str] = None
    address: Optional[AddressType] = JStruct[AddressType]


@s(auto_attribs=True)
class ArticleType:
    description: Optional[str] = None
    quantity: Optional[int] = None
    weight: Optional[int] = None
    value: Optional[int] = None
    hsCode: Optional[str] = None
    originCountry: Optional[str] = None
    originCountryLabel: Optional[str] = None
    currency: Optional[str] = None
    artref: Optional[str] = None
    originalIdent: Optional[str] = None
    vatAmount: Optional[int] = None
    customsFees: Optional[int] = None


@s(auto_attribs=True)
class CategoryType:
    value: Optional[int] = None


@s(auto_attribs=True)
class OriginalType:
    originalIdent: Optional[str] = None
    originalInvoiceNumber: Optional[str] = None
    originalInvoiceDate: Optional[str] = None
    originalParcelNumber: Optional[str] = None


@s(auto_attribs=True)
class ContentsType:
    article: List[ArticleType] = JList[ArticleType]
    category: Optional[CategoryType] = JStruct[CategoryType]
    original: List[OriginalType] = JList[OriginalType]
    explanations: Optional[str] = None


@s(auto_attribs=True)
class CustomsDeclarationsType:
    includeCustomsDeclarations: Optional[bool] = None
    numberOfCopies: Optional[int] = None
    contents: Optional[ContentsType] = JStruct[ContentsType]
    importersReference: Optional[str] = None
    importersContact: Optional[str] = None
    officeOrigin: Optional[str] = None
    comments: Optional[str] = None
    description: Optional[str] = None
    invoiceNumber: Optional[str] = None
    licenceNumber: Optional[str] = None
    certificatNumber: Optional[str] = None
    importerAddress: Optional[AddressType] = JStruct[AddressType]


@s(auto_attribs=True)
class FeaturesType:
    printTrackingBarcode: Optional[bool] = None


@s(auto_attribs=True)
class ParcelType:
    parcelNumber: Optional[str] = None
    insuranceAmount: Optional[int] = None
    insuranceValue: Optional[int] = None
    recommendationLevel: Optional[str] = None
    weight: Optional[int] = None
    nonMachinable: Optional[bool] = None
    returnReceipt: Optional[bool] = None
    instructions: Optional[str] = None
    pickupLocationId: Optional[str] = None
    ftd: Optional[bool] = None
    ddp: Optional[bool] = None
    codamount: Optional[int] = None
    codcurrency: Optional[str] = None
    cod: Optional[bool] = None


@s(auto_attribs=True)
class SenderType:
    senderParcelRef: Optional[str] = None
    address: Optional[AddressType] = JStruct[AddressType]


@s(auto_attribs=True)
class ServiceType:
    productCode: Optional[str] = None
    depositDate: Optional[str] = None
    mailBoxPicking: Optional[bool] = None
    mailBoxPickingDate: Optional[str] = None
    vatCode: Optional[int] = None
    vatPercentage: Optional[int] = None
    vatAmount: Optional[int] = None
    transportationAmount: Optional[int] = None
    totalAmount: Optional[int] = None
    orderNumber: Optional[str] = None
    commercialName: Optional[str] = None
    returnTypeChoice: Optional[int] = None
    reseauPostal: Optional[str] = None


@s(auto_attribs=True)
class UploadDocumentType:
    documentContent: List[str] = []


@s(auto_attribs=True)
class LetterType:
    service: Optional[ServiceType] = JStruct[ServiceType]
    parcel: Optional[ParcelType] = JStruct[ParcelType]
    customsDeclarations: Optional[CustomsDeclarationsType] = JStruct[CustomsDeclarationsType]
    sender: Optional[SenderType] = JStruct[SenderType]
    addressee: Optional[AddresseeType] = JStruct[AddresseeType]
    codSenderAddress: Optional[AddressType] = JStruct[AddressType]
    uploadDocument: Optional[UploadDocumentType] = JStruct[UploadDocumentType]
    features: Optional[FeaturesType] = JStruct[FeaturesType]


@s(auto_attribs=True)
class OutputFormatType:
    x: Optional[int] = None
    y: Optional[int] = None
    outputPrintingType: Optional[str] = None
    dematerialized: Optional[bool] = None
    returnType: Optional[str] = None
    printCODDocument: Optional[bool] = None


@s(auto_attribs=True)
class LabelRequestType:
    contractNumber: Optional[str] = None
    password: Optional[str] = None
    outputFormat: Optional[OutputFormatType] = JStruct[OutputFormatType]
    letter: Optional[LetterType] = JStruct[LetterType]
    fields: Optional[FieldsType] = JStruct[FieldsType]
