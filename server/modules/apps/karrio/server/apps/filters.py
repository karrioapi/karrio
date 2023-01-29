import django_filters
from django.db.models import Q

import karrio.server.filters as filters
import karrio.server.apps.models as models


class AppInstallationFilter(filters.FilterSet):
    created_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )
    metadata_key = filters.CharInFilter(
        field_name="metadata",
        method="metadata_key_filter",
    )
    metadata_value = django_filters.CharFilter(
        field_name="metadata",
        method="metadata_value_filter",
    )

    class Meta:
        model = models.App
        fields: list = []

    def metadata_key_filter(self, queryset, name, value):
        return queryset.filter(Q(metadata__has_key=value))

    def metadata_value_filter(self, queryset, name, value):
        return queryset.filter(Q(metadata__values__icontains=value))


class AppFilter(filters.FilterSet):
    feature = django_filters.CharFilter(field_name="features", lookup_expr="icontains")
    created_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )
    metadata_key = filters.CharInFilter(
        field_name="metadata",
        method="metadata_key_filter",
    )
    metadata_value = django_filters.CharFilter(
        field_name="metadata",
        method="metadata_value_filter",
    )

    class Meta:
        model = models.App
        fields: list = []

    def metadata_key_filter(self, queryset, name, value):
        return queryset.filter(Q(metadata__has_key=value))

    def metadata_value_filter(self, queryset, name, value):
        return queryset.filter(Q(metadata__values__icontains=value))
