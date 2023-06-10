import postnl_lib.rate_request as pnl
import postnl_lib.rate_response as pnl_response
import typing
import datetime
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.providers.postnl.error as error
import karrio.providers.postnl.utils as provider_utils
import karrio.providers.postnl.units as provider_units


def parse_rate_response(
    response: dict,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response_messages = []  # extract carrier response errors
    response_rates = []  # extract carrier response rates

    messages = error.parse_error_response(response_messages, settings)
    rates = [_extract_details(rate, settings) for rate in response_rates]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate = None  # parse carrier rate type

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service="",  # extract service from rate
        total_charge=0.0,  # extract the rate total rate cost
        currency="",  # extract the rate pricing currency
        transit_days=0,  # extract the rate transit days
        meta=dict(
            service_name="",  # extract the rate service human readable name
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels, max_weight=15)
    services = lib.to_services(payload.services, provider_units.ShippingService)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        option_type=provider_units.ShippingOption,
    )

    if len(packages) > 2:
        errors.FieldError(
            {"parcels": "Post NL does not support more than 2 packages per shipment."}
        )

    request = pnl.RateRequestType(
        OrderDate=lib.fdatetime(
            (options.shipment_date or datetime.datetime.now()),
            "%d-%m-%Y %H:%M:%S",
        ),
        ShippingDuration=1,
        CutOffTimes=[pnl.CutOffTimeType(Day="00")],
        HolidaySorting=options.holiday_sorting.state,
        Options=[_.value for _ in services],
        Locations=2,
        Days=2,
        Addresses=[
            pnl.AddressType(
                AddressType="02",
                Street=shipper.address_line,
                HouseNr=shipper.street_number,
                HouseNrExt=None,
                Zipcode=shipper.postal_code,
                City=shipper.city,
                Countrycode=shipper.country_code,
            ),
            pnl.AddressType(
                AddressType="01",
                Street=recipient.address_line,
                HouseNr=recipient.street_number,
                HouseNrExt=None,
                Zipcode=recipient.postal_code,
                City=recipient.city,
                Countrycode=recipient.country_code,
            ),
        ],
    )

    return lib.Serializable(request, lib.to_dict)
