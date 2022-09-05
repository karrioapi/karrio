import graphene
import graphene_django.filter as django_filter

import karrio.server.graph.utils as utils
import karrio.server.graph.extension.documents.types as types
import karrio.server.graph.extension.documents.mutations as mutations
import karrio.server.documents.models as models


class Query:
    document_template = graphene.Field(
        types.DocumentTemplateType, id=graphene.String(required=True)
    )
    document_templates = django_filter.DjangoFilterConnectionField(
        types.DocumentTemplateType,
        required=True,
        filterset_class=types.DocumentTemplateFilter,
        default_value=[],
    )

    @utils.authentication_required
    def resolve_document_template(self, info, **kwargs):
        return models.DocumentTemplate.access_by(info.context).filter(**kwargs).first()

    @utils.authentication_required
    def resolve_document_templates(self, info, **kwargs):
        return models.DocumentTemplate.access_by(info.context)


class Mutation:
    create_document_template = mutations.CreateDocumentTemplate.Field()
    update_document_template = mutations.UpdateDocumentTemplate.Field()
    delete_document_template = mutations.DeleteDocumentTemplate.Field()
