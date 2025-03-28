"""Karrio Chit Chats shipping API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.chitchats.error as error
import karrio.providers.chitchats.utils as provider_utils
import karrio.providers.chitchats.units as provider_units
from karrio.providers.chitchats.utils import make_request


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    """Parse a shipment response from Chit Chats API."""
    response = _response.deserialize()
    
    messages = error.parse_error_response(response, settings)
    
    try:
        # Extract shipment data
        shipment_data = response.get('shipment', {})
        if not shipment_data and isinstance(response, dict) and 'id' in response:
            # Sometimes the API returns just the shipment directly
            shipment_data = response
        
        # Extract tracking information
        tracking_number = shipment_data.get("carrier_tracking_code", "")
        if not tracking_number:
            tracking_number = shipment_data.get("id", "")
        
        # Extract label URLs
        label_url = shipment_data.get("postage_label_png_url", "")
        zpl_label_url = shipment_data.get("postage_label_zpl_url", "")
        
        # Determine if the shipment is complete
        is_ready = shipment_data.get("status") == "ready"
        
        # Get rate details if available
        selected_rate = None
        rates = shipment_data.get("rates", [])
        if rates and len(rates) > 0:
            for rate in rates:
                if rate.get("postage_type") == shipment_data.get("postage_type"):
                    selected_rate = {
                        "service_name": rate.get("postage_description", rate.get("postage_type", "")),
                        "total_charge": float(rate.get("purchase_amount") or rate.get("payment_amount") or rate.get("postage_fee", 0)),
                        "currency": rate.get("currency", "CAD"),
                    }
                    break
        
        # Create the shipment details
        return models.ShipmentDetails(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            tracking_number=tracking_number,
            shipment_identifier=shipment_data.get("id", ""),
            label_type="URL",
            label_url=label_url,
            selected_rate=selected_rate,
            meta={
                "carrier": shipment_data.get("carrier", ""),
                "status": shipment_data.get("status", ""),
                "batch_id": shipment_data.get("batch_id"),
                "tracking_url": shipment_data.get("tracking_url", ""),
                "zpl_label_url": zpl_label_url,
                "created_at": shipment_data.get("created_at", ""),
                "purchase_amount": shipment_data.get("purchase_amount"),
                "description": shipment_data.get("description"),
                "value": shipment_data.get("value"),
                "value_currency": shipment_data.get("value_currency"),
            }
        ), messages
    except Exception as e:
        messages.append(models.Message(
            code="500",
            message=f"Error parsing shipment response: {str(e)}",
            carrier_id=settings.carrier_id
        ))
        # Return a minimal shipment object
        return models.ShipmentDetails(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            tracking_number="",
            shipment_identifier=""
        ), messages


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a shipment request for Chit Chats API."""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    service = lib.to_services(payload.services).first
    options = lib.to_shipping_options(payload.options)
    packages = lib.to_packages(
        payload.parcels,
        required=["weight"],
        options=options
    )
    package = packages[0]  # Get the first package details
    
    # Prepare the request data
    request_data = {
        "name": recipient.person_name,
        "address_1": recipient.address_line1,
        "address_2": recipient.address_line2,
        "city": recipient.city,
        "province_code": recipient.state_code,
        "postal_code": recipient.postal_code,
        "country_code": recipient.country_code,
        "phone": recipient.phone_number,
        "email": recipient.email,
        
        # Package information
        "package_contents": options.get("package_contents", settings.default_options["package_contents"]),
        "description": options.get("description", f"1 {options.get('item_description', 'Package')}"),
        "value": str(options.get("value", "0")),
        "value_currency": options.get("value_currency", settings.default_options["currency"]),
        
        # Order information (if available)
        "order_id": options.get("order_id", ""),
        "order_store": options.get("order_store", ""),
        
        # Package dimensions and weight
        "package_type": provider_units.map_package_type(options.get("package_type", "parcel")),
        "weight_unit": provider_units.map_weight_unit(package.weight_unit),
        "weight": package.weight.value,
        "size_unit": provider_units.map_dimension_unit(package.dimension_unit),
        "size_x": package.length.value,
        "size_y": package.width.value,
        "size_z": package.height.value,
        
        # Service options
        "insurance_requested": options.get("insurance", settings.default_options["insurance_requested"]),
        "signature_requested": options.get("signature", settings.default_options["signature_requested"]),
        
        # Shipping service selection
        "postage_type": service.value if service else options.get("postage_type", ""),
        "ship_date": options.get("ship_date", "today"),
    }
    
    # Add return address if provided
    if shipper:
        request_data.update({
            "return_name": shipper.person_name,
            "return_address_1": shipper.address_line1,
            "return_address_2": shipper.address_line2 or "",
            "return_city": shipper.city,
            "return_province_code": shipper.state_code,
            "return_postal_code": shipper.postal_code,
            "return_country_code": shipper.country_code,
            "return_phone": shipper.phone_number,
        })
    
    # Add customs/international information if needed
    if recipient.country_code != shipper.country_code:
        # Add line items for international shipments
        commodities = lib.to_items(payload.customs.commodities or [])
        if commodities:
            request_data["line_items"] = [
                {
                    "description": item.description,
                    "quantity": item.quantity,
                    "value": item.value_amount,
                    "weight": item.weight,
                    "weight_unit": provider_units.map_weight_unit(item.weight_unit or "g"),
                    "hs_tariff_code": item.hs_code,
                    "origin_country": item.origin_country or shipper.country_code,
                }
                for item in commodities
            ]
    
    return lib.Serializable(request_data, lib.identity)


def parse_shipment_buy_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    """Parse a shipment buy response."""
    # The buy response is the same format as the shipment response
    return parse_shipment_response(_response, settings)


def shipment_buy_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a request to buy postage for a shipment."""
    request_data = {}
    
    # Add postage_type if specified
    if payload.service and payload.service.code:
        request_data["postage_type"] = payload.service.code
    
    ctx = {"shipment_id": payload.shipment_identifier}
    
    return lib.Serializable(request_data, lib.identity, ctx=ctx) 
