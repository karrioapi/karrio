import rest_framework.fields as fields

import karrio.server.manager.serializers as manager_serializers
import karrio.server.serializers as serializers


class ShippingMethod(serializers.EntitySerializer):
    object_type = fields.CharField(
        default="shipping-method",
        help_text="Specifies the object type",
    )
    name = fields.CharField(
        required=True,
        help_text="The shipping method name.",
    )
    description = fields.CharField(
        required=False,
        help_text="The shipping method description.",
    )
    carrier_code = fields.CharField(
        required=True,
        help_text="The carrier code.",
    )
    carrier_service = fields.CharField(
        required=True,
        help_text="The carrier service.",
    )
    carrier_ids = fields.ListField(
        required=False,
        help_text="The carrier ids.",
    )
    carrier_options = fields.DictField(
        required=False,
        help_text="The carrier options.",
    )
    metadata = fields.DictField(
        required=False,
        help_text="The metadata.",
    )
    is_active = fields.BooleanField(
        required=True,
        help_text="The is active.",
    )
    test_mode = fields.BooleanField(
        required=True,
        help_text="Specify whether the shipping method is in test mode or not.",
    )
    created_at = fields.CharField(
        required=True,
        help_text="""The shipping method creation datetime.<br/>
        Date Format: `YYYY-MM-DD HH:MM:SS.mmmmmmz`
        """,
    )


class BuyShipmentData(manager_serializers.ShipmentUpdateData):
    reference = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment reference",
    )
