import graphene
from graphene.types import generic
from graphene_django.types import ErrorType

from karrio.core.utils import DP
import karrio.server.graph.utils as utils
import karrio.server.events.models as models
import karrio.server.graph.extension.events.types as types
from karrio.server.events.serializers.webhook import WebhookSerializer


class CreateWebhook(utils.ClientMutation):
    webhook = graphene.Field(types.WebhookType)

    class Input:
        url = graphene.String(required=True)
        description = graphene.String(required=False)
        enabled_events = graphene.List(types.EventStatusEnum, required=True)
        disabled = graphene.Boolean(required=False, default_value=False)
        test_mode = graphene.Boolean(required=True, default_value=False)

    @classmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_webhooks"])
    def mutate_and_get_payload(cls, root, info, **inputs):
        serializer = WebhookSerializer(
            context=info.context,
            data=DP.to_dict(inputs),
        )

        if not serializer.is_valid():
            return cls(errors=ErrorType.from_errors(serializer.errors))

        webhook = serializer.save()

        return cls(errors=None, webhook=webhook)


class UpdateWebhook(utils.ClientMutation):
    webhook = graphene.Field(types.WebhookType)

    class Input:
        id = graphene.String(required=True)
        url = graphene.String(required=False)
        description = graphene.String(required=False)
        enabled_events = graphene.List(types.EventStatusEnum, required=False)
        disabled = graphene.Boolean(required=False)
        test_mode = graphene.Boolean(required=False)

    @classmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_webhooks"])
    def mutate_and_get_payload(cls, root, info, id: str, **inputs):
        webhook = models.Webhook.access_by(info.context).get(id=id)

        serializer = WebhookSerializer(
            webhook,
            context=info.context,
            data=DP.to_dict(inputs),
            partial=True,
        )

        if not serializer.is_valid():
            return cls(errors=ErrorType.from_errors(serializer.errors))

        serializer.save()

        # refetch the shipment to get the updated state with signals processed
        update = models.Webhook.access_by(info.context).get(id=id)

        return cls(errors=None, webhook=update)
