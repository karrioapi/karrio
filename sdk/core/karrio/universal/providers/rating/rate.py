from typing import Tuple, List
from karrio.core.utils import Serializable
from karrio.core.models import (
    RateRequest,
    RateDetails,
    Message,
    ServiceLevel,
)
from karrio.universal.providers.rating.utils import (
    RatingMixinSettings,
    PackageServices,
)
from karrio.core.utils.transformer import to_multi_piece_rates


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
        carrier_id=settings.carrier_id,
        currency=service.currency,
        transit_days=service.estimated_transit_days,
        service=service.service_code,
        total_charge=service.cost,
        meta=dict(service_name=service.service_name),
        carrier_name=getattr(settings, "custom_carrier_name", settings.carrier_name),
    )


def rate_request(payload: RateRequest, _) -> Serializable[RateRequest]:
    return Serializable(payload)
