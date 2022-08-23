import typing
from urllib import response
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.chronopost.utils as provider_utils
import karrio.providers.chronopost.error as provider_error
import chronopost_lib.trackingservice as chronopost


def parse_tracking_response(
    responses: typing.List[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    tracking_nodes: typing.List[chronopost.eventInfoComp] = [
        lib.find_element("events", response, chronopost.eventInfoComp)
        for response in responses
    ]
    errors = [
        provider_error.parse_error_response(result, settings) for result in responses
    ]
    tracking_details = [
        _extract_details(tracking_nodes[t], settings, responses[t])
        for t in range(len(tracking_nodes))
    ]

    return tracking_details, errors


def _extract_details(
    detail: typing.List[chronopost.eventInfoComp],
    settings: provider_utils.Settings,
    response: typing.List[lib.Element],
) -> models.TrackingDetails:
    tracking_number: chronopost.listEventInfoComps = lib.find_element(
        "listEventInfoComp", response, chronopost.listEventInfoComps, first=True
    )
    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number.skybillNumber,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.eventDate, "%Y-%m%dT%H%:%M:%S"),
                description=event.eventLabel,
                code=event.code,
                time=lib.ftime(event.eventDate, "%Y-%m%dT%H%:%M:%S"),
                location=event.officeLabel,
            )
            for event in detail
        ],
        estimated_delivery=None,
        delivered=True if "D" in [event.code for event in detail] else False,
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
