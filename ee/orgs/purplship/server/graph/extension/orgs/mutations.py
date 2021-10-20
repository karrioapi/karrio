from graphene_django.rest_framework import mutation

from purplship.server.serializers import make_fields_optional
import purplship.server.orgs.serializers as serializers


class SerializerMutation(mutation.SerializerMutation):
    class Meta:
        abstract = True

    @classmethod
    def get_serializer_kwargs(cls, root, info, **input):
        data = input.copy()

        if 'id' in input:
            org = cls._meta.model_class.objects.get(id=data.pop('id'))

            return {'instance': org, 'data': data, 'partial': True, 'context': info.context}

        return {'data': data, 'partial': False, 'context': info.context}


class CreateOrganization(SerializerMutation):

    class Meta:
        model_operations = ("create",)
        convert_choices_to_enum = False
        serializer_class = serializers.OrganizationModelSerializer


class UpdateOrganization(SerializerMutation):

    class Meta:
        model_operations = ("update",)
        convert_choices_to_enum = False
        serializer_class = make_fields_optional(serializers.OrganizationModelSerializer)
