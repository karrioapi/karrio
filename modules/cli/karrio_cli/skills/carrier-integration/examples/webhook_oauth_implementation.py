"""Example: Webhook & OAuth Implementation Pattern

This example demonstrates the canonical patterns for implementing:
1. Webhook registration/deregistration
2. OAuth authentication flows
3. Callback event handling
"""

# === FILE: karrio/providers/[carrier]/webhook/__init__.py ===

from karrio.providers.[carrier].webhook.register import (
    parse_webhook_registration_response,
    webhook_registration_request,
)
from karrio.providers.[carrier].webhook.deregister import (
    parse_webhook_deregistration_response,
    webhook_deregistration_request,
)


# === FILE: karrio/providers/[carrier]/webhook/register.py ===

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.[carrier].error as error
import karrio.providers.[carrier].utils as provider_utils
import karrio.schemas.[carrier].webhook_request as carrier_req
import karrio.schemas.[carrier].webhook_response as carrier_res


def parse_webhook_registration_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.WebhookRegistrationDetails, typing.List[models.Message]]:
    """Parse webhook registration response."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    webhook = (
        _extract_details(response, settings)
        if not any(messages)
        else None
    )
    
    return webhook, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.WebhookRegistrationDetails:
    """Extract webhook registration details."""
    webhook = lib.to_object(carrier_res.WebhookResponseType, data)
    
    return models.WebhookRegistrationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        webhook_id=webhook.webhookId,
        url=webhook.url if hasattr(webhook, 'url') else None,
        events=webhook.events if hasattr(webhook, 'events') else [],
        meta=dict(
            status=webhook.status if hasattr(webhook, 'status') else None,
            secret=webhook.secret if hasattr(webhook, 'secret') else None,
        ),
    )


def webhook_registration_request(
    payload: models.WebhookRegistrationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create webhook registration request."""
    request = carrier_req.WebhookRequestType(
        url=payload.url,
        events=payload.events or [
            "shipment.created",
            "shipment.status.updated",
            "shipment.delivered",
            "tracking.updated",
        ],
        # Optional: secret for signature validation
        secret=payload.options.get("secret") if payload.options else None,
        # Account
        accountNumber=settings.account_number,
    )
    
    return lib.Serializable(request, lib.to_dict)


# === FILE: karrio/providers/[carrier]/webhook/deregister.py ===

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.[carrier].error as error
import karrio.providers.[carrier].utils as provider_utils


def parse_webhook_deregistration_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    """Parse webhook deregistration response."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    success = response.get("success", False) or response.get("deleted", False)
    
    confirmation = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=success,
            operation="Deregister Webhook",
        )
        if success and not any(messages)
        else None
    )
    
    return confirmation, messages


def webhook_deregistration_request(
    payload: models.WebhookDeregistrationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create webhook deregistration request."""
    # Most APIs just need the webhook ID
    return lib.Serializable(payload.webhook_id)


# === FILE: karrio/providers/[carrier]/callback/__init__.py ===

from karrio.providers.[carrier].callback.event import on_webhook_event
from karrio.providers.[carrier].callback.oauth import (
    on_oauth_authorize,
    on_oauth_callback,
)


# === FILE: karrio/providers/[carrier]/callback/event.py ===

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.[carrier].utils as provider_utils
import karrio.providers.[carrier].units as provider_units


def on_webhook_event(
    event: dict,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.TrackingDetails], typing.List[models.Message]]:
    """Process incoming webhook event.
    
    This function is called when the carrier sends a webhook notification.
    It parses the event and returns standardized tracking updates.
    """
    event_type = event.get("type", "")
    
    # Route to appropriate handler based on event type
    handlers = {
        "tracking.updated": _handle_tracking_event,
        "shipment.status.updated": _handle_status_event,
        "shipment.delivered": _handle_delivery_event,
    }
    
    handler = handlers.get(event_type, _handle_unknown_event)
    return handler(event, settings)


def _handle_tracking_event(
    event: dict,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.TrackingDetails], typing.List[models.Message]]:
    """Handle tracking update events."""
    tracking_number = event.get("trackingNumber")
    status_code = event.get("status", "")
    
    # Map carrier status to Karrio unified status
    status = provider_units.TrackingStatus.map(status_code)
    
    # Build tracking event
    tracking_event = models.TrackingEvent(
        date=lib.fdate(event.get("timestamp")),
        description=event.get("description", ""),
        code=event.get("statusCode"),
        location=event.get("location", ""),
    )
    
    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        status=status.value,
        events=[tracking_event],
        delivered=status.value == "delivered",
    ), []


def _handle_status_event(
    event: dict,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.TrackingDetails], typing.List[models.Message]]:
    """Handle shipment status update events."""
    # Similar to tracking but may include additional shipment context
    return _handle_tracking_event(event, settings)


def _handle_delivery_event(
    event: dict,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.TrackingDetails], typing.List[models.Message]]:
    """Handle delivery confirmation events."""
    tracking_number = event.get("trackingNumber")
    
    tracking_event = models.TrackingEvent(
        date=lib.fdate(event.get("deliveryDate")),
        description="Package delivered",
        code="DELIVERED",
        location=event.get("deliveryLocation", ""),
    )
    
    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        status="delivered",
        events=[tracking_event],
        delivered=True,
        info=models.TrackingInfo(
            signed_by=event.get("signedBy"),
        ) if event.get("signedBy") else None,
    ), []


def _handle_unknown_event(
    event: dict,
    settings: provider_utils.Settings,
) -> typing.Tuple[None, typing.List[models.Message]]:
    """Handle unknown event types."""
    return None, [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code="UNKNOWN_EVENT",
            message=f"Unknown webhook event type: {event.get('type')}",
        )
    ]


# === FILE: karrio/providers/[carrier]/callback/oauth.py ===

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.[carrier].error as error
import karrio.providers.[carrier].utils as provider_utils


def on_oauth_authorize(
    settings: provider_utils.Settings,
    redirect_uri: str,
    state: str = None,
) -> str:
    """Generate OAuth authorization URL.
    
    This is called when initiating the OAuth flow.
    Returns the URL to redirect the user to for authorization.
    """
    params = lib.to_query_string({
        "client_id": settings.client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "shipments tracking",  # Adjust scopes as needed
        "state": state,
    })
    
    return f"{settings.oauth_url}/authorize?{params}"


def on_oauth_callback(
    code: str,
    settings: provider_utils.Settings,
    redirect_uri: str,
) -> typing.Tuple[typing.Optional[dict], typing.List[models.Message]]:
    """Handle OAuth callback and exchange code for tokens.
    
    This is called when the user is redirected back after authorization.
    Exchanges the authorization code for access/refresh tokens.
    """
    try:
        response = lib.request(
            url=f"{settings.oauth_url}/token",
            method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=lib.to_query_string({
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "client_id": settings.client_id,
                "client_secret": settings.client_secret,
            }),
            decoder=lib.to_dict,
        )
        
        if "error" in response:
            return None, [
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=response.get("error"),
                    message=response.get("error_description", "OAuth error"),
                )
            ]
        
        return {
            "access_token": response.get("access_token"),
            "refresh_token": response.get("refresh_token"),
            "expires_in": response.get("expires_in"),
            "token_type": response.get("token_type", "Bearer"),
        }, []
        
    except Exception as e:
        return None, [
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code="OAUTH_ERROR",
                message=str(e),
            )
        ]


# === FILE: karrio/mappers/[carrier]/callback.py ===

"""Callback mapper for webhook and OAuth handling."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.[carrier].callback as callback
import karrio.mappers.[carrier].settings as provider_settings


class CallbackMapper:
    """Maps callback events to Karrio models."""
    
    settings: provider_settings.Settings
    
    def __init__(self, settings: provider_settings.Settings):
        self.settings = settings
    
    def process_webhook_event(
        self,
        event: dict,
    ) -> typing.Tuple[typing.Optional[models.TrackingDetails], typing.List[models.Message]]:
        """Process incoming webhook event."""
        return callback.on_webhook_event(event, self.settings)
    
    def get_oauth_authorize_url(
        self,
        redirect_uri: str,
        state: str = None,
    ) -> str:
        """Get OAuth authorization URL."""
        return callback.on_oauth_authorize(self.settings, redirect_uri, state)
    
    def process_oauth_callback(
        self,
        code: str,
        redirect_uri: str,
    ) -> typing.Tuple[typing.Optional[dict], typing.List[models.Message]]:
        """Process OAuth callback."""
        return callback.on_oauth_callback(code, self.settings, redirect_uri)


# === FILE: karrio/mappers/[carrier]/proxy.py (webhook portion) ===

def register_webhook(self, request: lib.Serializable) -> lib.Deserializable[str]:
    """Register a webhook endpoint."""
    response = lib.request(
        url=f"{self.settings.server_url}/webhooks",
        data=lib.to_json(request.serialize()),
        trace=self.trace_as("json"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.settings.api_key}",
        },
    )
    return lib.Deserializable(response, lib.to_dict)


def deregister_webhook(self, request: lib.Serializable) -> lib.Deserializable[str]:
    """Deregister a webhook endpoint."""
    webhook_id = request.serialize()
    
    response = lib.request(
        url=f"{self.settings.server_url}/webhooks/{webhook_id}",
        trace=self.trace_as("json"),
        method="DELETE",
        headers={
            "Authorization": f"Bearer {self.settings.api_key}",
        },
    )
    return lib.Deserializable(response, lib.to_dict)


# === FILE: karrio/providers/[carrier]/utils.py (OAuth token caching) ===

"""OAuth token management in utils.py"""

import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """Carrier connection settings with OAuth support."""
    
    # OAuth credentials
    client_id: str
    client_secret: str
    
    # Optional: Pre-existing tokens
    access_token: str = None
    refresh_token: str = None
    
    @property
    def carrier_name(self):
        return "carrier"
    
    @property
    def server_url(self):
        return (
            "https://api.sandbox.carrier.com"
            if self.test_mode
            else "https://api.carrier.com"
        )
    
    @property
    def oauth_url(self):
        return (
            "https://auth.sandbox.carrier.com"
            if self.test_mode
            else "https://auth.carrier.com"
        )
    
    @property
    def authorization(self):
        """Get valid access token, refreshing if needed."""
        cache_key = f"{self.carrier_name}|{self.client_id}|{self.client_secret}"
        
        def get_token():
            """Fetch new token via client credentials."""
            response = lib.request(
                url=f"{self.oauth_url}/token",
                method="POST",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=lib.to_query_string({
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                }),
                decoder=lib.to_dict,
            )
            
            if "error" in response:
                raise errors.ShippingSDKError(response.get("error_description", "OAuth error"))
            
            expiry = datetime.datetime.now() + datetime.timedelta(
                seconds=float(response.get("expires_in", 3600))
            )
            
            return {
                **response,
                "expiry": lib.fdatetime(expiry),
            }
        
        # Use thread-safe token caching
        token = self.connection_cache.thread_safe(
            refresh_func=get_token,
            cache_key=cache_key,
            buffer_minutes=30,
            token_field="access_token",
        )
        
        return token.get("access_token")


# === Webhook Event Types Reference ===

"""
Common webhook event types to handle:

Shipment Events:
- shipment.created
- shipment.label.created
- shipment.status.updated
- shipment.pickup.scheduled
- shipment.in_transit
- shipment.out_for_delivery
- shipment.delivered
- shipment.cancelled
- shipment.exception

Tracking Events:
- tracking.updated
- tracking.exception
- tracking.delivered

Pickup Events:
- pickup.scheduled
- pickup.completed
- pickup.cancelled

Returns:
- return.initiated
- return.received
- return.processed
"""
