from typing import Tuple, List
from purplship.core.utils import Serializable
from purplship.core.models import (
    RateRequest,
    RateDetails,
    Message,
    ServiceLevel,
)
from purplship.universal.providers.rating.utils import (
    RatingMixinSettings,
    PackageServices,
)
from sdk.core.purplship.core.utils.transformer import to_multi_piece_rates


def parse_rate_response(
    response: Tuple[PackageServices, List[Message]], settings: RatingMixinSettings
) -> Tuple[List[RateDetails], List[Message]]:
    packages, messages = response
    rates = to_multi_piece_rates(
        [
            (package_ref, [_extract_details(service, settings) for service in services])
            for package_ref, services in packages
        ]
    )

    return rates, messages


def _extract_details(
    service: ServiceLevel, settings: RatingMixinSettings
) -> RateDetails:
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
