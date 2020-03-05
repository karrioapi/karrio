from pyups.freight_pickup_web_service_schema import (
    FreightPickupRequest
)
from purplship.core.utils.xml import Element
from purplship.core.models import PickupDetails, PickupRequest
from purplship.carriers.ups import Settings


def parse_pickup_response(response: Element, settings: Settings) -> PickupDetails:
    pass


def freight_pickup_request(payload: PickupRequest, settings: Settings) -> FreightPickupRequest:
    return FreightPickupRequest(
        Request=None,
        PickupRequestConfirmationNumber=None,
        DestinationPostalCode=None,
        DestinationCountryCode=None,
        Requester=None,
        ShipFrom=None,
        ShipTo=None,
        PickupDate=None,
        EarliestTimeReady=None,
        LatestTimeReady=None,
        ShipmentServiceOptions=None,
        ShipmentDetail=None,
        ExistingShipmentID=None,
        POM=None,
        PickupInstructions=None,
        AdditionalComments=None,
        HandlingInstructions=None,
        SpecialInstructions=None,
        DeliveryInstructions=None
    )
