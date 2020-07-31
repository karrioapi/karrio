import attr
from typing import List, Dict
from enum import Enum
from jstruct import JStruct, JList, REQUIRED
from purplship.core.utils import to_dict
from purplship.core.models import (
    Doc,
    Parcel,
    Message,
    Address,
    Insurance,
    TrackingDetails,
    TrackingRequest,
    ShipmentDetails,
    Payment as BasePayment,
    Customs as BaseCustoms,
    RateRequest as BaseRateRequest,
    ShipmentRequest as BaseShipmentRequest,
    ChargeDetails
)


class ShipmentStatus(Enum):
    created = 'created'
    cancelled = 'cancelled'
    purchased = 'purchased'


class CarrierSettings:
    def __init__(self, carrier_name: str, carrier_id: str, test: bool = None, id: str = None, **kwargs):
        self.carrier_name = carrier_name
        self.carrier_id = carrier_id
        self.test = test
        self.id = id

        for name, value in kwargs.items():
            if name not in ['carrier_ptr']:
                self.__setattr__(name, value)

    def dict(self):
        return {
            name: value for name, value in self.__dict__.items()
            if name not in ['carrier_name']
        }

    @classmethod
    def create(cls, data: object):
        return cls(**to_dict(data))


@attr.s(auto_attribs=True)
class Rate:
    carrier_name: str
    carrier_id: str
    currency: str
    transit_days: int = None
    service: str = None
    discount: float = None
    base_charge: float = 0.0
    total_charge: float = 0.0
    duties_and_taxes: float = None
    extra_charges: List[ChargeDetails] = []
    id: str = None
    carrier_ref: str = None


@attr.s(auto_attribs=True)
class Payment(BasePayment):
    id: str = None


@attr.s(auto_attribs=True)
class Customs(BaseCustoms):
    id: str = None


@attr.s(auto_attribs=True)
class RateRequest(BaseRateRequest):
    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcels: List[Parcel] = JList[Parcel, REQUIRED]

    services: List[str] = []
    options: Dict = {}
    reference: str = ""

    carrier_ids: List[str] = []


@attr.s(auto_attribs=True)
class ShipmentRequest(BaseShipmentRequest):
    service: str = JStruct[str, REQUIRED]
    selected_rate_id: str = JStruct[str, REQUIRED]

    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcels: List[Parcel] = JList[Parcel, REQUIRED]
    rates: List[Rate] = JList[Rate, REQUIRED]

    payment: Payment = JStruct[Payment]
    customs: Customs = JStruct[Customs]
    doc_images: List[Doc] = JList[Doc]

    options: Dict = {}
    reference: str = ""
    id: str = None


@attr.s(auto_attribs=True)
class Shipment:
    carrier_id: str
    carrier_name: str
    tracking_number: str
    label: str
    service: str
    selected_rate_id: str

    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcels: List[Parcel] = JList[Parcel, REQUIRED]
    rates: List[Rate] = JList[Rate, REQUIRED]
    selected_rate: Rate = JStruct[Rate, REQUIRED]

    payment: Payment = JStruct[Payment]
    customs: Customs = JStruct[Customs]
    doc_images: List[Doc] = JList[Doc]

    options: Dict = {}
    reference: str = ""
    tracking_url: str = None
    status: str = ""


@attr.s(auto_attribs=True)
class ErrorResponse:
    messages: List[Message] = JList[Message]


@attr.s(auto_attribs=True)
class RateResponse:
    messages: List[Message] = JList[Message]
    rates: List[Rate] = JList[Rate]


@attr.s(auto_attribs=True)
class ShipmentResponse:
    messages: List[Message] = JList[Message]
    shipment: Shipment = JStruct[Shipment]


@attr.s(auto_attribs=True)
class TrackingResponse:
    messages: List[Message] = JList[Message]
    tracking_details: TrackingDetails = JStruct[TrackingDetails]


@attr.s(auto_attribs=True)
class Error:
    message: str = None
    code: str = None
    details: Dict = None
