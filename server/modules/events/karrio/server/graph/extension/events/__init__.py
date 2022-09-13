import graphene
import graphene_django.filter as django_filter

import karrio.server.graph.utils as utils
import karrio.server.graph.extension.events.mutations as mutations
import karrio.server.graph.extension.events.types as types
import karrio.server.events.models as models


class Query:
    webhook = graphene.Field(types.WebhookType, id=graphene.String(required=True))
    webhooks = django_filter.DjangoFilterConnectionField(
        types.WebhookType,
        required=True,
        default_value=[],
        filterset_class=types.WebhookFilter,
    )

    event = graphene.Field(types.EventType, id=graphene.String(required=True))
    events = django_filter.DjangoFilterConnectionField(
        types.EventType,
        required=True,
        default_value=[],
        filterset_class=types.EventFilter,
    )

    @utils.authentication_required
    @utils.authorization_required()
    def resolve_webhook(self, info, id: str, **kwargs):
        return models.Webhook.access_by(info.context).filter(id=id).first()

    @utils.authentication_required
    @utils.authorization_required()
    def resolve_webhooks(self, info, **kwargs):
        return models.Webhook.access_by(info.context)

    @utils.authentication_required
    @utils.authorization_required()
    def resolve_event(self, info, id: str, **kwargs):
        return models.Event.access_by(info.context).filter(id=id).first()

    @utils.authentication_required
    @utils.authorization_required()
    def resolve_events(self, info, **kwargs):
        return models.Event.access_by(info.context)


class Mutation:
    create_webhook = mutations.CreateWebhook.Field()
    update_webhook = mutations.UpdateWebhook.Field()
    delete_webhook = utils.create_delete_mutation(
        "DeleteWebhook", models.Webhook
    ).Field()
