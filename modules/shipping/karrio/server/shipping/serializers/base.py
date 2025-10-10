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
        allow_blank=True,
        allow_null=True,
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
    carrier_id = fields.CharField(
        allow_blank=True,
        allow_null=True,
        required=False,
        help_text="The carrier id.",
    )
    carrier_options = fields.DictField(
        required=False,
        default={},
        help_text="""<details>
        <summary>The options available for the shipment.</summary>

        {
            "currency": "USD",
            "insurance": 100.00,
            "cash_on_delivery": 30.00,
            "dangerous_good": true,
            "declared_value": 150.00,
            "sms_notification": true,
            "email_notification": true,
            "email_notification_to": "shipper@mail.com",
            "hold_at_location": true,
            "paperless_trade": true,
            "preferred_service": "fedex_express_saver",
            "shipment_date": "2020-01-01",  # TODO: deprecate
            "shipping_date": "2020-01-01T00:00",
            "shipment_note": "This is a shipment note",
            "signature_confirmation": true,
            "saturday_delivery": true,
            "is_return": true,
            "shipper_instructions": "This is a shipper instruction",
            "recipient_instructions": "This is a recipient instruction",
            "doc_files": [
                {
                    "doc_type": "commercial_invoice",
                    "doc_file": "base64 encoded file",
                    "doc_name": "commercial_invoice.pdf",
                    "doc_format": "pdf",
                }
            ],
            "doc_references": [
                {
                    "doc_id": "123456789",
                    "doc_type": "commercial_invoice",
                }
            ],
        }
        </details>
        """,
    )
    metadata = fields.DictField(
        required=False,
        default={},
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
