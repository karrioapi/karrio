import karrio.schemas.dhl_poland.services as dhl
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dhl_poland.error as provider_error
import karrio.providers.dhl_poland.utils as provider_utils


def parse_tracking_response(
    _response: lib.Deserializable[typing.Dict[str, lib.Element]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    details = [
        _extract_tracking_details(node, settings)
        for node in response.values()
        if lib.find_element("getTrackAndTraceInfoResult", node, first=True) is not None
    ]
    errors: typing.List[models.Message] = sum(
        [
            provider_error.parse_error_response(
                node, settings, dict(tracking_number=number)
            )
            for number, node in response.items()
            if lib.find_element("Fault", node, first=True) is not None
        ],
        [],
    )

    return details, errors


def _extract_tracking_details(
    node: lib.Element,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    track: dhl.TrackAndTraceResponse = lib.find_element(
        "getTrackAndTraceInfoResult", node, dhl.TrackAndTraceResponse, first=True
    )
    events = [
        lib.to_object(dhl.TrackAndTraceEvent, item)
        for item in lib.find_element("item", node)
    ]

    return models.TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=track.shipmentId,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.timestamp, "%Y-%m-%d %H:%M:%S"),
                description=event.description,
                location=event.terminal,
                code=event.status,
                time=lib.flocaltime(event.timestamp, "%Y-%m-%d %H:%M:%S"),
            )
            for event in events
        ],
        delivered=any(track.receivedBy or ""),
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(track.shipmentId),
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    requests = {
        tracking_number: lib.create_envelope(
            body_prefix="",
            body_content=dhl.getTrackAndTraceInfo(
                authData=settings.auth_data,
                shipmentId=tracking_number,
            ),
        )
        for tracking_number in payload.tracking_numbers
    }

    return lib.Serializable(
        requests,
        lambda requests: {
            number: settings.serialize(
                request,
                "getTrackAndTraceInfo",
                settings.server_url,
            )
            for number, request in requests.items()
        },
    )
