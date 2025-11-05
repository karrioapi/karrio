"""Karrio DPD Group tracking implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dpd_group.error as error
import karrio.providers.dpd_group.utils as provider_utils
import karrio.providers.dpd_group.units as provider_units
import karrio.schemas.dpd_group.tracking_response as dpd_group


def parse_tracking_response(
    _response: lib.Deserializable,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    """Parse DPD Group tracking response."""
    responses = _response.deserialize()
    tracking_details = []
    all_messages = []

    # Handle list of (tracking_number, response_dict) tuples from proxy
    if not isinstance(responses, list):
        responses = [(None, responses)]

    for tracking_number, response in responses:
        # Parse errors
        messages = error.parse_error_response(response, settings)
        if messages:
            all_messages.extend(messages)
            continue

        # Handle empty or invalid responses
        if not isinstance(response, dict):
            continue

        # Parse tracking data
        tracking_data = lib.to_object(dpd_group.TrackingResponseType, response)

        detail = models.TrackingDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            tracking_number=tracking_data.trackingNumber if hasattr(tracking_data, 'trackingNumber') else tracking_number,
            status=provider_units.TrackingStatus.map(tracking_data.status if hasattr(tracking_data, 'status') else ""),
            events=[
                models.TrackingEvent(
                    date=lib.fdate(event.timestamp, "%Y-%m-%dT%H:%M:%SZ") if hasattr(event, 'timestamp') and event.timestamp else None,
                    description=event.description if hasattr(event, 'description') else "",
                    code=event.status if hasattr(event, 'status') else "",
                    time=lib.ftime(event.timestamp, "%Y-%m-%dT%H:%M:%SZ") if hasattr(event, 'timestamp') and event.timestamp else None,
                    location=", ".join(filter(None, [
                        getattr(event.location, 'city', None) if hasattr(event, 'location') and event.location else None,
                        getattr(event.location, 'postalCode', None) if hasattr(event, 'location') and event.location else None,
                        getattr(event.location, 'country', None) if hasattr(event, 'location') and event.location else None,
                    ])) if hasattr(event, 'location') and event.location else "",
                )
                for event in (tracking_data.events or [])
            ],
            estimated_delivery=lib.fdate(tracking_data.estimatedDelivery) if hasattr(tracking_data, 'estimatedDelivery') and tracking_data.estimatedDelivery else None,
            info=models.TrackingInfo(
                carrier_tracking_link=settings.tracking_url.format(
                    tracking_data.trackingNumber if hasattr(tracking_data, 'trackingNumber') else tracking_number
                ),
                shipment_service=None,
            ),
        )
        tracking_details.append(detail)

    return tracking_details, all_messages


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create DPD Group tracking request."""
    # For DPD Group, tracking is done via GET requests with tracking number in URL
    # So we just return the tracking numbers
    return lib.Serializable(payload.tracking_numbers)
