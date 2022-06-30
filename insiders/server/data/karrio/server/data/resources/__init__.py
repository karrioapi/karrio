from django.contrib.auth import get_user_model

import karrio.server.data.resources.shipments as shipments
import karrio.server.data.resources.orders as orders
import karrio.server.data.resources.tracking as tracking

User = get_user_model()


def export(resource: str, query_params: dict, context) -> dict:
    """Generate a file to export."""

    if resource == "orders":
        return orders.order_resource(query_params, context).export()

    if resource == "shipments":
        return shipments.shipment_resource(query_params, context).export()

    raise Exception("Unknown resource")
