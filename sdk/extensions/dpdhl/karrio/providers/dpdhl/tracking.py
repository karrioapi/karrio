import dpdhl_lib.tracking_response as tracking
import dpdhl_lib.tracking_request as dpdhl
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dpdhl.error as error
import karrio.providers.dpdhl.utils as provider_utils
import karrio.providers.dpdhl.units as provider_units


def parse_tracking_response(
    _responses: lib.Deserializable[typing.List[lib.Element]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _responses.deserialize()
    response_messages = [
        result
        for result in responses
        if result.get("code") != "0" or result.get("body") is not None
    ]
    response_details = [
        result[0]
        for result in responses
        if result.get("code") == "0" and next(iter(result), None) is not None
    ]

    trackers = [_extract_details(rate, settings) for rate in response_details]
    messages: typing.List[models.Message] = sum(
        [error.parse_error_response(_, settings) for _ in response_messages], start=[]
    )

    return trackers, messages


def _extract_details(
    data: lib.Element,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    details = lib.to_object(tracking.dataType, data)
    events: typing.List[tracking.dataType2] = (
        [d for d in details.data.data] if details.data is not None else []
    )
    delivered = details.ice == "DLVRD"
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if details.ice in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=details.piece_identifier,
        events=[
            models.TrackingEvent(
                code=event.ice,
                description=event.event_status,
                date=lib.fdate(event.event_timestamp, "%d.%m.%Y %H:%M"),
                time=lib.fdate(event.event_timestamp, "%d.%m.%Y %H:%M"),
                location=lib.join(
                    event.event_location,
                    event.event_country,
                    separator=", ",
                    join=True,
                ),
            )
            for event in events
        ],
        status=status,
        delivered=delivered,
        estimated_delivery=lib.fdate(details.delivery_date),
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(
                details.piece_identifier
            ),
            customer_name=details.pan_recipient_name,
            shipment_destination_country=details.dest_country,
            shipment_destination_postal_code=details.pan_recipient_postalcode,
            shipment_origin_country=details.origin_country,
            shipment_service=details.product_name,
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = [
        dpdhl.data(
            appname=settings.zt_id,
            password=settings.zt_password,
            request="d-get-piece-detail",
            language_code=settings.language_code,
            piece_code=tracking_number,
        )
        for tracking_number in payload.tracking_numbers
    ]

    return lib.Serializable(
        request,
        lambda requests: [
            f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n{lib.to_xml(req)}'
            for req in requests
        ],
    )
