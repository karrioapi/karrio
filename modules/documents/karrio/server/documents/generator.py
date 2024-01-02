import io
import typing
import base64
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
    def generate(document: models.DocumentTemplate, data: dict, **kwargs) -> io.BytesIO:
        shipment_contexts = data.get("shipments_context") or (
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
    distinct_items = [
        __ for _, __ in ({item.parent_id: item for item in items}).items()
    ]

    return [
        {
            **LineItemSerializer(item.parent or item).data,
            "ship_quantity": items.filter(parent_id=item.parent_id).aggregate(
                Sum("quantity")
            )["quantity__sum"],
            "order": (OrderSerializer(item.order).data if item.order else {}),
        }
        for item in distinct_items
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

    return carrier.data.to_dict()


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


def generate_document(slug: str, shipment, **kwargs) -> dict:
    template = models.DocumentTemplate.objects.get(slug=slug)
    carrier = kwargs.get("carrier") or getattr(shipment, "selected_rate_carrier", None)
    params = dict(
        shipments_context=[
            dict(
                shipment=ShipmentSerializer(shipment).data,
                line_items=get_shipment_item_contexts(shipment),
                carrier=get_carrier_context(carrier.settings),
                orders=OrderSerializer(
                    get_shipment_order_contexts(shipment),
                    many=True,
                ).data,
            )
        ]
    )
    document = Documents.generate(template, params).getvalue()

    return dict(
        doc_format="PDF",
        doc_name=f"{template.name}.pdf",
        doc_type=(template.metadata or {}).get("doc_type") or "commercial_invoice",
        doc_file=base64.b64encode(document).decode("utf-8"),
    )
