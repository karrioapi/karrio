# Data migration: Populate JSON fields from FK/M2M relations
# Phase 2 of the Address/Parcel/Product refactoring

from django.db import migrations


def address_to_dict(address):
    """Convert Address model instance to JSON dict."""
    if address is None:
        return None

    return {
        "id": address.id,
        "postal_code": address.postal_code,
        "city": address.city,
        "country_code": address.country_code,
        "federal_tax_id": address.federal_tax_id,
        "state_tax_id": address.state_tax_id,
        "person_name": address.person_name,
        "company_name": address.company_name,
        "email": address.email,
        "phone_number": address.phone_number,
        "state_code": address.state_code,
        "suburb": address.suburb,
        "residential": address.residential,
        "street_number": address.street_number,
        "address_line1": address.address_line1,
        "address_line2": address.address_line2,
        "validate_location": address.validate_location,
        "validation": address.validation,
    }


def commodity_to_dict(commodity, id_prefix="cmd"):
    """Convert Commodity model instance to JSON dict."""
    if commodity is None:
        return None

    return {
        "id": f"{id_prefix}_{commodity.id[-12:]}",  # Generate new JSON ID
        "template_id": commodity.id,  # Keep reference to original
        "weight": commodity.weight,
        "weight_unit": commodity.weight_unit,
        "quantity": commodity.quantity,
        "sku": commodity.sku,
        "title": commodity.title,
        "description": commodity.description,
        "value_amount": float(commodity.value_amount) if commodity.value_amount else None,
        "value_currency": commodity.value_currency,
        "origin_country": commodity.origin_country,
        "hs_code": commodity.hs_code,
        "product_url": commodity.product_url,
        "image_url": commodity.image_url,
        "metadata": commodity.metadata,
        "parent_id": commodity.parent_id,  # Preserve parent reference
    }


def parcel_to_dict(parcel):
    """Convert Parcel model instance to JSON dict with items."""
    if parcel is None:
        return None

    items = [
        commodity_to_dict(item, id_prefix="itm")
        for item in parcel.items.all()
    ]

    return {
        "id": f"pcl_{parcel.id[-12:]}",  # Generate new JSON ID
        "template_id": parcel.id,  # Keep reference to original
        "weight": parcel.weight,
        "weight_unit": parcel.weight_unit,
        "width": parcel.width,
        "height": parcel.height,
        "length": parcel.length,
        "dimension_unit": parcel.dimension_unit,
        "packaging_type": parcel.packaging_type,
        "package_preset": parcel.package_preset,
        "is_document": parcel.is_document,
        "description": parcel.description,
        "content": parcel.content,
        "reference_number": parcel.reference_number,
        "freight_class": parcel.freight_class,
        "options": parcel.options,
        "items": items,
    }


def customs_to_dict(customs):
    """Convert Customs model instance to JSON dict with commodities."""
    if customs is None:
        return None

    commodities = [
        commodity_to_dict(c, id_prefix="cmd")
        for c in customs.commodities.all()
    ]

    return {
        "id": customs.id,
        "content_type": customs.content_type,
        "content_description": customs.content_description,
        "incoterm": customs.incoterm,
        "invoice": customs.invoice,
        "invoice_date": str(customs.invoice_date) if customs.invoice_date else None,
        "commercial_invoice": customs.commercial_invoice,
        "certify": customs.certify,
        "signer": customs.signer,
        "duty": customs.duty,
        "options": customs.options,
        "duty_billing_address": address_to_dict(customs.duty_billing_address),
        "commodities": commodities,
    }


def populate_shipment_json_fields(apps, schema_editor):
    """Populate Shipment JSON fields from FK/M2M relations."""
    Shipment = apps.get_model("manager", "Shipment")

    # Process in batches to avoid memory issues
    batch_size = 500
    total = Shipment.objects.count()

    for offset in range(0, total, batch_size):
        shipments = Shipment.objects.select_related(
            "shipper",
            "recipient",
            "return_address",
            "billing_address",
            "customs",
            "customs__duty_billing_address",
        ).prefetch_related(
            "parcels",
            "parcels__items",
            "customs__commodities",
        )[offset:offset + batch_size]

        for shipment in shipments:
            changes = []

            # Populate shipper_data
            if shipment.shipper and not shipment.shipper_data:
                shipment.shipper_data = address_to_dict(shipment.shipper)
                changes.append("shipper_data")

            # Populate recipient_data
            if shipment.recipient and not shipment.recipient_data:
                shipment.recipient_data = address_to_dict(shipment.recipient)
                changes.append("recipient_data")

            # Populate return_address_data
            if shipment.return_address and not shipment.return_address_data:
                shipment.return_address_data = address_to_dict(shipment.return_address)
                changes.append("return_address_data")

            # Populate billing_address_data
            if shipment.billing_address and not shipment.billing_address_data:
                shipment.billing_address_data = address_to_dict(shipment.billing_address)
                changes.append("billing_address_data")

            # Populate parcels_data
            if shipment.parcels.exists() and not shipment.parcels_data:
                shipment.parcels_data = [
                    parcel_to_dict(p) for p in shipment.parcels.all()
                ]
                changes.append("parcels_data")

            # Populate customs_data
            if shipment.customs and not shipment.customs_data:
                shipment.customs_data = customs_to_dict(shipment.customs)
                changes.append("customs_data")

            if changes:
                shipment.save(update_fields=changes)


def line_item_to_dict(line_item):
    """Convert LineItem/Commodity to JSON dict for orders."""
    return {
        "id": f"oli_{line_item.id[-12:]}",  # Generate new JSON ID
        "template_id": line_item.id,  # Keep reference to original
        "weight": line_item.weight,
        "weight_unit": line_item.weight_unit,
        "quantity": line_item.quantity,
        "unfulfilled_quantity": getattr(line_item, "unfulfilled_quantity", line_item.quantity),
        "sku": line_item.sku,
        "title": line_item.title,
        "description": line_item.description,
        "value_amount": float(line_item.value_amount) if line_item.value_amount else None,
        "value_currency": line_item.value_currency,
        "origin_country": line_item.origin_country,
        "hs_code": line_item.hs_code,
        "product_url": line_item.product_url,
        "image_url": line_item.image_url,
        "metadata": line_item.metadata,
    }


def populate_order_json_fields(apps, schema_editor):
    """Populate Order JSON fields from FK/M2M relations."""
    Order = apps.get_model("orders", "Order")

    # Process in batches
    batch_size = 500
    total = Order.objects.count()

    for offset in range(0, total, batch_size):
        orders = Order.objects.select_related(
            "shipping_to",
            "shipping_from",
            "billing_address",
        ).prefetch_related(
            "line_items",
        )[offset:offset + batch_size]

        for order in orders:
            changes = []

            # Populate shipping_to_data
            if order.shipping_to and not order.shipping_to_data:
                order.shipping_to_data = address_to_dict(order.shipping_to)
                changes.append("shipping_to_data")

            # Populate shipping_from_data
            if order.shipping_from and not order.shipping_from_data:
                order.shipping_from_data = address_to_dict(order.shipping_from)
                changes.append("shipping_from_data")

            # Populate billing_address_data
            if order.billing_address and not order.billing_address_data:
                order.billing_address_data = address_to_dict(order.billing_address)
                changes.append("billing_address_data")

            # Populate line_items_data
            if order.line_items.exists() and not order.line_items_data:
                order.line_items_data = [
                    line_item_to_dict(item) for item in order.line_items.all()
                ]
                changes.append("line_items_data")

            if changes:
                order.save(update_fields=changes)


def reverse_noop(apps, schema_editor):
    """Reverse migration is a no-op - data remains in both fields."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0071_product_proxy"),
        ("orders", "0021_add_json_fields"),
    ]

    operations = [
        migrations.RunPython(
            populate_shipment_json_fields,
            reverse_noop,
        ),
        migrations.RunPython(
            populate_order_json_fields,
            reverse_noop,
        ),
    ]
