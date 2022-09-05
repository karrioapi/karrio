import graphene
import graphene_django.filter as django_filter

import karrio.server.graph.utils as utils
import karrio.server.graph.extension.orders.mutations as mutations
import karrio.server.graph.extension.orders.types as types
import karrio.server.orders.filters as filters
import karrio.server.orders.models as models


class Query:
    order = graphene.Field(types.OrderType, id=graphene.String(required=True))
    orders = django_filter.DjangoFilterConnectionField(
        types.OrderType,
        required=True,
        filterset_class=filters.OrderFilters,
        default_value=[],
    )

    @utils.authentication_required
    @utils.authorization_required(["ORDERS_MANAGEMENT"])
    def resolve_order(self, info, **kwargs):
        return models.Order.access_by(info.context).filter(**kwargs).first()

    @utils.authentication_required
    @utils.authorization_required(["ORDERS_MANAGEMENT"])
    def resolve_orders(self, info, **kwargs):
        return models.Order.access_by(info.context)


class Mutation:
    create_order = mutations.CreateOrder.Field()
    partial_order_update = mutations.PartialOrderUpdate.Field()
