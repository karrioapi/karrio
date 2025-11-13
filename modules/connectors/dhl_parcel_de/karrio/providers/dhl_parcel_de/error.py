import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dhl_parcel_de.utils as provider_utils


def parse_error_response(
    response: typing.Union[typing.List[dict], dict],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]
    messages = []

    # Parse top-level errors
    errors = [
        response.get("status") if isinstance(response.get("status"), dict) else response
        for response in responses
        if (
            ("title" in response and (response.get("title") or "") != "ok")
            or (
                isinstance(response.get("status"), dict)
                and "title" in response.get("status", {})
                and (response.get("status", {}).get("title") or "").lower() != "ok"
            )
        )
    ]

    # Create messages for top-level errors
    for error in errors:
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=str(error.get("status") or error.get("statusCode")),
                message=error.get("detail") or error.get("title"),
                details={
                    "title": error.get("title"),
                    "instance": error.get("instance"),
                    **kwargs,
                },
            )
        )

    # Parse validation messages from items
    for response in responses:
        items = response.get("items", [])
        for item in items:
            shipment_no = item.get("shipmentNo")
            validation_messages = item.get("validationMessages", [])

            for validation_msg in validation_messages:
                validation_state = validation_msg.get("validationState", "")
                property_name = validation_msg.get("property", "")
                message_text = validation_msg.get("validationMessage", "")

                # Only process validation messages with actual error/warning states and messages
                # Skip placeholder/informational messages (validationState: "string" or empty)
                if (
                    message_text
                    and validation_state
                    and validation_state.lower() in ["error", "warning"]
                ):
                    details = {
                        "property": property_name,
                        "validationState": validation_state,
                    }
                    if shipment_no:
                        details["shipmentNo"] = shipment_no

                    messages.append(
                        models.Message(
                            carrier_id=settings.carrier_id,
                            carrier_name=settings.carrier_name,
                            code=validation_state,
                            message=f"{property_name}: {message_text}" if property_name else message_text,
                            details={**details, **kwargs},
                        )
                    )

    return messages
