from typing import Union, List, Tuple
from pyusps.ratev4request import RateV4Request
from pyusps.intlratev2request import IntlRateV2Request
from purplship.core.units import Country
from purplship.core.errors import OriginNotServicedError
from purplship.core.utils.serializable import Serializable
from purplship.core.models import RateRequest, RateDetails, Message
from purplship.core.utils.xml import Element
from purplship.carriers.usps import Settings
from purplship.carriers.usps.rate.rate_v4 import rate_v4_request, parse_rate_v4_response
from purplship.carriers.usps.rate.intl_rate import (
    intl_rate_request,
    parse_intl_rate_response,
)


def parse_rate_request(
    response: Element, settins: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    is_intl = response.tag == "IntlRateV2Response"
    return (parse_intl_rate_response if is_intl else parse_rate_v4_response)(
        response, settins
    )


def rate_request(
    payload: RateRequest, settings: Settings
) -> Serializable[Union[RateV4Request, IntlRateV2Request]]:
    """Create the appropriate USPS rate request depending on the destination

    :param payload: PurplShip unified API rate request data
    :param settings: USPS connection and auth settings
    :return: a domestic or international USPS compatible request
    :raises: an OriginNotServicedError when origin country is not serviced by the carrier
    """
    if payload.shipper.country_code and payload.shipper.country_code != Country.US.name:
        raise OriginNotServicedError(
            payload.shipper.country_code, settings.carrier_id
        )

    is_local = (
        payload.recipient.country_code is None
        or payload.recipient.country_code == Country.US.name
    )
    return (rate_v4_request if is_local else intl_rate_request)(payload, settings)
