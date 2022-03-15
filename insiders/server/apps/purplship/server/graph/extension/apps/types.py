import django_filters
from django.db.models import Q
import graphene
import graphene.types.generic as generic

import karrio.server.graph.utils as utils
import karrio.server.apps.models as models


class AppInstallationFilter(django_filters.FilterSet):
    created_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )
    metadata_key = utils.CharInFilter(
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
        return queryset.filter(Q(metadata__values__contains=value))


class AppInstallationType(utils.BaseObjectType):
    metadata = generic.GenericScalar()
    access_scopes = graphene.List(graphene.String, default_value=[])

    class Meta:
        model = models.AppInstallation
        exclude = ("org",)
        interfaces = (utils.CustomNode,)


class AppFilter(django_filters.FilterSet):
    feature = django_filters.CharFilter(field_name="features", lookup_expr="icontains")
    created_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )
    metadata_key = utils.CharInFilter(
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
        return queryset.filter(Q(metadata__values__contains=value))


class PublicAppType(utils.BaseObjectType):
    features = graphene.List(graphene.String, default_value=[])
    installation = graphene.Field(AppInstallationType)
    metadata = generic.GenericScalar()

    class Meta:
        model = models.App
        exclude = ("installations", "registration", "org")
        interfaces = (utils.CustomNode,)

    def resolve_installation(self, info):
        return self.installations.filter(org=info.context.org).first()


class AppType(utils.BaseObjectType):
    client_id = graphene.String(required=True)
    client_secret = graphene.String(required=True)
    features = graphene.List(graphene.String, default_value=[])
    installation = graphene.Field(AppInstallationType)
    redirect_uris = graphene.String(required=True)
    metadata = generic.GenericScalar()

    class Meta:
        model = models.App
        exclude = ("installations", "registration", "org")
        interfaces = (utils.CustomNode,)
