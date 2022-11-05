from datetime import datetime
from usps_lib.rate_v4_response import PostageType, SpecialServiceType
from usps_lib.rate_v4_request import (
    RateV4Request,
    PackageType,
    SpecialServicesType,
    ShipDateType,
)

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.providers.usps.error as provider_error
import karrio.providers.usps.units as provider_units
import karrio.providers.usps.utils as provider_utils


def parse_rate_response(
    response: lib.Element, settings: provider_utils.Settings
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    rates: typing.List[models.RateDetails] = [
        _extract_details(package, settings)
        for package in lib.find_element("Postage", response)
    ]
    return rates, provider_error.parse_error_response(response, settings)


def _extract_details(
    postage_node: lib.Element, settings: provider_utils.Settings
) -> models.RateDetails:
    postage: PostageType = lib.to_object(PostageType, postage_node)

    service = provider_units.ServiceClassID.map(str(postage.CLASSID))
    charges: typing.List[SpecialServiceType] = getattr(
        postage.SpecialServices, "SpecialService", []
    )
    rate = lib.to_decimal((
        lib.find_element("CommercialPlusRate", postage_node, first=True) or
        lib.find_element("CommercialRate", postage_node, first=True) or
        lib.find_element("Rate", postage_node, first=True)
    ).text)
    commitment_date_node = lib.find_element("CommitmentDate", postage_node, first=True)
    estimated_date = lib.to_date(getattr(commitment_date_node, "text", None))
    transit = (
        (estimated_date.date() - datetime.now().date()).days
        if estimated_date is not None
        else None
    )

    return models.RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        service=service.name_or_key,
        total_charge=rate,
        currency=units.Currency.USD.name,
        transit_days=transit,
        extra_charges=[
            models.ChargeDetails(
                name=charge.ServiceName,
                amount=lib.to_decimal(charge.Price),
                currency=units.Currency.USD.name,
            )
            for charge in charges
        ],
        meta=dict(service_name=(service.name or postage.MailService)),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable[RateV4Request]:
    """Create the appropriate USPS rate request depending on the destination

    :param payload: Karrio unified API rate request data
    :param settings: USPS connection and auth settings
    :return: a domestic or international USPS compatible request
    :raises: an OriginNotServicedError when origin country is not serviced by the carrier
    """

    if (
        payload.shipper.country_code is not None
        and payload.shipper.country_code != units.Country.US.name
    ):
        raise errors.OriginNotServicedError(payload.shipper.country_code)

    if (
        payload.recipient.country_code is not None
        and payload.recipient.country_code != units.Country.US.name
    ):
        raise errors.DestinationNotServicedError(payload.recipient.country_code)

    package = lib.to_packages(
        payload.parcels, package_option_type=provider_units.ShippingOption
    ).single
    container = provider_units.PackagingType[package.packaging_type or "your_packaging"]
    options = lib.to_shipping_options(
        payload.options,
        package_options=package.options,
        initializer=provider_units.shipping_options_initializer,
    )
    service = (
        units.Services(payload.services, provider_units.ShipmentService).first
        or provider_units.ShipmentService.usps_all
    )

    request = RateV4Request(
        USERID=settings.username,
        Revision="2",
        Package=[
            PackageType(
                ID=0,
                Service=service.value,
                FirstClassMailType=(
                    provider_units.FirstClassMailType[container.name].value
                    if "first_class" in service.value
                    else None
                ),
                ZipOrigination=payload.shipper.postal_code,
                ZipDestination=payload.recipient.postal_code,
                Pounds=0,
                Ounces=package.weight.OZ,
                Container=container.value,
                Width=package.width.IN,
                Length=package.length.IN,
                Height=package.height.IN,
                Girth=(
                    package.girth.value if package.packaging_type == "tube" else None
                ),
                Value=options.declared_value.state,
                AmountToCollect=options.cash_on_delivery.state,
                SpecialServices=(
                    SpecialServicesType(
                        SpecialService=[option.code for _, option in options.items()]
                    )
                    if any(options.items())
                    else None
                ),
                Content=None,
                GroundOnly=options.usps_option_ground_only.state,
                SortBy=(
                    provider_units.SortLevelType[container.name].value
                    if service.value in ["All", "Online"]
                    else None
                ),
                Machinable=(options.usps_option_machinable_item.state or False),
                ReturnLocations=options.usps_option_return_service_info.state,
                ReturnServiceInfo=options.usps_option_return_service_info.state,
                DropOffTime=(
                    "13:30" if options.shipment_date.state is not None else None
                ),
                ShipDate=(
                    ShipDateType(valueOf_=lib.fdate(options.shipment_date.state))
                    if options.shipment_date.state is not None
                    else None
                ),
            )
        ],
    )

    return lib.Serializable(request, lib.to_xml)
