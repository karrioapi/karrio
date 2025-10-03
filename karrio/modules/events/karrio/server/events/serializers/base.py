import karrio.lib as lib
import karrio.server.serializers as serializers


class EventTypes(lib.StrEnum):
    all = "all"
    shipment_purchased = "shipment_purchased"
    shipment_cancelled = "shipment_cancelled"
    shipment_fulfilled = "shipment_fulfilled"
    shipment_out_for_delivery = "shipment_out_for_delivery"
    shipment_needs_attention = "shipment_needs_attention"
    shipment_delivery_failed = "shipment_delivery_failed"
    tracker_created = "tracker_created"
    tracker_updated = "tracker_updated"
    order_created = "order_created"
    order_updated = "order_updated"
    order_fulfilled = "order_fulfilled"
    order_cancelled = "order_cancelled"
    order_delivered = "order_delivered"
    batch_queued = "batch_queued"
    batch_failed = "batch_failed"
    batch_running = "batch_running"
    batch_completed = "batch_completed"


EVENT_TYPES = [(c.value, c.value) for c in list(EventTypes)]


class WebhookData(serializers.Serializer):
    url = serializers.URLField(
        required=True, help_text="The URL of the webhook endpoint."
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="An optional description of what the webhook is used for.",
    )
    enabled_events = serializers.ListField(
        required=True,
        child=serializers.ChoiceField(choices=EVENT_TYPES),
        help_text="The list of events to enable for this endpoint.",
    )
    disabled = serializers.BooleanField(
        required=False,
        allow_null=True,
        help_text="Indicates that the webhook is disabled",
    )


class Webhook(serializers.EntitySerializer, WebhookData):
    object_type = serializers.CharField(
        default="webhook", help_text="Specifies the object type"
    )
    last_event_at = serializers.DateTimeField(
        required=False,
        allow_null=True,
        help_text="The datetime of the last event sent.",
    )
    secret = serializers.CharField(help_text="Header signature secret")
    test_mode = serializers.BooleanField(
        help_text="Specified whether it was created with a carrier in test mode",
    )
