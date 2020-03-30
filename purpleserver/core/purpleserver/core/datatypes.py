from typing import Callable
from purplship.core.models import *


@attr.s(auto_attribs=True)
class CarrierSettings:
    carrier: str
    settings: dict

    @property
    def clean_settings(self):
        return {
            **{k: v for k, v in self.settings.items() if k not in ['id', 'test']},
            "server_url": CARRIER_URLS[self.carrier](self.settings['test'])
        }


@attr.s(auto_attribs=True)
class ShipmentRate:
    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcel: Parcel = JStruct[Parcel, REQUIRED]
    options: Dict = {}
    rates: List[RateDetails] = JList[RateDetails]


@attr.s(auto_attribs=True)
class Shipment:
    carrier: str
    carrier_name: str
    label: str
    tracking_number: str
    selected_rate: RateDetails
    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcel: Parcel = JStruct[Parcel, REQUIRED]
    options: Dict = {}
    rates: List[RateDetails] = JList[RateDetails]


@attr.s(auto_attribs=True)
class CompleteRateResponse:
    messages: List[Message] = JList[Message]
    shipment: ShipmentRate = JStruct[ShipmentRate]


@attr.s(auto_attribs=True)
class CompleteShipmentResponse:
    messages: List[Message] = JList[Message]
    shipment: Shipment = JStruct[Shipment]


@attr.s(auto_attribs=True)
class CompleteTrackingResponse:
    messages: List[Message] = JList[Message]
    tracking_details: TrackingDetails = JStruct[TrackingDetails]


CARRIER_URLS: Dict[str, Callable[[bool], str]] = {
    'caps': lambda test: {True: "https://ct.soa-gw.canadapost.ca", False: "https://soa-gw.canadapost.ca"}[test],
    'dhl': lambda _: "https://xmlpi-ea.dhl.com/XMLShippingServlet",
    'fedex': lambda test: {True: "https://wsbeta.fedex.com:443/web-services", False: "https://ws.fedex.com:443/web-services"}[test],
    'purolator': lambda test: {True: "https://devwebservices.purolator.com", False: "https://webservices.purolator.com"}[test],
    'ups': lambda test: {True: "https://wwwcie.ups.com/webservices", False: "https://onlinetools.ups.com/webservices"}[test],
}
