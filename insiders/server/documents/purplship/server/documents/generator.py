import io
import typing
from jinja2 import Template
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
from purplship.server.documents import models
from purplship.server.manager.models import Shipment
from purplship.server.orders.models import Order
from purplship.server.orders.serializers import Order as OrderSerializer
from purplship.server.core.serializers import Shipment as ShipmentSerializer
from purplship.server.documents.utils import ORDER_SAMPLE, SHIPMENT_SAMPLE

font_config = FontConfiguration()
PAGE_SEPARATOR = '<p style="page-break-before: always"></p>'


class Documents:
    @staticmethod
    def generate(document: models.DocumentTemplate, data: dict, context) -> io.BytesIO:
        payload = dict(
            shipments=(
                get_related_shipments(data["shipments"], context)
                if "shipments" in data and "shipment" in document.related_objects
                else []
            ),
            orders=(
                get_related_orders(data["orders"], context)
                if "orders" in data and "order" in document.related_objects
                else []
            ),
        )

        template = Template(document.template)
        content = PAGE_SEPARATOR.join(
            [template.render(shipment=ctx) for ctx in payload["shipments"]]
            + [template.render(order=ctx) for ctx in payload["orders"]]
        )

        buffer = io.BytesIO()
        HTML(string=content).write_pdf(
            buffer,
            stylesheets=["https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css"],
            font_config=font_config,
        )

        return buffer


def get_related_shipments(shipment_ids: str, context) -> typing.List[Shipment]:
    if shipment_ids == "sample":
        return [SHIPMENT_SAMPLE]

    ids = shipment_ids.split(",")
    return ShipmentSerializer(
        Shipment.access_by(context).filter(id__in=ids), many=True
    ).data


def get_related_orders(order_ids: str, context) -> typing.List[Order]:
    if order_ids == "sample":
        return [ORDER_SAMPLE]

    ids = order_ids.split(",")
    return OrderSerializer(Order.access_by(context).filter(id__in=ids), many=True).data
