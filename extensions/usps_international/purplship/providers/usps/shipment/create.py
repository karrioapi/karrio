from typing import Tuple, List

from purplship.core.errors import OriginNotServicedError, DestinationNotServicedError
from purplship.core.units import Country
from purplship.core.utils import Serializable, Element, XP
from purplship.core.models import (
    ShipmentRequest,
    ShipmentDetails,
    Message
)

import purplship.providers.usps_international.shipment.first_class as first_class
import purplship.providers.usps_international.shipment.priority as priority
import purplship.providers.usps_international.shipment.express as express
import purplship.providers.usps_international.shipment.gxg as gxg
from purplship.providers.usps_international.utils import Settings


def parse_shipment_response(response: Element, settings: Settings) -> Tuple[ShipmentDetails, List[Message]]:
    if response.tag == 'eVSFirstClassMailIntlResponse':
        return first_class.parse_shipment_response(response, settings)
    if response.tag == 'eVSGXGGetLabelResponse':
        return gxg.parse_shipment_response(response, settings)
    if response.tag == 'eVSPriorityMailIntlResponse':
        return priority.parse_shipment_response(response, settings)
    else:
        return express.parse_shipment_response(response, settings)


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable:

    if payload.shipper.country_code is not None and payload.shipper.country_code != Country.US.name:
        raise OriginNotServicedError(payload.shipper.country_code)

    if payload.recipient.country_code == Country.US.name:
        raise DestinationNotServicedError(payload.recipient.country_code)

    if 'first_class' in payload.service:
        request = first_class.rate_request(payload, settings)
    elif 'express' in payload.service:
        request = express.rate_request(payload, settings)
    elif 'priority' in payload.service:
        request = priority.rate_request(payload, settings)
    else:
        request = gxg.rate_request(payload, settings)

    return Serializable(request, XP.export)
