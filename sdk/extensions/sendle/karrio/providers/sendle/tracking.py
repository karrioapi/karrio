import sendle_lib.tracking_response as sendle
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.sendle.error as error
import karrio.providers.sendle.utils as provider_utils


def parse_tracking_response(
    response: typing.List[typing.Tuple[str, dict]], settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    errors = [e for ref, e in response if "error" in e]
    tracking_details = [
        _extract_detail((ref, lib.to_object(sendle.Tracking, d)), settings)
        for ref, d in response
        if "tracking_events" in d
    ]

    return tracking_details, error.parse_error_response(errors, settings)


def _extract_detail(
    detail: typing.Tuple[str, sendle.Tracking], settings: provider_utils.Settings
) -> models.TrackingDetails:
    tracking_number, tracking_details = detail
    estimated_delivery = (
        tracking_details.scheduling.estimated_delivery_date_minimum
        or tracking_details.scheduling.estimated_delivery_date_maximum
        or tracking_details.scheduling.delivered_on
    )

    return models.TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking_number,
        events=[
            models.TrackingEvent(
                date=lib.fdatetime(
                    getattr(event, "local_scan_time", None) or event.scan_time,
                    try_formats=["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"],
                    output_format="%Y-%m-%d",
                ),
                description=event.description,
                location=(
                    lib.text(event.origin_location, event.destination_location, separator=" to ")
                    if (event.origin_location and event.destination_location)
                    else event.location
                ),
                code=event.event_type,
                time=lib.fdatetime(
                    getattr(event, "local_scan_time", None) or event.scan_time,
                    try_formats=["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"],
                    output_format="%H:%M",
                ),
            )
            for event in reversed(tracking_details.tracking_events)
        ],
        estimated_delivery=lib.fdate(estimated_delivery, "%Y-%m-%d"),
        delivered=(tracking_details.state == "Delivered"),
    )


def tracking_request(payload: models.TrackingRequest, _) -> lib.Serializable[list]:
    request = payload.tracking_numbers

    return lib.Serializable(request)
