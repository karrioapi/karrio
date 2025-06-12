import io
import typing
import base64
import jinja2
import weasyprint
from django.db.models import Sum
import weasyprint.text.fonts as fonts

import karrio.lib as lib
import karrio.server.documents.utils as utils
import karrio.server.core.dataunits as dataunits
import karrio.server.orders.models as order_models
import karrio.server.manager.models as manager_models
import karrio.server.documents.models as document_models
import karrio.server.orders.serializers as orders_serializers
import karrio.server.manager.serializers as manager_serializers

FONT_CONFIG = fonts.FontConfiguration()
PAGE_SEPARATOR = '<p style="page-break-before: always"></p>'
STYLESHEETS = [
    weasyprint.CSS(url="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css"),
    weasyprint.CSS(
        string="""
        @page { margin: 1cm }
        @font-face {
            font-family: 'system';
            src: local('Arial');
        }
        body { font-family: 'system', sans-serif; }
    """
    ),
]
UNITS = {
    "PAGE_SEPARATOR": PAGE_SEPARATOR,
    "CountryISO": lib.units.CountryISO.as_dict(),
    **dataunits.REFERENCE_MODELS,
}


class Documents:
    @staticmethod
    def generate(
        template: str,
        data: dict = {},
        related_object: str = None,
        **kwargs,
    ) -> io.BytesIO:
        options = kwargs.get("options") or {}
        metadata = kwargs.get("metadata") or {}
        shipment_contexts = data.get("shipments_context") or lib.identity(
            get_shipments_context(data["shipments"])
            if "shipments" in data and related_object == "shipment"
            else []
        )
        order_contexts = data.get("orders_context") or lib.identity(
            get_orders_context(data["orders"])
            if "orders" in data and related_object == "order"
            else []
        )
        generic_contexts = data.get("generic_context") or lib.identity(
            [{"data": data}] if related_object is None else []
        )
        filename = lib.identity(
            dict(filename=kwargs.get("doc_name")) if kwargs.get("doc_name") else {}
        )

        prefetch = lambda ctx: {
            k: v
            for o in lib.run_concurently(
                lambda _: {
                    _[0]: str(
                        lib.failsafe(
                            lambda: _[1].render(
                                **ctx,
                                metadata=metadata,
                                units=UNITS,
                                utils=utils,
                                lib=lib,
                            )
                        )
                        or ""
                    )
                },
                [
                    (key, jinja2.Template(value))
                    for key, value in options.get("prefetch", {}).items()
                ],
            )
            for k, v in o.items()
        }

        jinja_template = jinja2.Template(template)
        all_contexts = shipment_contexts + order_contexts + generic_contexts
        rendered_pages = lib.run_asynchronously(
            lambda ctx: jinja_template.render(
                **ctx,
                metadata=metadata,
                units=UNITS,
                utils=utils,
                lib=lib,
                prefetch=prefetch(ctx),
            ),
            all_contexts,
        )
        content = PAGE_SEPARATOR.join(rendered_pages)

        buffer = io.BytesIO()
        html = weasyprint.HTML(string=content, encoding="utf-8")
        html.write_pdf(
            buffer,
            stylesheets=STYLESHEETS,
            font_config=FONT_CONFIG,
            optimize_size=("fonts", "images"),
        )

        return buffer

    @staticmethod
    def generate_template(
        document: document_models.DocumentTemplate,
        data: dict,
        **kwargs,
    ) -> io.BytesIO:
        return Documents.generate(
            template=document.template,
            data=data,
            options=document.options,
            metadata=document.metadata,
            related_object=document.related_object,
            **kwargs,
        )

    @staticmethod
    def generate_shipment_document(slug: str, shipment, **kwargs) -> dict:
        template = document_models.DocumentTemplate.objects.get(slug=slug)
        carrier = kwargs.get("carrier") or getattr(
            shipment, "selected_rate_carrier", None
        )
        params = dict(
            shipments_context=[
                dict(
                    shipment=manager_serializers.Shipment(shipment).data,
                    line_items=get_shipment_item_contexts(shipment),
                    carrier=get_carrier_context(carrier),
                    orders=orders_serializers.Order(
                        get_shipment_order_contexts(shipment),
                        many=True,
                    ).data,
                )
            ]
        )
        document = Documents.generate_template(template, params).getvalue()

        return dict(
            doc_format="PDF",
            doc_name=f"{template.name}.pdf",
            doc_type=(template.metadata or {}).get("doc_type") or "commercial_invoice",
            doc_file=base64.b64encode(document).decode("utf-8"),
        )


# -----------------------------------------------------------
# contexts data parsers
# -----------------------------------------------------------
# region


def get_shipments_context(shipment_ids: str) -> typing.List[dict]:
    if shipment_ids == "sample":
        return [utils.SHIPMENT_SAMPLE]

    ids = shipment_ids.split(",")
    shipments = manager_models.Shipment.objects.filter(id__in=ids)

    return [
        dict(
            shipment=manager_serializers.Shipment(shipment).data,
            line_items=get_shipment_item_contexts(shipment),
            carrier=get_carrier_context(shipment.selected_rate_carrier),
            orders=orders_serializers.Order(
                get_shipment_order_contexts(shipment), many=True
            ).data,
        )
        for shipment in shipments
    ]


def get_shipment_item_contexts(shipment):
    items = order_models.LineItem.objects.filter(
        commodity_parcel__parcel_shipment=shipment
    )
    distinct_items = [
        __ for _, __ in ({item.parent_id: item for item in items}).items()
    ]

    return [
        {
            **orders_serializers.LineItem(item.parent or item).data,
            "ship_quantity": items.filter(parent_id=item.parent_id).aggregate(
                Sum("quantity")
            )["quantity__sum"],
            "order": (orders_serializers.Order(item.order).data if item.order else {}),
        }
        for item in distinct_items
    ]


def get_shipment_order_contexts(shipment):
    return (
        order_models.Order.objects.filter(
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
    orders = order_models.Order.objects.filter(id__in=ids)

    return [
        dict(
            order=orders_serializers.Order(order).data,
        )
        for order in orders
    ]


# endregion
