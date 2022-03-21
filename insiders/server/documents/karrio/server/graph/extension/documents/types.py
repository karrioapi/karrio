import graphene
import django_filters
from django.db.models import Q

import karrio.server.graph.utils as utils
import karrio.server.documents.models as models


class TemplateRelatedObject(graphene.Enum):
    shipment = "shipment"
    order = "order"


class DocumentTemplateFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    related_object = django_filters.CharFilter(
        field_name="related_object", lookup_expr="icontains"
    )

    class Meta:
        model = models.DocumentTemplate
        fields: list = []


class DocumentTemplateType(utils.BaseObjectType):
    related_object = TemplateRelatedObject()

    class Meta:
        model = models.DocumentTemplate
        exclude = ("org",)
        interfaces = (utils.CustomNode,)
