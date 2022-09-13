import ups_freight_lib.tracking_response as ups
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.ups_freight.error as error
import karrio.providers.ups_freight.utils as provider_utils


def parse_tracking_response(
    responses: typing.List[typing.Tuple[str, dict]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    packages = [
        result["trackResponse"]["shipment"][0]
        for _, result in responses
        if "trackResponse" in result
        and result["trackResponse"]["shipment"][0].get("package") is not None
    ]
    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(
                [
                    *(  # get errors from the response object returned by UPS
                        result["response"].get("errors", [])
                        if "response" in result
                        else []
                    ),
                    *(  # get warnings from the trackResponse object returned by UPS
                        result["trackResponse"]["shipment"][0].get("warnings", [])
                        if "trackResponse" in result
                        else []
                    ),
                ],
                settings,
                details=dict(tracking_number=tracking_number),
            )
            for tracking_number, result in responses
        ],
        [],
    )

    details = [_extract_details(package, settings) for package in packages]

    return details, messages


def _extract_details(
    detail: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    package: ups.PackageType = next(
        iter(lib.to_object(ups.ShipmentType, detail).package)
    )
    delivered = any(a.status.type == "D" for a in package.activity)
    estimated_delivery = next(
        iter([d.date for d in package.deliveryDate if d.type == "DEL"]), None
    )

    return models.TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=package.trackingNumber,
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
                    if a.location
                    else None
                ),
                time=lib.ftime(a.time, "%H%M%S"),
                code=a.status.code if a.status else None,
            )
            for a in package.activity
        ],
        delivered=delivered,
        estimated_delivery=lib.fdate(estimated_delivery, "%Y%m%d"),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable[typing.List[lib.Envelope]]:
    return lib.Serializable(payload.tracking_numbers)
