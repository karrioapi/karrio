from typing import List
from karrio.core.models import Message
from karrio.providers.dhl_ecommerce_europe.utils import Settings


def parse_error_response(response: dict, settings: Settings) -> List[Message]:
    """Parse error messages from DHL eCommerce Europe API response."""
    
    messages: List[Message] = []
    
    # Handle standard error structure
    if "errors" in response:
        for error in response["errors"]:
            messages.append(
                Message(
                    code=error.get("code"),
                    message=error.get("message", error.get("detail")),
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                )
            )
    
    # Handle single error structure
    if "error" in response:
        error = response["error"]
        messages.append(
            Message(
                code=error.get("code"),
                message=error.get("message", error.get("detail")),
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
            )
        )
    
    # Handle validation errors
    if "detail" in response and response.get("status") >= 400:
        messages.append(
            Message(
                code=str(response.get("status")),
                message=response.get("detail"),
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
            )
        )
    
    return messages 