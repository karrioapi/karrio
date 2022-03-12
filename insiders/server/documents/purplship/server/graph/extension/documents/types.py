import graphene
import django_filters
from django.db.models import Q

import purplship.server.graph.utils as utils
import purplship.server.documents.models as models


class TemplateRelatedObject(graphene.Enum):
    shipment = "shipment"
    order = "order"


class DocumentTemplateFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    related_objects = django_filters.CharFilter(
        field_name="related_objects",
        method="related_objects_filter",
    )

    class Meta:
        model = models.DocumentTemplate
        fields: list = []

    def related_objects_filter(self, queryset, name, value):
        return queryset.filter(Q(related_objects__contains=value))


class DocumentTemplateType(utils.BaseObjectType):
    related_objects = graphene.List(TemplateRelatedObject, default_value=[])

    class Meta:
        model = models.DocumentTemplate
        exclude = ("org",)
        interfaces = (utils.CustomNode,)
