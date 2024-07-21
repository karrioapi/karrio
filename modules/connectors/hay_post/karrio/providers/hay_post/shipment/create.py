import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.hay_post.error as error
import karrio.providers.hay_post.utils as provider_utils
import karrio.providers.hay_post.units as provider_units
import karrio.schemas.hay_post.order_create_request as hay_post
import karrio.schemas.hay_post.order_create_response as hay_post_response


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    shipment = (
        _extract_details(response, settings) if response.get("key") is None else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    shipment = lib.to_object(hay_post_response.OrderCreateResponseType, data)
    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.barcode,
        shipment_identifier=str(shipment.id),
        docs=models.Documents(
            label="No label...",
        ),
        meta=dict(
            revertOrderId=shipment.revertOrderId,
            revertBarcode=shipment.revertBarcode,
            postalcode=shipment.postalcode,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service)

    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    additional_services = [
        int(service.value.code)
        for service in provider_units.ShippingOption
        if service.name in options
    ]

    shipper_country_id = lib.to_int(
        provider_units.ShippingCountries.map(shipper.country_code).value
    )
    recipient_country_id = lib.to_int(
        provider_units.ShippingCountries.map(recipient.country_code).value
    )

    request = hay_post.OrderCreateRequestType(
        customerId=int(settings.customer_id),
        serviceCategoryDirectionId=service.value,
        weight=packages.weight.value,
        destinationAddress=hay_post.NAddressType(
            countryId=recipient_country_id,
            street=recipient.street,
            cityVillage=recipient.city,
            postalCode=recipient.postal_code,
            receiverInfo=hay_post.ReceiverInfoType(
                companyName=recipient.company_name,
                firstName=recipient.person_name,
                phoneNumber=recipient.phone_number,
                email=recipient.email,
            ),
        ),
        returnAddress=hay_post.NAddressType(
            countryId=shipper_country_id,
            street=shipper.street,
            cityVillage=shipper.city,
            postalCode=shipper.postal_code,
            receiverInfo=hay_post.ReceiverInfoType(
                companyName=shipper.company_name,
                firstName=shipper.person_name,
                phoneNumber=shipper.phone_number,
                email=shipper.email,
            ),
        ),
        additionalServices=additional_services,
    )

    return lib.Serializable(request, lib.to_dict)
