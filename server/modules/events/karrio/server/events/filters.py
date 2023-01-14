import typing
from django.db.models import Q

import karrio.server.events.serializers as serializers
import karrio.server.events.models as models
import karrio.server.filters as filters


class WebhookFilter(filters.FilterSet):
    created_after = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    description = filters.CharFilter(field_name="description", lookup_expr="icontains")
    events = filters.MultipleChoiceFilter(
        field_name="enabled_events",
        method="events_filter",
        choices=[(s, s) for s in serializers.EVENT_TYPES],
    )
    disabled = filters.BooleanFilter(field_name="disabled")
    test_mode = filters.BooleanFilter(field_name="test_mode")
    url = filters.CharFilter(field_name="url", lookup_expr="icontains")

    class Meta:
        model = models.Webhook
        fields: typing.List[str] = []

    def events_filter(self, queryset, name, values):
        if any(values):
            query = Q(enabled_events__icontains=values[0])

            for value in values[1:]:
                query &= Q(enabled_events__icontains=value)

            return queryset.filter(query | Q(enabled_events__icontains="all"))

        return queryset.filter(enabled_events__icontains="all")


class EventFilter(filters.FilterSet):
    entity_id = filters.CharFilter(method="entity_filter", field_name="response")
    date_after = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    date_before = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    type = filters.MultipleChoiceFilter(
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
