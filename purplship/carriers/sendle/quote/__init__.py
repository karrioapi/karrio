from typing import List, Tuple, Union
from purplship.core.utils import to_dict, Serializable, format_date, decimal
from purplship.core.models import RateRequest, RateDetails, Message
from purplship.core.units import Country
from purplship.core.errors import OriginNotServicedError
from pysendle.quotes import (
    DomesticParcelQuote,
    InternationalParcelQuote,
    ParcelQuoteResponse,
)
from purplship.carriers.sendle.error import parse_error_response
from purplship.carriers.sendle.utils import Settings
from purplship.carriers.sendle.units import Plan
from purplship.carriers.sendle.quote.domestic import domestic_quote_request
from purplship.carriers.sendle.quote.international import international_quote_request


ParcelQuoteRequest = Union[DomesticParcelQuote, InternationalParcelQuote]


def parse_parcel_quote_response(
    response: dict, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    parcel_quotes: List[ParcelQuoteResponse] = [
        ParcelQuoteResponse(**p) for p in response
    ] if isinstance(response, list) else []
    return (
        [_extract_quote(p, settings) for p in parcel_quotes],
        parse_error_response([response], settings),
    )


def _extract_quote(
    parcel_quote: ParcelQuoteResponse, settings: Settings
) -> RateDetails:
    return RateDetails(
        carrier=settings.carrier,
        carrier_name=settings.carrier_name,
        service=Plan(parcel_quote.plan_name).name,
        base_charge=decimal(parcel_quote.quote.gross.amount),
        duties_and_taxes=decimal(parcel_quote.quote.tax.amount),
        total_charge=decimal(parcel_quote.quote.net.amount),
        currency=parcel_quote.quote.net.currency,
        estimated_delivery=format_date(parcel_quote.eta.date_range[-1]),
    )


def parcel_quote_request(
    payload: RateRequest, settings: Settings
) -> Serializable[ParcelQuoteRequest]:
    """Create the appropriate Sendle rate request depending on the destination

    :param payload: PurplShip unified API rate request data
    :param settings: Sendle connection and authentication settings
    :return: a domestic or international Sendle compatible request
    :raises: an OriginNotServicedError when origin country is not serviced by the carrier
    """
    if payload.shipper.country_code and payload.shipper.country_code != Country.AU.name:
        raise OriginNotServicedError(
            payload.shipper.country_code, settings.carrier_name
        )
    is_international = (
        payload.recipient.country_code is None
        or payload.recipient.country_code == Country.AU.name
    )
    request = (
        domestic_quote_request if is_international else international_quote_request
    )(payload)
    return Serializable(request, _request_serializer)


def _request_serializer(request: ParcelQuoteRequest) -> dict:
    return to_dict(request)
