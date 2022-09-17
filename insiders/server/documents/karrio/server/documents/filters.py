import django_filters
import karrio.server.documents.models as models


class DocumentTemplateFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    related_object = django_filters.CharFilter(
        field_name="related_object", lookup_expr="icontains"
    )
    active = django_filters.BooleanFilter(field_name="active")

    class Meta:
        model = models.DocumentTemplate
        fields: list = []
