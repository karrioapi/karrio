"""Karrio Chit Chats rating API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.chitchats.error as error
import karrio.providers.chitchats.utils as provider_utils
import karrio.providers.chitchats.units as provider_units
from karrio.providers.chitchats.utils import make_request


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    """Parse the rate response from Chit Chats API."""
    response = _response.deserialize()
    
    messages = error.parse_error_response(response, settings)
    rates = []
    
    try:
        # Handle both shipment and batch responses
        shipment_data = response.get('shipment', {})
        if not shipment_data and isinstance(response, list) and len(response) > 0:
            # Handle case where the response is a list of shipments
            shipment_data = response[0]
        
        rates_data = shipment_data.get('rates', [])
        
        if not rates_data:
            messages.append(models.Message(
                code="404",
                message="No rates found in response",
                carrier_id=settings.carrier_id
            ))
            return rates, messages
        
        rates = [_extract_details(rate_data, settings) for rate_data in rates_data]
    except Exception as e:
        messages.append(models.Message(
            code="500",
            message=f"Error parsing rates response: {str(e)}",
            carrier_id=settings.carrier_id
        ))
    
    return rates, messages


def _extract_details(
    rate_data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    """Extract rate details from a single rate entry."""
    service_name = rate_data.get('postage_type', 'unknown')
    service_display_name = rate_data.get('postage_description',
                          settings.services.get(service_name, {}).get('name', service_name))
    total_charge = float(rate_data.get('purchase_amount') or 
                        rate_data.get('payment_amount') or 
                        rate_data.get('postage_fee', 0))
    currency = rate_data.get('currency', "CAD")
    
    # Extract transit info if available
    transit_info = rate_data.get('delivery_time_description', '')
    transit_days = None
    if 'delivery in' in transit_info.lower():
        try:
            parts = transit_info.split('in')
            days_part = parts[1].strip().split()[0]
            transit_days = int(days_part)
        except:
            transit_days = None
    
    # Extract additional fees
    extra_charges = []
    
    # Add insurance fee if present
    if rate_data.get('insurance_fee') and float(rate_data.get('insurance_fee', 0)) > 0:
        extra_charges.append({
            "name": "Insurance Fee",
            "amount": float(rate_data.get('insurance_fee', 0)),
            "currency": currency
        })
    
    # Add delivery fee if present
    if rate_data.get('delivery_fee') and float(rate_data.get('delivery_fee', 0)) > 0:
        extra_charges.append({
            "name": "Delivery Fee",
            "amount": float(rate_data.get('delivery_fee', 0)),
            "currency": currency
        })
    
    # Add taxes if present
    if rate_data.get('federal_tax') and float(rate_data.get('federal_tax', 0)) > 0:
        extra_charges.append({
            "name": rate_data.get('federal_tax_label', 'Federal Tax'),
            "amount": float(rate_data.get('federal_tax', 0)),
            "currency": currency
        })
    
    if rate_data.get('provincial_tax') and float(rate_data.get('provincial_tax', 0)) > 0:
        extra_charges.append({
            "name": rate_data.get('provincial_tax_label', 'Provincial Tax'),
            "amount": float(rate_data.get('provincial_tax', 0)),
            "currency": currency
        })
    
    return models.RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        service_name=service_display_name,
        service_code=service_name,
        total_charge=total_charge,
        currency=currency,
        transit_days=transit_days,
        extra_charges=extra_charges,
        meta={
            "postage_type": service_name,
            "carrier": rate_data.get('postage_carrier_type'),
            "tracking_included": rate_data.get('tracking_type_description', '').lower().startswith('full tracking'),
            "is_insured": rate_data.get('is_insured', False),
            "payment_amount": rate_data.get('payment_amount')
        }
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a rate request for Chit Chats API."""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    options = lib.to_shipping_options(payload.options)
    packages = lib.to_packages(
        payload.parcels,
        required=["weight"],
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
        "package_contents": options.get("package_contents", settings.default_options["package_contents"]),
        "description": options.get("description", f"1 {options.get('item_description', 'Package')}"),
        "value": str(options.get("value", "0")),
        "value_currency": options.get("value_currency", settings.default_options["currency"]),
        "package_type": provider_units.map_package_type(options.get("package_type", "parcel")),
        "weight_unit": provider_units.map_weight_unit(package.weight_unit),
        "weight": package.weight.value,
        "size_unit": provider_units.map_dimension_unit(package.dimension_unit),
        "size_x": package.length.value,
        "size_y": package.width.value,
        "size_z": package.height.value,
        "postage_type": "unknown",  # Use "unknown" to get all available rates
        "ship_date": options.get("ship_date", "today"),
        "insurance_requested": options.get("insurance", settings.default_options["insurance_requested"]),
        "signature_requested": options.get("signature", settings.default_options["signature_requested"]),
    }
    
    if shipper:
        # Add return address if provided
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
    
    return lib.Serializable(request_data, lib.identity) 
