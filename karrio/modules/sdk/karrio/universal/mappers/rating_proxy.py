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

        # resolve matching zone
        selected_zone: typing.Optional[models.ServiceZone] = None

        for zone in service.zones or []:
            # Check Location inclusion
            _cover_supported_cities = (
                zone.cities is not None
                and recipient.city is not None
                and recipient.city.lower() in [_.lower() for _ in zone.cities]
            ) or not any(zone.cities or [])
            _cover_supported_countries = (
                zone.country_codes is not None
                and recipient.country_code in zone.country_codes
            ) or not any(zone.country_codes or [])
            _cover_supported_postal_codes = (
                zone.postal_codes is not None
                and recipient.postal_code is not None
                and str(recipient.postal_code).lower()
                in [str(_).lower() for _ in zone.postal_codes]
            ) or not any(zone.postal_codes or [])

            # Check if weight and dimensions fit restrictions
            _match_zone_min_weight_requirements = (
                zone.min_weight is not None
                and package.weight[service.weight_unit]
                >= units.Weight(zone.min_weight, service.weight_unit).value
            ) or (zone.min_weight is None)
            _match_zone_max_weight_requirements = (
                zone.max_weight is not None
                and package.weight[service.weight_unit]
                <= units.Weight(zone.max_weight, service.weight_unit).value
            ) or (zone.max_weight is None)

            # Check if best fit zone is selected
            _best_fit_zone_selected = (
                selected_zone is not None
                and selected_zone.max_weight is not None
                and (
                    selected_zone.rate < zone.rate
                    or (
                        selected_zone.max_weight is not None
                        and zone.max_weight is not None
                        and selected_zone.max_weight < zone.max_weight
                    )
                    or (
                        selected_zone.min_weight is not None
                        and zone.min_weight is not None
                        and selected_zone.min_weight < zone.min_weight
                    )
                )
            )

            if (
                _cover_supported_cities
                and _cover_supported_countries
                and _cover_supported_postal_codes
                and _match_zone_min_weight_requirements
                and _match_zone_max_weight_requirements
                and _best_fit_zone_selected is False
            ):
                selected_zone = zone

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
                    meta=dict(service_name=service.service_name),
                )
            )

    return rates, errors
