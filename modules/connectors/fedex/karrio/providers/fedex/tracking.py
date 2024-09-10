import karrio.schemas.fedex.tracking_request as fedex
import karrio.schemas.fedex.tracking_response as tracking
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.fedex.error as provider_error
import karrio.providers.fedex.utils as provider_utils
import karrio.providers.fedex.units as provider_units

DATETIME_FORMATS = ["%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"]


def parse_tracking_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    results = response.get("output", {}).get("completeTrackResults") or []
    details = [
        _extract_details(result, settings)
        for result in results
        if result.get("trackResults") is not None
        and result["trackResults"][0].get("scanEvents") is not None
    ]
    messages: typing.List[models.Message] = sum(
        [
            provider_error.parse_error_response(
                result.get("trackResults"),
                settings,
                tracking_number=result.get("trackingNumber"),
            )
            for result in results
            if result.get("trackResults") is not None
        ],
        start=provider_error.parse_error_response(response, settings),
    )

    return details, messages


def _extract_details(
    result: dict,
    settings: provider_utils.Settings,
) -> typing.Optional[models.TrackingDetails]:
    package = lib.to_object(tracking.CompleteTrackResultType, result)
    detail = max(
        package.trackResults,
        key=lambda item: max(
            lib.to_date(event.date, try_formats=DATETIME_FORMATS).replace(tzinfo=None)
            for event in item.scanEvents
        ),
        default=None,
    )
    estimated_delivery = lib.failsafe(
        lambda: lib.fdate(
            detail.standardTransitTimeWindow.window.begins
            or detail.estimatedDeliveryTimeWindow.window.begins,
            try_formats=DATETIME_FORMATS,
        )
    )
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if detail.latestStatusDetail.code in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )
    delivered = status == "delivered"
    img = lib.failsafe(
        lambda: (
            provider_utils.get_proof_of_delivery(package.trackingNumber, settings)
            if delivered
            else None
        )
    )

    return models.TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=package.trackingNumber,
        events=[
            models.TrackingEvent(
                date=lib.fdate(e.date, try_formats=DATETIME_FORMATS),
                time=lib.flocaltime(e.date, try_formats=DATETIME_FORMATS),
                code=e.eventType,
                location=lib.identity(
                    lib.join(
                        e.scanLocation.city,
                        e.scanLocation.stateOrProvinceCode,
                        e.scanLocation.postalCode,
                        e.scanLocation.countryCode,
                        join=True,
                        separator=", ",
                    )
                    if e.scanLocation
                    else e.locationType
                ),
                description=(lib.text(e.exceptionDescription) or e.eventDescription),
            )
            for e in detail.scanEvents
        ],
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(package.trackingNumber),
            shipment_service=lib.failsafe(lambda: detail.serviceDetail.description),
            package_weight_unit=lib.failsafe(
                lambda: detail.shipmentDetails.weight[0].unit
            ),
            package_weight=lib.failsafe(
                lambda: lib.to_decimal(detail.shipmentDetails.weight[0].value)
            ),
            shipment_destination_postal_code=lib.failsafe(
                lambda: detail.destinationLocation.locationContactAndAddress.address.postalCode
            ),
            shipment_destination_country=lib.failsafe(
                lambda: detail.destinationLocation.locationContactAndAddress.address.countryCode
            ),
            shipment_origin_postal_code=lib.failsafe(
                lambda: detail.originLocation.locationContactAndAddress.address.postalCode
            ),
            shipment_origin_country=lib.failsafe(
                lambda: detail.originLocation.locationContactAndAddress.address.countryCode
            ),
            signed_by=lib.failsafe(lambda: detail.deliveryDetails.signedByName),
        ),
        images=lib.identity(models.Images(signature_image=img) if img else None),
        estimated_delivery=estimated_delivery,
        delivered=(status == "delivered"),
        status=status,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = fedex.TrackingRequestType(
        includeDetailedScans=True,
        trackingInfo=[
            fedex.TrackingInfoType(
                shipDateBegin=None,
                shipDateEnd=None,
                trackingNumberInfo=fedex.TrackingNumberInfoType(
                    trackingNumber=tracking_number,
                    carrierCode=None,
                    trackingNumberUniqueId=None,
                ),
            )
            for tracking_number in payload.tracking_numbers
        ],
    )

    return lib.Serializable(request, lib.to_dict)
