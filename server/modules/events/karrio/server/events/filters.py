import typing
import django_filters
from django.db.models import Q

import karrio.server.events.serializers as serializers
import karrio.server.events.models as models


class WebhookFilter(django_filters.FilterSet):
    created_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )
    description = django_filters.CharFilter(
        field_name="description", lookup_expr="icontains"
    )
    events = django_filters.MultipleChoiceFilter(
        field_name="enabled_events",
        method="events_filter",
        choices=[(s, s) for s in serializers.EVENT_TYPES],
    )
    disabled = django_filters.BooleanFilter(field_name="disabled")
    test_mode = django_filters.BooleanFilter(field_name="test_mode")
    url = django_filters.CharFilter(field_name="url", lookup_expr="icontains")

    class Meta:
        model = models.Webhook
        fields: typing.List[str] = []

    def events_filter(self, queryset, name, values):
        return queryset.filter(
            Q(enabled_events__contains=values)
            | Q(enabled_events__contains=["all"])
        )


class EventFilter(django_filters.FilterSet):
    entity_id = django_filters.CharFilter(method="entity_filter", field_name="response")
    date_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    date_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )
    type = django_filters.MultipleChoiceFilter(
        field_name="type",
        method="types_filter",
        choices=[
            (c.value, c.value)
            for c in list(serializers.EventTypes)
            if c != serializers.EventTypes.all
        ],
    )

    class Meta:
        model = models.Event
        fields: typing.List[str] = []

    def entity_filter(self, queryset, name, value):
        try:
            return queryset.filter(data__id=value)
        except:
            return queryset

    def types_filter(self, queryset, name, values):
        return queryset.filter(Q(type__in=values))
