from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class HeaderType:
    MessageVersion: Optional[str] = None
    MessageIdentifier: Optional[str] = None
    CreateTimestamp: Optional[str] = None
    DocumentType: Optional[str] = None
    Environment: Optional[str] = None
    SourceSystemCode: Optional[str] = None
    MessageSender: Optional[str] = None
    MessageReceiver: Optional[str] = None


@s(auto_attribs=True)
class BillToPartyType:
    AccountCode: Optional[int] = None


@s(auto_attribs=True)
class PhysicalAddressType:
    Suburb: Optional[str] = None
    StateCode: Optional[str] = None
    PostalCode: Optional[int] = None
    CountryCode: Optional[str] = None


@s(auto_attribs=True)
class ConsignPartyType:
    PhysicalAddress: Optional[PhysicalAddressType] = JStruct[PhysicalAddressType]


@s(auto_attribs=True)
class ExtraServicesAmountType:
    Currency: Optional[str] = None
    Value: Optional[float] = None


@s(auto_attribs=True)
class ShipmentFinancialsType:
    ExtraServicesAmount: Optional[ExtraServicesAmountType] = JStruct[ExtraServicesAmountType]


@s(auto_attribs=True)
class ShipmentFlagsType:
    ExtraServiceFlag: Optional[bool] = None


@s(auto_attribs=True)
class CommodityType:
    CommodityCode: Optional[str] = None
    CommodityDescription: Optional[str] = None


@s(auto_attribs=True)
class DimensionsType:
    Width: Optional[int] = None
    Length: Optional[int] = None
    Height: Optional[int] = None
    Volume: Optional[float] = None
    Weight: Optional[float] = None


@s(auto_attribs=True)
class ShipmentItemTotalsType:
    ShipmentItemCount: Optional[int] = None


@s(auto_attribs=True)
class ShipmentItemType:
    Commodity: Optional[CommodityType] = JStruct[CommodityType]
    ShipmentItemTotals: Optional[ShipmentItemTotalsType] = JStruct[ShipmentItemTotalsType]
    Dimensions: Optional[DimensionsType] = JStruct[DimensionsType]


@s(auto_attribs=True)
class ShipmentItemsType:
    ShipmentItem: List[ShipmentItemType] = JList[ShipmentItemType]


@s(auto_attribs=True)
class ShipmentServiceType:
    ServiceCode: Optional[str] = None
    ShipmentProductCode: Optional[str] = None


@s(auto_attribs=True)
class SystemFieldsType:
    PickupDateTime: Optional[str] = None


@s(auto_attribs=True)
class RequestType:
    BusinessID: Optional[str] = None
    SystemFields: Optional[SystemFieldsType] = JStruct[SystemFieldsType]
    ShipmentService: Optional[ShipmentServiceType] = JStruct[ShipmentServiceType]
    ShipmentFlags: Optional[ShipmentFlagsType] = JStruct[ShipmentFlagsType]
    ShipmentFinancials: Optional[ShipmentFinancialsType] = JStruct[ShipmentFinancialsType]
    FreightMode: Optional[str] = None
    BillToParty: Optional[BillToPartyType] = JStruct[BillToPartyType]
    ConsignorParty: Optional[ConsignPartyType] = JStruct[ConsignPartyType]
    ConsigneeParty: Optional[ConsignPartyType] = JStruct[ConsignPartyType]
    ShipmentItems: Optional[ShipmentItemsType] = JStruct[ShipmentItemsType]


@s(auto_attribs=True)
class RateEnquiryType:
    Request: Optional[RequestType] = JStruct[RequestType]


@s(auto_attribs=True)
class TollMessageType:
    Header: Optional[HeaderType] = JStruct[HeaderType]
    RateEnquiry: Optional[RateEnquiryType] = JStruct[RateEnquiryType]


@s(auto_attribs=True)
class RateRequestType:
    TollMessage: Optional[TollMessageType] = JStruct[TollMessageType]
