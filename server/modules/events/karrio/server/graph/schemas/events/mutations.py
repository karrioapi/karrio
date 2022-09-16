import typing
import strawberry
from strawberry.types import Info

import karrio.lib as lib
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
            context=info.context,
            data=lib.to_dict(inputs),
        )

        if not serializer.is_valid():
            return CreateWebhookMutation(errors=utils.ErrorType.from_errors(serializer.errors))

        webhook = serializer.save()

        return CreateWebhookMutation(errors=None, webhook=webhook)  # type:ignore


@strawberry.type
class UpdateWebhookMutation(utils.BaseMutation):
    webhook: typing.Optional[types.WebhookType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_webhooks"])
    def mutate(
        info: Info, **input: inputs.UpdateWebhookMutationInput
    ) -> "UpdateWebhookMutation":
        webhook = models.Webhook.access_by(info.context).get(id=input.get("id"))

        serializer = serializers.WebhookSerializer(
            webhook,
            context=info.context,
            data=lib.to_dict(inputs),
            partial=True,
        )

        if not serializer.is_valid():
            return UpdateWebhookMutation(errors=utils.ErrorType.from_errors(serializer.errors))

        serializer.save()

        # refetch the shipment to get the updated state with signals processed
        update = models.Webhook.access_by(info.context).get(id=id)

        return UpdateWebhookMutation(errors=None, webhook=update)  # type:ignore
