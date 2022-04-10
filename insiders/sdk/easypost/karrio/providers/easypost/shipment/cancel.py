from typing import List, Tuple
from karrio.core.models import ShipmentCancelRequest, ConfirmationDetails, Message
from karrio.core.utils import (
    Serializable,
)
from karrio.providers.easypost.error import parse_error_response
from karrio.providers.easypost.utils import Settings


def parse_shipment_cancel_response(
    response: dict, settings: Settings
) -> Tuple[ConfirmationDetails, List[Message]]:
    pass


def shipment_cancel_request(
    payload: ShipmentCancelRequest, settings: Settings
) -> Serializable[str]:
    pass
