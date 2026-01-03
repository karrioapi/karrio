"""Karrio DPD Group error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dpd_meta.utils as provider_utils
import karrio.schemas.dpd_meta.error_response as dpd_error


def parse_error_response(
    response: typing.Union[dict, typing.Any],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse DPD META-API error response."""
    errors = []

    # Handle dict response
    if isinstance(response, dict):
        # Check for DPD standard error format (official format from META-API docs)
        if "errorCode" in response or "errorMessage" in response:
            error = lib.to_object(dpd_error.ErrorResponseType, response)
            
            # Build error details including debugList if present
            error_details = {
                **kwargs,
                "errorOrigin": error.errorOrigin,
            }
            
            # Add debugList to details if present (for troubleshooting)
            if error.debugList:
                error_details["debugList"] = [
                    {
                        "request": item.request,
                        "response": item.response,
                        "methodName": item.methodName,
                    }
                    for item in error.debugList
                ]
            
            # Include error code in message for better visibility in UI
            error_code = error.errorCode or "ERROR"
            error_message = error.errorMessage or "Unknown error"
            display_message = f"Error Code {error_code}: {error_message}" if error.errorCode else error_message
            
            errors.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=error_code,
                    message=display_message,
                    details=error_details,
                )
            )
        # Check for HTTP error response
        elif response.get("detail"):
            errors.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code="HTTP_ERROR",
                    message=response.get("detail"),
                    details=kwargs,
                )
            )
        # Check for validation errors (DPD META-API validation format)
        elif response.get("errors") or response.get("message"):
            msg = response.get("message") or response.get("errors") or str(response)
            error_code = response.get("code") or "VALIDATION_ERROR"
            # Include code in message for visibility
            display_message = f"Error Code {error_code}: {msg}" if response.get("code") else str(msg)
            
            errors.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=error_code,
                    message=display_message,
                    details={**kwargs, "raw_response": response},
                )
            )

    return errors
