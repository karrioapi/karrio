from typing import List, Tuple
from karrio.core.utils import Serializable, SF, NF, DP
from karrio.core.models import (
    Documents,
    ShipmentRequest,
    ShipmentDetails,
    RateDetails,
    Message,
    ChargeDetails,
    Address,
)
from karrio.core.units import Packages, Options
from karrio.providers.amazon_mws.utils import Settings
from karrio.providers.amazon_mws.units import (
    Service,
    PackagingType,
    Option,
    PaymentType,
)
from karrio.providers.amazon_mws.error import parse_error_response


def parse_shipment_response(
    response: dict, settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    pass


def _extract_shipment(node: dict, settings: Settings) -> ShipmentDetails:
    pass


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable:
    pass
