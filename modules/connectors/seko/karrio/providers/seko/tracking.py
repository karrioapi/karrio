"""Karrio SEKO Logistics tracking API implementation."""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.seko.error as error
import karrio.providers.seko.units as provider_units
import karrio.providers.seko.utils as provider_utils
import karrio.schemas.seko.tracking_response as tracking


def parse_tracking_response(
    _response: lib.Deserializable[list[dict]],
    settings: provider_utils.Settings,
) -> tuple[list[models.TrackingDetails], list[models.Message]]:
    responses = _response.deserialize()

    messages: list[models.Message] = error.parse_error_response(responses, settings)
    tracking_details = [
        _extract_details(_, settings)
        for _ in (responses if isinstance(responses, list) else [responses])
        if any(_.get("Events", []))
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    details = lib.to_object(tracking.TrackingResponseElementType, data)
    events = list(reversed(details.Events))
    latest_status = lib.identity(events[0].OmniCode if any(events) else getattr(details, "Status", None))
    status = next(
        (status.name for status in list(provider_units.TrackingStatus) if latest_status in status.value),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=details.ConsignmentNo,
        events=[
            models.TrackingEvent(
                date=lib.fdate(
                    event.EventDT,
                    try_formats=["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"],
                ),
                description=event.Description,
                code=event.OmniCode or event.Code,
                time=lib.flocaltime(
                    event.EventDT,
                    try_formats=["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"],
                ),
                location=event.Location,
                timestamp=lib.fiso_timestamp(
                    event.EventDT,
                    try_formats=["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"],
                ),
                status=next(
                    (s.name for s in list(provider_units.TrackingStatus) if (event.OmniCode or event.Code) in s.value),
                    None,
                ),
                reason=next(
                    (
                        r.name
                        for r in list(provider_units.TrackingIncidentReason)
                        if (event.OmniCode or event.Code) in r.value
                    ),
                    None,
                ),
            )
            for event in events
        ],
        delivered=status == "delivered",
        status=status,
        info=models.TrackingInfo(
            carrier_tracking_link=details.Tracking,
            expected_delivery=lib.fdate(
                details.Delivered,
                try_formats=["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"],
            ),
            shipping_date=lib.fdate(
                details.Picked,
                try_formats=["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"],
            ),
        ),
        meta=dict(reference=details.Reference1),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:

    # map data to convert karrio model to seko specific type
    request = payload.tracking_numbers

    return lib.Serializable(request, lib.to_dict)
