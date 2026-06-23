"""Inbound carrier webhook processing.

Generic, carrier-agnostic: connectors supply the parsing + ack via their
`Hooks.on_webhook_event`; this module resolves the carrier/tracker, applies the
update, and renders the response.

A single entry point — `process(request, identifier)` — backs one URL
(`/connections/webhook/<identifier>/events`). The `identifier` is resolved as a
connection pk first (per-connection registration, e.g. teleship); failing that
it is treated as a carrier name (one static URL per integration, e.g. DPD's
push), parsed with a stub gateway and the tracker resolved from the tracking
number.

`process` returns `(body, status, content_type)`; `render_response` turns that
into an HTTP response (a verbatim connector ack body, e.g. DPD's `<push>` XML,
or the default JSON envelope).
"""

import hmac

import django.http as http
import karrio.lib as lib
import karrio.server.providers.models as providers
import rest_framework.response as response
from django.conf import settings
from karrio.server.core.logging import logger
from rest_framework import status as http_status

_CONTENT_TYPES = dict(xml="application/xml", json="application/json", text="text/plain")


def process(request, identifier: str) -> tuple:
    """Resolve `identifier` as a connection pk first, otherwise a carrier name."""
    import karrio.server.core.gateway as gateway

    connection = providers.CarrierConnection.objects.filter(pk=identifier).first()
    if connection is not None:
        event, messages = gateway.Hooks.on_webhook_event(payload=_payload(request), carrier=connection)
        _apply_tracking(event, tracker_filter=dict(carrier__connection_id=str(connection.id)))
        return _result(event, messages, connection.carrier_name, connection.carrier_id)

    return _process_carrier(request, identifier)


def _process_carrier(request, carrier_name: str) -> tuple:
    import karrio.core.errors as sdk_errors
    import karrio.server.core.gateway as gateway

    if not _authorized(request, carrier_name):
        return _error("Unauthorized", http_status.HTTP_403_FORBIDDEN)

    try:
        stub_gateway = gateway.Hooks.create_stub_gateway(carrier_name)
    except sdk_errors.ShippingSDKError:
        return _error(f"Unknown webhook target: {carrier_name}", http_status.HTTP_404_NOT_FOUND)

    event, messages = gateway.Hooks.on_webhook_event(payload=_payload(request), gateway=stub_gateway)
    _apply_tracking(event, tracker_filter=dict(carrier__carrier_name=carrier_name))
    return _result(event, messages, carrier_name, carrier_name)


def render_response(result: tuple):
    """Verbatim connector ack body with its Content-Type when set, else JSON."""
    body, status_code, content_type = result
    if content_type is not None and not isinstance(body, dict):
        return http.HttpResponse(body, status=status_code, content_type=content_type)
    return response.Response(body, status=status_code)


def _payload(request) -> dict:
    return dict(
        url=request.build_absolute_uri(),
        body=request.data,
        query=dict(request.query_params),
        headers=dict(request.headers),
    )


def _authorized(request, carrier_name: str) -> bool:
    # Defense-in-depth for a public, carrier-unauthenticated endpoint. The
    # authoritative network control is the ingress allow-list (see SPECS); here
    # an optional shared-secret token and source-IP allowlist, both off by
    # default but required once set.
    token = (getattr(settings, "WEBHOOK_CARRIER_TOKENS", None) or {}).get(carrier_name)
    allowlist = (getattr(settings, "WEBHOOK_CARRIER_IP_ALLOWLIST", None) or {}).get(carrier_name)

    if token:
        presented = request.query_params.get("token") or request.headers.get("X-Webhook-Token") or ""
        if not hmac.compare_digest(presented, token):
            return False

    if allowlist and _client_ip(request) not in allowlist:
        return False

    if not token and not allowlist:
        logger.warning("Carrier webhook endpoint has no token or IP allowlist configured", carrier_name=carrier_name)

    return True


def _client_ip(request) -> str:
    # Never trust the left-most (client-supplied) X-Forwarded-For value. With
    # WEBHOOK_TRUSTED_PROXY_COUNT proxy hops in front, take that entry from the
    # right (the address the trusted proxy saw); otherwise the real TCP peer.
    proxies = getattr(settings, "WEBHOOK_TRUSTED_PROXY_COUNT", 0) or 0
    if proxies > 0:
        chain = [ip.strip() for ip in request.META.get("HTTP_X_FORWARDED_FOR", "").split(",") if ip.strip()]
        if len(chain) >= proxies:
            return chain[-proxies]
    return (request.META.get("REMOTE_ADDR") or "").strip()


def _apply_tracking(event, *, tracker_filter: dict) -> None:
    if not (event and event.tracking):
        return

    import karrio.server.manager.models as manager_models
    import karrio.server.manager.serializers.tracking as tracking_serializers

    tracking_number = event.tracking_number or event.tracking.tracking_number
    if not tracking_number:
        return

    # tracking_number is not unique → no-op on an ambiguous match.
    matches = list(manager_models.Tracking.objects.filter(tracking_number=tracking_number, **tracker_filter)[:2])
    if len(matches) == 1:
        tracking_serializers.update_tracker(matches[0], lib.to_dict(event.tracking))
    elif len(matches) > 1:
        logger.warning(
            "Ambiguous webhook tracker match; skipping update",
            tracking_number=tracking_number,
            tracker_filter=tracker_filter,
        )


def _result(event, messages, carrier_name, carrier_id) -> tuple:
    # Verbatim connector ack body (e.g. DPD XML) over the default JSON.
    if event is not None and getattr(event, "response", None):
        return (
            event.response,
            http_status.HTTP_200_OK,
            _CONTENT_TYPES.get(event.response_format or "text", "text/plain"),
        )

    return (
        dict(
            operation="Webhook event",
            success=len(messages) == 0,
            carrier_name=carrier_name,
            carrier_id=carrier_id,
            messages=lib.to_dict(messages),
        ),
        http_status.HTTP_200_OK,
        None,
    )


def _error(message: str, status_code: int) -> tuple:
    return (dict(operation="Webhook event", success=False, messages=[{"message": message}]), status_code, None)
