import typing

import karrio.server.filters as filters
import karrio.server.orgs.models as models


class OrgFilters(filters.FilterSet):
    name = filters.CharFilter(field_name="path", lookup_expr="icontains")
    created_after = filters.DateTimeFilter(field_name="created", lookup_expr="gte")
    created_before = filters.DateTimeFilter(field_name="created", lookup_expr="lte")
    is_active = filters.BooleanFilter(
        help_text="This flag is used to filter out active/inactive organizations.",
    )

    class Meta:
        model = models.Organization
        fields: typing.List[str] = []
