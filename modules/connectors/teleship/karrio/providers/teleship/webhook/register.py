"""Karrio Teleship webhook registration implementation."""

import typing
import karrio.schemas.teleship.webhook_request as teleship
import karrio.schemas.teleship.webhook_response as webhook
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.teleship.error as error
import karrio.providers.teleship.utils as provider_utils


def parse_webhook_registration_response(
    _response: lib.Deserializable[str],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.WebhookRegistrationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    details = lib.to_object(webhook.WebhookResponseType, response)

    webhook_details = (
        models.WebhookRegistrationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            webhook_identifier=details.id,
            secret=details.secret,
            meta=lib.to_dict(details),
        )
        if details and details.id
        else None
    )

    return webhook_details, messages


def webhook_registration_request(
    payload: models.WebhookRegistrationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a Teleship webhook registration request"""

    request = teleship.WebhookRequestType(
        url=payload.url,
        description=payload.description,
        enabled=True,
        enabledEvents=(payload.enabled_events if any(payload.enabled_events) else ["*"]),
    )

    return lib.Serializable(request, lib.to_dict)
