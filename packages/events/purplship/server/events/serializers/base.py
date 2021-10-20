from enum import Enum
from purplship.server import serializers

from purplship.server.core.serializers import EntitySerializer


class EventTypes(Enum):
    all = 'all'
    shipment_purchased = 'shipment.purchased'
    shipment_cancelled = 'shipment.cancelled'
    shipment_fulfilled = 'shipment.fulfilled'
    tracker_created = 'tracker.created'
    tracker_updated = 'tracker.updated'


EVENT_TYPES = [(c.value, c.value) for c in list(EventTypes)]


class WebhookData(serializers.Serializer):
    url = serializers.URLField(
        required=True, help_text="The URL of the webhook endpoint.")
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True,
        help_text="An optional description of what the webhook is used for.")
    enabled_events = serializers.ListField(
        required=True,
        child=serializers.ChoiceField(choices=EVENT_TYPES),
        help_text="The list of events to enable for this endpoint.")
    test_mode = serializers.BooleanField(
        required=True,
        help_text="Specified whether it was created with a carrier in test mode")
    disabled = serializers.BooleanField(
        required=False, allow_null=True,
        help_text="Indicates that the webhook is disabled")


class Webhook(WebhookData, EntitySerializer):
    last_event_at = serializers.DateTimeField(
        required=False, allow_null=True,
        help_text="The datetime of the last event sent.")
