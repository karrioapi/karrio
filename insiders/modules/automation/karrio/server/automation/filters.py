import typing
import django.db.models as models

import karrio.server.conf as conf
import karrio.server.filters as filters
import karrio.server.automation.models as automation
import karrio.server.automation.serializers as automation_serializers


class WorkflowFilter(filters.FilterSet):
    keyword = filters.CharFilter(
        method="keyword_filter",
        help_text="workflow' keyword and indexes search",
    )

    class Meta:
        model = automation.Workflow
        fields: typing.List[str] = []

    def keyword_filter(self, queryset, name, value):
        if "postgres" in conf.settings.DB_ENGINE:
            from django.contrib.postgres.search import SearchVector

            return queryset.annotate(
                search=SearchVector(
                    "id",
                    "reference",
                )
            ).filter(search=value)

        return queryset.filter(
            models.Q(id__icontains=value)
            | models.Q(recipient__address_line1__icontains=value)
        )


class WorkflowConnectionFilter(filters.FilterSet):
    keyword = filters.CharFilter(
        method="keyword_filter",
        help_text="workflow connection' keyword and indexes search",
    )
    action_type = filters.MultipleChoiceFilter(
        field_name="action_type",
        choices=[(c, c) for c in automation_serializers.ACTION_TYPE],
    )

    class Meta:
        model = automation.WorkflowConnection
        fields: typing.List[str] = []

    def keyword_filter(self, queryset, name, value):
        if "postgres" in conf.settings.DB_ENGINE:
            from django.contrib.postgres.search import SearchVector

            return queryset.annotate(
                search=SearchVector(
                    "id",
                    "name",
                    "slug",
                    "description",
                    "auth_host",
                    "auth_endpoint",
                )
            ).filter(search=value)

        return queryset.filter(
            models.Q(id__icontains=value)
            | models.Q(name__icontains=value)
            | models.Q(slug__icontains=value)
            | models.Q(description__icontains=value)
            | models.Q(auth_host__icontains=value)
            | models.Q(auth_endpoint__icontains=value)
        )


class WorkflowActionFilter(filters.FilterSet):
    keyword = filters.CharFilter(
        method="keyword_filter",
        help_text="workflow action' keyword and indexes search",
    )
    auth_type = filters.MultipleChoiceFilter(
        field_name="auth_type",
        choices=[(c, c) for c in automation_serializers.AUTH_TYPE],
    )

    class Meta:
        model = automation.WorkflowAction
        fields: typing.List[str] = []

    def keyword_filter(self, queryset, name, value):
        if "postgres" in conf.settings.DB_ENGINE:
            from django.contrib.postgres.search import SearchVector

            return queryset.annotate(
                search=SearchVector(
                    "id",
                    "name",
                    "slug",
                    "description",
                    "api_host",
                    "api_endpoint",
                )
            ).filter(search=value)

        return queryset.filter(
            models.Q(id__icontains=value)
            | models.Q(name__icontains=value)
            | models.Q(slug__icontains=value)
            | models.Q(description__icontains=value)
            | models.Q(api_host__icontains=value)
            | models.Q(api_endpoint__icontains=value)
        )


class WorkflowEventFilter(filters.FilterSet):
    keyword = filters.CharFilter(
        method="keyword_filter",
        help_text="workflow event' keyword and indexes search",
    )
    status = filters.MultipleChoiceFilter(
        field_name="status",
        choices=[(c, c) for c in automation_serializers.WORKFLOW_EVENT_STATUS],
    )
    event_type = filters.MultipleChoiceFilter(
        field_name="event_type",
        choices=[(c, c) for c in automation_serializers.WORKFLOW_EVENT_TYPE],
    )
    parameters_key = filters.CharInFilter(
        field_name="parameters",
        method="parameters_key_filter",
        help_text="event parameters keys.",
    )

    class Meta:
        model = automation.WorkflowEvent
        fields: typing.List[str] = []

    def keyword_filter(self, queryset, name, value):
        if "postgres" in conf.settings.DB_ENGINE:
            from django.contrib.postgres.search import SearchVector

            return queryset.annotate(
                search=SearchVector(
                    "id",
                    "workflow__id",
                )
            ).filter(search=value)

        return queryset.filter(
            models.Q(id__icontains=value) | models.Q(workflow__id__icontains=value)
        )

    def parameters_key_filter(self, queryset, name, value):
        print("parameters_key_filter", value)
        return queryset.filter(models.Q(parameters__has_keys=value))


class ShippingRuleFilter(filters.FilterSet):
    keyword = filters.CharFilter(
        method="keyword_filter",
        help_text="shipping rule' keyword and indexes search",
    )

    class Meta:
        model = automation.ShippingRule
        fields: typing.List[str] = []

    def keyword_filter(self, queryset, name, value):
        if "postgres" in conf.settings.DB_ENGINE:
            from django.contrib.postgres.search import SearchVector

            return queryset.annotate(
                search=SearchVector(
                    "id",
                    "name",
                    "slug",
                    "description",
                )
            ).filter(search=value)

        return queryset.filter(
            models.Q(id__icontains=value)
            | models.Q(name__icontains=value)
            | models.Q(slug__icontains=value)
            | models.Q(description__icontains=value)
        )
