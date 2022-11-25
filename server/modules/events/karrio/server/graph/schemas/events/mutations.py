import typing
import strawberry
from strawberry.types import Info

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.events.types as types
import karrio.server.graph.schemas.events.inputs as inputs
import karrio.server.events.serializers.webhook as serializers
import karrio.server.events.models as models


@strawberry.type
class CreateWebhookMutation(utils.BaseMutation):
    webhook: typing.Optional[types.WebhookType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_webhooks"])
    def mutate(
        info: Info, **input: inputs.CreateWebhookMutationInput
    ) -> "CreateWebhookMutation":
        serializer = serializers.WebhookSerializer(
            data=input,
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)

        return CreateWebhookMutation(webhook=serializer.save())  # type:ignore


@strawberry.type
class UpdateWebhookMutation(utils.BaseMutation):
    webhook: typing.Optional[types.WebhookType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_webhooks"])
    def mutate(
        info: Info, **input: inputs.UpdateWebhookMutationInput
    ) -> "UpdateWebhookMutation":
        id = input.get("id")
        webhook = models.Webhook.access_by(info.context.request).get(id=id)

        serializer = serializers.WebhookSerializer(
            webhook,
            data=input,
            partial=True,
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # refetch the shipment to get the updated state with signals processed
        update = models.Webhook.access_by(info.context.request).get(id=id)

        return UpdateWebhookMutation(webhook=update)  # type:ignore
