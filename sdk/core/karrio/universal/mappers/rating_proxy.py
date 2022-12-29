import attr
from typing import List, Tuple
from karrio.core.utils import (
    Tracer,
    Serializable,
    Deserializable,
)
from karrio.core.models import (
    Message,
    RateRequest,
    ServiceLevel,
)
from karrio.core.units import (
    Weight,
    Dimension,
    Packages,
    Package,
)
from karrio.universal.providers.rating import RatingMixinSettings, PackageServices


@attr.s(auto_attribs=True)
class RatingMixinProxy:
    settings: RatingMixinSettings
    tracer: Tracer = attr.field(factory=Tracer)

    def trace(self, *args, **kwargs):
        return self.tracer.with_metadata(dict(connection=self.settings))(
            *args, **kwargs
        )

    def get_rates(
        self, request: Serializable[RateRequest]
    ) -> Deserializable[Tuple[PackageServices, List[Message]]]:
        response = filter_service_level(request.serialize(), self.settings)

        return Deserializable(response)


def filter_service_level(
    request: RateRequest, settings: RatingMixinSettings
) -> Tuple[PackageServices, List[Message]]:
    errors: List[Message] = []
    packages = Packages(request.parcels)
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
    selected_services = [
        s.service_code for s in settings.services
        if s.service_code in request.services
    ]

    def match_requirements(package: Package, service: ServiceLevel) -> bool:
        # Check if service requested
        explicitly_requested = service.service_code in selected_services
        implicitly_requested = len(selected_services or []) == 0
        excluded = len(selected_services or []) > 0 and not explicitly_requested

        if not service.active or excluded:
            return False

        # Check if destination covered
        cover_domestic_shipment = (
            service.domicile is True and service.domicile == is_domicile
        )
        cover_international_shipment = (
            service.international is True and service.international == is_international
        )
        cover_all_destination = (
            service.domicile is None and service.international is None
        )
        explicit_destination_covered = explicitly_requested and (
            cover_domestic_shipment
            or cover_international_shipment
            or cover_all_destination
        )
        implicit_destination_covered = implicitly_requested and (
            cover_domestic_shipment
            or cover_international_shipment
            or cover_all_destination
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

    services = [
        (
            f'{getattr(pkg, "id", index)}',
            [
                service
                for service in settings.services
                if match_requirements(pkg, service)
            ],
        )
        for index, pkg in enumerate(packages, 1)
    ]

    return services, errors
