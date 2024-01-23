from django.db.models import Q
from import_export import resources

import karrio.lib as lib
from karrio.server.orders.serializers.order import OrderSerializer
from karrio.server.orders.filters import OrderFilters
from karrio.server.orders import models

DEFAULT_HEADERS = {
    # Order details
    "id": "ID",
    "order_id": "Order number",
    "order_date": "Order date",
    "order_source": "Order source",
    "order_status": "Status",
    "order_total": "Total",
    "order_currency": "Order Currency",
    "order_created_at": "Created at",
    # Item details
    "title": "Item title",
    "description": "Item Description",
    "quantity": "Item quantity",
    "sku": "Item sku",
    "hs_code": "HS tariff number",
    "value_amount": "Item price",
    "value_currency": "Item currency",
    "weight": "Item weight",
    "weight_unit": "Item weight unit",
    # Shipping details
    "shipping_to_name": "Shipping name",
    "shipping_to_company": "Shipping company",
    "shipping_to_address1": "Shipping address 1",
    "shipping_to_address2": "Shipping address 2",
    "shipping_to_city": "Shipping city",
    "shipping_to_state": "Shipping state",
    "shipping_to_postal_code": "Shipping postal code",
    "shipping_to_country": "Shipping country",
    "shipping_to_residential": "Shipping residential",
    # Billing details
    "shipping_from_name": "From name",
    "shipping_from_company": "From company",
    "shipping_from_address1": "From address 1",
    "shipping_from_address2": "From address 2",
    "shipping_from_city": "From city",
    "shipping_from_state": "From state",
    "shipping_from_postal_code": "From postal code",
    "shipping_from_country": "From country",
    "shipping_from_residential": "From residential",
    # Billing details
    "billing_name": "Billing name",
    "billing_company": "Billing company",
    "billing_address1": "Billing address 1",
    "billing_address2": "Billing address 2",
    "billing_city": "Billing city",
    "billing_state": "Billing state",
    "billing_postal_code": "Billing postal code",
    "billing_country": "Billing country",
    # extra
    "metadata": "Item Metadata",
    "options": "Options",
}


def order_export_resource(query_params: dict, context, **kwargs):
    queryset = models.LineItem.access_by(context)
    _exclude = query_params.get("exclude", "").split(",")
    _fields = (
        "description",
        "quantity",
        "weight",
        "weight_unit",
        "sku",
        "hs_code",
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

        if "id" not in _exclude:
            id = resources.Field()

            def dehydrate_id(self, row):
                return row.order.id

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
                        lib.to_decimal(li.value_amount) or 0.0
                        for li in row.order.line_items.all()
                    ],
                    0.0,
                )

        if "options" not in _exclude:
            options = resources.Field()

            def dehydrate_options(self, row):
                return row.order.options

        if "shipping_to_name" not in _exclude:
            shipping_to_name = resources.Field()

            def dehydrate_shipping_to_name(self, row):
                return row.order.shipping_to.person_name

        if "shipping_to_company" not in _exclude:
            shipping_to_company = resources.Field()

            def dehydrate_shipping_to_company(self, row):
                return row.order.shipping_to.company_name

        if "shipping_to_address1" not in _exclude:
            shipping_to_address1 = resources.Field()

            def dehydrate_shipping_to_address1(self, row):
                return row.order.shipping_to.address_line1

        if "shipping_to_address2" not in _exclude:
            shipping_to_address2 = resources.Field()

            def dehydrate_shipping_to_address2(self, row):
                return row.order.shipping_to.address_line2

        if "shipping_to_city" not in _exclude:
            shipping_to_city = resources.Field()

            def dehydrate_shipping_to_city(self, row):
                return row.order.shipping_to.city

        if "shipping_to_state" not in _exclude:
            shipping_to_state = resources.Field()

            def dehydrate_shipping_to_state(self, row):
                return row.order.shipping_to.state_code

        if "shipping_to_postal_code" not in _exclude:
            shipping_to_postal_code = resources.Field()

            def dehydrate_shipping_to_postal_code(self, row):
                return row.order.shipping_to.postal_code

        if "shipping_to_country" not in _exclude:
            shipping_to_country = resources.Field()

            def dehydrate_shipping_to_country(self, row):
                return row.order.shipping_to.country_code

        if "shipping_to_residential" not in _exclude:
            shipping_to_residential = resources.Field()

            def dehydrate_shipping_to_residential(self, row):
                return "yes" if row.order.shipping_to.residential else "no"

        if "shipping_from_name" not in _exclude:
            shipping_from_name = resources.Field()

            def dehydrate_shipping_from_name(self, row):
                return getattr(row.order.shipping_from, "person_name", None)

        if "shipping_from_company" not in _exclude:
            shipping_from_company = resources.Field()

            def dehydrate_shipping_from_company(self, row):
                return getattr(row.order.shipping_from, "company_name", None)

        if "shipping_from_address1" not in _exclude:
            shipping_from_address1 = resources.Field()

            def dehydrate_shipping_from_address1(self, row):
                return getattr(row.order.shipping_from, "address_line1", None)

        if "shipping_from_address2" not in _exclude:
            shipping_from_address2 = resources.Field()

            def dehydrate_shipping_from_address2(self, row):
                return getattr(row.order.shipping_from, "address_line2", None)

        if "shipping_from_city" not in _exclude:
            shipping_from_city = resources.Field()

            def dehydrate_shipping_from_city(self, row):
                return getattr(row.order.shipping_from, "city", None)

        if "shipping_from_state" not in _exclude:
            shipping_from_state = resources.Field()

            def dehydrate_shipping_from_state(self, row):
                return getattr(row.order.shipping_from, "state_code", None)

        if "shipping_from_postal_code" not in _exclude:
            shipping_from_postal_code = resources.Field()

            def dehydrate_shipping_from_postal_code(self, row):
                return getattr(row.order.shipping_from, "postal_code", None)

        if "shipping_from_country" not in _exclude:
            shipping_from_country = resources.Field()

            def dehydrate_shipping_from_country(self, row):
                return getattr(row.order.shipping_from, "country_code", None)

        if "shipping_from_residential" not in _exclude:
            shipping_from_residential = resources.Field()

            def dehydrate_shipping_from_residential(self, row):
                if getattr(row.order.shipping_from, "country_code", None) is None:
                    return None

                return "yes" if row.order.shipping_from.residential else "no"

        if "billing_name" not in _exclude:
            billing_name = resources.Field()

            def dehydrate_billing_name(self, row):
                return getattr(row.order.billing_address, "person_name", None)

        if "billing_company" not in _exclude:
            billing_company = resources.Field()

            def dehydrate_billing_company(self, row):
                return getattr(row.order.billing_address, "company_name", None)

        if "billing_address1" not in _exclude:
            billing_address1 = resources.Field()

            def dehydrate_billing_address1(self, row):
                return getattr(row.order.billing_address, "address_line1", None)

        if "billing_address2" not in _exclude:
            billing_address2 = resources.Field()

            def dehydrate_billing_address2(self, row):
                return getattr(row.order.billing_address, "address_line2", None)

        if "billing_city" not in _exclude:
            billing_city = resources.Field()

            def dehydrate_billing_city(self, row):
                return getattr(row.order.billing_address, "city", None)

        if "billing_state" not in _exclude:
            billing_state = resources.Field()

            def dehydrate_billing_state(self, row):
                return getattr(row.order.billing_address, "state_code", None)

        if "billing_postal_code" not in _exclude:
            billing_postal_code = resources.Field()

            def dehydrate_billing_postal_code(self, row):
                return getattr(row.order.billing_address, "postal_code", None)

        if "billing_country" not in _exclude:
            billing_country = resources.Field()

            def dehydrate_billing_country(self, row):
                return getattr(row.order.billing_address, "country_code", None)

    return Resource()


def order_import_resource(
    query_params: dict,
    context,
    data_fields: dict = None,
    batch_id: str = None,
    **kwargs
):
    queryset = models.Order.access_by(context)
    field_headers = data_fields if data_fields is not None else DEFAULT_HEADERS
    _exclude = query_params.get("exclude", "").split(",")
    _fields = (
        "id",
        "order_id",
        "order_date",
        "order_source",
        "order_status",
        "options",
        "description",
        "quantity",
        "sku",
        "hs_code",
        "value_amount",
        "value_currency",
        "weight",
        "weight_unit",
        "metadata",
        "shipping_to_name",
        "shipping_to_company",
        "shipping_to_address1",
        "shipping_to_address2",
        "shipping_to_city",
        "shipping_to_state",
        "shipping_to_postal_code",
        "shipping_to_country",
        "shipping_to_residential",
        "shipping_from_name",
        "shipping_from_company",
        "shipping_from_address1",
        "shipping_from_address2",
        "shipping_from_city",
        "shipping_from_state",
        "shipping_from_postal_code",
        "shipping_from_country",
        "shipping_from_residential",
        "billing_name",
        "billing_company",
        "billing_address1",
        "billing_address2",
        "billing_city",
        "billing_state",
        "billing_postal_code",
        "billing_country",
    )

    _Base = type(
        "ResourceFields",
        (resources.ModelResource,),
        {
            k: resources.Field(readonly=(k not in models.Order.__dict__))
            for k in field_headers.keys()
            if k not in _exclude
        },
    )

    class Resource(_Base, resources.ModelResource):
        class Meta:
            model = models.Order
            fields = _fields
            exclude = _exclude
            export_order = [k for k in field_headers.keys() if k not in _exclude]
            force_init_instance = True

        def get_queryset(self):
            return queryset

        def get_export_headers(self):
            headers = super().get_export_headers()
            return [field_headers.get(k, k) for k in headers]

        def init_instance(self, row=None):
            order_id = row.get(field_headers["order_id"])
            source = row.get(field_headers["order_source"])
            meta = {} if batch_id is None else dict(meta=dict(batch_ids=[batch_id]))
            queryset = models.Order.access_by(context).filter(
                order_id=order_id, source=source
            )

            if queryset.exists():
                _order = queryset.first()
                _order.meta = {
                    **(_order.meta or {}),
                    "batch_ids": [
                        *(meta.get("batch_ids") or []),
                        *((_order.meta or {}).get("batch_ids") or []),
                    ],
                }
                _order.save()

                instance = _order

            else:
                _data = lib.to_dict(
                    dict(
                        source=source,
                        order_id=order_id,
                        status="unfulfilled",
                        test_mode=context.test_mode,
                        created_by_id=context.user.id,
                        order_date=row.get(field_headers["order_date"]),
                        options=lib.to_dict(row.get(field_headers["options"]) or "{}"),
                        shipping_to=dict(
                            person_name=row.get(field_headers["shipping_to_name"]),
                            company_name=row.get(field_headers["shipping_to_company"]),
                            address_line1=row.get(
                                field_headers["shipping_to_address1"]
                            ),
                            address_line2=row.get(
                                field_headers["shipping_to_address2"]
                            ),
                            city=row.get(field_headers["shipping_to_city"]),
                            state_code=row.get(field_headers["shipping_to_state"]),
                            postal_code=row.get(
                                field_headers["shipping_to_postal_code"]
                            ),
                            country_code=row.get(field_headers["shipping_to_country"]),
                            residential=row.get(
                                field_headers["shipping_to_residential"]
                            ),
                        ),
                        line_items=[
                            dict(
                                description=row.get(field_headers["description"]),
                                quantity=row.get(field_headers["quantity"]),
                                sku=row.get(field_headers["sku"]),
                                hs_code=row.get(field_headers["hs_code"]),
                                value_amount=row.get(field_headers["value_amount"]),
                                value_currency=row.get(field_headers["value_currency"]),
                                weight=row.get(field_headers["weight"]),
                                weight_unit=row.get(field_headers["weight_unit"]),
                            )
                        ],
                        shipping_from=(
                            dict(
                                person_name=row.get(
                                    field_headers["shipping_from_name"]
                                ),
                                company_name=row.get(
                                    field_headers["shipping_from_company"]
                                ),
                                address_line1=row.get(
                                    field_headers["shipping_from_address1"]
                                ),
                                address_line2=row.get(
                                    field_headers["shipping_from_address2"]
                                ),
                                city=row.get(field_headers["shipping_from_city"]),
                                state_code=row.get(
                                    field_headers["shipping_from_state"]
                                ),
                                postal_code=row.get(
                                    field_headers["shipping_from_postal_code"]
                                ),
                                country_code=row.get(
                                    field_headers["shipping_from_country"]
                                ),
                                residential=row.get(
                                    field_headers["shipping_from_residential"]
                                ),
                            )
                            if any(["From" in key for key in row.keys()])
                            else None
                        ),
                        billing_address=(
                            dict(
                                person_name=row.get(field_headers["billing_name"]),
                                company_name=row.get(field_headers["billing_company"]),
                                address_line1=row.get(
                                    field_headers["billing_address1"]
                                ),
                                address_line2=row.get(
                                    field_headers["billing_address2"]
                                ),
                                city=row.get(field_headers["billing_city"]),
                                state_code=row.get(field_headers["billing_state"]),
                                postal_code=row.get(
                                    field_headers["billing_postal_code"]
                                ),
                                country_code=row.get(field_headers["billing_country"]),
                            )
                            if any(["Billing" in key for key in row.keys()])
                            else None
                        ),
                        **meta,
                    )
                )

                instance = (
                    OrderSerializer.map(data=_data, context=context).save().instance
                )

            return instance

    return Resource()
