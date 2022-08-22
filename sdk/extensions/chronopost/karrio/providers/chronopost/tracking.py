import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.chronopost.utils as provider_utils
import chronopost_lib.trackingservice as chronopost


def parse_tracking_response(
    responses: typing.List[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response_messages = [
        result for result in responses if result.get("errorCode") != "0"
    ]
    response_details = [
        result[0]
        for result in responses
        if result.get("code") == "0" and next(iter(result), None) is not None
    ]
    messages = [_extract_errors(response_messages, settings)]
    tracking_details = [_extract_details(rate, settings) for rate in response_details]

    return tracking_details, messages


def _extract_errors(
    data: lib.Element,
    settings: provider_utils.Settings,
) -> models.Message:
    return models.Message(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        message=data.get("errorMessage"),
        code=data.get("errorCode"),
    )


def _extract_details(
    data: lib.Element,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    tracking = lib.to_object(chronopost.resultTrackSkybillV2, data)
    events: typing.List[chronopost.eventInfoComp] = (
        [event for event in tracking.listEventInfoComp] if tracking is not None else []
    )
    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking.listEventInfoComp.skybillNumber,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.eventDate, "%Y-%m%dT%H%:%M:%S"),
                description=event.eventLabel,
                code=event.eventLabel,
                time=lib.ftime(event.eventDate, "%Y-%m%dT%H%:%M:%S"),
                location=None,
            )
            for event in events
        ],
        estimated_delivery=None,
        delivered=False,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = [
        chronopost.trackSkybillV2(
            language=settings.language, skybillNumber=tracking_number
        )
        for tracking_number in payload.tracking_numbers
    ]
    return lib.Serializable(
        request, lambda requests: [lib.to_xml(req) for req in requests]
    )
