import karrio.schemas.usps_wt.track_field_request as usps
import karrio.schemas.usps_wt.track_response as tracking
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.usps_wt.error as error
import karrio.providers.usps_wt.utils as provider_utils
import karrio.providers.usps_wt.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    tracks_info = lib.find_element("TrackInfo", response)
    details = [
        _extract_details(node, settings)
        for node in tracks_info
        if len(lib.find_element("TrackDetail", node)) > 0
    ]

    return details, error.parse_error_response(response, settings)


def _extract_details(
    node: lib.Element,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    info = lib.to_object(tracking.TrackInfoType, node)
    events: typing.List[tracking.TrackDetailType] = [
        *([info.TrackSummary] or []),
        *info.TrackDetail,
    ]
    delivered = info.StatusCategory.lower() == "delivered"
    expected_delivery = lib.fdate(
        info.ExpectedDeliveryDate or info.PredictedDeliveryDate,
        "%B %d, %Y",
    )
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if str(getattr(events[0], "EventCode", None)) in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=info.ID,
        estimated_delivery=expected_delivery,
        delivered=delivered,
        status=status,
        events=[
            models.TrackingEvent(
                code=str(event.EventCode),
                date=lib.fdate(event.EventDate, "%B %d, %Y"),
                time=lib.flocaltime(event.EventTime, "%H:%M %p"),
                description=event.Event,
                location=lib.join(
                    event.EventCity,
                    event.EventState,
                    event.EventCountry,
                    str(event.EventZIPCode or ""),
                    join=True,
                    separator=", ",
                ),
            )
            for event in events
        ],
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(info.ID),
            shipment_destination_postal_code=info.DestinationZip,
            shipment_destination_country=info.DestinationCountryCode,
            shipment_origin_country=info.OriginCountryCode,
            shipment_origin_postal_code=info.OriginZip,
            shipment_service=info.Class,
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = usps.TrackFieldRequest(
        USERID=settings.username,
        PASSWORD=settings.password,
        Revision="1",
        ClientIp="127.0.0.1",
        SourceId="Karrio",
        TrackID=[
            usps.TrackIDType(
                ID=tracking_number,
                DestinationZipCode=None,
                MailingDate=None,
            )
            for tracking_number in payload.tracking_numbers
        ],
    )

    return lib.Serializable(request, lib.to_xml)
