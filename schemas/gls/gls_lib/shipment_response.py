from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class Barcodes:
    Primary2D: Optional[str] = None
    Secondary2D: Optional[str] = None
    Primary1D: Optional[str] = None
    Primary1DPrint: Optional[bool] = None


@s(auto_attribs=True)
class ExpressData:
    AlternateDelivery: Optional[bool] = None
    ImportStation: Optional[int] = None
    TourNumber: Optional[int] = None
    CourierParcelNumber: Optional[str] = None
    Kurier1D: Optional[str] = None
    KurierTourNumber: Optional[int] = None
    KurierImportStation: Optional[int] = None


@s(auto_attribs=True)
class NDIArea:
    NDI1D: Optional[int] = None
    GBProductIdentifier: Optional[int] = None
    GBPostOffice1D: Optional[str] = None
    CHParcelNumber: Optional[int] = None
    CHPRI1D: Optional[int] = None
    CHSI1D: Optional[int] = None


@s(auto_attribs=True)
class RoutingInfo:
    Tour: Optional[str] = None
    InboundSortingFlag: Optional[int] = None
    FinalLocationCode: Optional[str] = None
    HubLocation: Optional[str] = None
    LastRoutingDate: Optional[str] = None


@s(auto_attribs=True)
class Information:
    Name: Optional[str] = None
    Value: Optional[str] = None


@s(auto_attribs=True)
class Service:
    Header: Optional[str] = None
    Information: List[Information] = JList[Information]


@s(auto_attribs=True)
class ServiceArea:
    Service: List[Service] = JList[Service]


@s(auto_attribs=True)
class ParcelDatum:
    TrackID: Optional[str] = None
    ExchangeParcelID: Optional[str] = None
    ParcelNumber: Optional[str] = None
    ShipmentUnitReference: Optional[str] = None
    Barcodes: Optional[Barcodes] = JStruct[Barcodes]
    RoutingInfo: Optional[RoutingInfo] = JStruct[RoutingInfo]
    ServiceArea: Optional[ServiceArea] = JStruct[ServiceArea]
    ExpressData: Optional[ExpressData] = JStruct[ExpressData]
    NDIArea: Optional[NDIArea] = JStruct[NDIArea]
    HandlingInformation: Optional[str] = None


@s(auto_attribs=True)
class PrintDatum:
    Data: Optional[str] = None
    LabelFormat: Optional[str] = None


@s(auto_attribs=True)
class CreatedShipment:
    ShipmentReference: List[str] = JList[str]
    ParcelData: List[ParcelDatum] = JList[ParcelDatum]
    PrintData: List[PrintDatum] = JList[PrintDatum]
    CustomerID: Optional[int] = None
    PickupLocation: Optional[str] = None
    GDPR: List[str] = JList[str]
    Nemonico: Optional[str] = None


@s(auto_attribs=True)
class ShipmentResponse:
    CreatedShipment: Optional[CreatedShipment] = JStruct[CreatedShipment]
