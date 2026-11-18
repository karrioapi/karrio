"""Karrio Teleship webhook event processing implementation."""

import hmac
import json
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

    # Fail closed: an event is only processed once its sender is authenticated.
    rejection = webhook_signature_error(payload, settings)
    if rejection is not None:
        return None, [rejection]

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


SIGNATURE_HEADER = "x-teleship-signature"


def webhook_signature_error(
    payload: models.RequestPayload,
    settings: provider_utils.Settings,
) -> typing.Optional[models.Message]:
    """Authenticate an inbound event; None when the signature is valid.

    Fails closed, with a distinct message for each reason:
    - webhook_secret_not_configured: the connection has no stored secret
    - webhook_signature_missing: no x-teleship-signature header
    - invalid_signature: the signature matches none of the accepted forms
    """
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
    """Verify the webhook signature (HMAC-SHA256 hex) with the stored secret.

    JavaScript equivalent (Teleship, openapi-public.json "Security & Signature
    Verification"):
        const expectedSignature = crypto
          .createHmac('sha256', secret)
          .update(JSON.stringify(payload))
          .digest('hex');

    Always False without a stored secret or without the signature header.
    """

    return webhook_signature_error(payload, settings) is None


def signed_payloads(payload: models.RequestPayload) -> typing.List[bytes]:
    """The byte strings a valid signature may have been made over.

    1. the raw request body, exactly as received;
    2. its compact re-serialisation in received key order (what
       JSON.stringify(payload) produces), for a sender whose body is not
       byte-identical to its own stringify. Without raw bytes this is the
       parsed body, whose key order is whatever the caller kept. Absent when
       that form cannot be encoded (an escaped lone surrogate).

    The indented, key-sorted form of lib.to_json is never accepted.
    """
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
