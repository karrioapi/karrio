from typing import Dict, Any, List
from karrio.core.models import Message


def parse_error_response(response: Dict[str, Any]) -> List[Message]:
    """Parse error response from Chit Chats API."""
    messages = []
    
    if 'error' in response:
        error_data = response.get('error', {})
        code = "400"  # Default error code
        
        # Extract the error message
        if isinstance(error_data, dict):
            message = error_data.get('message', 'Unknown error')
        else:
            message = str(error_data)
        
        messages.append(
            Message(
                code=code,
                message=message,
                carrier_id="chitchats"
            )
        )
    else:
        # If there's no structured error response, create a generic error message
        messages.append(
            Message(
                code="500",
                message="An unexpected error occurred processing the Chit Chats API response",
                carrier_id="chitchats"
            )
        )
    
    return messages 
