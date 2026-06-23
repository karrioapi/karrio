import karrio.schemas.canadapost.track as capost
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.canadapost.error as error
import karrio.providers.canadapost.units as provider_units
import karrio.providers.canadapost.utils as provider_utils


def parse_tracking_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    responses = lib.to_list(response)
    details: typing.List[lib.Element] = []
    for node in responses:
        tag = getattr(node, "tag", "")
        local_name = tag.split("}")[-1] if isinstance(tag, str) else ""
        # Canada Post may return <tracking-detail> as the response root.
        if local_name == "tracking-detail":
            details.append(node)
            continue
        details.extend(lib.find_element("tracking-detail", node))
    tracking_details: typing.List[models.TrackingDetails] = [
        _extract_tracking(node, settings)
        for node in details
        if len(lib.find_element("occurrence", node)) > 0
    ]

    return tracking_details, error.parse_error_response(response, settings)


def _extract_tracking(
    detail_node: lib.Element,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    details = lib.to_object(capost.tracking_detail, detail_node)
    events: typing.List[capost.occurrenceType] = details.significant_events.occurrence
    last_event = events[0]
    estimated_delivery = lib.fdate(
        details.changed_expected_date or details.expected_delivery_date,
        "%Y-%m-%d",
    )
    status = provider_units.map_tracking_status(
        last_event.event_identifier,
        last_event.event_description,
    )

    return models.TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=details.pin,
        estimated_delivery=estimated_delivery,
        delivered=status == "delivered",
        status=status,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.event_date, "%Y-%m-%d"),
                time=lib.flocaltime(event.event_time, "%H:%M:%S"),
                code=event.event_identifier,
                location=lib.join(
                    event.event_site, event.event_province, join=True, separator=", "
                ),
                description=event.event_description,
                timestamp=lib.fiso_timestamp(
                    lib.fdate(event.event_date, "%Y-%m-%d"),
                    lib.ftime(event.event_time, "%H:%M:%S"),
                ),
                status=provider_units.map_tracking_status(
                    event.event_identifier,
                    event.event_description,
                ),
                reason=provider_units.map_tracking_incident_reason(
                    event.event_identifier,
                ),
            )
            for event in events
        ],
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(details.pin),
            shipment_destination_postal_code=details.destination_postal_id,
            shipment_delivery_date=estimated_delivery,
            shipment_service=details.service_name,
            signed_by=last_event.signatory_name,
        ),
    )


def tracking_request(payload: models.TrackingRequest, _) -> lib.Serializable:
    return lib.Serializable(payload.tracking_numbers)
