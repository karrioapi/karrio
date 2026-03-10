"""Karrio SmartKargo tracking API implementation."""

import karrio.schemas.smartkargo.tracking_response as smartkargo_res

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.smartkargo.error as error
import karrio.providers.smartkargo.utils as provider_utils
import karrio.providers.smartkargo.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(
                response, settings, tracking_number=tracking_number
            )
            for tracking_number, response in responses
        ],
        start=[],
    )

    tracking_details = [
        _extract_details(details, settings, tracking_number)
        for tracking_number, details in responses
        if _has_valid_tracking(details)
    ]

    return tracking_details, messages


def _has_valid_tracking(data: dict) -> bool:
    """Check if the response contains valid tracking data."""
    # SmartKargo returns an array of events or an error object
    if isinstance(data, list) and any(data):
        return True
    return False


def _extract_details(
    data: typing.List[dict],
    settings: provider_utils.Settings,
    tracking_number: str,
) -> models.TrackingDetails:
    """Extract tracking details from SmartKargo tracking response.

    SmartKargo returns an array of tracking events, each with:
    - eventType: status code (BKD, RCS, DEP, DDL, etc.)
    - eventDate: ISO datetime string
    - eventLocation: location code
    - description: human-readable description
    """
    # Convert events to typed objects
    events = [
        lib.to_object(smartkargo_res.TrackingResponseElementType, event)
        for event in data
    ]

    # Sort events by date (most recent first)
    sorted_events = sorted(
        events,
        key=lambda e: e.eventDate or "",
        reverse=True,
    )

    # Get latest event for status
    latest_event = sorted_events[0] if sorted_events else None
    latest_status_code = latest_event.eventType if latest_event else ""

    # Map carrier status to karrio standard tracking status
    status = (
        provider_units.TrackingStatus.find(latest_status_code).name
        or "in_transit"
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.eventDate, "%Y-%m-%dT%H:%M:%S"),
                description=event.description,
                code=event.eventType,
                time=lib.ftime(event.eventDate, "%Y-%m-%dT%H:%M:%S"),
                location=event.eventLocation,
                timestamp=lib.fiso_timestamp(
                    event.eventDate,
                    current_format="%Y-%m-%dT%H:%M:%S",
                ),
                status=provider_units.TrackingStatus.find(event.eventType).name,
                reason=provider_units.TrackingIncidentReason.find(event.eventType).name,
            )
            for event in sorted_events
        ],
        estimated_delivery=lib.fdate(
            latest_event.estimatedDeliveryDate if latest_event else None,
            "%Y-%m-%dT%H:%M:%S",
        ),
        delivered=(status == "delivered"),
        status=status,
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(tracking_number),
            shipment_package_count=lib.to_int(getattr(latest_event, "pieces", None)),
            package_weight=lib.to_decimal(getattr(latest_event, "weight", None)),
            package_weight_unit="KG",
        ),
        meta=lib.to_dict(
            dict(
                smartkargo_flight_number=getattr(latest_event, "flightNumber", None),
                smartkargo_air_waybill=getattr(latest_event, "airWaybill", None),
                smartkargo_prefix=getattr(latest_event, "prefix", None),
                smartkargo_header_reference=getattr(
                    latest_event, "headerReference", None
                ),
                smartkargo_package_reference=getattr(
                    latest_event, "packageReference", None
                ),
                smartkargo_piece_reference=getattr(
                    latest_event, "pieceReference", None
                ),
            )
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a tracking request for SmartKargo API.

    SmartKargo supports two tracking lookup strategies:
    - Primary:  GET /tracking?prefix=<PREFIX>&Airwaybill=<AWB>
      Resolved from shipment meta options (smartkargo_prefix, smartkargo_air_waybill)
      or by parsing the tracking number (3 alpha + digits, e.g. "XIA00291643")
    - Fallback: GET /tracking?packageReference=<ref>
      Used for legacy / non-AWB references (e.g. "yogi045")
    """
    import re

    _AWB_PATTERN = re.compile(r"^([A-Za-z]{3})[-_ ]?([0-9]+)$")
    options = payload.options or {}

    def _build_query_params(tracking_number: str) -> dict:
        # Check shipment meta passed via options (per-tracking or global)
        tracking_options = options.get(tracking_number) or options
        prefix = tracking_options.get("smartkargo_prefix")
        airwaybill = tracking_options.get("smartkargo_air_waybill")

        if prefix and airwaybill:
            return dict(prefix=prefix, Airwaybill=airwaybill)

        # Parse from tracking number format (e.g. "XIA00291643")
        match = _AWB_PATTERN.match(tracking_number or "")
        if match is not None:
            prefix, airwaybill = match.groups()
            return dict(prefix=prefix.upper(), Airwaybill=airwaybill)

        # Last resort: lookup by package reference
        return dict(packageReference=tracking_number)

    request = [
        dict(
            tracking_number=tracking_number,
            query_params=_build_query_params(tracking_number),
        )
        for tracking_number in payload.tracking_numbers
    ]

    return lib.Serializable(request, lib.to_dict)
