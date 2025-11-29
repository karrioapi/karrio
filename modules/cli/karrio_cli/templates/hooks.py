"""HOOKS TEMPLATES"""
from jinja2 import Template


HOOKS_EVENT_TEMPLATE = Template("""\"\"\"Karrio {{name}} webhook event processing implementation.\"\"\"

import hmac
import typing
import hashlib
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils
import karrio.providers.{{id}}.units as provider_units
import karrio.providers.{{id}}.tracking as tracking_provider


def on_webhook_event(
    payload: models.RequestPayload,
    settings: provider_utils.Settings,
) -> typing.Tuple[models.WebhookEventDetails, typing.List[models.Message]]:
    \"\"\"Process incoming webhook events from {{name}}.

    Expected payload format:
    {
      "eventName": "shipment.updated",
      "objectType": "shipment",
      "objectId": "6f384ad7-f8bf-40ce-8bf0-715248738f10",
      "data": {
        // Event-specific data (see examples below)
      }
    }
    \"\"\"

    if not verify_webhook_signature(payload, settings):
        return None, [
            models.Message(
                code="invalid_signature",
                message=f"Invalid webhook signature for {settings.carrier_name} webhook",
            )
        ]

    messages = error.parse_error_response(payload.body, settings)
    body = lib.typed(payload.body)

    # Extract tracking or shipment details based on event type
    tracking = lib.identity(
        tracking_provider._extract_details(
            body.data,
            settings,
            tracking_number=body.data.get("trackingNumber") if body.data else None,
        )
        if body.objectType == "shipment" and body.data
        else None
    )

    details = lib.identity(
        models.WebhookEventDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            tracking=tracking,
        )
        if body
        else None
    )

    return details, messages


def verify_webhook_signature(
    payload: models.RequestPayload,
    settings: provider_utils.Settings,
) -> bool:
    \"\"\"Verify the webhook signature using HMAC-SHA256.

    JavaScript equivalent:
        const crypto = require('crypto');

        function verifyWebhookSignature(payload, signature, secret) {
          const expectedSignature = crypto
            .createHmac('sha256', secret)
            .update(JSON.stringify(payload))
            .digest('hex');

          return crypto.timingSafeEqual(
            Buffer.from(signature),
            Buffer.from(expectedSignature)
          );
        }
    \"\"\"

    # Get the signature from headers
    headers = lib.typed(payload.headers)
    signature = headers.get("x-{{id}}-signature")
    secret = settings.connection_config.webhook_secret.state

    # If no signature provided, skip verification (or return False for strict mode)
    if not signature or not secret:
        return True

    # Compute expected signature using HMAC-SHA256
    # The payload body should be JSON serialized consistently
    payload_bytes = lib.to_json(payload.body).encode("utf-8")
    secret_bytes = secret.encode("utf-8")

    expected_signature = hmac.new(
        secret_bytes,
        payload_bytes,
        hashlib.sha256,
    ).hexdigest()

    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(signature, expected_signature)
""")


HOOKS_OAUTH_TEMPLATE = Template("""\"\"\"Karrio {{name}} OAuth processing implementation.\"\"\"

import typing
import urllib.parse
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils


def on_oauth_authorize(
    payload: models.OAuthAuthorizePayload,
    settings: provider_utils.Settings,
) -> typing.Tuple[models.OAuthAuthorizeRequest, typing.List[models.Message]]:
    \"\"\"Create OAuth authorize request for {{name}}.

    Generates the authorization URL and parameters needed to initiate
    the OAuth flow with {{name}}.
    \"\"\"
    messages: typing.List[models.Message] = []

    # Get OAuth credentials from system config
    client_id = settings.connection_system_config.get("{{id | upper}}_OAUTH_CLIENT_ID")
    redirect_uri = payload.options.get("redirect_uri", "")
    scope = payload.options.get("scope", "")

    if not client_id:
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code="OAUTH_CONFIG_ERROR",
                message="{{id | upper}}_OAUTH_CLIENT_ID is not configured in system settings",
            )
        )

    # Build authorization URL parameters
    auth_params = dict(
        client_id=client_id or "",
        response_type="code",
        redirect_uri=redirect_uri,
        scope=scope,
        state=payload.state or "",
    )

    authorization_url = lib.identity(
        f"{settings.server_url}/oauth/authorize?{urllib.parse.urlencode(auth_params)}"
        if client_id
        else None
    )

    return (
        models.OAuthAuthorizeRequest(
            carrier_name=settings.carrier_name,
            state=payload.state,
            meta=dict(
                authorization_url=authorization_url,
                client_id=client_id,
                scope=scope,
                redirect_uri=redirect_uri,
            ),
        ),
        messages,
    )


def on_oauth_callback(
    payload: models.RequestPayload,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[typing.List[typing.Dict]], typing.List[models.Message]]:
    \"\"\"Process OAuth authorization callback.

    Extracts the authorization code from the callback and returns
    credentials that can be used to complete the OAuth flow.
    \"\"\"
    messages = error.parse_error_response(
        payload.body,
        lib.typed(
            dict(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
            )
        ),
    )

    # Extract authorization code from callback
    code = payload.query.get("code") if payload.query else None
    state = payload.query.get("state") if payload.query else None

    if not code:
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code="OAUTH_CALLBACK_ERROR",
                message="No authorization code received in callback",
            )
        )
        return None, messages

    # Get OAuth credentials from system config
    client_id = settings.connection_system_config.get("{{id | upper}}_OAUTH_CLIENT_ID")
    client_secret = settings.connection_system_config.get("{{id | upper}}_OAUTH_CLIENT_SECRET")

    credentials = [
        dict(
            code=code,
            state=state,
            client_id=client_id,
            client_secret=client_secret,
        )
    ]

    return credentials, messages
""")


HOOKS_INIT_TEMPLATE = Template("""from karrio.providers.{{id}}.hooks.event import on_webhook_event
from karrio.providers.{{id}}.hooks.oauth import (
    on_oauth_authorize,
    on_oauth_callback,
)
""")


HOOKS_MAPPER_TEMPLATE = Template("""\"\"\"Karrio {{name}} client hooks.\"\"\"

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.api.hooks as hooks
import karrio.providers.{{id}} as provider
import karrio.mappers.{{id}}.settings as provider_settings


class Hooks(hooks.Hooks):
    settings: provider_settings.Settings

    def on_webhook_event(
        self, payload: models.RequestPayload
    ) -> typing.Tuple[models.WebhookEventDetails, typing.List[models.Message]]:
        return provider.on_webhook_event(payload, self.settings)

    def on_oauth_authorize(
        self, payload: models.OAuthAuthorizePayload
    ) -> typing.Tuple[models.OAuthAuthorizeRequest, typing.List[models.Message]]:
        return provider.on_oauth_authorize(payload, self.settings)

    def on_oauth_callback(
        self, payload: models.RequestPayload
    ) -> typing.Tuple[typing.List[typing.Dict], typing.List[models.Message]]:
        return provider.on_oauth_callback(payload, self.settings)
""")
