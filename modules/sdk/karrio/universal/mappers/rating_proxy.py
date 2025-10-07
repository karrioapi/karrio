import attr
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.utils as utils
import karrio.core.models as models
from karrio.universal.providers.rating import (
    RatingMixinSettings,
    PackageRates,
)


@attr.s(auto_attribs=True)
class RatingMixinProxy:
    settings: RatingMixinSettings
    tracer: utils.Tracer = attr.field(factory=utils.Tracer)

    def trace(self, *args, **kwargs):
        return self.tracer.with_metadata(
            dict(
                connection=dict(
                    id=self.settings.id,
                    test_mode=self.settings.test_mode,
                    carrier_id=self.settings.carrier_id,
                    carrier_name=self.settings.carrier_name,
                )
            )
        )(*args, **kwargs)

    def get_rates(
        self, request: utils.Serializable
    ) -> utils.Deserializable[typing.List[typing.Tuple[str, PackageRates]]]:
        _request = request.serialize()

        shipper = lib.to_address(_request.shipper)
        recipient = lib.to_address(_request.recipient)
        packages = lib.to_packages(_request.parcels)
        has_origin = any(
            [
                _request.shipper.country_code,
                self.settings.account_country_code,
            ]
        )
        is_domicile = has_origin and (
            _request.shipper.country_code == _request.recipient.country_code
            or self.settings.account_country_code == _request.recipient.country_code
        )
        is_international = not is_domicile
        selected_services = [
            s.service_code
            for s in self.settings.shipping_services
            if s.service_code in _request.services
        ]

        response: typing.List[typing.Tuple[str, PackageRates]] = [
            (
                f'{getattr(pkg, "id", idx)}',
                get_available_rates(
                    pkg,
                    shipper,
                    recipient,
                    self.settings,
                    is_domicile=is_domicile,
                    is_international=is_international,
                    selected_services=selected_services,
                ),
            )
            for idx, pkg in enumerate(packages, 1)
        ]

        return utils.Deserializable(response)


def calculate_zone_specificity(
    zone: models.ServiceZone,
) -> int:
    """
    Calculate how specific a zone is.
    Higher score = more specific = better match.

    Scoring:
    - Postal code match: 1000 points (most specific)
    - City match: 100 points (medium specific)
    - Country match only: 10 points (least specific)
    - Weight range defined: +5 points
    - Both weight bounds defined: +5 points (total +10)
    """
    score = 0

    # Location specificity (mutually exclusive layers)
    if zone.postal_codes:
        score += 1000  # Most specific
    elif zone.cities:
        score += 100  # Medium specific
    elif zone.country_codes:
        score += 10  # Least specific

    # Weight range specificity
    if zone.min_weight is not None or zone.max_weight is not None:
        score += 5

    # Both bounds defined is more specific
    if zone.min_weight is not None and zone.max_weight is not None:
        score += 5

    return score


def check_location_match(
    zone: models.ServiceZone,
    recipient: units.ComputedAddress,
) -> bool:
    """
    Check if recipient location matches zone criteria.

    Returns True if:
    - Zone has no location restrictions (matches all), OR
    - Recipient matches postal code list (if defined), OR
    - Recipient matches city list (if defined), OR
    - Recipient matches country code list (if defined)
    """
    # Check postal codes (most specific)
    if zone.postal_codes:
        return recipient.postal_code is not None and str(
            recipient.postal_code
        ).lower() in [str(pc).lower() for pc in zone.postal_codes]

    # Check cities (medium specific)
    if zone.cities:
        return recipient.city is not None and recipient.city.lower() in [
            city.lower() for city in zone.cities
        ]

    # Check country codes (least specific)
    if zone.country_codes:
        return recipient.country_code in zone.country_codes

    # No location restrictions = matches all
    return True


def check_weight_match(
    zone: models.ServiceZone,
    package: units.Package,
    service,
) -> bool:
    """
    Check if package weight fits within zone's weight range.

    Weight range logic (inclusive min, exclusive max):
    - min_weight <= package_weight < max_weight

    Examples:
    - Zone: 0-0.5kg, Package: 0.3kg -> Match ✅
    - Zone: 0-0.5kg, Package: 0.5kg -> No match ❌ (equals max)
    - Zone: 0.5-1.0kg, Package: 0.5kg -> Match ✅ (equals min)
    """
    # If zone has no weight restrictions, always match
    if zone.min_weight is None and zone.max_weight is None:
        return True

    # Default to KG if service doesn't specify weight unit
    weight_unit = service.weight_unit or "KG"
    package_weight = package.weight[weight_unit]

    # Check min weight (inclusive)
    if zone.min_weight is not None:
        min_weight_value = units.Weight(zone.min_weight, weight_unit).value
        if package_weight < min_weight_value:
            return False

    # Check max weight (exclusive)
    if zone.max_weight is not None:
        max_weight_value = units.Weight(zone.max_weight, weight_unit).value
        if package_weight >= max_weight_value:
            return False

    return True


def find_best_matching_zone(
    zones: typing.List[models.ServiceZone],
    package: units.Package,
    recipient: units.ComputedAddress,
    service,
) -> typing.Optional[models.ServiceZone]:
    """
    Find the most specific zone that matches package and destination.

    Selection priority:
    1. Location match (must match)
    2. Weight range match (must fit)
    3. Highest specificity score (postal > city > country)
    4. Tightest weight range (smallest gap)
    5. Lowest rate (tie-breaker)

    Returns:
        Best matching zone, or None if no matches found
    """
    matching_zones: typing.List[typing.Tuple[int, float, float, models.ServiceZone]] = (
        []
    )

    for zone in zones:
        # Must match location
        if not check_location_match(zone, recipient):
            continue

        # Must fit weight range
        if not check_weight_match(zone, package, service):
            continue

        # Calculate metrics for sorting
        specificity = calculate_zone_specificity(zone)
        weight_range = (zone.max_weight or float("inf")) - (zone.min_weight or 0)
        rate = zone.rate or 0.0

        # Store as tuple: (specificity, weight_range, rate, zone)
        matching_zones.append((specificity, weight_range, rate, zone))

    if not matching_zones:
        return None

    # Sort by priority:
    # 1. Highest specificity (descending) - use negative
    # 2. Tightest weight range (ascending)
    # 3. Lowest rate (ascending)
    best_match = min(matching_zones, key=lambda t: (-t[0], t[1], t[2]))

    return best_match[3]  # Return the zone


def get_available_rates(
    package: units.Package,
    shipper: units.ComputedAddress,
    recipient: units.ComputedAddress,
    settings: RatingMixinSettings,
    is_domicile: bool = None,
    is_international: bool = None,
    selected_services: typing.List[str] = [],
) -> PackageRates:
    errors: typing.List[models.Message] = []
    rates: typing.List[models.RateDetails] = []
    services = [svc for svc in settings.shipping_services if svc.active]

    for service in services:
        # Check if service requested
        explicitly_requested = service.service_code in selected_services
        implicitly_requested = len(selected_services or []) == 0
        excluded = len(selected_services or []) > 0 and not explicitly_requested

        if not service.active or excluded:
            continue

        # Check if destination covered
        # Service explicitly supports domestic shipments
        cover_domestic_shipment = service.domicile is True and is_domicile is True

        # Service explicitly supports international shipments
        cover_international_shipment = (
            service.international is True and is_international is True
        )

        # Service supports all destinations (both flags None OR both flags True)
        cover_all_destination = (
            service.domicile is None and service.international is None
        ) or (service.domicile is True and service.international is True)
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
            <= units.Dimension(service.max_length or 0, service.dimension_unit).value
        ) or (service.max_length is None)
        match_height_requirements = (
            service.max_height is not None
            and package.height[service.dimension_unit]
            <= units.Dimension(service.max_height, service.dimension_unit).value
        ) or (service.max_height is None)
        match_width_requirements = (
            service.max_width is not None
            and package.width[service.dimension_unit]
            <= units.Dimension(service.max_width, service.dimension_unit).value
        ) or (service.max_width is None)
        match_min_weight_requirements = (
            service.min_weight is not None
            and package.weight[service.weight_unit]
            >= units.Weight(service.min_weight, service.weight_unit).value
        ) or (service.min_weight is None)
        match_max_weight_requirements = (
            service.max_weight is not None
            and package.weight[service.weight_unit]
            <= units.Weight(service.max_weight, service.weight_unit).value
        ) or (service.max_weight is None)

        # resolve matching zone using improved algorithm
        selected_zone: typing.Optional[models.ServiceZone] = find_best_matching_zone(
            zones=service.zones or [],
            package=package,
            recipient=recipient,
            service=service,
        )

        # error validations
        if explicitly_requested and not explicit_destination_covered:
            errors.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code="destination_not_supported",
                    message=f"the service {service.service_code} does not cover the requested destination",
                )
            )
        if (
            explicitly_requested
            and destination_covered
            and service.max_length is not None
            and not match_length_requirements
        ):
            errors.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code="invalid_dimension",
                    message=f"length size exceeds service {service.service_code} max length",
                )
            )
        if (
            explicitly_requested
            and destination_covered
            and service.max_height is not None
            and not match_height_requirements
        ):
            errors.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code="invalid_dimension",
                    message=f"height size exceeds service {service.service_code} max height",
                )
            )
        if (
            explicitly_requested
            and destination_covered
            and service.max_width is not None
            and not match_width_requirements
        ):
            errors.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code="invalid_dimension",
                    message=f"the width size exceeds service {service.service_code} max width",
                )
            )
        if (
            explicitly_requested
            and destination_covered
            and service.max_weight is not None
            and not match_max_weight_requirements
        ):
            errors.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code="invalid_weight",
                    message=f"the weight exceeds service {service.service_code} max weight",
                )
            )

        if (
            destination_covered
            and match_length_requirements
            and match_height_requirements
            and match_width_requirements
            and match_min_weight_requirements
            and match_max_weight_requirements
            and selected_zone is not None
        ):
            carrier_name = getattr(
                settings,
                "custom_carrier_name",
                settings.carrier_name,
            )
            transit_days = (
                service.transit_days
                if selected_zone.transit_days is None
                else selected_zone.transit_days
            )

            rates.append(
                models.RateDetails(
                    carrier_name=carrier_name,
                    carrier_id=settings.carrier_id,
                    service=service.service_code,
                    currency=service.currency,
                    transit_days=transit_days,
                    total_charge=selected_zone.rate,
                    extra_charges=[
                        models.ChargeDetails(
                            name="Base Charge",
                            amount=selected_zone.rate,
                            currency=service.currency,
                        )
                    ],
                    meta=lib.to_dict(  # type: ignore
                        dict(
                            carrier_service_code=service.carrier_service_code,
                            service_name=service.service_name,
                        )
                    ),
                )
            )

    return rates, errors
