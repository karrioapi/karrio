from typing import Tuple, List

from karrio.core.errors import OriginNotServicedError, DestinationNotServicedError
from karrio.core.units import Country
from karrio.core.utils import Serializable, Element
from karrio.core.models import (
    ShipmentRequest,
    ShipmentDetails,
    Message
)

import karrio.providers.usps_international.shipment.priority_mail as priority_mail
import karrio.providers.usps_international.shipment.first_class_mail as first_class_mail
import karrio.providers.usps_international.shipment.priority_express as priority_express
import karrio.providers.usps_international.shipment.global_express_guaranteed as global_express_guaranteed
from karrio.providers.usps_international.units import ServiceType
from karrio.providers.usps_international.utils import Settings


def parse_shipment_response(response: Element, settings: Settings) -> Tuple[ShipmentDetails, List[Message]]:
    if response.tag == 'eVSFirstClassMailIntlResponse':
        return first_class_mail.parse_shipment_response(response, settings)

    if response.tag == 'eVSGXGGetLabelResponse':
        return global_express_guaranteed.parse_shipment_response(response, settings)

    if response.tag == 'eVSPriorityMailIntlResponse':
        return priority_mail.parse_shipment_response(response, settings)

    else:
        return priority_express.parse_shipment_response(response, settings)


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable:

    if payload.shipper.country_code is not None and payload.shipper.country_code != Country.US.name:
        raise OriginNotServicedError(payload.shipper.country_code)

    if payload.recipient.country_code == Country.US.name:
        raise DestinationNotServicedError(payload.recipient.country_code)

    service = ServiceType[payload.service]

    # Create a First Class Mail Shipment Request
    if service == ServiceType.usps_first_class_mail_international:
        return first_class_mail.shipment_request(payload, settings)

    # Create a GXG Shipment Request
    elif service == ServiceType.usps_global_express_guaranteed:
        return global_express_guaranteed.shipment_request(payload, settings)

    # Create a Priority Mail Shipment Request
    elif service == ServiceType.usps_priority_mail_international:
        return priority_mail.shipment_request(payload, settings)

    # Fallback to creating a Priority Express Mail Shipment Request
    else:
        return priority_express.shipment_request(payload, settings)
