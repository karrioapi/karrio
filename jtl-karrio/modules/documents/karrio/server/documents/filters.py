import karrio.server.filters as filters
import karrio.server.documents.models as models


class DocumentTemplateFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    related_object = filters.CharFilter(
        field_name="related_object", lookup_expr="icontains"
    )
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = models.DocumentTemplate
        fields: list = []
