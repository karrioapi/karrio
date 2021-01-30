from typing import Tuple, List, Union
import usps_lib.evs_request as evs
import usps_lib.evs_express_mail_intl_request as evs_express
import usps_lib.evs_first_class_mail_intl_request as evs_first_class
import usps_lib.evs_priority_mail_intl_request as evs_priority
import usps_lib.evs_gxg_get_label_request as evs_gxg

from purplship.core.errors import OriginNotServicedError
from purplship.core.units import Country
from purplship.core.utils import Serializable, Element
from purplship.core.models import (
    ShipmentRequest,
    ShipmentDetails,
    Message
)

import purplship.providers.usps.shipment.intl as intl
import purplship.providers.usps.shipment.local as local
from purplship.providers.usps.utils import Settings

eVSRequest = Union[
    evs.eVSRequest,
    evs_gxg.eVSGXGGetLabelRequest,
    evs_express.eVSExpressMailIntlRequest,
    evs_priority.eVSPriorityMailIntlRequest,
    evs_first_class.eVSFirstClassMailIntlRequest,
]


def parse_shipment_response(response: Element, settings: Settings) -> Tuple[ShipmentDetails, List[Message]]:
    if response.tag == 'eVSRequest':
        return local.parse_shipment_response(response, settings)

    return intl.parse_shipment_response(response, settings)


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[eVSRequest]:

    if payload.shipper.country_code is not None and payload.shipper.country_code != Country.US.name:
        raise OriginNotServicedError(payload.shipper.country_code)

    if payload.recipient.country_code is None or payload.recipient.country_code == Country.US.name:
        return local.rate_request(payload, settings)

    return intl.rate_request(payload, settings)
