import karrio.schemas.zoom2u.shipping_request as zoom2u
import karrio.schemas.zoom2u.shipping_response as shipping
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.zoom2u.error as error
import karrio.providers.zoom2u.utils as provider_utils
import karrio.providers.zoom2u.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    shipment = _extract_details(response, settings) if len(messages) == 0 else None

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    shipment = lib.to_object(shipping.ShippingResponseType, data)

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.reference,
        shipment_identifier=shipment.reference,
        label_type="PDF",
        docs=models.Documents(label="No label..."),
        meta=dict(
            trackingCode=shipment.trackingCode,
            carrier_tracking_link=shipment.trackinglink,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    package = lib.to_packages(payload.parcels).single
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=package.options,
        option_type=provider_units.ShippingOption,
    )

    request = zoom2u.ShippingRequestType(
        PurchaseOrderNumber=options.purchase_order_number.state or payload.reference,
        PackageDescription=package.description,
        DeliverySpeed=service,
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
