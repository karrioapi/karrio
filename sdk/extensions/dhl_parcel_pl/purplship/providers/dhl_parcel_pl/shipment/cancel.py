from typing import List, Tuple
from purplship.core.models import ShipmentCancelRequest, ConfirmationDetails, Message
from purplship.core.utils import (
    create_envelope,
    Envelope,
    Element,
    Serializable,
)
from purplship.providers.dhl_parcel_pl.error import parse_error_response
from purplship.providers.dhl_parcel_pl.utils import Settings


def parse_shipment_cancel_response(
    response: Element, settings: Settings
) -> Tuple[ConfirmationDetails, List[Message]]:
    pass


def shipment_cancel_request(
    payload: ShipmentCancelRequest, settings: Settings
) -> Serializable[Envelope]:
    pass
