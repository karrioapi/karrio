import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AddressType:
    Name: typing.Optional[str] = None
    Company: typing.Optional[str] = None
    AddressLine1: typing.Optional[str] = None
    AddressLine2: typing.Optional[str] = None
    AddressLine3: typing.Optional[str] = None
    City: typing.Optional[str] = None
    State: typing.Optional[str] = None
    Zip: typing.Optional[str] = None
    Country: typing.Optional[str] = None
    Phone: typing.Optional[str] = None
    Email: typing.Optional[str] = None
    Vat: typing.Optional[str] = None
    PudoLocationId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ConsignorAddressType:
    Name: typing.Optional[str] = None
    Company: typing.Optional[str] = None
    AddressLine1: typing.Optional[str] = None
    AddressLine2: typing.Optional[str] = None
    AddressLine3: typing.Optional[str] = None
    City: typing.Optional[str] = None
    State: typing.Optional[str] = None
    Zip: typing.Optional[str] = None
    Country: typing.Optional[str] = None
    Phone: typing.Optional[str] = None
    Email: typing.Optional[str] = None
    Vat: typing.Optional[str] = None
    Eori: typing.Optional[str] = None
    NlVat: typing.Optional[str] = None
    EuEori: typing.Optional[str] = None
    GbEori: typing.Optional[str] = None
    Ioss: typing.Optional[str] = None
    LocalTaxNumber: typing.Optional[str] = None
    Art23: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ProductType:
    Description: typing.Optional[str] = None
    Sku: typing.Optional[str] = None
    HsCode: typing.Optional[str] = None
    OriginCountry: typing.Optional[str] = None
    ImgUrl: typing.Optional[str] = None
    PurchaseUrl: typing.Optional[str] = None
    Quantity: typing.Optional[str] = None
    Value: typing.Optional[str] = None
    Weight: typing.Optional[str] = None
    DaysForReturn: typing.Optional[str] = None
    NonReturnable: typing.Optional[str] = None
    PreferentialOriginTag: typing.Optional[str] = None
    BondedGoods: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentType:
    LabelFormat: typing.Optional[str] = None
    ShipperReference: typing.Optional[str] = None
    OrderReference: typing.Optional[str] = None
    OrderDate: typing.Optional[str] = None
    DisplayId: typing.Optional[str] = None
    InvoiceNumber: typing.Optional[str] = None
    Service: typing.Optional[str] = None
    Weight: typing.Optional[str] = None
    WeightUnit: typing.Optional[str] = None
    Length: typing.Optional[str] = None
    Width: typing.Optional[str] = None
    Height: typing.Optional[str] = None
    DimUnit: typing.Optional[str] = None
    Value: typing.Optional[str] = None
    ShippingValue: typing.Optional[str] = None
    Currency: typing.Optional[str] = None
    CustomsDuty: typing.Optional[str] = None
    Description: typing.Optional[str] = None
    DeclarationType: typing.Optional[str] = None
    DangerousGoods: typing.Optional[str] = None
    Source: typing.Optional[str] = None
    ExportCarrierName: typing.Optional[str] = None
    ExportAwb: typing.Optional[str] = None
    ConsignorAddress: typing.Optional[ConsignorAddressType] = jstruct.JStruct[ConsignorAddressType]
    ConsigneeAddress: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    ImporterAddress: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    Products: typing.Optional[typing.List[ProductType]] = jstruct.JList[ProductType]


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    Apikey: typing.Optional[str] = None
    Command: typing.Optional[str] = None
    Shipment: typing.Optional[ShipmentType] = jstruct.JStruct[ShipmentType]
