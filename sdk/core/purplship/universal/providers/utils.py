import attr
from typing import List, Tuple
from jstruct import JList

from purplship.core.settings import Settings
from purplship.core.units import Dimension, Packages, Weight
from purplship.core.models import Message, RateRequest, ServiceLevel
from sdk.core.purplship.core.models import LabelTemplate, ServiceLabel, ShipmentRequest


@attr.s(auto_attribs=True)
class RatingMixinSettings(Settings):
    """Universal rating settings mixin."""

    # Additional properties
    services: List[ServiceLevel] = JList[ServiceLevel]


@attr.s(auto_attribs=True)
class ShippingMixinSettings(Settings):
    """Universal shipping settings mixin."""

    # Additional properties
    templates: List[LabelTemplate] = JList[LabelTemplate]


def filter_service_level(
    request: RateRequest, settings: RatingMixinSettings
) -> Tuple[List[ServiceLevel], List[Message]]:
    errors: List[Message] = []
    package = Packages(request.parcels).single
    has_origin = any(
        [
            request.shipper.country_code,
            settings.account_country_code,
        ]
    )
    is_domicile = has_origin and (
        request.shipper.country_code == request.recipient.country_code
        or settings.account_country_code == request.recipient.country_code
    )
    is_international = not is_domicile

    def match_requirements(service: ServiceLevel) -> bool:
        # Check if service requested
        explicitly_requested = service.service_code in request.services
        implicitly_requested = len(request.services or []) == 0
        excluded = len(request.services or []) > 0 and not explicitly_requested

        if not service.active or excluded:
            return False

        # Check if destination covered
        cover_domestic_shipment = (
            service.domicile is True and service.domicile == is_domicile
        )
        cover_international_shipment = (
            service.international is True and service.international == is_international
        )
        explicit_destination_covered = explicitly_requested and (
            cover_domestic_shipment or cover_international_shipment
        )
        implicit_destination_covered = implicitly_requested and (
            cover_domestic_shipment or cover_international_shipment
        )

        destination_covered = (
            explicit_destination_covered or implicit_destination_covered
        )

        # Check if weight and dimensions fit restrictions
        match_length_requirements = (
            service.max_length is not None
            and package.length[service.dimension_unit]
            <= Dimension(service.max_length or 0, service.dimension_unit).value
        ) or (service.max_length is None)
        match_height_requirements = (
            service.max_height is not None
            and package.height[service.dimension_unit]
            <= Dimension(service.max_height, service.dimension_unit).value
        ) or (service.max_height is None)
        match_width_requirements = (
            service.max_width is not None
            and package.width[service.dimension_unit]
            <= Dimension(service.max_width, service.dimension_unit).value
        ) or (service.max_width is None)
        match_weight_requirements = (
            service.max_weight is not None
            and package.weight[service.weight_unit]
            <= Weight(service.max_weight, service.weight_unit).value
        ) or (service.max_weight is None)

        # error validations
        if explicitly_requested and not explicit_destination_covered:
            errors.append(
                Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code="destination_not_supported",
                    message=f"the service {service.service_code} does not cover the requested destination",
                )
            )
        if (
            destination_covered
            and service.max_length is not None
            and not match_length_requirements
        ):
            errors.append(
                Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code="invalid_dimension",
                    message=f"length size exceeds service {service.service_code} max length",
                )
            )
        if (
            destination_covered
            and service.max_height is not None
            and not match_height_requirements
        ):
            errors.append(
                Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code="invalid_dimension",
                    message=f"height size exceeds service {service.service_code} max height",
                )
            )
        if (
            destination_covered
            and service.max_width is not None
            and not match_width_requirements
        ):
            errors.append(
                Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code="invalid_dimension",
                    message=f"the width size exceeds service {service.service_code} max width",
                )
            )
        if (
            destination_covered
            and service.max_weight is not None
            and not match_weight_requirements
        ):
            errors.append(
                Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code="invalid_weight",
                    message=f"the weight exceeds service {service.service_code} max weight",
                )
            )

        return (
            destination_covered
            and match_length_requirements
            and match_height_requirements
            and match_width_requirements
            and match_weight_requirements
        )

    services = [service for service in settings.services if match_requirements(service)]

    return services, errors


def generate_service_label(
    request: ShipmentRequest, settings: ShippingMixinSettings
) -> Tuple[ServiceLabel, List[Message]]:

    messages = []
    service_label = ServiceLabel(
        label="",
        label_type="",
        tracking_number="",
    )

    return service_label, messages
