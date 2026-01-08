"""Karrio GLS Group tracking implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.gls.error as error
import karrio.providers.gls.utils as provider_utils
import karrio.providers.gls.units as provider_units
import karrio.schemas.gls.tracking_response as gls_tracking


def parse_tracking_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    """Parse GLS Track and Trace API response."""
    response = _response.deserialize()
    messages: typing.List[models.Message] = []
    tracking_details: typing.List[models.TrackingDetails] = []

    # Parse the T&T API response (ParcelsResponseDTO)
    parcels_response = lib.to_object(gls_tracking.TrackingResponseType, response)

    for parcel in parcels_response.parcels or []:
        # Check for parcel-level errors
        if parcel.errorCode:
            messages.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=parcel.errorCode,
                    message=parcel.errorMessage or "Unknown error",
                    details=dict(tracking_number=parcel.requested),
                )
            )
            continue

        # Extract tracking details for this parcel
        tracking_details.append(_extract_details(parcel, settings))

    return tracking_details, messages


def _extract_details(
    parcel: gls_tracking.ParcelType,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    """Extract tracking details from a GLS parcel."""
    # Extract events (sorted by datetime, newest first)
    events = [
        models.TrackingEvent(
            date=lib.fdate(event.eventDateTime, "%Y-%m-%dT%H:%M:%S%z") if event.eventDateTime else None,
            description=event.description or "",
            location=", ".join(
                filter(None, [event.city, event.postalCode, event.country])
            ),
            code=event.code,
            time=lib.ftime(event.eventDateTime, "%Y-%m-%dT%H:%M:%S%z") if event.eventDateTime else None,
        )
        for event in (parcel.events or [])
    ]

    # Map GLS status codes to Karrio standard statuses
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if parcel.status in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=parcel.unitno or parcel.requested,
        status=status,
        events=events,
        meta=dict(
            requested=parcel.requested,
            unitno=parcel.unitno,
            status_datetime=parcel.statusDateTime,
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a tracking request for GLS Track and Trace API."""
    return lib.Serializable(payload.tracking_numbers)
