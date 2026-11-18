"""HOOKS TEMPLATES"""
from jinja2 import Template


HOOKS_EVENT_TEMPLATE = Template("""\"\"\"Karrio {{name}} webhook event processing implementation.\"\"\"

import hmac
import json
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

    # Fail closed: an event is only processed once its sender is authenticated.
    rejection = webhook_signature_error(payload, settings)
    if rejection is not None:
        return None, [rejection]

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


SIGNATURE_HEADER = "x-{{id}}-signature"


def webhook_signature_error(
    payload: models.RequestPayload,
    settings: provider_utils.Settings,
) -> typing.Optional[models.Message]:
    \"\"\"Authenticate an inbound event; None when the signature is valid.

    Fails closed, with a distinct message for each reason:
    - webhook_secret_not_configured: the connection has no stored secret
    - webhook_signature_missing: no signature header
    - invalid_signature: the signature matches none of the accepted forms

    A connector that verifies a signature must never skip the check because the
    header or the secret is absent: this route is public, so an unsigned event
    is an unauthenticated one.
    \"\"\"
    secret = settings.connection_config.webhook_secret.state
    headers = {str(k).lower(): v for k, v in (payload.headers or {}).items()}
    signature = headers.get(SIGNATURE_HEADER)

    if not secret:
        return models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code="webhook_secret_not_configured",
            message=(
                f"No webhook secret is configured for this {settings.carrier_name} "
                "connection: the event was not accepted"
            ),
        )

    if not signature:
        return models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code="webhook_signature_missing",
            message=(
                f"Missing {SIGNATURE_HEADER} header on {settings.carrier_name} "
                "webhook event"
            ),
        )

    return (
        None
        if _signature_matches(str(signature), secret, signed_payloads(payload))
        else models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code="invalid_signature",
            message=f"Invalid webhook signature for {settings.carrier_name} webhook",
        )
    )


def verify_webhook_signature(
    payload: models.RequestPayload,
    settings: provider_utils.Settings,
) -> bool:
    \"\"\"Verify the webhook signature (HMAC-SHA256 hex) with the stored secret.

    JavaScript equivalent:
        const expectedSignature = crypto
          .createHmac('sha256', secret)
          .update(JSON.stringify(payload))
          .digest('hex');

    Always False without a stored secret or without the signature header.
    \"\"\"

    return webhook_signature_error(payload, settings) is None


def signed_payloads(payload: models.RequestPayload) -> typing.List[bytes]:
    \"\"\"The byte strings a valid signature may have been made over.

    1. the raw request body, exactly as received (payload.raw_body);
    2. its compact re-serialisation in received key order (what
       JSON.stringify(payload) produces). Absent when that form cannot be
       encoded (an escaped lone surrogate).

    Never the indented, key-sorted output of lib.to_json.
    \"\"\"
    raw = (
        payload.raw_body.encode("utf-8")
        if isinstance(payload.raw_body, str)
        else payload.raw_body
    )
    parsed = lib.failsafe(lambda: json.loads(raw)) if raw else (payload.body or None)
    # A body that parses but has no UTF-8 form (an escaped lone surrogate) has no
    # compact candidate: it is simply absent, the raw body is still compared.
    compact = (
        lib.failsafe(
            lambda: json.dumps(
                parsed, separators=(",", ":"), ensure_ascii=False
            ).encode("utf-8")
        )
        if parsed is not None
        else None
    )

    return [_ for _ in [raw, compact] if _]


def _signature_matches(
    signature: str,
    secret: str,
    signed: typing.List[bytes],
) -> bool:
    given = signature.encode("utf-8")
    # Every candidate is compared, in constant time (bytes: also safe for a
    # non-ASCII header value).
    matches = [
        hmac.compare_digest(
            given,
            hmac.new(secret.encode("utf-8"), _, hashlib.sha256)
            .hexdigest()
            .encode("utf-8"),
        )
        for _ in signed
    ]

    return any(matches)
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


TEST_HOOKS_EVENT_TEMPLATE = Template('''"""{{name}} carrier webhook event tests.

Inbound events fail closed: no stored secret, no signature header or a wrong
signature are each rejected with their own message and nothing is applied.
"""

import hmac
import json
import hashlib
import unittest
import karrio.sdk as karrio
import karrio.core.models as models
import karrio.providers.{{id}}.hooks.event as event_hooks
from .fixture import gateway, client_id, client_secret

webhook_secret = "whsec_test_webhook_secret"
gateway_with_secret = karrio.gateway["{{id}}"].create(
    dict(client_id=client_id, client_secret=client_secret, test_mode=True, config=dict(webhook_secret=webhook_secret)),
)
WebhookEvent = {"eventName": "shipment.updated", "objectType": "shipment", "objectId": "shp-1", "data": {}}


def compact(body: dict) -> bytes:
    """What JSON.stringify(payload) produces."""
    return json.dumps(body, separators=(",", ":"), ensure_ascii=False).encode()


def sign(raw: bytes, secret: str = webhook_secret) -> str:
    return hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()


class Test{{compact_name}}WebhookEvent(unittest.TestCase):
    def payload(self, headers=None):
        raw = compact(WebhookEvent)
        return models.RequestPayload(
            url="https://api.karrio.io/v1/connections/webhook/{{id}}-123/events",
            body=WebhookEvent,
            headers=headers or {},
            raw_body=raw,
        )

    def test_on_webhook_event_rejects_a_missing_signature_header(self):
        details, messages = event_hooks.on_webhook_event(self.payload(), gateway_with_secret.settings)

        self.assertIsNone(details)
        self.assertEqual([_.code for _ in messages], ["webhook_signature_missing"])

    def test_on_webhook_event_rejects_a_wrong_signature(self):
        headers = {"x-{{id}}-signature": sign(compact(WebhookEvent), "another-secret")}
        details, messages = event_hooks.on_webhook_event(self.payload(headers), gateway_with_secret.settings)

        self.assertIsNone(details)
        self.assertEqual([_.code for _ in messages], ["invalid_signature"])

    def test_on_webhook_event_rejects_when_no_secret_is_stored(self):
        headers = {"x-{{id}}-signature": sign(compact(WebhookEvent))}
        details, messages = event_hooks.on_webhook_event(self.payload(headers), gateway.settings)

        self.assertIsNone(details)
        self.assertEqual([_.code for _ in messages], ["webhook_secret_not_configured"])

    def test_on_webhook_event_accepts_a_signed_event(self):
        headers = {"X-{{id | title}}-Signature": sign(compact(WebhookEvent))}
        details, messages = event_hooks.on_webhook_event(self.payload(headers), gateway_with_secret.settings)

        self.assertEqual(messages, [])
        self.assertIsNotNone(details)


if __name__ == "__main__":
    unittest.main()
''')
