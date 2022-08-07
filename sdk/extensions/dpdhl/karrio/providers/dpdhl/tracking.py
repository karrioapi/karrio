import dpdhl_lib.tracking_request as dpdhl
import dpdhl_lib.tracking_response as dpdhl_response
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dpdhl.error as error
import karrio.providers.dpdhl.utils as provider_utils
import karrio.providers.dpdhl.units as provider_units


def parse_tracking_response(
    responses: typing.List[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response_messages = [result for result in responses if result.get("code") != "0"]
    response_details = [
        result[0]
        for result in responses
        if result.get("code") == "0" and next(iter(result), None) is not None
    ]

    messages = [_extract_errors(result, settings) for result in response_messages]
    trackers = [_extract_details(rate, settings) for rate in response_details]

    return trackers, messages


def _extract_errors(
    data: lib.Element,
    settings: provider_utils.Settings,
) -> models.Message:
    return models.Message(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        message=data.get("error"),
        code=data.get("code"),
    )


def _extract_details(
    data: lib.Element,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    tracking = lib.to_object(dpdhl_response.dataType, data)
    events: typing.List[dpdhl_response.dataType2] = (
        [d for d in tracking.data.data] if tracking.data is not None else []
    )
    delivered = tracking.ice == "DLVRD"

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking.piece_identifier,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.event_timestamp, "%d.%m.%Y %H:%M"),
                description=event.event_status,
                code=event.ice,
                time=lib.fdate(event.event_timestamp, "%d.%m.%Y %H:%M"),
                location=lib.join(
                    event.event_location,
                    event.event_country,
                    join=True,
                    separator=", ",
                ),
            )
            for event in events
        ],
        estimated_delivery=lib.fdate(tracking.delivery_date),
        delivered=delivered,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = [
        dpdhl.data(
            appname=settings.app_id,
            password=settings.signature,
            request="d-get-piece-detail",
            language_code=settings.language_code,
            piece_code=tracking_number,
        )
        for tracking_number in payload.tracking_numbers
    ]

    return lib.Serializable(
        request, lambda requests: [lib.to_xml(req) for req in requests]
    )
