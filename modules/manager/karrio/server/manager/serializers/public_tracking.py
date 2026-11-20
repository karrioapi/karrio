"""Capability-link response for the public tracking page.

Keep this independent of the authenticated tracker serializer: new private
fields added there must never become public by inheritance.
"""

from rest_framework import serializers


class PublicEventString(serializers.CharField):
    def to_representation(self, value):
        return value if isinstance(value, str) else None


class PublicTrackingEvent(serializers.Serializer):
    date = PublicEventString(allow_null=True, default=None)
    time = PublicEventString(allow_null=True, default=None)
    location = PublicEventString(allow_null=True, default=None)
    description = PublicEventString(allow_null=True, default=None)


class PublicTrackingStatus(serializers.Serializer):
    carrier_name = serializers.CharField(allow_null=True)
    tracking_number = serializers.CharField()
    status = serializers.CharField()
    delivered = serializers.BooleanField(allow_null=True)
    estimated_delivery = serializers.DateField(allow_null=True)
    events = PublicTrackingEvent(many=True, allow_null=True)
