import typing
from django.db.models import Q

import karrio.server.filters as filters
import karrio.server.tenants.models as models


class TenantFilter(filters.FilterSet):
    schema_name = filters.CharFilter(
        field_name="schema_name",
    )
    app_domain = filters.CharFilter(
        field_name="app_domains",
        method="app_domains_filter",
        help_text="app domains.",
    )
    api_domain = filters.CharFilter(
        field_name="domains",
        method="api_domains_filter",
        help_text="API domains.",
    )

    class Meta:
        model = models.Client
        fields: typing.List[str] = []

    def app_domains_filter(self, queryset, name, value):
        return queryset.filter(Q(app_domains__contains=value))

    def api_domains_filter(self, queryset, name, value):
        return queryset.filter(Q(domains__domain__contains=value))
