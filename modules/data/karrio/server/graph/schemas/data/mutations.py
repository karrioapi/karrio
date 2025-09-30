import typing
import strawberry
from strawberry.types import Info

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.data.types as types
import karrio.server.graph.schemas.data.inputs as inputs
import karrio.server.data.serializers as serializers
import karrio.server.data.models as models


@strawberry.type
class CreateDataTemplateMutation(utils.BaseMutation):
    template: typing.Optional[types.DataTemplateType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["DATA_IMPORT_EXPORT"])
    def mutate(
        info: Info, **input: inputs.CreateDataTemplateMutationInput
    ) -> "CreateDataTemplateMutation":
        serializer = serializers.DataTemplateModelSerializer(
            data=input,
            context=info.context,
        )
        serializer.is_valid(raise_exception=True)

        return CreateDataTemplateMutation(template=serializer.save())  # type:ignore


@strawberry.type
class UpdateDataTemplateMutation(utils.BaseMutation):
    template: typing.Optional[types.DataTemplateType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["DATA_IMPORT_EXPORT"])
    def mutate(
        info: Info, **input: inputs.UpdateDataTemplateMutationInput
    ) -> "UpdateDataTemplateMutation":
        instance = models.DataTemplate.access_by(info.context.request).get(id=input["id"])

        serializer = serializers.DataTemplateModelSerializer(
            instance,
            data=serializers.process_dictionaries_mutations(
                ["fields_mapping"], input, instance
            ),
            partial=True,
            context=info.context,
        )
        serializer.is_valid(raise_exception=True)

        return UpdateDataTemplateMutation(template=serializer.save())  # type:ignore
