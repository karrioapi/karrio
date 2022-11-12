import io
import typing
from jinja2 import Template
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
from django.db.models import Sum

from karrio.core.units import CountryISO
from karrio.server.core.dataunits import REFERENCE_MODELS
from karrio.server.manager.models import Shipment
from karrio.server.orders.models import Order, LineItem
from karrio.server.orders.serializers import (
    Order as OrderSerializer,
    LineItem as LineItemSerializer,
)
from karrio.server.core.serializers import (
    Shipment as ShipmentSerializer,
    CarrierSettings,
)
from karrio.server.documents import models
from karrio.server.documents import utils

FONT_CONFIG = FontConfiguration()
PAGE_SEPARATOR = '<p style="page-break-before: always"></p>'
STYLESHEETS = ["https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css"]
UNITS = {
    "PAGE_SEPARATOR": PAGE_SEPARATOR,
    "CountryISO": CountryISO.as_dict(),
    **REFERENCE_MODELS,
}


class Documents:
    @staticmethod
    def generate(document: models.DocumentTemplate, data: dict, context) -> io.BytesIO:
        shipment_contexts = (
            get_shipments_context(data["shipments"])
            if "shipments" in data and document.related_object == "shipment"
            else []
        )
        order_contexts = (
            get_orders_context(data["orders"])
            if "orders" in data and document.related_object == "order"
            else []
        )

        template = Template(document.template)
        content = PAGE_SEPARATOR.join(
            [
                template.render(**ctx, units=UNITS, utils=utils)
                for ctx in shipment_contexts
            ]
            + [
                template.render(**ctx, units=UNITS, utils=utils)
                for ctx in order_contexts
            ]
        )

        buffer = io.BytesIO()
        HTML(string=content).write_pdf(
            buffer,
            stylesheets=STYLESHEETS,
            font_config=FONT_CONFIG,
        )

        return buffer


def get_shipments_context(shipment_ids: str) -> typing.List[dict]:
    if shipment_ids == "sample":
        return [utils.SHIPMENT_SAMPLE]

    ids = shipment_ids.split(",")
    shipments = Shipment.objects.filter(id__in=ids)

    return [
        dict(
            shipment=ShipmentSerializer(shipment).data,
            line_items=get_shipment_item_contexts(shipment),
            carrier=get_carrier_context(shipment.selected_rate_carrier.settings),
            orders=OrderSerializer(
                get_shipment_order_contexts(shipment), many=True
            ).data,
        )
        for shipment in shipments
    ]


def get_shipment_item_contexts(shipment):
    items = LineItem.objects.filter(commodity_parcel__parcel_shipment=shipment)

    return [
        {
            **LineItemSerializer(item.parent or item).data,
            "ship_quantity": items.filter(parent_id=item.parent_id).aggregate(
                Sum("quantity")
            )["quantity__sum"],
            "order": OrderSerializer(item.order or {}).data,
        }
        for item in items.order_by("parent_id").distinct("parent_id")
    ]


def get_shipment_order_contexts(shipment):
    return (
        Order.objects.filter(
            line_items__children__commodity_parcel__parcel_shipment=shipment
        )
        .order_by("-order_date")
        .distinct()
    )


def get_carrier_context(carrier=None):
    if carrier is None:
        return {}

    carrier_name = getattr(
        carrier,
        "custom_carrier_name",
        getattr(carrier, "carrier_name", ""),
    )
    display_name = getattr(
        carrier,
        "display_name",
        REFERENCE_MODELS.get("carriers", {}).get(carrier.carrier_name),
    )

    return {
        **CarrierSettings(carrier).data,
        "carrier_name": carrier_name,
        "display_name": display_name,
        "metadata": carrier.metadata or {},
    }


def get_orders_context(order_ids: str) -> typing.List[dict]:
    if order_ids == "sample":
        return [utils.ORDER_SAMPLE]

    ids = order_ids.split(",")
    orders = Order.objects.filter(id__in=ids)

    return [
        dict(
            order=OrderSerializer(order).data,
        )
        for order in orders
    ]
