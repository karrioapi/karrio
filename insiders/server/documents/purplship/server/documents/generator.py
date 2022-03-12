import io
import typing
from jinja2 import Template
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
from purplship.server.documents import models
from purplship.server.manager.models import Shipment
from purplship.server.orders.models import Order

font_config = FontConfiguration()
PAGE_SEPARATOR = '<p style="page-break-before: always"></p>'


class Documents:
    @staticmethod
    def generate(document: models.DocumentTemplate, data: dict, context) -> io.BytesIO:
        payload = dict(
            shipments=(
                Shipment.access_by(context).filter(id__in=data["shipments"].split(","))
                if "shipments" in data and "shipment" in document.related_objects
                else []
            ),
            orders=(
                Order.access_by(context).filter(id__in=data["orders"].split(","))
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
        HTML(string=content).write_pdf(buffer, font_config=font_config)

        return buffer
