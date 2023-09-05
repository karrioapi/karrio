from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class BarcodesType:
    Primary2D: Optional[str] = None
    Secondary2D: Optional[str] = None
    Primary1D: Optional[str] = None
    Primary1DPrint: Optional[bool] = None


@s(auto_attribs=True)
class ExpressDataType:
    AlternateDelivery: Optional[bool] = None
    ImportStation: Optional[int] = None
    TourNumber: Optional[int] = None
    CourierParcelNumber: Optional[str] = None
    Kurier1D: Optional[str] = None
    KurierTourNumber: Optional[int] = None
    KurierImportStation: Optional[int] = None


@s(auto_attribs=True)
class NDIAreaType:
    NDI1D: Optional[int] = None
    GBProductIdentifier: Optional[int] = None
    GBPostOffice1D: Optional[str] = None
    CHParcelNumber: Optional[int] = None
    CHPRI1D: Optional[int] = None
    CHSI1D: Optional[int] = None


@s(auto_attribs=True)
class RoutingInfoType:
    Tour: Optional[str] = None
    InboundSortingFlag: Optional[int] = None
    FinalLocationCode: Optional[str] = None
    HubLocation: Optional[str] = None
    LastRoutingDate: Optional[str] = None


@s(auto_attribs=True)
class InformationType:
    Name: Optional[str] = None
    Value: Optional[str] = None


@s(auto_attribs=True)
class ServiceType:
    Header: Optional[str] = None
    Information: List[InformationType] = JList[InformationType]


@s(auto_attribs=True)
class ServiceAreaType:
    Service: List[ServiceType] = JList[ServiceType]


@s(auto_attribs=True)
class ParcelDatumType:
    TrackID: Optional[str] = None
    ExchangeParcelID: Optional[str] = None
    ParcelNumber: Optional[str] = None
    ShipmentUnitReference: Optional[str] = None
    Barcodes: Optional[BarcodesType] = JStruct[BarcodesType]
    RoutingInfo: Optional[RoutingInfoType] = JStruct[RoutingInfoType]
    ServiceArea: Optional[ServiceAreaType] = JStruct[ServiceAreaType]
    ExpressData: Optional[ExpressDataType] = JStruct[ExpressDataType]
    NDIArea: Optional[NDIAreaType] = JStruct[NDIAreaType]
    HandlingInformation: Optional[str] = None


@s(auto_attribs=True)
class PrintDatumType:
    Data: Optional[str] = None
    LabelFormat: Optional[str] = None


@s(auto_attribs=True)
class CreatedShipmentType:
    ShipmentReference: List[str] = []
    ParcelData: List[ParcelDatumType] = JList[ParcelDatumType]
    PrintData: List[PrintDatumType] = JList[PrintDatumType]
    CustomerID: Optional[int] = None
    PickupLocation: Optional[str] = None
    GDPR: List[str] = []
    Nemonico: Optional[str] = None


@s(auto_attribs=True)
class ShipmentResponseType:
    CreatedShipment: Optional[CreatedShipmentType] = JStruct[CreatedShipmentType]
