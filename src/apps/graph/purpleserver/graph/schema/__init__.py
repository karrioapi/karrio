import graphene
import graphene_django.filter as django_filter
from graphene_django.debug import DjangoDebug

import purpleserver.core.gateway as gateway
import purpleserver.providers.models as providers
import purpleserver.manager.models as manager
import purpleserver.event.models as event
import purpleserver.graph.models as graph
import purpleserver.graph.schema.mutations as mutations
import purpleserver.graph.schema.types as types


class Query(graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='_debug')

    user = graphene.Field(types.UserType)
    token = graphene.Field(types.TokenType)

    user_connections = graphene.List(types.ConnectionType)
    system_connections = graphene.List(types.SystemConnectionType)

    default_templates = graphene.List(types.TemplateType)
    address_templates = django_filter.DjangoFilterConnectionField(types.AddressTemplateType)
    customs_templates = django_filter.DjangoFilterConnectionField(types.CustomsTemplateType)
    parcel_templates = django_filter.DjangoFilterConnectionField(types.ParcelTemplateType)

    log = graphene.Field(types.LogType, id=graphene.Int(required=True))
    logs = django_filter.DjangoFilterConnectionField(types.LogType)
    shipments = django_filter.DjangoFilterConnectionField(types.ShipmentType)
    trackers = django_filter.DjangoFilterConnectionField(types.TrackerType)
    webhooks = django_filter.DjangoFilterConnectionField(types.WebhookType)

    def resolve_user(self, info):
        return types.User.objects.get(id=info.context.user.id)

    def resolve_token(self, info):
        user = self.resolve_user(info)
        return user.auth_token

    def resolve_user_connections(self, info, **kwargs):
        connections = providers.Carrier.objects.access_with(info.context.user).all()
        return [connection.settings for connection in connections]

    def resolve_system_connections(self, _, **kwargs):
        return gateway.Carriers.list(system_only=True, **kwargs)

    def resolve_default_templates(self, info, **kwargs):
        return graph.Template.objects.access_with(info.context.user).filter(is_default=True)

    def resolve_address_templates(self, info, **kwargs):
        return graph.Template.objects.access_with(info.context.user).filter(address__isnull=False, **kwargs)

    def resolve_customs_templates(self, info, **kwargs):
        return graph.Template.objects.access_with(info.context.user).filter(customs__isnull=False, **kwargs)

    def resolve_parcel_templates(self, info, **kwargs):
        return graph.Template.objects.access_with(info.context.user).filter(parcel__isnull=False, **kwargs)

    def resolve_log(self, info, **kwargs):
        return info.context.user.apirequestlog_set.filter(**kwargs).first()

    def resolve_logs(self, info, **kwargs):
        return info.context.user.apirequestlog_set.filter(**kwargs)

    def resolve_shipments(self, info, **kwargs):
        return manager.Shipment.objects.access_with(info.context.user).filter(**kwargs)

    def resolve_trackers(self, info, **kwargs):
        return manager.Tracking.objects.access_with(info.context.user).filter(**kwargs)

    def resolve_webhooks(self, info, **kwargs):
        return event.Webhook.objects.access_with(info.context.user).filter(**kwargs)


class Mutation(graphene.ObjectType):
    mutate_user = mutations.UserMutation.Field()
    mutate_token = mutations.TokenMutation.Field()

    create_template = mutations.CreateTemplate.Field()
    update_template = mutations.UpdateTemplate.Field()
    delete_template = mutations.create_delete_mutation('DeleteTemplate', graph.Template).Field()

    delete_payment = mutations.create_delete_mutation(
        'DeletePayment', manager.Payment, customs__template__isnull=False).Field()
    discard_commodity = mutations.create_delete_mutation(
        'DiscardCommodity', manager.Commodity, customs__template__isnull=False).Field()

    create_connection = mutations.CreateConnection.Field()
    update_connection = mutations.UpdateConnection.Field()
    delete_connection = mutations.create_delete_mutation('DeleteConnection', providers.Carrier).Field()


schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=False)
