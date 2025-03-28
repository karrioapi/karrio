"""Karrio Chit Chats batch operations."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.chitchats.error as error
import karrio.providers.chitchats.utils as provider_utils


def parse_batch_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    """Parse a batch response."""
    response = _response.deserialize()
    
    messages = error.parse_error_response(response, settings)
    
    try:
        # Extract batch data
        batch_data = response.get('batch', {})
        if not batch_data and isinstance(response, dict) and 'id' in response:
            # Sometimes the API returns just the batch directly
            batch_data = response
        
        batch = models.ConfirmationDetails(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            operation="Create Batch",
            success=True,
            reference=str(batch_data.get('id')),
            meta={
                "description": batch_data.get('description'),
                "status": batch_data.get('status'),
                "created_at": batch_data.get('created_at'),
                "label_url": batch_data.get('label_png_url'),
                "zpl_label_url": batch_data.get('label_zpl_url'),
            }
        )
        
        return batch, messages
    except Exception as e:
        messages.append(models.Message(
            code="500",
            message=f"Error parsing batch response: {str(e)}",
            carrier_id=settings.carrier_id
        ))
        # Return an empty batch
        return models.ConfirmationDetails(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            operation="Create Batch",
            success=False
        ), messages


def batch_request(
    payload: models.ManifestRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a batch request."""
    request_data = {
        "description": payload.reference or f"Batch created via Karrio on {lib.today()}"
    }
    
    return lib.Serializable(request_data, lib.identity)


def parse_add_to_batch_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    """Parse an add to batch response."""
    response = _response.deserialize()
    
    messages = error.parse_error_response(response, settings)
    
    # The API doesn't return batch details when adding shipments to a batch
    # So we construct a basic batch object with the batch ID
    batch = models.ConfirmationDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        operation="Add to Batch",
        success=response.get("success", True),
        reference=str(_response.ctx.get("batch_id", "")),
        meta={
            "message": response.get("message", "Shipments added to batch")
        }
    )
    
    return batch, messages


def add_to_batch_request(
    payload: models.ManifestRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a request to add shipments to a batch."""
    request_data = {
        "batch_id": int(payload.reference),
        "shipment_ids": payload.shipment_identifiers
    }
    
    ctx = {"batch_id": payload.reference}
    
    return lib.Serializable(request_data, lib.identity, ctx=ctx) 
