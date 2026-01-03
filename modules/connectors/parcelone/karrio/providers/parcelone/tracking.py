"""Karrio ParcelOne tracking implementation."""

import typing
import karrio.schemas.parcelone.shipping_wcf as parcelone
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.parcelone.error as error
import karrio.providers.parcelone.utils as provider_utils
import karrio.providers.parcelone.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    """Parse tracking response from ParcelOne API."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    tracking_results: typing.List[parcelone.ShipmentTrackingResult] = lib.find_element(
        "ShipmentTrackingResult", response, parcelone.ShipmentTrackingResult
    )

    tracking_details = [
        _extract_tracking_details(result, settings)
        for result in tracking_results
        if _has_tracking_events(result)
    ]

    return tracking_details, messages


def _has_tracking_events(result: parcelone.ShipmentTrackingResult) -> bool:
    """Check if the tracking result has events."""
    return result.Trackings is not None and any(result.Trackings.TrackingResult)


def _extract_tracking_details(
    result: parcelone.ShipmentTrackingResult,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    """Extract tracking details from ShipmentTrackingResult element."""
    tracking_id = lib.failsafe(lambda: result.ActionResult.TrackingID)
    events = sorted(
        [
            _parse_tracking_event(event)
            for event in lib.failsafe(lambda: result.Trackings.TrackingResult) or []
        ],
        key=lambda e: e.date or "",
        reverse=True,
    )
    latest_event = next(iter(events), None)
    status = provider_units.TrackingStatus.find(latest_event.code) if latest_event else None

    return models.TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking_id,
        events=events,
        delivered=(status.name == "delivered") if status else False,
        status=status.name if status else None,
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(tracking_id) if tracking_id else None,
        ),
    )


def _parse_tracking_event(event: parcelone.TrackingResult) -> models.TrackingEvent:
    """Parse a single tracking event."""
    datetime_str = event.TrackingDateTime or ""
    date = lib.fdate(datetime_str, try_formats=["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"])
    time = lib.flocaltime(datetime_str, try_formats=["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"])

    return models.TrackingEvent(
        date=date,
        time=time,
        description=event.TrackingStatus,
        code=event.TrackingStatusCode,
        location=event.TrackingLocation,
        timestamp=lib.fiso_timestamp(datetime_str, current_format="%Y-%m-%dT%H:%M:%S"),
        status=provider_units.TrackingStatus.find(event.TrackingStatusCode).name,
        reason=provider_units.TrackingIncidentReason.find(event.TrackingStatusCode).name,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create ParcelOne tracking request."""
    requests = [
        parcelone.identifyShipment(
            ShipmentRefField="TrackingID",
            ShipmentRefValue=tracking_number,
        )
        for tracking_number in payload.tracking_numbers
    ]

    return lib.Serializable(
        requests,
        lambda reqs: _request_serializer(reqs, settings),
    )


def _request_serializer(
    requests: typing.List[parcelone.identifyShipment],
    settings: provider_utils.Settings,
) -> str:
    """Serialize tracking request to SOAP envelope."""
    identify_xml = "".join([
        lib.to_xml(
            req,
            name_="wcf:identifyShipment",
            namespacedef_='xmlns:wcf="http://schemas.datacontract.org/2004/07/ShippingWCF"',
        )
        for req in requests
    ])

    body = f"""<tns:getTrackings>
            <tns:ShippingData>
                {identify_xml}
            </tns:ShippingData>
        </tns:getTrackings>"""

    return provider_utils.create_envelope(body, settings)
