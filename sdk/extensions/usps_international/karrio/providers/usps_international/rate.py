from datetime import datetime, timezone
from usps_lib.intl_rate_v2_request import (
    IntlRateV2Request,
    PackageType,
    ExtraServicesType,
    GXGType,
)
from usps_lib.intl_rate_v2_response import ServiceType

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.providers.usps_international.error as provider_error
import karrio.providers.usps_international.units as provider_units
import karrio.providers.usps_international.utils as provider_utils


def parse_rate_response(
    response: lib.Element, settings: provider_utils.Settings
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    quotes: typing.List[models.RateDetails] = [
        _extract_details(package, settings)
        for package in lib.find_element("Service", response)
    ]
    return quotes, provider_error.parse_error_response(response, settings)


def _extract_details(
    postage_node: lib.Element, settings: provider_utils.Settings
) -> models.RateDetails:
    postage: ServiceType = lib.to_object(ServiceType, postage_node)
    service = provider_units.ServiceClassID.map(str(postage.ID))
    delivery_date = lib.to_date(postage.GuaranteeAvailability, "%m/%d/%Y")
    transit = (
        (delivery_date.date() - datetime.now().date()).days
        if delivery_date is not None
        else None
    )

    charges = [
        ("Base charge", postage.Postage),
        *((s.ServiceName, s.Price) for s in postage.ExtraServices.ExtraService),
    ]

    return models.RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        service=service.name_or_key,
        total_charge=lib.to_decimal(postage.Postage),
        currency=units.Currency.USD.name,
        transit_days=transit,
        extra_charges=[
            models.ChargeDetails(
                name=name,
                amount=lib.to_decimal(amount),
                currency=units.Currency.USD.name,
            )
            for name, amount in charges
            if amount
        ],
        meta=dict(service_name=service.name or postage.SvcDescription),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable[IntlRateV2Request]:
    """Create the appropriate USPS International rate request depending on the destination

    :param payload: Karrio unified API rate request data
    :param settings: USPS International connection and auth settings
    :return: a domestic or international USPS International compatible request
    :raises:
        - OriginNotServicedError when origin country is not serviced by the carrier
        - DestinationNotServicedError when destination country is US
    """

    if (
        payload.shipper.country_code is not None
        and payload.shipper.country_code != units.Country.US.name
    ):
        raise errors.OriginNotServicedError(payload.shipper.country_code)

    if payload.recipient.country_code == units.Country.US.name:
        raise errors.DestinationNotServicedError(payload.recipient.country_code)

    recipient = lib.to_address(payload.recipient)
    services = lib.to_services(payload.services, provider_units.ShippingService)
    package = lib.to_packages(
        payload.parcels,
        package_option_type=provider_units.ShippingOption,
        max_weight=units.Weight(70, units.WeightUnit.LB),
    ).single
    options = lib.to_shipping_options(
        payload.options,
        package_options=package.options,
        initializer=provider_units.shipping_options_initializer,
    )

    commercial = next(("Y" for svc in services if "commercial" in svc.name), "N")
    commercial_plus = next(("Y" for svc in services if "plus" in svc.name), "N")
    acceptance_date = (
        datetime.isoformat((options.shipment_date.state or datetime.now(timezone.utc)),
    ) if recipient.postal_code else None)

    request = IntlRateV2Request(
        USERID=settings.username,
        Revision="2",
        Package=[
            PackageType(
                ID=0,
                Pounds=0,
                Ounces=package.weight.OZ,
                Machinable=options.usps_option_machinable_item.state or False,
                MailType=provider_units.PackagingType[
                    package.packaging_type or "package"
                ].value,
                GXG=(
                    GXGType(POBoxFlag="N", GiftFlag="N")
                    if any(
                        "global_express_guaranteed" in s.name for s in payload.services
                    )
                    else None
                ),
                ValueOfContents=(options.declared_value.state or ""),
                Country=recipient.country_name,
                Width=package.width.IN,
                Length=package.length.IN,
                Height=package.height.IN,
                Girth=(
                    package.girth.value if package.packaging_type == "tube" else None
                ),
                OriginZip=payload.shipper.postal_code,
                CommercialFlag=commercial,
                CommercialPlusFlag=commercial_plus,
                AcceptanceDateTime=acceptance_date,
                DestinationPostalCode=recipient.postal_code,
                ExtraServices=(
                    ExtraServicesType(
                        ExtraService=[option.code for _, option in options.items()]
                    )
                    if any(options.items())
                    else None
                ),
                Content=None,
            )
        ],
    )

    return lib.Serializable(request, lib.to_xml)
