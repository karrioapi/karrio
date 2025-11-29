"""Karrio Teleship webhook event processing implementation."""

import hmac
import typing
import hashlib
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.teleship.error as error
import karrio.providers.teleship.utils as provider_utils
import karrio.providers.teleship.units as provider_units
import karrio.schemas.teleship.tracking_response as tracking_res


def on_webhook_event(
    payload: models.RequestPayload,
    settings: provider_utils.Settings,
) -> typing.Tuple[models.WebhookEventDetails, typing.List[models.Message]]:
    """
    webhook payloads follow a structure:
    {
      "eventName": "label.generated",
      "objectType": "shipment",
      "objectId": "6f384ad7-f8bf-40ce-8bf0-715248738f10",
      "data": {
        // Event-specific data (see examples below)
      }
    }
    """

    if not verify_webhook_signature(payload, settings):
        return None, [
            models.Message(
                code="invalid_signature",
                message=f"Invalid webhook signature for {settings.carrier_name} webhook",
            )
        ]

    messages = error.parse_error_response(payload.body, settings)
    body = lib.to_dict(payload.body) if payload.body else {}
    data = body.get("data") or {}

    # Extract tracking details from webhook event data
    tracking = lib.identity(
        _extract_webhook_tracking(data, settings)
        if body.get("eventName") == "shipment.updated" and data.get("trackingNumber")
        else None
    )
    details = models.WebhookEventDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=data.get("trackingNumber"),
        shipment_identifier=body.get("objectId"),
        tracking=tracking,
        shipment=None,
    )

    return details, messages


def _extract_webhook_tracking(
    data: typing.Any,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    """Extract tracking details from webhook event data.

    Webhook data structure differs from tracking API response - timestamps include
    milliseconds and the data is nested under 'data' in the webhook payload.
    """

    tracking = lib.to_object(tracking_res.TrackingResponseType, data)
    last_event = next(iter(tracking.events or []), None)
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if last_event and last_event.code in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    # Teleship webhook timestamps include milliseconds: "2025-11-27T05:48:00.000Z"
    timestamp_formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking.trackingNumber,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.timestamp, try_formats=timestamp_formats),
                time=lib.flocaltime(event.timestamp, try_formats=timestamp_formats),
                description=event.description,
                code=event.code,
                location=event.location,
            )
            for event in (tracking.events or [])
        ],
        delivered=status == "delivered",
        status=status,
        estimated_delivery=lib.fdate(
            tracking.estimatedDelivery, try_formats=timestamp_formats
        ),
        info=models.TrackingInfo(
            shipment_service=tracking.firstMile.carrier,
            carrier_tracking_link=settings.tracking_url.format(tracking.trackingNumber),
            customer_name=tracking.shipTo.address.city,
            shipment_destination_country=tracking.shipTo.address.country,
            shipment_origin_country=tracking.shipFrom.address.country,
        ),
        meta=dict(
            shipment_id=tracking.shipmentId,
            customer_reference=tracking.customerReference,
            ship_date=tracking.shipDate,
            last_mile_carrier=tracking.lastMile.carrier,
            last_mile_tracking=tracking.lastMile.trackingNumber,
        ),
    )


def verify_webhook_signature(
    payload: models.RequestPayload,
    settings: provider_utils.Settings,
) -> bool:
    """Verify the webhook signature using HMAC-SHA256.

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
    """

    # Get the signature from headers (access dict directly - headers contain hyphens)
    headers = payload.headers or {}
    signature = headers.get("x-teleship-signature")
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
