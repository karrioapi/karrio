from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class Field:
    key: Optional[str] = None
    value: Optional[str] = None


@s(auto_attribs=True)
class Fields:
    field: List[Field] = JList[Field]
    customField: List[Field] = JList[Field]


@s(auto_attribs=True)
class Address:
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
class Addressee:
    addresseeParcelRef: Optional[str] = None
    codeBarForReference: Optional[bool] = None
    serviceInfo: Optional[str] = None
    promotionCode: Optional[str] = None
    address: Optional[Address] = JStruct[Address]


@s(auto_attribs=True)
class Article:
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
class Category:
    value: Optional[int] = None


@s(auto_attribs=True)
class Original:
    originalIdent: Optional[str] = None
    originalInvoiceNumber: Optional[str] = None
    originalInvoiceDate: Optional[str] = None
    originalParcelNumber: Optional[str] = None


@s(auto_attribs=True)
class Contents:
    article: List[Article] = JList[Article]
    category: Optional[Category] = JStruct[Category]
    original: List[Original] = JList[Original]
    explanations: Optional[str] = None


@s(auto_attribs=True)
class CustomsDeclarations:
    includeCustomsDeclarations: Optional[bool] = None
    numberOfCopies: Optional[int] = None
    contents: Optional[Contents] = JStruct[Contents]
    importersReference: Optional[str] = None
    importersContact: Optional[str] = None
    officeOrigin: Optional[str] = None
    comments: Optional[str] = None
    description: Optional[str] = None
    invoiceNumber: Optional[str] = None
    licenceNumber: Optional[str] = None
    certificatNumber: Optional[str] = None
    importerAddress: Optional[Address] = JStruct[Address]


@s(auto_attribs=True)
class Features:
    printTrackingBarcode: Optional[bool] = None


@s(auto_attribs=True)
class Parcel:
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
class Sender:
    senderParcelRef: Optional[str] = None
    address: Optional[Address] = JStruct[Address]


@s(auto_attribs=True)
class Service:
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
class UploadDocument:
    documentContent: List[str] = []


@s(auto_attribs=True)
class Letter:
    service: Optional[Service] = JStruct[Service]
    parcel: Optional[Parcel] = JStruct[Parcel]
    customsDeclarations: Optional[CustomsDeclarations] = JStruct[CustomsDeclarations]
    sender: Optional[Sender] = JStruct[Sender]
    addressee: Optional[Addressee] = JStruct[Addressee]
    codSenderAddress: Optional[Address] = JStruct[Address]
    uploadDocument: Optional[UploadDocument] = JStruct[UploadDocument]
    features: Optional[Features] = JStruct[Features]


@s(auto_attribs=True)
class OutputFormat:
    x: Optional[int] = None
    y: Optional[int] = None
    outputPrintingType: Optional[str] = None
    dematerialized: Optional[bool] = None
    returnType: Optional[str] = None
    printCODDocument: Optional[bool] = None


@s(auto_attribs=True)
class LabelRequest:
    contractNumber: Optional[str] = None
    password: Optional[str] = None
    outputFormat: Optional[OutputFormat] = JStruct[OutputFormat]
    letter: Optional[Letter] = JStruct[Letter]
    fields: Optional[Fields] = JStruct[Fields]
