import karrio.server.filters as filters
import karrio.server.data.models as models
import karrio.server.data.serializers as serializers


class DataTemplateFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    slug = filters.CharFilter(field_name="slug", lookup_expr="icontains")
    resource_type = filters.MultipleChoiceFilter(
        field_name="resource_type",
        choices=[(c.value, c.value) for c in list(serializers.ResourceType)],
        help_text=f"""
        the data template resource type
        Values: {', '.join([f"`{s.name}`" for s in list(serializers.ResourceType)])}
        """,
    )

    class Meta:
        model = models.DataTemplate
        fields: list = []


class BatchOperationFilter(filters.FilterSet):
    resource_type = filters.MultipleChoiceFilter(
        field_name="resource_type",
        choices=[(c.value, c.value) for c in list(serializers.ResourceType)],
        help_text=f"""
        the batch resource type
        Values: {', '.join([f"`{s.name}`" for s in list(serializers.ResourceType)])}
        """,
    )
    status = filters.MultipleChoiceFilter(
        field_name="status",
        choices=[(c.value, c.value) for c in list(serializers.BatchOperationStatus)],
        help_text=f"""
        the batch operation status
        Values: {', '.join([f"`{s.name}`" for s in list(serializers.BatchOperationStatus)])}
        """,
    )

    class Meta:
        model = models.BatchOperation
        fields: list = []
