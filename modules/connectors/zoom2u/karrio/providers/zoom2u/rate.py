import karrio.schemas.zoom2u.rate_request as zoom2u
import karrio.schemas.zoom2u.rate_response as rating
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.zoom2u.error as error
import karrio.providers.zoom2u.utils as provider_utils
import karrio.providers.zoom2u.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    _responses = _response.deserialize()
    responses = _responses if isinstance(_responses, list) else [_responses]

    messages = error.parse_error_response(responses, settings)
    rates = [
        _extract_details(rate, settings)
        for rate in responses
        if rate.get("message") is None
    ]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate = lib.to_object(rating.RateResponseElementType, data)
    service = provider_units.ShippingService.map(rate.deliverySpeed)

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        total_charge=lib.to_money(rate.price),
        currency=settings.connection_config.currency.state or "AUD",
        transit_days=1,
        estimated_delivery=lib.fdate(rate.deliveredBy, "%Y-%m-%dT%H:%M:%S%z"),
        meta=dict(
            service_name=service.value_or_key,
            earliestPickupEta=rate.earliestPickupEta,
            earliestDropEta=rate.earliestDropEta,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    package = lib.to_packages(payload.parcels).single
    service = lib.to_services(payload.services, provider_units.ShippingService).first
    options = lib.to_shipping_options(
        payload.options,
        package_options=package.options,
        option_type=provider_units.ShippingOption,
    )

    request = zoom2u.RateRequestType(
        PurchaseOrderNumber=options.purchase_order_number.state or payload.reference,
        PackageDescription=package.description,
        DeliverySpeed=getattr(service, "value", None),
        ReadyDateTime=lib.fdatetime(
            options.ready_datetime.state,
            current_format="%Y-%m-%d %H:%M:%S",
            output_format="%Y-%m-%dT%H:%M:%S.%fZ",
        ),
        VehicleType=provider_units.VehiculeType.map(
            options.vehicle_type.state or "Car"
        ).value,
        PackageType=provider_units.PackagingType.map(
            package.packaging_type or "Box"
        ).value,
        Pickup=zoom2u.DropoffType(
            ContactName=shipper.contact,
            Email=shipper.email,
            Phone=shipper.phone_number,
            UnitNumber=None,
            StreetNumber=shipper.street_number,
            Street=shipper.street_name,
            Suburb=shipper.city,
            State=shipper.state_code,
            Postcode=shipper.postal_code,
            Country=shipper.country_name,
            Notes=options.pickup_notes.state,
        ),
        Dropoff=zoom2u.DropoffType(
            ContactName=recipient.contact,
            Email=recipient.email,
            Phone=recipient.phone_number,
            UnitNumber=None,
            StreetNumber=recipient.street_number,
            Street=recipient.street_name,
            Suburb=recipient.city,
            State=recipient.state_code,
            Postcode=recipient.postal_code,
            Country=recipient.country_name,
            Notes=options.dropoff_notes.state,
        ),
    )

    return lib.Serializable(request, lib.to_dict)
