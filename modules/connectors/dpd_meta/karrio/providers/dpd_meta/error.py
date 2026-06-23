"""Karrio DPD Meta error parser."""

import typing

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.dpd_meta.utils as provider_utils
import karrio.schemas.dpd_meta.error_response as dpd_error


def parse_error_response(
    response: dict | list | typing.Any,
    settings: provider_utils.Settings,
    **kwargs,
) -> list[models.Message]:
    """Parse DPD META-API error response.

    Handles dict, list, and unexpected response formats.
    """
    errors = []

    # Normalize: wrap dict in list for uniform handling (like DHL Parcel DE)
    results = response if isinstance(response, list) else [response]

    for result in results:
        if not isinstance(result, dict):
            continue

        # Check for DPD standard error format (official format from META-API docs)
        if "errorCode" in result or "errorMessage" in result:
            error = lib.to_object(dpd_error.ErrorResponseType, result)

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

            error_code = error.errorCode or "ERROR"
            error_message = error.errorMessage or "Unknown error"
            display_message = f"Error Code {error_code}: {error_message}" if error.errorCode else error_message

            errors.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=error_code,
                    message=lib.text(display_message, max=200),
                    details=error_details,
                )
            )
        # Check for HTTP error response (from lib.error_decoder)
        elif result.get("detail") or result.get("http_status"):
            http_status = result.get("http_status", "")
            http_message = result.get("http_message", "")
            detail = result.get("detail") or f"HTTP {http_status}: {http_message}"
            errors.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=str(http_status or "HTTP_ERROR"),
                    message=lib.text(detail, max=200),
                    details=kwargs,
                )
            )
        # Check for validation errors (DPD META-API validation format)
        elif result.get("errors") or result.get("message"):
            msg = result.get("message") or result.get("errors") or str(result)
            error_code = result.get("code") or "VALIDATION_ERROR"
            display_message = f"Error Code {error_code}: {msg}" if result.get("code") else str(msg)

            errors.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=error_code,
                    message=lib.text(display_message, max=200),
                    details=kwargs,
                )
            )

    return errors


WS_AUTH_EXPIRED_CODES = ("LOGIN_5", "LOGIN_6")


def is_ws_auth_expired(messages: list[models.Message]) -> bool:
    """LOGIN_5 (authtoken invalid) / LOGIN_6 (session expired) → the cached
    public-WS authToken is dead and DPD mandates a fresh login."""
    return any(message.code in WS_AUTH_EXPIRED_CODES for message in messages)


def parse_soap_faults(
    response: lib.Element,
    settings: provider_utils.Settings,
) -> list[models.Message]:
    """Parse DPD public-WS SOAP faults into karrio Messages.

    Mirrors the dpd (classic) connector's fault handling: the `<detail>`
    carries the specific fault (`authenticationFault` / `dataFault` /
    `systemFault`) with `errorCode` + `errorMessage`; the generic
    `<soap:Fault>` `faultcode` / `faultstring` is the fallback when no
    `<detail>` is present.
    """
    faults: list[lib.Element] = lib.find_element("Fault", response)
    details: list[lib.Element] = sum(([*node] for node in lib.find_element("detail", response)), start=[])

    if details:
        errors = [(node.findtext("errorCode"), node.findtext("errorMessage")) for node in details]
    else:
        errors = [(node.findtext("faultcode"), node.findtext("faultstring")) for node in faults]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=code or "SOAP_FAULT",
            message=message or "DPD SOAP fault",
        )
        for code, message in errors
    ]
