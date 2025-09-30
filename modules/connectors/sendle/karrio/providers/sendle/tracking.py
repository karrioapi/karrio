import karrio.schemas.sendle.tracking_request as sendle
import karrio.schemas.sendle.tracking_response as tracking
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.sendle.error as error
import karrio.providers.sendle.utils as provider_utils
import karrio.providers.sendle.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(response, settings, tracking_number=_)
            for _, response in responses
        ],
        start=[],
    )
    tracking_details = [
        _extract_details(details, settings, dict(tracking_number=_))
        for _, details in responses
        if details.get("tracking_events") is not None
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict,
) -> models.TrackingDetails:
    tracking_number = ctx.get("tracking_number")
    details = lib.to_object(tracking.TrackingResponseType, data)
    events = reversed(details.tracking_events)
    estimated_delivery = (
        details.scheduling.estimated_delivery_date_minimum
        or details.scheduling.estimated_delivery_date_maximum
        or details.scheduling.delivered_on
    )
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if details.state in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        events=[
            models.TrackingEvent(
                date=lib.fdatetime(
                    event.local_scan_time or event.scan_time,
                    try_formats=["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"],
                    output_format="%Y-%m-%d",
                ),
                description=event.description,
                location=(
                    lib.text(
                        event.origin_location,
                        event.destination_location,
                        separator=" to ",
                    )
                    if (event.origin_location and event.destination_location)
                    else event.location
                ),
                code=event.event_type,
                time=lib.fdatetime(
                    event.local_scan_time or event.scan_time,
                    try_formats=["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"],
                    output_format="%H:%M %p",
                ),
            )
            for event in events
        ],
        estimated_delivery=lib.fdate(estimated_delivery, "%Y-%m-%d"),
        delivered=status == provider_units.TrackingStatus.delivered.name,
        status=status,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = [sendle.TrackingRequestType(ref=ref) for ref in payload.tracking_numbers]

    return lib.Serializable(request, lib.to_dict)
