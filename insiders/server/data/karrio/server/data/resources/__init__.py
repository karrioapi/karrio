from django.contrib.auth import get_user_model
from import_export import resources

import karrio.server.data.resources.shipments as shipments
import karrio.server.data.resources.orders as orders
import karrio.server.data.resources.tracking as tracking
import karrio.server.data.models as models

User = get_user_model()


def export(
    resource_type: str, query_params: dict, context, data_fields: dict = None
) -> dict:
    """Generate a file to export."""

    resource = get_resource(
        resource_type, query_params, context, data_fields=data_fields
    )

    return resource.export()


def get_resource(
    resource_type: str, params: dict, context, data_fields: dict = None
) -> resources.ModelResource:

    if resource_type == "orders":
        return orders.order_resource(params, context, data_fields=data_fields)

    if resource_type == "tracking":
        return tracking.tracking_resource(params, context, data_fields=data_fields)

    if resource_type == "shipments":
        return shipments.shipment_resource(params, context, data_fields=data_fields)

    raise Exception("Unsupported resource")
