"""Karrio Amazon Shipping tracking implementation."""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.amazon_shipping.error as error
import karrio.providers.amazon_shipping.units as provider_units
import karrio.providers.amazon_shipping.utils as provider_utils
import karrio.schemas.amazon_shipping.tracking_response as amazon


def parse_tracking_response(
    _response: lib.Deserializable[list[tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> tuple[list[models.TrackingDetails], list[models.Message]]:
    """Parse tracking response from Amazon Shipping API."""
    responses = _response.deserialize()

    messages: list[models.Message] = sum(
        [
            error.parse_error_response(response, settings, tracking_number=tracking_id)
            for tracking_id, response in responses
            if response.get("errors")
        ],
        [],
    )

    trackers = [
        _extract_details(tracking_id, response, settings)
        for tracking_id, response in responses
        if not response.get("errors")
    ]

    return trackers, messages


def _extract_details(
    tracking_id: str,
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    """Extract tracking details from API response payload. See SPECS.md."""
    payload = data.get("payload") or {}
    details = lib.to_object(amazon.Payload, payload)
    events = details.eventHistory or []
    summary = details.summary

    # Check if delivered based on summary status
    delivered = lib.failsafe(lambda: summary.status == "Delivered") or False

    # Get status from the latest event
    latest_event = next(iter(events), None)
    status = lib.failsafe(
        lambda: next(
            (s.name for s in list(provider_units.TrackingStatus) if latest_event.eventCode in s.value),
            None,
        )
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=details.trackingId or tracking_id,
        delivered=delivered,
        status=status,
        estimated_delivery=lib.fdate(
            details.promisedDeliveryDate,
            "%Y-%m-%dT%H:%M:%SZ",
        ),
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.eventTime, "%Y-%m-%dT%H:%M:%SZ"),
                time=lib.flocaltime(event.eventTime, "%Y-%m-%dT%H:%M:%SZ"),
                code=event.eventCode,
                description=event.eventCode,
                location=lib.join(
                    lib.failsafe(lambda: event.location.city),
                    lib.failsafe(lambda: event.location.stateOrRegion),
                    lib.failsafe(lambda: event.location.postalCode),
                    lib.failsafe(lambda: event.location.countryCode),
                    join=True,
                    separator=", ",
                ),
                timestamp=lib.fiso_timestamp(
                    event.eventTime,
                    current_format="%Y-%m-%dT%H:%M:%SZ",
                ),
                status=next(
                    (s.name for s in list(provider_units.TrackingStatus) if event.eventCode in s.value),
                    None,
                ),
                reason=next(
                    (r.name for r in list(provider_units.TrackingIncidentReason) if event.eventCode in r.value),
                    None,
                ),
            )
            for event in events
        ],
        meta=dict(
            carrier_tracking_id=details.trackingId,
            alternate_tracking_id=details.alternateLegTrackingId,
            received_by=lib.failsafe(lambda: summary.proofOfDelivery.receivedBy),
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create Amazon Shipping tracking request (one entry per number). See SPECS.md."""
    tracking_data = [
        dict(
            tracking_id=tracking_number,
            carrier_id=payload.options.get("carrier_id", "AMZN_US"),
        )
        for tracking_number in payload.tracking_numbers
    ]

    return lib.Serializable(tracking_data)
