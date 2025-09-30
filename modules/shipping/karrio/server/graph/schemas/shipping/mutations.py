import uuid
import typing
import strawberry
from strawberry.types import Info

import karrio.server.graph.utils as utils
import karrio.server.shipping.models as models
import karrio.server.serializers as serializers
import karrio.server.graph.schemas.shipping.types as types
import karrio.server.graph.schemas.shipping.inputs as inputs
import karrio.server.shipping.serializers.shipping_method as model_serializers


@strawberry.type
class CreateShippingMethodMutation(utils.BaseMutation):
    shipping_method: typing.Optional[types.ShippingMethodType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    def mutate(
        info: Info,
        **input: inputs.CreateShippingMethodMutationInput,
    ) -> "CreateShippingMethodMutation":
        data = input.copy()
        data.update(slug=f"$.{uuid.uuid4().hex}.shipping_method")

        shipping_method = (
            model_serializers.ShippingMethodModelSerializer.map(
                data=data,
                context=info.context.request,
            )
            .save()
            .instance
        )

        return CreateShippingMethodMutation(
            shipping_method=models.ShippingMethod.objects.get(id=shipping_method.id)
        )  # type:ignore


@strawberry.type
class UpdateShippingMethodMutation(utils.BaseMutation):
    shipping_method: typing.Optional[types.ShippingMethodType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    def mutate(
        info: Info,
        metadata: typing.Optional[utils.JSON] = None,
        **input: inputs.UpdateShippingMethodMutationInput,
    ) -> "UpdateShippingMethodMutation":
        data = input.copy()
        instance = models.ShippingMethod.access_by(info.context.request).get(
            id=data.get("id"),
        )

        if metadata is not None:
            data.update(
                serializers.process_dictionaries_mutations(["metadata"], data, instance)
            )

        shipping_method = (
            model_serializers.ShippingMethodModelSerializer.map(
                data=data,
                partial=True,
                instance=instance,
                context=info.context.request,
            )
            .save()
            .instance
        )

        return UpdateShippingMethodMutation(
            shipping_method=models.ShippingMethod.objects.get(id=shipping_method.id)
        )  # type:ignore
