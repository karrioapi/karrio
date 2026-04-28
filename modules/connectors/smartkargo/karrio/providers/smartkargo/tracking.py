"""Karrio SmartKargo tracking API implementation."""

import re
import karrio.schemas.smartkargo.tracking_response as smartkargo

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.smartkargo.error as error
import karrio.providers.smartkargo.utils as provider_utils
import karrio.providers.smartkargo.units as provider_units

DATETIME_FORMATS = ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"]

# SmartKargo upstream occasionally emits .NET ticks-precision timestamps
# (7 fractional digits, e.g. "2026-04-17T23:43:17.6571145"), exceeding Python's
# strptime %f cap of 6. Truncate to microseconds so %f parses cleanly.
_TICKS_RE = re.compile(r"(\.\d{6})\d+")


def _normalize_event_date(date_str: typing.Optional[str]) -> typing.Optional[str]:
    if not date_str:
        return date_str
    return _TICKS_RE.sub(r"\1", date_str)


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
        if isinstance(details, list) and any(details)
    ]

    return tracking_details, messages


def _extract_details(
    data: typing.List[dict],
    settings: provider_utils.Settings,
    tracking_number: str,
) -> models.TrackingDetails:
    """Extract tracking details from SmartKargo response (standard or partner).

    Uses a single unified schema — the `location` field is nullable.
    When present (partner response), it provides rich address data.
    When absent (standard response), `eventLocation` code is used.
    """
    events = [
        lib.to_object(smartkargo.TrackingResponseElementType, event) for event in data
    ]

    latest = events[0] if events else None
    status = (
        provider_units.TrackingStatus.find(latest.eventType if latest else "").name
        or "in_transit"
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        events=[
            models.TrackingEvent(
                date=lib.fdate(
                    _normalize_event_date(e.eventDate),
                    try_formats=DATETIME_FORMATS,
                ),
                description=e.description,
                code=e.eventType,
                time=lib.ftime(
                    _normalize_event_date(e.eventDate),
                    try_formats=DATETIME_FORMATS,
                ),
                location=(
                    lib.join(
                        e.location.city,
                        e.location.state,
                        join=True,
                        separator=", ",
                    )
                    if e.location and e.location.city
                    else e.eventLocation
                ),
                timestamp=lib.fiso_timestamp(
                    _normalize_event_date(e.eventDate),
                    try_formats=DATETIME_FORMATS,
                ),
                status=provider_units.TrackingStatus.find(e.eventType).name,
                reason=provider_units.TrackingIncidentReason.find(e.eventType).name,
                latitude=lib.failsafe(lambda: float(e.location.latitude)),
                longitude=lib.failsafe(lambda: float(e.location.longitude)),
            )
            for e in events
        ],
        estimated_delivery=lib.fdate(
            _normalize_event_date(getattr(latest, "estimatedDeliveryDate", None)),
            try_formats=DATETIME_FORMATS,
        ),
        delivered=(status == "delivered"),
        status=status,
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(tracking_number),
            shipment_package_count=lib.to_int(getattr(latest, "pieces", None)),
            package_weight=lib.to_decimal(getattr(latest, "weight", None)),
            package_weight_unit="KG",
        ),
        meta=lib.to_dict(
            dict(
                smartkargo_flight_number=getattr(latest, "flightNumber", None),
                smartkargo_air_waybill=getattr(latest, "airWaybill", None),
                smartkargo_prefix=getattr(latest, "prefix", None),
                smartkargo_header_reference=getattr(latest, "headerReference", None),
                smartkargo_package_reference=getattr(latest, "packageReference", None),
                smartkargo_piece_reference=getattr(latest, "pieceReference", None),
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
    _AWB_PATTERN = re.compile(r"^([A-Za-z]{3})[-_ ]?([0-9]+)$")
    options = payload.options or {}

    def _build_query_params(tracking_number: str) -> dict:
        tracking_options = options.get(tracking_number) or options
        prefix = tracking_options.get("smartkargo_prefix")
        airwaybill = tracking_options.get("smartkargo_air_waybill")

        if prefix and airwaybill:
            return dict(prefix=prefix, Airwaybill=airwaybill)

        match = _AWB_PATTERN.match(tracking_number or "")
        if match is not None:
            prefix, airwaybill = match.groups()
            return dict(prefix=prefix.upper(), Airwaybill=airwaybill)

        return dict(packageReference=tracking_number)

    request = [
        dict(
            tracking_number=tracking_number,
            query_params=_build_query_params(tracking_number),
        )
        for tracking_number in payload.tracking_numbers
    ]

    return lib.Serializable(request, lib.to_dict)
