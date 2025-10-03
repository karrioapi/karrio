import rest_framework.fields as fields

import karrio.server.manager.serializers as manager_serializers
import karrio.server.serializers as serializers
import karrio.server.openapi as openapi


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


class PurchaseShipmentPayload(serializers.Serializer):
    shipment_id = fields.CharField(required=True, help_text="The shipment id.")

@openapi.extend_schema_field(
    openapi.PolymorphicProxySerializer(
        component_name="PurchaseShippingMethodData",
        serializers=[
            manager_serializers.ShipmentData,
            PurchaseShipmentPayload,
        ],
        resource_type_field_name=None,
    )
)
class ShippingMethodData(serializers.DictField):
    pass
