from typing import Tuple, List
from purplship.core.utils import Serializable
from purplship.core.models import (
    RateRequest,
    RateDetails,
    Message,
    ServiceLevel,
)
from purplship.universal.mappers.settings import Settings


def parse_rate_response(
    response: Tuple[List[ServiceLevel], List[Message]], settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    services, errors = response
    rates = [_extract_details(service, settings) for service in services]
    return rates, errors


def _extract_details(service: ServiceLevel, settings: Settings) -> RateDetails:
    return RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency=service.currency,
        transit_days=service.estimated_transit_days,
        service=service.service_code,
        base_charge=service.cost,
        total_charge=service.cost,
        meta=dict(service_name=service.service_name),
    )


def rate_request(payload: RateRequest, _) -> Serializable[RateRequest]:
    return Serializable(payload)
