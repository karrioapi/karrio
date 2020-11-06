from typing import Union, List, Tuple
from purplship.core.units import Country
from purplship.core.errors import OriginNotServicedError
from purplship.core.utils.serializable import Serializable
from purplship.core.models import RateRequest, RateDetails, Message
from purplship.core.utils.xml import Element

import purplship.providers.usps.rate.local as local
import purplship.providers.usps.rate.intl as intl
from purplship.providers.usps import Settings

USPSRateRequest = Union[local.RateV4Request, intl.IntlRateV2Request]


def parse_rate_response(response: Element, settings: Settings) -> Tuple[List[RateDetails], List[Message]]:
    if response.tag == "IntlRateV2Response":
        return intl.parse_rate_response(response, settings)

    return local.parse_rate_response(response, settings)


def rate_request(payload: RateRequest, settings: Settings) -> Serializable[USPSRateRequest]:
    """Create the appropriate USPS rate request depending on the destination

    :param payload: Purplship unified API rate request data
    :param settings: USPS connection and auth settings
    :return: a domestic or international USPS compatible request
    :raises: an OriginNotServicedError when origin country is not serviced by the carrier
    """

    if payload.shipper.country_code is not None and payload.shipper.country_code != Country.US.name:
        raise OriginNotServicedError(payload.shipper.country_code)

    if payload.recipient.country_code is None or payload.recipient.country_code == Country.US.name:
        return local.rate_request(payload, settings)

    return intl.rate_request(payload, settings)
