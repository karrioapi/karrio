import karrio.lib as lib
import karrio.server.serializers as serializers
import karrio.server.documents.models as models
import karrio.server.core.validators as validators


class TemplateRelatedObject(lib.StrEnum):
    shipment = "shipment"
    order = "order"
    other = "other"


class DocumentTemplateData(serializers.Serializer):
    name = serializers.CharField(max_length=255, help_text="The template name")
    slug = serializers.CharField(max_length=255, help_text="The template slug")
    template = serializers.CharField(help_text="The template content")
    active = serializers.BooleanField(default=True, help_text="disable template flag.")
    description = serializers.CharField(
        max_length=255, help_text="The template description", required=False
    )
    metadata = serializers.PlainDictField(
        help_text="The template metadata", required=False
    )
    options = serializers.PlainDictField(
        help_text="The template rendering options", required=False
    )
    related_object = serializers.ChoiceField(
        choices=TemplateRelatedObject,
        help_text="The template related object",
        required=False,
        default=TemplateRelatedObject.other,
    )


class DocumentTemplate(serializers.EntitySerializer, DocumentTemplateData):
    object_type = serializers.CharField(
        default="document-template", help_text="Specifies the object type"
    )
    preview_url = serializers.URLField(
        help_text="The template preview URL",
        required=False,
    )


class DocumentData(serializers.Serializer):
    template_id = serializers.CharField(
        help_text="The template name. **Required if template is not provided.**",
        required=False,
    )
    template = serializers.CharField(
        help_text="The template content. **Required if template_id is not provided.**",
        required=False,
    )
    doc_format = serializers.CharField(
        help_text="The format of the document",
        required=False,
    )
    doc_name = serializers.CharField(
        help_text="The file name",
        required=False,
    )
    data = serializers.PlainDictField(
        help_text="The template data",
        required=False,
        default={},
    )
    options = serializers.PlainDictField(
        help_text="The template rendering options",
        required=False,
    )


class GeneratedDocument(serializers.Serializer):
    template_id = serializers.CharField(
        help_text="The template name",
        required=False,
    )
    doc_format = serializers.CharField(
        help_text="The format of the document",
        required=False,
    )
    doc_name = serializers.CharField(
        help_text="The file name",
        required=False,
    )
    doc_file = serializers.CharField(
        help_text="A base64 file content",
        required=True,
    )
