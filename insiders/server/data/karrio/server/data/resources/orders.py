from django.db.models import Q
from import_export import resources

from karrio.core.utils import NF
from karrio.server.orders import models
from karrio.server.orders.filters import OrderFilters

DEFAULT_HEADERS = {
    # Order details
    "order_id": "Order ID",
    "order_date": "Order date",
    "order_source": "Source",
    "order_status": "Status",
    "order_total": "Total",
    "order_currency": "Order Currency",
    "order_created_at": "Created at",
    # Lineitem details
    "description": "Lineitem title",
    "quantity": "Lineitem quantity",
    "sku": "Lineitem sku",
    "value_amount": "Lineitem price",
    "value_currency": "Lineitem currency",
    "weight": "Lineitem weight",
    "weight_unit": "Lineitem weight unit",
    # Shipping details
    "recipient_name": "Recipient name",
    "recipient_company": "Company",
    "recipient_address_line1": "address Line 1",
    "recipient_address_line2": "address Line 2",
    "recipient_city": "city",
    "recipient_state": "State/Province",
    "recipient_postal_code": "Zip/Postal Code",
    "recipient_country": "country",
    "recipient_residential": "residential",
    "metadata": "Metadata",
}


def order_resource(query_params: dict, context):
    queryset = models.LineItem.access_by(context)
    _exclude = query_params.get("exclude", "").split(",")
    _fields = (
        "description",
        "quantity",
        "weight",
        "weight_unit",
        "sku",
        "value_amount",
        "value_currency",
        "metadata",
    )

    if "status" not in query_params:
        queryset = queryset.filter(
            Q(commodity_order__status__in=["fulfilled", "delivered"]),
        )

    class Resource(resources.ModelResource):
        class Meta:
            model = models.LineItem
            fields = _fields
            exclude = _exclude
            export_order = [k for k in DEFAULT_HEADERS.keys() if k not in _exclude]

        def get_queryset(self):
            orders = OrderFilters(query_params, models.Order.access_by(context)).qs
            return queryset.filter(commodity_order__in=orders)

        def get_export_headers(self):
            headers = super().get_export_headers()
            return [DEFAULT_HEADERS.get(k, k) for k in headers]

        if "order_id" not in _exclude:
            order_id = resources.Field()

            def dehydrate_order_id(self, row):
                return row.order.order_id

        if "order_date" not in _exclude:
            order_date = resources.Field()

            def dehydrate_order_date(self, row):
                return row.order.order_date

        if "order_status" not in _exclude:
            order_status = resources.Field()

            def dehydrate_order_status(self, row):
                return row.order.status

        if "order_source" not in _exclude:
            order_source = resources.Field()

            def dehydrate_order_source(self, row):
                return row.order.source

        if "order_created_at" not in _exclude:
            order_created_at = resources.Field()

            def dehydrate_order_created_at(self, row):
                return row.order.created_at

        if "order_currency" not in _exclude:
            order_currency = resources.Field()

            def dehydrate_order_currency(self, row):
                return row.value_currency

        if "order_total" not in _exclude:
            order_total = resources.Field()

            def dehydrate_order_total(self, row):
                return sum(
                    [
                        NF.decimal(li.value_amount) or 0.0
                        for li in row.order.line_items.all()
                    ],
                    0.0,
                )

        if "recipient_name" not in _exclude:
            recipient_name = resources.Field()

            def dehydrate_recipient_name(self, row):
                return row.order.shipping_to.person_name

        if "recipient_company" not in _exclude:
            recipient_company = resources.Field()

            def dehydrate_recipient_company(self, row):
                return row.order.shipping_to.company_name

        if "recipient_address_line1" not in _exclude:
            recipient_address_line1 = resources.Field()

            def dehydrate_recipient_address_line1(self, row):
                return row.order.shipping_to.address_line1

        if "recipient_address_line2" not in _exclude:
            recipient_address_line2 = resources.Field()

            def dehydrate_recipient_address_line2(self, row):
                return row.order.shipping_to.address_line2

        if "recipient_city" not in _exclude:
            recipient_city = resources.Field()

            def dehydrate_recipient_city(self, row):
                return row.order.shipping_to.city

        if "recipient_state" not in _exclude:
            recipient_state = resources.Field()

            def dehydrate_recipient_state(self, row):
                return row.order.shipping_to.state_code

        if "recipient_postal_code" not in _exclude:
            recipient_postal_code = resources.Field()

            def dehydrate_recipient_postal_code(self, row):
                return row.order.shipping_to.postal_code

        if "recipient_country" not in _exclude:
            recipient_country = resources.Field()

            def dehydrate_recipient_country(self, row):
                return row.order.shipping_to.country_code

        if "recipient_residential" not in _exclude:
            recipient_residential = resources.Field()

            def dehydrate_recipient_residential(self, row):
                return "yes" if row.order.shipping_to.residential else "no"

    return Resource()
