import karrio.schemas.ups.tracking_response as ups
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.ups.error as error
import karrio.providers.ups.utils as provider_utils
import karrio.providers.ups.units as provider_units


def parse_tracking_response(
    _responses: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _responses.deserialize()
    packages = [
        result["trackResponse"]["shipment"][0]
        for _, result in responses
        if "trackResponse" in result
        and result["trackResponse"]["shipment"][0].get("package") is not None
    ]
    messages: typing.List[models.Message] = error.parse_error_response(
        [response for _, response in responses],
        settings=settings,
    )
    details = [_extract_details(package, settings) for package in packages]

    return details, messages


def _extract_details(
    detail: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    shipment: ups.ShipmentType = lib.to_object(ups.ShipmentType, detail)
    package: ups.PackageType = shipment.package[0]
    origin = next(
        (p for p in package.packageAddress or [] if p.type == "DESTINATION"), None
    )
    destination = next(
        (p for p in package.packageAddress or [] if p.type == "DESTINATION"), None
    )
    delivered = any(a.status.type == "D" for a in package.activity)
    estimated_delivery = next(
        iter([d.date for d in package.deliveryDate if d.type == "DEL"]), None
    )
    signature_image = lib.failsafe(
        lambda: getattr(package.deliveryInformation.signature, "image", None)
    )
    delivery_image = lib.failsafe(
        lambda: getattr(package.deliveryInformation.deliveryPhoto, "photo", None)
    )
    last_event = package.activity[0]
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if getattr(last_event.status, "type", None) in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=package.trackingNumber,
        estimated_delivery=lib.fdate(estimated_delivery, "%Y%m%d"),
        delivered=delivered,
        status=status,
        events=[
            models.TrackingEvent(
                date=lib.fdate(a.date, "%Y%m%d"),
                description=a.status.description if a.status else None,
                location=(
                    lib.join(
                        a.location.address.city,
                        a.location.address.stateProvince,
                        a.location.address.postalCode,
                        a.location.address.country,
                        join=True,
                        separator=", ",
                    )
                    if a.location and a.location.address
                    else None
                ),
                time=lib.flocaltime(a.time, "%H%M%S"),
                code=getattr(last_event.status, "code", None),
            )
            for a in package.activity
        ],
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(package.trackingNumber),
            signed_by=getattr(package.deliveryInformation, "receivedBy", None),
            shipment_service=getattr(package.service, "description", None),
            package_weight=getattr(package.weight, "weight", None),
            package_weight_unit=getattr(package.weight, "unitOfMeasurement", None),
            shipment_origin_country=(
                getattr(origin.address, "country", None) if origin else None
            ),
            shipment_origin_postal_code=(
                getattr(origin.address, "postalCode", None) if origin else None
            ),
            shipment_destination_country=(
                getattr(destination.address, "country", None) if origin else None
            ),
            shipment_destination_postal_code=(
                getattr(destination.address, "postalCode", None) if origin else None
            ),
            customer_name=(
                destination.attentionName or destination.name if destination else None
            ),
        ),
        images=models.Images(
            delivery_image=delivery_image,
            signature_image=signature_image,
        ),
    )


def tracking_request(payload: models.TrackingRequest, _) -> lib.Serializable:
    return lib.Serializable(payload.tracking_numbers)
