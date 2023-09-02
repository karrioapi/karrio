from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AddressType:
    AddressType: Optional[str] = None
    Building: Optional[str] = None
    City: Optional[str] = None
    CompanyName: Optional[str] = None
    CountryCode: Optional[str] = None
    DepartmentName: Optional[str] = None
    District: Optional[str] = None
    FirstName: Optional[str] = None
    Floor: Optional[str] = None
    HouseNumber: Optional[int] = None
    HouseNumberSuffix: Optional[str] = None
    LastName: Optional[str] = None
    Region: Optional[str] = None
    Remark: Optional[str] = None
    Street: Optional[str] = None
    Zipcode: Optional[str] = None


@s(auto_attribs=True)
class CustomerType:
    CustomerCode: Optional[str] = None
    CustomerNumber: Optional[int] = None
    Name: Optional[str] = None


@s(auto_attribs=True)
class DimensionType:
    Height: Optional[int] = None
    Length: Optional[int] = None
    Volume: Optional[int] = None
    Weight: Optional[int] = None
    Width: Optional[int] = None


@s(auto_attribs=True)
class EventType:
    Code: Optional[str] = None
    Description: Optional[str] = None
    DestinationLocationCode: Optional[str] = None
    LocationCode: Optional[int] = None
    RouteCode: Optional[str] = None
    RouteName: Optional[str] = None
    TimeStamp: Optional[str] = None


@s(auto_attribs=True)
class ExpectationType:
    ETAFrom: Optional[str] = None
    ETATo: Optional[str] = None


@s(auto_attribs=True)
class StatusType:
    TimeStamp: Optional[str] = None
    StatusCode: Optional[int] = None
    StatusDescription: Optional[str] = None
    PhaseCode: Optional[int] = None
    PhaseDescription: Optional[str] = None


@s(auto_attribs=True)
class ProductOptionType:
    OptionCode: Optional[int] = None
    CharacteristicCode: Optional[int] = None


@s(auto_attribs=True)
class ShipmentType:
    MainBarcode: Optional[str] = None
    Barcode: Optional[str] = None
    ShipmentAmount: Optional[int] = None
    ShipmentCounter: Optional[int] = None
    Customer: Optional[CustomerType] = JStruct[CustomerType]
    ProductCode: Optional[str] = None
    ProductDescription: Optional[str] = None
    Reference: Optional[str] = None
    DeliveryDate: Optional[str] = None
    Dimension: Optional[DimensionType] = JStruct[DimensionType]
    Address: List[AddressType] = JList[AddressType]
    Event: List[EventType] = JList[EventType]
    ProductOptions: List[ProductOptionType] = JList[ProductOptionType]
    Expectation: Optional[ExpectationType] = JStruct[ExpectationType]
    Status: Optional[StatusType] = JStruct[StatusType]
    OldStatus: List[StatusType] = JList[StatusType]


@s(auto_attribs=True)
class CompleteStatusType:
    Shipment: Optional[ShipmentType] = JStruct[ShipmentType]


@s(auto_attribs=True)
class TrackingResponseType:
    CompleteStatus: Optional[CompleteStatusType] = JStruct[CompleteStatusType]
