import karrio.schemas.australiapost.tracking_request as australiapost
import karrio.schemas.australiapost.tracking_response as tracking
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.australiapost.error as error
import karrio.providers.australiapost.utils as provider_utils
import karrio.providers.australiapost.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    tracking_results = response.get("tracking_results") or []
    messages = sum(
        [
            error.parse_error_response(
                result,
                settings,
                tracking_number=result.get("tracking_id"),
            )
            for result in tracking_results
            if "errors" in result
        ],
        start=error.parse_error_response(response, settings),
    )
    tracking_details = [
        _extract_details(details, settings)
        for details in tracking_results
        if "trackable_items" in details
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    detail = lib.to_object(tracking.TrackingResultType, data)
    item = detail.trackable_items[0]
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if item.status in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=detail.tracking_id,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.date, "%Y-%m-%dT%H:%M:%S%z"),
                description=event.description,
                location=event.location,
                time=lib.flocaltime(event.date, "%Y-%m-%dT%H:%M:%S%z"),
                timestamp=lib.fiso_timestamp(event.date, current_format="%Y-%m-%dT%H:%M:%S%z"),
                status=next(
                    (
                        s.name
                        for s in list(provider_units.TrackingStatus)
                        if item.status in s.value
                    ),
                    None,
                ),
                reason=next(
                    (
                        r.name
                        for r in list(provider_units.TrackingIncidentReason)
                        if item.status in r.value
                    ),
                    None,
                ),
            )
            for event in item.events
        ],
        delivered=(status == provider_units.TrackingStatus.delivered.name),
        status=status,
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(detail.tracking_id),
            shipment_service=item.product_type,
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = australiapost.TrackingRequestType(
        tracking_ids=payload.tracking_numbers,
    )

    return lib.Serializable(request, lib.to_dict)
