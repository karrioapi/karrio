import base64
import logging
import django.urls as urls
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
import rest_framework.pagination as pagination

import karrio.lib as lib
import karrio.server.openapi as openapi
import karrio.server.core.views.api as api
import karrio.server.documents.models as models
import karrio.server.documents.generator as generator
import karrio.server.documents.serializers as serializers

ENDPOINT_ID = "&&&&$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
logger = logging.getLogger(__name__)
DocumentTemplates = serializers.PaginatedResult(
    "DocumentTemplateList", serializers.DocumentTemplate
)


class DocumentTemplateList(api.GenericAPIView):
    queryset = models.DocumentTemplate.objects
    pagination_class = type(
        "CustomPagination",
        (pagination.LimitOffsetPagination,),
        dict(default_limit=20),
    )
    serializer_class = DocumentTemplates

    @openapi.extend_schema(
        tags=["Documents"],
        operation_id=f"{ENDPOINT_ID}list",
        extensions={"x-operationId": "listDocumentTemplates"},
        summary="List all templates",
        responses={
            200: DocumentTemplates(),
            404: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
    )
    def get(self, request: Request):
        """
        Retrieve all templates.
        """
        templates = models.DocumentTemplate.access_by(request)
        response = self.paginate_queryset(
            serializers.DocumentTemplate(templates, many=True).data
        )
        return self.get_paginated_response(response)

    @openapi.extend_schema(
        tags=["Documents"],
        operation_id=f"{ENDPOINT_ID}create",
        extensions={"x-operationId": "createDocumentTemplate"},
        summary="Create a template",
        request=serializers.DocumentTemplateData(),
        responses={
            201: serializers.DocumentTemplate(),
            400: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
    )
    def post(self, request: Request):
        """
        Create a new template.
        """
        template = (
            serializers.DocumentTemplateModelSerializer.map(
                data=request.data, context=request
            )
            .save()
            .instance
        )

        return Response(
            serializers.DocumentTemplate(template).data,
            status=status.HTTP_201_CREATED,
        )


class DocumentTemplateDetail(api.APIView):

    @openapi.extend_schema(
        tags=["Documents"],
        operation_id=f"{ENDPOINT_ID}retrieve",
        extensions={"x-operationId": "retrieveDocumentTemplate"},
        summary="Retrieve a template",
        responses={
            200: serializers.DocumentTemplate(),
            400: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve a template.
        """
        template = models.DocumentTemplate.access_by(request).get(pk=pk)
        return Response(serializers.DocumentTemplate(template).data)

    @openapi.extend_schema(
        tags=["Documents"],
        operation_id=f"{ENDPOINT_ID}update",
        extensions={"x-operationId": "updateDocumentTemplate"},
        summary="Update a template",
        request=serializers.DocumentTemplateData(),
        responses={
            200: serializers.DocumentTemplate(),
            400: serializers.ErrorResponse(),
            404: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
    )
    def patch(self, request: Request, pk: str):
        """
        update a template.
        """
        template = models.DocumentTemplate.access_by(request).get(pk=pk)

        serializers.DocumentTemplateModelSerializer.map(
            template,
            data=request.data,
        ).save()

        return Response(serializers.DocumentTemplate(template).data)

    @openapi.extend_schema(
        tags=["Documents"],
        operation_id=f"{ENDPOINT_ID}discard",
        extensions={"x-operationId": "discardDocumentTemplate"},
        summary="Delete a template",
        responses={
            200: serializers.DocumentTemplate(),
            404: serializers.ErrorResponse(),
            409: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
    )
    def delete(self, request: Request, pk: str):
        """
        Delete a template.
        """
        template = models.DocumentTemplate.access_by(request).get(pk=pk)

        template.delete(keep_parents=True)

        return Response(serializers.DocumentTemplate(template).data)


class DocumentGenerator(api.APIView):
    @openapi.extend_schema(
        tags=["Documents"],
        operation_id=f"{ENDPOINT_ID}generateDocument",
        summary="Generate a document",
        request=serializers.DocumentData(),
        responses={
            201: serializers.GeneratedDocument(),
            400: serializers.ErrorResponse(),
            404: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
    )
    def post(self, request: Request):
        """Generate any document.
        This API is designed to be used to generate GS1 labels,
        invoices and any document that requires external data.
        """
        try:
            data = serializers.DocumentData.map(data=request.data).data

            if data.get("template") is None and data.get("template_id") is None:
                return Response(
                    {"errors": [{"message": "template or template_id is required"}]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            document_template = lib.identity(
                None
                if data.get("template_id") is None
                else models.DocumentTemplate.objects.get(pk=data.get("template_id"))
            )

            try:
                doc_file = generator.Documents.generate(
                    getattr(document_template, "template", data.get("template")),
                    related_object=getattr(document_template, "related_object", None),
                    metadata=getattr(document_template, "metadata", {}),
                    data=data.get("data", {}),
                    options=data.get("options", {}),
                    doc_name=data.get("doc_name"),
                    doc_format=data.get("doc_format"),
                )

                document = serializers.GeneratedDocument.map(
                    data={
                        **data,
                        "doc_file": base64.b64encode(doc_file.getvalue()).decode("utf-8"),
                    }
                )

                return Response(document.data, status=status.HTTP_201_CREATED)

            except generator.TemplateRenderingError as e:
                error_message = e.message
                if e.line_number:
                    error_message += f" (line {e.line_number})"

                return Response(
                    {"errors": [{"message": error_message}]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except models.DocumentTemplate.DoesNotExist:
                return Response(
                    {"errors": [{"message": f"Document template with id '{data.get('template_id')}' not found"}]},
                    status=status.HTTP_404_NOT_FOUND,
                )
            except Exception as e:
                logger.exception(f"Unexpected error during document generation: {e}")
                return Response(
                    {"errors": [{"message": f"Document generation failed: {str(e)}"}]},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        except serializers.ValidationError as e:
            logger.error(f"Validation error: {e}")
            return Response(
                {"errors": [{"message": "Invalid input data"}]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.exception(f"Unexpected error in document generator: {e}")
            return Response(
                {"errors": [{"message": "Internal server error"}]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


urlpatterns = [
    urls.path(
        "documents/templates",
        DocumentTemplateList.as_view(),
        name="document-template-list",
    ),
    urls.path(
        "documents/templates/<str:pk>",
        DocumentTemplateDetail.as_view(),
        name="document-template-details",
    ),
    urls.path(
        "documents/generate",
        DocumentGenerator.as_view(),
        name="document-generator",
    ),
]
