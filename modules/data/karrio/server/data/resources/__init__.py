import karrio.server.data.models as models
import karrio.server.data.resources.orders as orders
import karrio.server.data.resources.rate_sheets as rate_sheets
import karrio.server.data.resources.shipments as shipments
import karrio.server.data.resources.trackers as trackers
from django.contrib.auth import get_user_model
from import_export import resources

User = get_user_model()


def export(resource_type: str, query_params: dict, context, data_fields: dict = None) -> dict:
    """Generate a file to export."""

    if resource_type == "rate_sheet":
        # Rate sheet export returns raw bytes, not a tablib dataset
        raise NotImplementedError(
            "Use export_rate_sheet() for rate_sheet exports — see views/data.py DataExport for the dedicated handler."
        )

    resource = get_export_resource(resource_type, query_params, context, data_fields=data_fields)

    return resource.export()


def get_export_resource(resource_type: str, params: dict, context, data_fields: dict = None) -> resources.ModelResource:

    if resource_type == "orders":
        return orders.order_export_resource(params, context, data_fields=data_fields)

    if resource_type == "trackers":
        return trackers.tracker_export_resource(params, context, data_fields=data_fields)

    if resource_type == "shipments":
        return shipments.shipment_export_resource(params, context, data_fields=data_fields)

    raise Exception("Unsupported resource")


def get_import_resource(
    resource_type: str, params: dict, context, data_fields: dict = None, **kwargs
) -> resources.ModelResource:

    if resource_type == "orders":
        return orders.order_import_resource(params, context, data_fields=data_fields, **kwargs)

    if resource_type == "trackers":
        return trackers.tracker_import_resource(params, context, data_fields=data_fields, **kwargs)

    if resource_type == "shipments":
        return shipments.shipment_import_resource(params, context, data_fields=data_fields, **kwargs)

    raise Exception("Unsupported resource")
