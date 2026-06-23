"""Karrio Landmark Global tracking API implementation."""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.landmark.error as error
import karrio.providers.landmark.units as provider_units
import karrio.providers.landmark.utils as provider_utils
import karrio.schemas.landmark.track_request as landmark_req
import karrio.schemas.landmark.track_response as landmark_res

# Supported datetime formats for Landmark Global
DATETIME_FORMATS = [
    "%m/%d/%Y %I:%M %p",  # 10/01/2025 03:02 PM
    "%-m/%d/%Y %I:%M %p",  # 0/01/2025 03:03 PM (single digit month)
    "%Y-%m-%d %H:%M:%S",  # 2019-01-01 13:21:45
]


def parse_tracking_response(
    _response: lib.Deserializable[list[tuple[str, lib.Element]]],
    settings: provider_utils.Settings,
) -> tuple[list[models.TrackingDetails], list[models.Message]]:
    responses = _response.deserialize()

    messages: list[models.Message] = sum(
        [
            error.parse_error_response(response, settings, tracking_number=tracking_number)
            for tracking_number, response in responses
        ],
        start=[],
    )

    tracking_details = [
        _extract_details(details, settings)
        for _, details in responses
        if len(lib.find_element("TrackingNumber", details)) > 0
    ]

    return tracking_details, messages


def _extract_details(
    data: lib.Element,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    """Extract tracking details from carrier response data"""

    details = lib.find_element("ShipmentDetails", data, landmark_res.ShipmentDetailsType, first=True)
    package = lib.find_element("Package", data, landmark_res.PackageType, first=True)

    # Build events in carrier order (preserves multi-leg sequencing)
    tracking_events = [
        models.TrackingEvent(
            date=lib.fdate(event.DateTime, try_formats=DATETIME_FORMATS),
            time=lib.flocaltime(
                event.DateTime,
                output_format="%I:%M %p",
                try_formats=DATETIME_FORMATS,
            ),
            description=event.Status,
            code=event.EventCode,
            location=event.Location,
            timestamp=lib.fiso_timestamp(
                event.DateTime,
                try_formats=DATETIME_FORMATS,
            ),
            status=next(
                (s.name for s in list(provider_units.TrackingStatus) if event.EventCode in s.value),
                None,
            ),
            reason=next(
                (r.name for r in list(provider_units.TrackingIncidentReason) if event.EventCode in r.value),
                None,
            ),
        )
        for event in package.Events.Event
    ]

    # Ensure newest-first order (Karrio convention)
    # Detect carrier order by comparing first and last event timestamps
    if len(tracking_events) >= 2:
        first_ts = tracking_events[0].timestamp or ""
        last_ts = tracking_events[-1].timestamp or ""
        if first_ts < last_ts:
            tracking_events = list(reversed(tracking_events))

    # Determine status: terminal statuses (delivered) take priority
    # regardless of event ordering in multi-leg shipments
    _delivered_codes = provider_units.TrackingStatus.delivered.value
    has_delivered = any(e.code in _delivered_codes for e in tracking_events)

    if has_delivered:
        status = provider_units.TrackingStatus.delivered.name
    else:
        latest_event = tracking_events[0] if tracking_events else None
        status = next(
            (
                status.name
                for status in list(provider_units.TrackingStatus)
                if latest_event and latest_event.code in status.value
            ),
            provider_units.TrackingStatus.in_transit.name,
        )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=package.LandmarkTrackingNumber,
        events=tracking_events,
        delivered=status == "delivered",
        status=status,
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(package.LandmarkTrackingNumber),
        ),
        meta=lib.to_dict(
            dict(
                last_mile_tracking_number=package.TrackingNumber,
                last_mile_carrier=lib.identity(
                    None if "routed" in (details.EndDeliveryCarrier or "").lower() else details.EndDeliveryCarrier
                ),
            )
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create tracking requests for the carrier API"""
    # Create a request for each tracking number
    requests = [
        landmark_req.TrackRequest(
            Login=landmark_req.LoginType(
                Username=settings.username,
                Password=settings.password,
            ),
            Test=settings.test_mode,
            ClientID=settings.client_id,
            Reference=payload.reference,
            TrackingNumber=tracking_number,
            PackageReference=None,
            RetrievalType="Historical",
        )
        for tracking_number in payload.tracking_numbers
    ]

    return lib.Serializable(
        requests,
        lambda __: [lib.typed(number=_.TrackingNumber, request=lib.to_xml(_)) for _ in __],
    )
