import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class BarcodesType:
    Primary2D: typing.Optional[str] = None
    Secondary2D: typing.Optional[str] = None
    Primary1D: typing.Optional[str] = None
    Primary1DPrint: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class ExpressAreaType:
    Kurier1D: typing.Optional[str] = None
    KurierTourNumber: typing.Optional[int] = None
    KurierImportStation: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ExpressDataType:
    AlternateDelivery: typing.Optional[bool] = None
    ImportStation: typing.Optional[int] = None
    TourNumber: typing.Optional[int] = None
    CourierParcelNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class NDIAreaType:
    NDI1D: typing.Optional[str] = None
    GBProductIdentifier: typing.Optional[int] = None
    GBPostOffice1D: typing.Optional[str] = None
    CHParcelNumber: typing.Optional[int] = None
    CHPRI1D: typing.Optional[int] = None
    CHSI1D: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class RoutingInfoType:
    Tour: typing.Optional[int] = None
    GeoTour: typing.Optional[int] = None
    LoadingArea: typing.Optional[int] = None
    DispositionFlag: typing.Optional[str] = None
    InboundSortingFlag: typing.Optional[str] = None
    FinalLocationCode: typing.Optional[str] = None
    HubLocation: typing.Optional[str] = None
    LastRoutingDate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class InformationType:
    Name: typing.Optional[str] = None
    Value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ServiceType:
    Header: typing.Optional[str] = None
    Information: typing.Optional[typing.List[InformationType]] = jstruct.JList[InformationType]


@attr.s(auto_attribs=True)
class ServiceAreaType:
    Service: typing.Optional[typing.List[ServiceType]] = jstruct.JList[ServiceType]


@attr.s(auto_attribs=True)
class ParcelDatumType:
    TrackID: typing.Optional[str] = None
    ParcelNumber: typing.Optional[str] = None
    ExchangeParcelID: typing.Optional[str] = None
    ShipmentUnitReference: typing.Optional[typing.List[str]] = None
    Barcodes: typing.Optional[BarcodesType] = jstruct.JStruct[BarcodesType]
    RoutingInfo: typing.Optional[RoutingInfoType] = jstruct.JStruct[RoutingInfoType]
    ServiceArea: typing.Optional[ServiceAreaType] = jstruct.JStruct[ServiceAreaType]
    ExpressData: typing.Optional[ExpressDataType] = jstruct.JStruct[ExpressDataType]
    ExpressArea: typing.Optional[ExpressAreaType] = jstruct.JStruct[ExpressAreaType]
    NDIArea: typing.Optional[NDIAreaType] = jstruct.JStruct[NDIAreaType]
    HandlingInformation: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PrintDatumType:
    Data: typing.Optional[str] = None
    LabelFormat: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CreatedShipmentType:
    ShipmentReference: typing.Optional[typing.List[str]] = None
    ParcelData: typing.Optional[typing.List[ParcelDatumType]] = jstruct.JList[ParcelDatumType]
    PrintData: typing.Optional[typing.List[PrintDatumType]] = jstruct.JList[PrintDatumType]
    CustomerID: typing.Optional[str] = None
    PickupLocation: typing.Optional[str] = None
    GDPR: typing.Optional[typing.List[str]] = None
    Nemonico: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentResponseType:
    CreatedShipment: typing.Optional[CreatedShipmentType] = jstruct.JStruct[CreatedShipmentType]
