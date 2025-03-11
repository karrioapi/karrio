import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class HeaderType:
    MessageVersion: typing.Optional[str] = None
    MessageIdentifier: typing.Optional[str] = None
    CreateTimestamp: typing.Optional[str] = None
    DocumentType: typing.Optional[str] = None
    Environment: typing.Optional[str] = None
    SourceSystemCode: typing.Optional[str] = None
    MessageSender: typing.Optional[str] = None
    MessageReceiver: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BillToPartyType:
    AccountCode: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PhysicalAddressType:
    Suburb: typing.Optional[str] = None
    StateCode: typing.Optional[str] = None
    PostalCode: typing.Optional[int] = None
    CountryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ConsignPartyType:
    PhysicalAddress: typing.Optional[PhysicalAddressType] = jstruct.JStruct[PhysicalAddressType]


@attr.s(auto_attribs=True)
class ExtraServicesAmountType:
    Currency: typing.Optional[str] = None
    Value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentFinancialsType:
    ExtraServicesAmount: typing.Optional[ExtraServicesAmountType] = jstruct.JStruct[ExtraServicesAmountType]


@attr.s(auto_attribs=True)
class ShipmentFlagsType:
    ExtraServiceFlag: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class CommodityType:
    CommodityCode: typing.Optional[str] = None
    CommodityDescription: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DimensionsType:
    Width: typing.Optional[int] = None
    Length: typing.Optional[int] = None
    Height: typing.Optional[int] = None
    Volume: typing.Optional[str] = None
    Weight: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentItemTotalsType:
    ShipmentItemCount: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ShipmentItemType:
    Commodity: typing.Optional[CommodityType] = jstruct.JStruct[CommodityType]
    ShipmentItemTotals: typing.Optional[ShipmentItemTotalsType] = jstruct.JStruct[ShipmentItemTotalsType]
    Dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]


@attr.s(auto_attribs=True)
class ShipmentItemsType:
    ShipmentItem: typing.Optional[typing.List[ShipmentItemType]] = jstruct.JList[ShipmentItemType]


@attr.s(auto_attribs=True)
class ShipmentServiceType:
    ServiceCode: typing.Optional[str] = None
    ShipmentProductCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class SystemFieldsType:
    PickupDateTime: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RequestType:
    BusinessID: typing.Optional[str] = None
    SystemFields: typing.Optional[SystemFieldsType] = jstruct.JStruct[SystemFieldsType]
    ShipmentService: typing.Optional[ShipmentServiceType] = jstruct.JStruct[ShipmentServiceType]
    ShipmentFlags: typing.Optional[ShipmentFlagsType] = jstruct.JStruct[ShipmentFlagsType]
    ShipmentFinancials: typing.Optional[ShipmentFinancialsType] = jstruct.JStruct[ShipmentFinancialsType]
    FreightMode: typing.Optional[str] = None
    BillToParty: typing.Optional[BillToPartyType] = jstruct.JStruct[BillToPartyType]
    ConsignorParty: typing.Optional[ConsignPartyType] = jstruct.JStruct[ConsignPartyType]
    ConsigneeParty: typing.Optional[ConsignPartyType] = jstruct.JStruct[ConsignPartyType]
    ShipmentItems: typing.Optional[ShipmentItemsType] = jstruct.JStruct[ShipmentItemsType]


@attr.s(auto_attribs=True)
class RateEnquiryType:
    Request: typing.Optional[RequestType] = jstruct.JStruct[RequestType]


@attr.s(auto_attribs=True)
class TollMessageType:
    Header: typing.Optional[HeaderType] = jstruct.JStruct[HeaderType]
    RateEnquiry: typing.Optional[RateEnquiryType] = jstruct.JStruct[RateEnquiryType]


@attr.s(auto_attribs=True)
class RateRequestType:
    TollMessage: typing.Optional[TollMessageType] = jstruct.JStruct[TollMessageType]
