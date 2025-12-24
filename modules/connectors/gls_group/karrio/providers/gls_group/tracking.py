"""Karrio GLS Group tracking implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.gls_group.error as error
import karrio.providers.gls_group.utils as provider_utils
import karrio.providers.gls_group.units as provider_units
import karrio.schemas.gls_group.tracking_response as gls_tracking


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    """Parse GLS Group tracking response."""
    responses = _response.deserialize()

    messages = sum(
        [
            error.parse_error_response(response, settings, tracking_number=tracking_number)
            for tracking_number, response in responses
        ],
        start=[],
    )

    tracking_details = [
        _extract_details(response, settings, tracking_number)
        for tracking_number, response in responses
        if not any(error.parse_error_response(response, settings))
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    tracking_number: str,
) -> models.TrackingDetails:
    """Extract tracking details from GLS Group response."""
    tracking = lib.to_object(gls_tracking.TrackingResponseType, data)

    # Extract events
    events = [
        models.TrackingEvent(
            date=lib.fdate(event.timestamp, "%Y-%m-%dT%H:%M:%SZ") if event.timestamp else None,
            description=event.description or "",
            location=", ".join(
                filter(
                    None,
                    [
                        event.location.city if hasattr(event, "location") and event.location else None,
                        event.location.country if hasattr(event, "location") and event.location else None,
                    ],
                )
            ),
            code=event.status if hasattr(event, "status") else None,
            time=lib.ftime(event.timestamp, "%Y-%m-%dT%H:%M:%SZ") if event.timestamp else None,
        )
        for event in (tracking.events or [])
    ]

    # Map GLS status codes to Karrio standard statuses
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if tracking.status in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking.trackingNumber or tracking_number,
        status=status,
        events=events,
        estimated_delivery=lib.fdate(tracking.estimatedDelivery) if hasattr(tracking, "estimatedDelivery") and tracking.estimatedDelivery else None,
        meta=dict(
            shipment_id=tracking.shipmentId if hasattr(tracking, "shipmentId") else None,
            product=tracking.product if hasattr(tracking, "product") else None,
            weight=tracking.weight if hasattr(tracking, "weight") else None,
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a tracking request for GLS Group API."""
    return lib.Serializable(payload.tracking_numbers)
