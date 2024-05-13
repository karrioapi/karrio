import karrio.schemas.eshipper.tracking_request as eshipper
import karrio.schemas.eshipper.tracking_response as tracking
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.eshipper.error as error
import karrio.providers.eshipper.utils as provider_utils
import karrio.providers.eshipper.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[typing.Union[dict, typing.List[dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    responses = response if isinstance(response, list) else [response]

    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(
                _, settings, tracking_number=_.get("trackingNumber")
            )
            for _ in responses
        ],
        start=[],
    )
    tracking_details = [
        _extract_details(_, settings)
        for _ in responses
        if _.get("trackingNumber") is not None
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    details = lib.to_object(tracking.TrackingResponseElementType, data)

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=details.trackingNumber,
        events=[
            models.TrackingEvent(
                code=event.originalEvent.name,
                location=event.location,
                description=event.description,
                date=lib.fdate(event.originalEvent.eventDate, "%Y-%m-%d %H:%M:%S"),
                time=lib.flocaltime(event.originalEvent.eventDate, "%Y-%m-%d %H:%M:%S"),
            )
            for event in details.event
        ],
        estimated_delivery=lib.fdate(details.expectedDeliveryDate, "%Y-%m-%d %H:%M:%S"),
        delivered=details.shipmentStatus.delivered,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = eshipper.TrackingRequestType(
        trackingNumbers=payload.tracking_numbers,
        includePublished=True,
        pageable=lib.to_json({"page": 0, "size": 25, "sort": []}),
    )

    return lib.Serializable(request, lib.to_dict)
