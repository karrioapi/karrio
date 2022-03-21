import io
import typing
from jinja2 import Template
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration

from karrio.core.units import CountryISO
from karrio.server.core.dataunits import REFERENCE_MODELS
from karrio.server.manager.models import Shipment
from karrio.server.orders.models import Order
from karrio.server.orders.serializers import Order as OrderSerializer
from karrio.server.core.serializers import (
    Commodity,
    ShipmentStatus,
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
            get_shipments_context(data["shipments"], context)
            if "shipments" in data and document.related_object == "shipment"
            else []
        )
        order_contexts = (
            get_orders_context(data["orders"], context)
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


def get_shipments_context(shipment_ids: str, context) -> typing.List[dict]:
    if shipment_ids == "sample":
        return [utils.SHIPMENT_SAMPLE]

    ids = shipment_ids.split(",")
    shipments = Shipment.objects.filter(id__in=ids)

    return [
        dict(
            shipment=ShipmentSerializer(shipment).data,
            carrier=get_carrier_context(shipment.selected_rate_carrier),
        )
        for shipment in shipments
    ]


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
        REFERENCE_MODELS["carriers"][carrier.carrier_name],
    )

    return {
        **CarrierSettings(carrier).data,
        "carrier_name": carrier_name,
        "display_name": display_name,
        "metadata": carrier.metadata or {},
    }


def get_orders_context(order_ids: str, context) -> typing.List[dict]:
    if order_ids == "sample":
        return [utils.ORDER_SAMPLE]

    ids = order_ids.split(",")
    orders = Order.objects.filter(id__in=ids)

    return [
        dict(
            order=OrderSerializer(order).data,
            fulfilments=get_fulfilments_context(order),
        )
        for order in orders
    ]


def get_fulfilments_context(order: Order) -> typing.List[dict]:
    return [
        dict(
            item=Commodity(item).data,
            fulfilled_quantity=sum(
                [
                    child.quantity or 0
                    for child in list(
                        item.children.exclude(
                            commodity_parcel__parcel_shipment__status__in=[
                                ShipmentStatus.cancelled.value,
                                ShipmentStatus.draft.value,
                            ]
                        ).filter(
                            commodity_parcel__isnull=False,
                            commodity_customs__isnull=True,
                        )
                    )
                ],
                0,
            ),
        )
        for item in order.line_items.all()
    ]
