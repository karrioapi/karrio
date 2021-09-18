import graphene
import graphene_django.filter as django_filter

from purpleserver.user.serializers import TokenSerializer

import purpleserver.core.views.api as api
import purpleserver.core.gateway as gateway
import purpleserver.providers.models as providers
import purpleserver.manager.models as manager
import purpleserver.events.models as events
import purpleserver.graph.serializers as serializers
import purpleserver.graph.models as graph
import purpleserver.graph.extension.base.mutations as mutations
import purpleserver.graph.extension.base.types as types


class Query:
    user = graphene.Field(types.UserType)
    token = graphene.Field(types.TokenType, org_id=graphene.String(required=False))

    user_connections = graphene.List(types.ConnectionType, test=graphene.Boolean(required=False))
    system_connections = graphene.List(types.SystemConnectionType, test=graphene.Boolean(required=False))

    default_templates = types.generic.GenericScalar()
    address_templates = django_filter.DjangoFilterConnectionField(types.AddressTemplateType)
    customs_templates = django_filter.DjangoFilterConnectionField(types.CustomsTemplateType)
    parcel_templates = django_filter.DjangoFilterConnectionField(types.ParcelTemplateType)

    log = graphene.Field(types.LogType, id=graphene.Int(required=True))
    logs = django_filter.DjangoFilterConnectionField(types.LogType, filterset_class=types.LogFilter)
    shipments = django_filter.DjangoFilterConnectionField(types.ShipmentType)
    trackers = django_filter.DjangoFilterConnectionField(types.TrackerType)
    webhooks = django_filter.DjangoFilterConnectionField(types.WebhookType)

    @types.login_required
    def resolve_user(self, info):
        return types.User.objects.get(id=info.context.user.id)

    @types.login_required
    def resolve_token(self, info, **kwargs):
        return TokenSerializer.retrieve_token(info.context, **kwargs)

    @types.login_required
    def resolve_user_connections(self, info, **kwargs):
        connections = providers.Carrier.access_by(info.context).filter(created_by__isnull=False, **kwargs)
        return [connection.settings for connection in connections]

    @types.login_required
    def resolve_system_connections(self, info, **kwargs):
        return gateway.Carriers.list(context=info.context, system_only=True, **kwargs)

    @types.login_required
    def resolve_default_templates(self, info, **kwargs):
        templates = graph.Template.access_by(info.context).filter(is_default=True)
        return [serializers.DefaultTemplateSerializer(template).data for template in templates]

    @types.login_required
    def resolve_address_templates(self, info, **kwargs):
        return graph.Template.access_by(info.context).filter(address__isnull=False)

    @types.login_required
    def resolve_customs_templates(self, info, **kwargs):
        return graph.Template.access_by(info.context).filter(customs__isnull=False)

    @types.login_required
    def resolve_parcel_templates(self, info, **kwargs):
        return graph.Template.access_by(info.context).filter(parcel__isnull=False)

    @types.login_required
    def resolve_log(self, info, **kwargs):
        return api.APILog.access_by(info.context).filter(**kwargs).first()

    @types.login_required
    def resolve_logs(self, info, **kwargs):
        return api.APILog.access_by(info.context)

    @types.login_required
    def resolve_shipments(self, info, **kwargs):
        return manager.Shipment.access_by(info.context)

    @types.login_required
    def resolve_trackers(self, info, **kwargs):
        return manager.Tracking.access_by(info.context)

    @types.login_required
    def resolve_webhooks(self, info, **kwargs):
        return events.Webhook.access_by(info.context)


class Mutation:
    update_user = mutations.UpdateUser.Field()
    register_user = mutations.RegisterUser.Field()
    mutate_token = mutations.TokenMutation.Field()

    create_template = mutations.CreateTemplate.Field()
    update_template = mutations.UpdateTemplate.Field()
    delete_template = mutations.create_delete_mutation('DeleteTemplate', graph.Template).Field()

    discard_commodity = mutations.create_delete_mutation(
        'DiscardCommodity', manager.Commodity, customs__template__isnull=False).Field()

    create_connection = mutations.CreateConnection.Field()
    update_connection = mutations.UpdateConnection.Field()
    delete_connection = mutations.create_delete_mutation('DeleteConnection', providers.Carrier).Field()
    mutate_system_connection = mutations.SystemCarrierMutation.Field()
