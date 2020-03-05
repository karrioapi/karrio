from pyups.pickup_web_service_schema import (
    PickupCreationRequest
)
from purplship.core.utils.xml import Element
from purplship.core.utils.serializable import Serializable
from purplship.core.models import PickupDetails, PickupRequest
from purplship.carriers.ups import Settings


def parse_pickup_creation_response(response: Element, settings: Settings) -> PickupDetails:
    pass


def pickup_creation_request(payload: PickupRequest, settings: Settings) -> Serializable[PickupCreationRequest]:
    request = PickupCreationRequest(
        Request=None,
        RatePickupIndicator=None,
        TaxInformationIndicator=None,
        UserLevelDiscountIndicator=None,
        Shipper=None,
        PickupDateInfo=None,
        PickupAddress=None,
        AlternateAddressIndicator=None,
        PickupPiece=None,
        TotalWeight=None,
        OverweightIndicator=None,
        TrackingData=None,
        TrackingDataWithReferenceNumber=None,
        PaymentMethod=None,
        SpecialInstruction=None,
        ReferenceNumber=None,
        FreightOptions=None,
        ServiceCategory=None,
        CashType=None,
        ShippingLabelsAvailable=None
    )
    return Serializable(request)
