import strawberry
from strawberry.types import Info

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.base as base
import karrio.server.graph.schemas.events.mutations as mutations
import karrio.server.graph.schemas.events.inputs as inputs
import karrio.server.graph.schemas.events.types as types
import karrio.server.events.models as models

extra_types: list = []


@strawberry.type
class Query:
    webhook: types.WebhookType = strawberry.field(resolver=types.WebhookType.resolve)
    webhooks: utils.Connection[types.WebhookType] = strawberry.field(
        resolver=types.WebhookType.resolve_list
    )

    event: types.EventType = strawberry.field(resolver=types.EventType.resolve)
    events: utils.Connection[types.EventType] = strawberry.field(
        resolver=types.EventType.resolve_list
    )


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_webhook(
        self, info: Info, input: inputs.CreateWebhookMutationInput
    ) -> mutations.CreateWebhookMutation:
        return mutations.CreateWebhookMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_webhook(
        self, info: Info, input: inputs.UpdateWebhookMutationInput
    ) -> mutations.UpdateWebhookMutation:
        return mutations.UpdateWebhookMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_webhook(
        self, info: Info, input: base.inputs.DeleteMutationInput
    ) -> base.mutations.DeleteMutation:
        return base.mutations.DeleteMutation.mutate(
            info, model=models.Webhook, **input.to_dict()
        )
