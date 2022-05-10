from django.contrib.auth import get_user_model
from karrio.server.data.resources.shipments import shipment_resource
from karrio.server.data.resources.orders import order_resource

User = get_user_model()


def export(resource: str, query_params: dict, context) -> dict:
    """Generate a file to export."""

    if resource == "orders":
        return order_resource(query_params, context).export()

    if resource == "shipments":
        return shipment_resource(query_params, context).export()

    raise Exception("Unknown resource")
