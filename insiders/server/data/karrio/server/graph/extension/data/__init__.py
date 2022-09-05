import graphene
import graphene_django.filter as django_filter

import karrio.server.graph.utils as utils
import karrio.server.data.models as models
import karrio.server.data.filters as filters
import karrio.server.graph.extension.data.types as types
import karrio.server.graph.extension.data.mutations as mutations


class Query:
    data_template = graphene.Field(
        types.DataTemplateType, id=graphene.String(required=True)
    )
    data_templates = django_filter.DjangoFilterConnectionField(
        types.DataTemplateType,
        required=True,
        filterset_class=filters.DataTemplateFilter,
        default_value=[],
    )
    batch_operations = django_filter.DjangoFilterConnectionField(
        types.BatchOperationType,
        required=True,
        filterset_class=filters.BatchOperationFilter,
        default_value=[],
    )

    @utils.authentication_required
    def resolve_data_template(self, info, **kwargs):
        return models.DataTemplate.access_by(info.context).filter(**kwargs).first()

    @utils.authentication_required
    def resolve_data_templates(self, info, **kwargs):
        return models.DataTemplate.access_by(info.context)

    @utils.authentication_required
    def resolve_batch_operations(self, info, **kwargs):
        return models.BatchOperation.access_by(info.context)


class Mutation:
    create_data_template = mutations.CreateDataTemplate.Field()
    update_data_template = mutations.UpdateDataTemplate.Field()
    delete_data_template = mutations.DeleteDataTemplate.Field()
