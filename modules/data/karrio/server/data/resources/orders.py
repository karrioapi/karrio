"""Order data export/import resources.

With JSON-based line_items storage, exports now iterate over Orders
and denormalize line items into rows.
"""
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


def _get_address_field(address_data, field_name, default=None):
    """Safely get a field from address JSON data."""
    if not address_data or not isinstance(address_data, dict):
        return default
    return address_data.get(field_name, default)


def order_export_resource(query_params: dict, context, **kwargs):
    """Create export resource for orders with JSON-based line items.

    With JSON storage, we export at the Order level and denormalize
    line items into the export data.
    """
    _exclude = query_params.get("exclude", "").split(",")

    # Base queryset filtering
    base_qs = models.Order.access_by(context)
    if "status" not in query_params:
        base_qs = base_qs.filter(
            Q(status__in=["fulfilled", "delivered"]),
        )

    class Resource(resources.ModelResource):
        class Meta:
            model = models.Order
            fields = (
                "id",
                "order_id",
                "order_date",
                "source",
                "status",
            )
            exclude = _exclude
            export_order = [k for k in DEFAULT_HEADERS.keys() if k not in _exclude]

        def get_queryset(self):
            return OrderFilters(query_params, base_qs).qs

        def get_export_headers(self, **kwargs):
            headers = super().get_export_headers(**kwargs)
            return [DEFAULT_HEADERS.get(k, k) for k in headers]

        # Order fields
        if "order_source" not in _exclude:
            order_source = resources.Field()

            def dehydrate_order_source(self, row):
                return row.source

        if "order_status" not in _exclude:
            order_status = resources.Field()

            def dehydrate_order_status(self, row):
                return row.status

        if "order_created_at" not in _exclude:
            order_created_at = resources.Field()

            def dehydrate_order_created_at(self, row):
                return row.created_at

        if "order_currency" not in _exclude:
            order_currency = resources.Field()

            def dehydrate_order_currency(self, row):
                line_items = row.line_items or []
                if line_items:
                    return line_items[0].get("value_currency")
                return None

        if "order_total" not in _exclude:
            order_total = resources.Field()

            def dehydrate_order_total(self, row):
                return sum(
                    [
                        lib.to_decimal(li.get("value_amount")) or 0.0
                        for li in (row.line_items or [])
                    ],
                    0.0,
                )

        if "options" not in _exclude:
            options = resources.Field()

            def dehydrate_options(self, row):
                return row.options

        # Line item fields (uses first line item for export)
        if "description" not in _exclude:
            description = resources.Field()

            def dehydrate_description(self, row):
                line_items = row.line_items or []
                return line_items[0].get("description") if line_items else None

        if "quantity" not in _exclude:
            quantity = resources.Field()

            def dehydrate_quantity(self, row):
                line_items = row.line_items or []
                return line_items[0].get("quantity") if line_items else None

        if "sku" not in _exclude:
            sku = resources.Field()

            def dehydrate_sku(self, row):
                line_items = row.line_items or []
                return line_items[0].get("sku") if line_items else None

        if "hs_code" not in _exclude:
            hs_code = resources.Field()

            def dehydrate_hs_code(self, row):
                line_items = row.line_items or []
                return line_items[0].get("hs_code") if line_items else None

        if "value_amount" not in _exclude:
            value_amount = resources.Field()

            def dehydrate_value_amount(self, row):
                line_items = row.line_items or []
                return line_items[0].get("value_amount") if line_items else None

        if "value_currency" not in _exclude:
            value_currency = resources.Field()

            def dehydrate_value_currency(self, row):
                line_items = row.line_items or []
                return line_items[0].get("value_currency") if line_items else None

        if "weight" not in _exclude:
            weight = resources.Field()

            def dehydrate_weight(self, row):
                line_items = row.line_items or []
                return line_items[0].get("weight") if line_items else None

        if "weight_unit" not in _exclude:
            weight_unit = resources.Field()

            def dehydrate_weight_unit(self, row):
                line_items = row.line_items or []
                return line_items[0].get("weight_unit") if line_items else None

        if "metadata" not in _exclude:
            metadata = resources.Field()

            def dehydrate_metadata(self, row):
                line_items = row.line_items or []
                return line_items[0].get("metadata") if line_items else None

        # Shipping to (JSON address)
        if "shipping_to_name" not in _exclude:
            shipping_to_name = resources.Field()

            def dehydrate_shipping_to_name(self, row):
                return _get_address_field(row.shipping_to, "person_name")

        if "shipping_to_company" not in _exclude:
            shipping_to_company = resources.Field()

            def dehydrate_shipping_to_company(self, row):
                return _get_address_field(row.shipping_to, "company_name")

        if "shipping_to_address1" not in _exclude:
            shipping_to_address1 = resources.Field()

            def dehydrate_shipping_to_address1(self, row):
                return _get_address_field(row.shipping_to, "address_line1")

        if "shipping_to_address2" not in _exclude:
            shipping_to_address2 = resources.Field()

            def dehydrate_shipping_to_address2(self, row):
                return _get_address_field(row.shipping_to, "address_line2")

        if "shipping_to_city" not in _exclude:
            shipping_to_city = resources.Field()

            def dehydrate_shipping_to_city(self, row):
                return _get_address_field(row.shipping_to, "city")

        if "shipping_to_state" not in _exclude:
            shipping_to_state = resources.Field()

            def dehydrate_shipping_to_state(self, row):
                return _get_address_field(row.shipping_to, "state_code")

        if "shipping_to_postal_code" not in _exclude:
            shipping_to_postal_code = resources.Field()

            def dehydrate_shipping_to_postal_code(self, row):
                return _get_address_field(row.shipping_to, "postal_code")

        if "shipping_to_country" not in _exclude:
            shipping_to_country = resources.Field()

            def dehydrate_shipping_to_country(self, row):
                return _get_address_field(row.shipping_to, "country_code")

        if "shipping_to_residential" not in _exclude:
            shipping_to_residential = resources.Field()

            def dehydrate_shipping_to_residential(self, row):
                residential = _get_address_field(row.shipping_to, "residential")
                return "yes" if residential else "no"

        # Shipping from (JSON address)
        if "shipping_from_name" not in _exclude:
            shipping_from_name = resources.Field()

            def dehydrate_shipping_from_name(self, row):
                return _get_address_field(row.shipping_from, "person_name")

        if "shipping_from_company" not in _exclude:
            shipping_from_company = resources.Field()

            def dehydrate_shipping_from_company(self, row):
                return _get_address_field(row.shipping_from, "company_name")

        if "shipping_from_address1" not in _exclude:
            shipping_from_address1 = resources.Field()

            def dehydrate_shipping_from_address1(self, row):
                return _get_address_field(row.shipping_from, "address_line1")

        if "shipping_from_address2" not in _exclude:
            shipping_from_address2 = resources.Field()

            def dehydrate_shipping_from_address2(self, row):
                return _get_address_field(row.shipping_from, "address_line2")

        if "shipping_from_city" not in _exclude:
            shipping_from_city = resources.Field()

            def dehydrate_shipping_from_city(self, row):
                return _get_address_field(row.shipping_from, "city")

        if "shipping_from_state" not in _exclude:
            shipping_from_state = resources.Field()

            def dehydrate_shipping_from_state(self, row):
                return _get_address_field(row.shipping_from, "state_code")

        if "shipping_from_postal_code" not in _exclude:
            shipping_from_postal_code = resources.Field()

            def dehydrate_shipping_from_postal_code(self, row):
                return _get_address_field(row.shipping_from, "postal_code")

        if "shipping_from_country" not in _exclude:
            shipping_from_country = resources.Field()

            def dehydrate_shipping_from_country(self, row):
                return _get_address_field(row.shipping_from, "country_code")

        if "shipping_from_residential" not in _exclude:
            shipping_from_residential = resources.Field()

            def dehydrate_shipping_from_residential(self, row):
                if _get_address_field(row.shipping_from, "country_code") is None:
                    return None
                residential = _get_address_field(row.shipping_from, "residential")
                return "yes" if residential else "no"

        # Billing address (JSON)
        if "billing_name" not in _exclude:
            billing_name = resources.Field()

            def dehydrate_billing_name(self, row):
                return _get_address_field(row.billing_address, "person_name")

        if "billing_company" not in _exclude:
            billing_company = resources.Field()

            def dehydrate_billing_company(self, row):
                return _get_address_field(row.billing_address, "company_name")

        if "billing_address1" not in _exclude:
            billing_address1 = resources.Field()

            def dehydrate_billing_address1(self, row):
                return _get_address_field(row.billing_address, "address_line1")

        if "billing_address2" not in _exclude:
            billing_address2 = resources.Field()

            def dehydrate_billing_address2(self, row):
                return _get_address_field(row.billing_address, "address_line2")

        if "billing_city" not in _exclude:
            billing_city = resources.Field()

            def dehydrate_billing_city(self, row):
                return _get_address_field(row.billing_address, "city")

        if "billing_state" not in _exclude:
            billing_state = resources.Field()

            def dehydrate_billing_state(self, row):
                return _get_address_field(row.billing_address, "state_code")

        if "billing_postal_code" not in _exclude:
            billing_postal_code = resources.Field()

            def dehydrate_billing_postal_code(self, row):
                return _get_address_field(row.billing_address, "postal_code")

        if "billing_country" not in _exclude:
            billing_country = resources.Field()

            def dehydrate_billing_country(self, row):
                return _get_address_field(row.billing_address, "country_code")

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

        def get_export_headers(self, **kwargs):
            headers = super().get_export_headers(**kwargs)
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
