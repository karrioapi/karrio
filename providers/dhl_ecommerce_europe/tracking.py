import karrio.schemas.dhl_ecommerce_europe.tracking_response as tracking
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dhl_ecommerce_europe.error as error
import karrio.providers.dhl_ecommerce_europe.utils as provider_utils
import karrio.providers.dhl_ecommerce_europe.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    tracking_details = []
    if "shipments" in response:
        tracking_response = lib.to_object(tracking.TrackingResponse, response)
        tracking_details = [
            _extract_details(shipment, settings) 
            for shipment in tracking_response.shipments
        ]

    return tracking_details, messages


def _extract_details(
    shipment: tracking.Shipment,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    # Handle both dict and object cases
    if isinstance(shipment, dict):
        shipment_data = shipment
    else:
        shipment_data = lib.to_dict(shipment)
    
    # Extract events
    events = []
    shipment_events = shipment_data.get('events', [])
    if shipment_events:
        for event_data in shipment_events:
            if isinstance(event_data, dict):
                event = event_data
            else:
                event = lib.to_dict(event_data)
                
            location = None
            if event.get('location') and event['location'].get('address'):
                addr = event['location']['address']
                location = f"{addr.get('addressLocality', '')}, {addr.get('postalCode', '')}, {addr.get('countryCode', '')}"
            
            events.append(
                models.TrackingEvent(
                    code=event.get('typeCode'),
                    description=event.get('description'),
                    date=lib.fdate(event.get('timestamp'), "%Y-%m-%dT%H:%M:%S"),
                    time=lib.ftime(event.get('timestamp'), "%Y-%m-%dT%H:%M:%S", "%H:%M:%S"),
                    location=location,
                )
            )

    # Extract status
    status = "in_transit"  # default
    shipment_status = shipment_data.get('status')
    if shipment_status:
        if isinstance(shipment_status, dict):
            status_code = shipment_status.get('statusCode')
        else:
            status_code = getattr(shipment_status, 'statusCode', None)
        
        if status_code:
            status = _extract_status(status_code)

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment_data.get('shipmentTrackingNumber'),
        events=events,
        status=status,
        delivered=status == "delivered",
        estimated_delivery=lib.fdate(shipment_data.get('estimatedTimeOfDelivery'), "%Y-%m-%dT%H:%M:%S") if shipment_data.get('estimatedTimeOfDelivery') else None,
        meta=dict(
            shipment_status=shipment_status,
        ),
    )


def _extract_status(status_code: str) -> str:
    """Extract and normalize the shipment status."""
    status_map = {
        "PU": "in_transit",  # Picked up
        "PL": "in_transit",  # Processed
        "IT": "in_transit",  # In transit
        "OK": "delivered",  # Delivered
        "DF": "delivery_failed",  # Delivery failed
        "RT": "delivery_failed",  # Returned
        "UD": "delivery_failed",  # Undelivered
        "delivered": "delivered",
        "in_transit": "in_transit",
        "exception": "delivery_failed",
    }
    
    return status_map.get(status_code.lower() if status_code else "", "in_transit")


def tracking_request(payload: models.TrackingRequest, settings: provider_utils.Settings) -> lib.Serializable:
    """Create tracking request for DHL eCommerce Europe."""
    
    request_data = {
        "trackingNumbers": payload.tracking_numbers,
        "service": "express",
        "requesterCountryCode": settings.shipper_country_code or "DE",
        "originCountryCode": settings.shipper_country_code or "DE",
    }

    return lib.Serializable(request_data) 
