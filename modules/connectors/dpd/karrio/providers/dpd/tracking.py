import karrio.schemas.dpd.ParcelLifecycleServiceV20 as dpd
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dpd.error as error
import karrio.providers.dpd.utils as provider_utils
import karrio.providers.dpd.units as provider_units


def parse_tracking_response(
    _responses: lib.Deserializable[typing.List[typing.Tuple[str, lib.Element]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _responses.deserialize()
    response_messages = []
    response_details = []

    for response in responses:
        results: list = lib.find_element("trackingresult", response[1])

        if len(results) > 0:
            response_details.append(response)
        else:
            response_messages.append(response)

    tracking_details = [_extract_details(_, settings) for _ in response_details]
    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(_[1], settings, **dict(tracking_number=_[0]))
            for _ in response_messages
        ],
        start=[],
    )

    return tracking_details, messages


def _extract_details(
    data: typing.Tuple[str, lib.Element],
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    tracking_number, node = data
    events: typing.List[dpd.StatusInfo] = [
        _ for _ in reversed(lib.find_element("statusInfo", node, dpd.StatusInfo))
    ]
    delivered = any([_.status == "Delivered" for _ in events])
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if next(iter(events), dpd.StatusInfo()).status in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        events=[
            models.TrackingEvent(
                code=event.status,
                location=event.location.content,
                date=lib.fdate(
                    event.date.content,
                    current_format="%m/%d/%Y %H:%M:%S %p",
                ),
                description=lib.join(
                    *[_.content for _ in event.description.content],
                    separator=",",
                    join=True,
                ),
                time=lib.flocaltime(
                    event.date.content,
                    current_format="%m/%d/%Y %H:%M:%S %p",
                ),
            )
            for event in events
        ],
        delivered=delivered,
        status=status,
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(tracking_number),
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = {
        tracking_number: lib.Envelope(
            Header=lib.Header(
                settings.authentication,
            ),
            Body=lib.Body(
                dpd.getTrackingData(
                    parcelLabelNumber=tracking_number,
                )
            ),
        )
        for tracking_number in payload.tracking_numbers
    }

    return lib.Serializable(
        request,
        lambda envelopes: {
            tracking_number: lib.envelope_serializer(
                envelope,
                namespace=(
                    'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
                    'xmlns:ns="http://dpd.com/common/service/types/Authentication/2.0" '
                    'xmlns:ns1="http://dpd.com/common/service/types/ParcelLifeCycleService/2.0"'
                ),
                prefixes=dict(
                    Envelope="soapenv",
                    authentication="ns",
                    delisId="",
                    authToken="",
                    messageLanguage="",
                    getTrackingData="ns1",
                    parcelLabelNumber="",
                ),
            )
            for tracking_number, envelope in envelopes.items()
        },
    )
