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
        if result.get("errorcode") == "0" and next(iter(result), None) is not None
    ]
    messages = [_extract_errors(result, settings) for result in response_messages]
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
        [event for event in tracking] if tracking.listEventInfoComp is not None else []
    )
    delivered = ["D" == event.code for event in events]
    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking.listEventInfoComp.skybillNumber,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.eventDate, "%Y-%m%dT%H%:%M:%S"),
                description=event.eventLabel,
                code=event.code,
                time=lib.ftime(event.eventDate, "%Y-%m%dT%H%:%M:%S"),
                location=event.officeLabel,
            )
            for event in events
        ],
        estimated_delivery=None,
        delivered=True if True in delivered else False,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = [
        lib.Envelope(
            Header=lib.Header(),
            Body=lib.Body(
                chronopost.trackSkybillV2(
                    language=settings.language, skybillNumber=tracking_number
                )
            ),
        )
        for tracking_number in payload.tracking_numbers
    ]
    return lib.Serializable(
        request,
        lambda requests: [
            lib.envelope_serializer(
                req,
                namespace=(
                    'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
                    'xmlns:cxf="http://cxf.tracking.soap.chronopost.fr/"'
                ),
                prefixes=dict(Envelope="soapenv"),
            )
            for req in requests
        ],
    )
