import uuid
import typing
import datetime
import rest_framework.status as status
import django.db.transaction as transaction
from rest_framework.reverse import reverse

import karrio.lib as lib
import karrio.core.units as units
import karrio.server.conf as conf
import karrio.server.core.utils as utils
import karrio.server.core.gateway as gateway
from karrio.server.core.utils import create_carrier_snapshot, resolve_carrier
import karrio.server.core.dataunits as dataunits
import karrio.server.core.datatypes as datatypes
import karrio.server.core.exceptions as exceptions
import karrio.server.providers.models as providers
import karrio.server.core.validators as validators
from karrio.server.core.logging import logger
from karrio.server.serializers import (
    Serializer,
    CharField,
    ChoiceField,
    BooleanField,
    owned_model_serializer,
    link_org,
    Context,
    PlainDictField,
    StringListField,
    process_json_object_mutation,
    process_json_array_mutation,
    process_customs_mutation,
)
from karrio.server.core.serializers import (
    SHIPMENT_STATUS,
    LABEL_TYPES,
    ShipmentCancelRequest,
    ShippingDocument,
    ShipmentDetails,
    ShipmentStatus,
    TrackerStatus,
    ShipmentData,
    Documents,
    Shipment,
    Payment,
    Message,
    Rate,
    Parcel,
)
from karrio.server.manager.serializers.document import DocumentUploadSerializer
from karrio.server.manager.serializers.rate import RateSerializer
import karrio.server.manager.models as models

DEFAULT_CARRIER_FILTER: typing.Any = dict(active=True, capability="shipping")


@owned_model_serializer
class ShipmentSerializer(ShipmentData):
    status = ChoiceField(required=False, choices=SHIPMENT_STATUS)
    selected_rate_id = CharField(required=False)
    rates = Rate(many=True, required=False)
    label = CharField(required=False, allow_blank=True, allow_null=True)
    tracking_number = CharField(required=False, allow_blank=True, allow_null=True)
    shipment_identifier = CharField(required=False, allow_blank=True, allow_null=True)
    selected_rate = Rate(required=False, allow_null=True)
    tracking_url = CharField(required=False, allow_blank=True, allow_null=True)
    test_mode = BooleanField(required=False)
    docs = Documents(required=False)
    meta = PlainDictField(required=False, allow_null=True)
    messages = Message(many=True, required=False, default=[])
    # Override parcels to use Parcel (with id) instead of ParcelData (without id)
    parcels = Parcel(many=True, allow_empty=False, help_text="The shipment's parcels")

    @transaction.atomic
    def create(
        self, validated_data: dict, context: Context, **kwargs
    ) -> models.Shipment:
        # fmt: off
        # Apply shipping method if specified (HIGHEST PRIORITY - supersedes service)
        apply_shipping_method_flag, validated_data = resolve_shipping_method(
            validated_data, context
        )
        options = validated_data.get("options") or {}

        service = validated_data.get("service")
        carrier_ids = validated_data.get("carrier_ids") or []
        fetch_rates = validated_data.get("fetch_rates") is not False
        services = [service] if service is not None else validated_data.get("services")

        # Check if we should skip rate fetching for has_alternative_services
        skip_rate_fetching, resolved_carrier_name, _ = (
            resolve_alternative_service_carrier(
                service=service,
                carrier_ids=carrier_ids,
                carriers=[],  # Pre-check before loading carriers
                options=options,
                context=context,
            )
        )

        carriers = gateway.Connections.list(
            context=context,
            carrier_ids=carrier_ids,
            **({"carrier_name": resolved_carrier_name} if resolved_carrier_name else {}),
            **({"services": services} if any(services) and not skip_rate_fetching else {}),
            **{"raise_not_found": True, **DEFAULT_CARRIER_FILTER},
        )
        payment = validated_data.get("payment") or lib.to_dict(
            datatypes.Payment(currency=options.get("currency"))
        )
        rating_data = {
            **validated_data,
            **({"services": services} if any(services) else {}),
        }
        rates = validated_data.get("rates") or []
        messages = validated_data.get("messages") or []
        apply_shipping_rules = lib.identity(
            getattr(conf.settings, "SHIPPING_RULES", False)
            and options.get("apply_shipping_rules", False)
        )

        # Get live rates (skip if has_alternative_services is enabled)
        if (fetch_rates or apply_shipping_rules) and not skip_rate_fetching:
            rate_response: datatypes.RateResponse = (
                RateSerializer.map(data=rating_data, context=context)
                .save(carriers=carriers)
                .instance
            )
            rates = lib.to_dict(rate_response.rates)
            messages = lib.to_dict(rate_response.messages)

        # Create synthetic rate when skipping rate fetching
        if skip_rate_fetching:
            _, _, rates = resolve_alternative_service_carrier(
                service=service,
                carrier_ids=carrier_ids,
                carriers=carriers,
                options=options,
                context=context,
            )

        # Process JSON fields for addresses, parcels, and customs
        json_fields = {}

        if "shipper" in validated_data:
            json_fields.update(shipper=process_json_object_mutation(
                "shipper", validated_data, None,
                model_class=models.Address, object_type="address", id_prefix="adr",
            ))

        if "recipient" in validated_data:
            json_fields.update(recipient=process_json_object_mutation(
                "recipient", validated_data, None,
                model_class=models.Address, object_type="address", id_prefix="adr",
            ))

        if "return_address" in validated_data:
            json_fields.update(return_address=process_json_object_mutation(
                "return_address", validated_data, None,
                model_class=models.Address, object_type="address", id_prefix="adr",
            ))

        if "billing_address" in validated_data:
            json_fields.update(billing_address=process_json_object_mutation(
                "billing_address", validated_data, None,
                model_class=models.Address, object_type="address", id_prefix="adr",
            ))

        json_fields.update(parcels=process_json_array_mutation(
            "parcels", validated_data, None,
            id_prefix="pcl", model_class=models.Parcel,
            nested_arrays={"items": ("itm", models.Commodity)},
            object_type="parcel", data_field_name="parcels",
        ))

        if "customs" in validated_data:
            json_fields.update(customs=process_customs_mutation(
                validated_data, None,
                address_model=models.Address, product_model=models.Commodity,
            ))

        shipment = models.Shipment.objects.create(
            **{
                **{
                    key: value
                    for key, value in validated_data.items()
                    if key in models.Shipment.DIRECT_PROPS and value is not None
                },
                **json_fields,
                "rates": rates,
                "payment": payment,
                "services": services,
                "messages": messages,
                "test_mode": context.test_mode,
            }
        )

        # carriers M2M removed - carrier info now in selected_rate JSON

        # Buy label if preferred service is selected, shipping method applied, shipping rules applied, or skip rate fetching
        if (service and fetch_rates) or apply_shipping_method_flag or apply_shipping_rules or skip_rate_fetching:
            from karrio.server.tracing.utils import set_tracing_context
            set_tracing_context(object_id=shipment.id)
            return buy_shipment_label(
                shipment,
                context=context,
                service=service,
            )
        # fmt: on
        return shipment

    @transaction.atomic
    def update(
        self, instance: models.Shipment, validated_data: dict, context: Context
    ) -> models.Shipment:
        changes = []
        data = validated_data.copy()
        carriers = validated_data.get("carriers") or []

        for key, val in data.items():
            if key in models.Shipment.DIRECT_PROPS and getattr(instance, key) != val:
                setattr(instance, key, val)
                changes.append(key)
                validated_data.pop(key)

            # Note: RELATIONAL_PROPS handling removed - FK relationships converted to JSONFields

        if "shipper" in data:
            instance.shipper = process_json_object_mutation(
                "shipper",
                data,
                instance,
                model_class=models.Address,
                object_type="address",
                id_prefix="adr",
            )
            changes.append("shipper")

        if "recipient" in data:
            instance.recipient = process_json_object_mutation(
                "recipient",
                data,
                instance,
                model_class=models.Address,
                object_type="address",
                id_prefix="adr",
            )
            changes.append("recipient")

        if "return_address" in data:
            instance.return_address = process_json_object_mutation(
                "return_address",
                data,
                instance,
                model_class=models.Address,
                object_type="address",
                id_prefix="adr",
            )
            changes.append("return_address")

        if "billing_address" in data:
            instance.billing_address = process_json_object_mutation(
                "billing_address",
                data,
                instance,
                model_class=models.Address,
                object_type="address",
                id_prefix="adr",
            )
            changes.append("billing_address")

        if "parcels" in data:
            instance.parcels = process_json_array_mutation(
                "parcels",
                data,
                instance,
                id_prefix="pcl",
                model_class=models.Parcel,
                nested_arrays={"items": ("itm", models.Commodity)},
                object_type="parcel",
                data_field_name="parcels",
            )
            changes.append("parcels")

        if "customs" in data:
            instance.customs = process_customs_mutation(
                data,
                instance,
                address_model=models.Address,
                product_model=models.Commodity,
            )
            changes.append("customs")

        if "docs" in validated_data:
            changes.append("label")
            changes.append("invoice")
            changes.append("extra_documents")
            instance.label = validated_data["docs"].get("label") or instance.label
            instance.invoice = validated_data["docs"].get("invoice") or instance.invoice
            instance.extra_documents = (
                validated_data["docs"].get("extra_documents")
                or instance.extra_documents
                or []
            )

        if "selected_rate" in validated_data:
            selected_rate = validated_data.get("selected_rate", {})
            # Try to find carrier for connection metadata
            carrier = providers.CarrierConnection.objects.filter(
                carrier_id=selected_rate.get("carrier_id")
            ).first()
            instance.test_mode = selected_rate.get("test_mode", instance.test_mode)

            # Store carrier snapshot in dedicated field (consistent with Tracking, Pickup, etc.)
            if carrier:
                instance.carrier = create_carrier_snapshot(carrier)
                changes += ["carrier"]

            instance.selected_rate = selected_rate
            changes += ["selected_rate"]

        if any(changes):
            instance.save(update_fields=changes)

        # carriers M2M removed - carrier info now in selected_rate JSON

        return instance


class ShipmentPurchaseData(Serializer):
    selected_rate_id = CharField(
        required=False,
        allow_null=True,
        help_text="The shipment selected rate.",
    )
    service = CharField(
        required=False,
        allow_null=True,
        help_text="The carrier service to use for the shipment (alternative to selected_rate_id).",
    )
    label_type = ChoiceField(
        required=False,
        choices=LABEL_TYPES,
        default=units.LabelType.PDF.name,
        help_text="The shipment label file type.",
    )
    payment = Payment(required=False, help_text="The payment details")
    reference = CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment reference",
    )
    metadata = PlainDictField(
        required=False, help_text="User metadata for the shipment"
    )

    def validate(self, data):
        if not data.get("selected_rate_id") and not data.get("service"):
            raise exceptions.APIException(
                "Either 'selected_rate_id' or 'service' must be provided.",
                code="validation_error",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return data


class ShipmentUpdateData(validators.OptionDefaultSerializer):
    label_type = ChoiceField(
        required=False,
        choices=LABEL_TYPES,
        default=units.LabelType.PDF.name,
        help_text="The shipment label file type.",
    )
    payment = Payment(required=False, help_text="The payment details")
    options = PlainDictField(
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
            "shipping_charges": 10.00,
            "is_return": true,
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
    reference = CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment reference",
    )
    metadata = PlainDictField(
        required=False, help_text="User metadata for the shipment"
    )


class ShipmentRateData(validators.OptionDefaultSerializer):
    services = StringListField(
        required=False,
        allow_null=True,
        help_text="""The requested carrier service for the shipment.<br/>
        Please consult [the reference](#operation/references) for specific carriers services.<br/>
        **Note that this is a list because on a Multi-carrier rate request you could
        specify a service per carrier.**
        """,
    )
    carrier_ids = StringListField(
        required=False,
        allow_null=True,
        help_text="""The list of configured carriers you wish to get rates from.<br/>
        **Note that the request will be sent to all carriers in nothing is specified**
        """,
    )
    options = PlainDictField(
        required=False,
        default={},
        help_text="""<details>
        <summary>The options available for the shipment.</summary>

        {
            "currency": "USD",
            "insurance": 100.00,
            "insured_by": "carrier",
            "cash_on_delivery": 30.00,
            "dangerous_good": true,
            "declared_value": 150.00,
            "sms_notification": true,
            "email_notification": true,
            "email_notification_to": "shipper@mail.com",
            "hold_at_location": true,
            "locker_id": "123456789",
            "paperless_trade": true,
            "preferred_service": "fedex_express_saver",
            "shipment_date": "2020-01-01",  # TODO: deprecate
            "shipping_date": "2020-01-01T00:00",
            "shipment_note": "This is a shipment note",
            "signature_confirmation": true,
            "saturday_delivery": true,
            "shipping_charges": 10.00,
            "is_return": true,
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
    reference = CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The shipment reference",
    )
    metadata = PlainDictField(
        required=False, help_text="User metadata for the shipment"
    )


@owned_model_serializer
class ShipmentPurchaseSerializer(Shipment):
    rates = Rate(many=True, required=True)
    payment = Payment(required=True)
    options = PlainDictField(
        required=False,
        default={},
        help_text="""<details>
        <summary>The options available for the shipment.</summary>

        {
            "currency": "USD",
            "insurance": 100.00,
            "insured_by": "carrier",
            "cash_on_delivery": 30.00,
            "dangerous_good": true,
            "declared_value": 150.00,
            "sms_notification": true,
            "email_notification": true,
            "email_notification_to": "shipper@mail.com",
            "hold_at_location": true,
            "locker_id": "123456789",
            "paperless_trade": true,
            "preferred_service": "fedex_express_saver",
            "shipment_date": "2020-01-01",  # TODO: deprecate
            "shipping_date": "2020-01-01T00:00",
            "shipment_note": "This is a shipment note",
            "signature_confirmation": true,
            "saturday_delivery": true,
            "shipping_charges": 10.00,
            "is_return": true,
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
    reference = CharField(required=False, allow_blank=True, allow_null=True)

    def create(self, validated_data: dict, **kwargs) -> datatypes.Shipment:
        return gateway.Shipments.create(
            Shipment(validated_data).data,
            carrier=validated_data.get("carrier"),
            selected_rate=kwargs.get("selected_rate"),
            resolve_tracking_url=lib.identity(
                lambda tracking_number, carrier_name: reverse(
                    "karrio.server.manager:shipment-tracker",
                    kwargs=dict(
                        tracking_number=tracking_number, carrier_name=carrier_name
                    ),
                )
            ),
            **kwargs,
        )


class ShipmentCancelSerializer(Shipment):
    def update(
        self, instance: models.Shipment, validated_data: dict, context=None, **kwargs
    ) -> datatypes.ConfirmationResponse:
        if instance.status == ShipmentStatus.purchased.value:
            # Resolve carrier from carrier snapshot
            carrier = resolve_carrier(instance.carrier or {}, context)
            gateway.Shipments.cancel(
                payload={
                    **ShipmentCancelRequest(instance).data,
                    "options": {
                        **instance.options,
                        **instance.meta,
                        **(validated_data.get("options") or {}),
                    },
                },
                carrier=carrier,
            )

        instance.status = ShipmentStatus.cancelled.value
        instance.save(update_fields=["status"])
        remove_shipment_tracker(instance)

        return instance


@validators.shipment_documents_accessor(include_base64=True)
class PurchasedShipment(Shipment):
    shipping_documents = ShippingDocument(
        required=False,
        many=True,
        default=[],
        help_text="The list of shipping documents",
    )


def fetch_shipment_rates(
    shipment: models.Shipment,
    context: typing.Any,
    data: dict = dict(),
) -> models.Shipment:
    # carrier_ids can be passed in data, or default to empty list (query all carriers)
    carrier_ids = data.get("carrier_ids", [])

    carriers = gateway.Connections.list(
        active=True,
        capability="shipping",
        context=context,
        carrier_ids=carrier_ids,
    )

    rate_response: datatypes.RateResponse = (
        RateSerializer.map(
            context=context, data={**ShipmentData(shipment).data, **data}
        )
        .save(carriers=carriers)
        .instance
    )

    updated_shipment = (
        ShipmentSerializer.map(
            shipment,
            context=context,
            data={
                "rates": Rate(rate_response.rates, many=True).data,
                "messages": lib.to_dict(rate_response.messages),
                **data,
            },
        )
        .save(carriers=carriers)
        .instance
    )

    return updated_shipment


@utils.require_selected_rate
def buy_shipment_label(
    shipment: models.Shipment,
    context: typing.Any = None,
    data: dict = dict(),
    selected_rate: typing.Union[dict, datatypes.Rate] = None,
    **kwargs,
) -> models.Shipment:
    extra: dict = {}
    invoice: dict = {}
    selected_rate = lib.to_dict(selected_rate or {})
    invoice_template = shipment.options.get("invoice_template")

    payload = {**data, "selected_rate_id": selected_rate.get("id")}
    carrier = gateway.Connections.first(
        carrier_id=selected_rate.get("carrier_id"),
        test_mode=selected_rate.get("test_mode"),
        context=context,
    )

    is_paperless_trade = lib.identity(
        "paperless" in carrier.capabilities
        and shipment.options.get("paperless_trade") == True
    )
    pre_purchase_generation = invoice_template is not None and is_paperless_trade

    # Generate invoice in advance if is_paperless_trade
    if pre_purchase_generation:
        # Set carrier snapshot on shipment (consistent with other models)
        shipment.carrier = create_carrier_snapshot(carrier)
        shipment.selected_rate = selected_rate
        document = generate_custom_invoice(invoice_template, shipment)
        invoice = dict(invoice=document["doc_file"])

        # Handle Paperless flow per carrier

        if carrier.carrier_name == "ups":
            # TODO:: Check support for dedicated document upload before upload...
            upload = upload_customs_forms(shipment, document, context=context)
            extra.update(
                options={**shipment.options, **dict(doc_references=upload.documents)},
            )
        else:
            extra.update(
                options={**shipment.options, **dict(doc_files=[document])},
            )

    # Submit shipment to carriers
    response: Shipment = lib.identity(
        ShipmentPurchaseSerializer.map(
            context=context,
            data={**Shipment(shipment).data, **payload, **extra},
        )
        .save(carrier=carrier, selected_rate=selected_rate, **kwargs)
        .instance
    )

    # Merge response parcel data with existing parcel data to preserve all fields (weight, etc.)
    existing_parcels = shipment.parcels or []
    merged_parcels = []
    for idx, response_parcel in enumerate(response.parcels):
        existing_parcel = existing_parcels[idx] if idx < len(existing_parcels) else {}
        merged_parcels.append(
            {
                **existing_parcel,  # Keep existing data (weight, weight_unit, etc.)
                "id": response_parcel.id or existing_parcel.get("id"),
                "reference_number": response_parcel.reference_number
                or existing_parcel.get("reference_number"),
            }
        )

    extra.update(
        parcels=merged_parcels,
        docs={**lib.to_dict(response.docs), **invoice},
    )

    # Update shipment state - preserve original meta and merge with response meta
    response_details = ShipmentDetails(response).data
    merged_meta = {
        **(shipment.meta or {}),
        **(response_details.get("meta") or {}),
        **(
            {"rule_activity": kwargs.get("rule_activity")}
            if kwargs.get("rule_activity")
            else {}
        ),
    }

    # Set selected_rate with carrier snapshot directly on shipment before update
    # (This is more reliable than depending on serializer validation)
    # Set carrier snapshot on shipment (consistent with other models)
    shipment.carrier = create_carrier_snapshot(carrier)
    shipment.selected_rate = selected_rate
    shipment.save(update_fields=["carrier", "selected_rate"])

    purchased_shipment = lib.identity(
        ShipmentSerializer.map(
            shipment,
            context=context,
            data={
                **payload,
                **response_details,
                **extra,
                "meta": merged_meta,
            },
        )
        .save()
        .instance
    )

    utils.failsafe(
        lambda: (
            create_shipment_tracker(purchased_shipment, context=context),
            (
                None
                if pre_purchase_generation
                else generate_custom_invoice(invoice_template, purchased_shipment)
            ),
        )
    )

    return purchased_shipment


def reset_related_shipment_rates(shipment: typing.Optional[models.Shipment]):
    if shipment is not None:
        changes = []

        if shipment.selected_rate is not None:
            changes += ["selected_rate"]
            shipment.selected_rate = None

        if len(shipment.rates or []) > 0:
            changes += ["rates"]
            shipment.rates = []

        if len(shipment.messages or []) > 0:
            changes += ["messages"]
            shipment.messages = []

        if any(changes):
            shipment.save(update_fields=changes)


def can_mutate_shipment(
    shipment: models.Shipment,
    update: bool = False,
    delete: bool = False,
    purchase: bool = False,
    payload: dict = None,
):
    if update and [*(payload or {}).keys()] == ["metadata"]:
        return

    if purchase and shipment.status == ShipmentStatus.purchased.value:
        raise exceptions.APIException(
            f"The shipment is '{shipment.status}' and cannot be purchased again",
            code="state_error",
            status_code=status.HTTP_409_CONFLICT,
        )

    if update and shipment.status != ShipmentStatus.draft.value:
        raise exceptions.APIException(
            f"Shipment is {shipment.status} and cannot be updated anymore...",
            code="state_error",
            status_code=status.HTTP_409_CONFLICT,
        )

    if delete and shipment.status not in [
        ShipmentStatus.purchased.value,
        ShipmentStatus.draft.value,
    ]:
        raise exceptions.APIException(
            f"The shipment is '{shipment.status}' and can not be cancelled anymore...",
            code="state_error",
            status_code=status.HTTP_409_CONFLICT,
        )

    if delete and shipment.shipment_pickup.exists():
        raise exceptions.APIException(
            (
                f"This shipment is scheduled for pickup '{shipment.shipment_pickup.first().pk}' "
                "Please cancel this shipment pickup before."
            ),
            code="state_error",
            status_code=status.HTTP_409_CONFLICT,
        )


def compute_estimated_delivery(
    selected_rate: typing.Optional[dict],
    options: typing.Optional[dict],
) -> typing.Tuple[typing.Optional[str], typing.Optional[str]]:
    """Compute estimated delivery date from rate and shipment options.

    This function extracts the estimated delivery date from the selected rate,
    or computes it from transit days and shipping date if not directly available.

    Args:
        selected_rate: The selected shipping rate dictionary
        options: The shipment options dictionary

    Returns:
        A tuple of (estimated_delivery, shipping_date_str) where:
        - estimated_delivery: The estimated delivery date string (YYYY-MM-DD format) or None
        - shipping_date_str: The shipping date string from options or None
    """
    _rate = selected_rate or {}
    _options = options or {}

    shipping_date_str = _options.get("shipping_date") or _options.get("shipment_date")
    estimated_delivery = _rate.get("estimated_delivery")
    transit_days = _rate.get("transit_days")

    if not estimated_delivery and transit_days and shipping_date_str:
        shipping_date = lib.to_date(
            shipping_date_str,
            current_format="%Y-%m-%dT%H:%M",
            try_formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S"],
        )
        if shipping_date:
            estimated_date = shipping_date + datetime.timedelta(days=int(transit_days))
            estimated_delivery = lib.fdate(estimated_date)

    return estimated_delivery, shipping_date_str


def remove_shipment_tracker(shipment: models.Shipment):
    if hasattr(shipment, "shipment_tracker"):
        shipment.shipment_tracker.delete()


def create_shipment_tracker(shipment: typing.Optional[models.Shipment], context):
    rate_provider = (shipment.meta or {}).get("rate_provider") or shipment.carrier_name
    # Resolve carrier from carrier snapshot
    carrier_snapshot = shipment.carrier or {}
    carrier = resolve_carrier(carrier_snapshot, context)

    # Get rate provider carrier if supported instead of carrier account
    if (
        rate_provider != shipment.carrier_name
    ) and rate_provider in dataunits.CARRIER_NAMES:
        carrier = (
            providers.CarrierConnection.access_by(context)
            .filter(carrier_code=rate_provider)
            .first()
        )

    # Handle hub extension tracking - resolve from snapshot if carrier is None
    if carrier and carrier.gateway.is_hub:
        # Keep the hub carrier
        pass
    elif carrier is None and carrier_snapshot:
        # Try to resolve again if carrier is None
        carrier = resolve_carrier(carrier_snapshot, context)

    # Get dhl universal account if a dhl integration doesn't support tracking API
    if (
        carrier
        and "dhl" in carrier.carrier_name
        and "get_tracking" not in carrier.gateway.proxy_methods
    ):
        carrier = gateway.Connections.first(
            carrier_name="dhl_universal",
            context=context,
        )

    if carrier is not None and "get_tracking" in carrier.gateway.proxy_methods:
        # Create shipment tracker
        try:
            # Use JSON fields for data access
            parcels = shipment.parcels or []
            shipper = shipment.shipper or {}
            recipient = shipment.recipient or {}

            pkg_weight = sum([p.get("weight") or 0.0 for p in parcels], 0.0)
            estimated_delivery, shipping_date_str = compute_estimated_delivery(
                shipment.selected_rate, shipment.options
            )

            tracker = models.Tracking.objects.create(
                tracking_number=shipment.tracking_number,
                delivered=False,
                shipment=shipment,
                carrier=create_carrier_snapshot(carrier),
                test_mode=carrier.test_mode,
                created_by=shipment.created_by,
                status=TrackerStatus.pending.value,
                estimated_delivery=estimated_delivery,
                events=utils.default_tracking_event(event_at=shipment.updated_at),
                options={shipment.tracking_number: dict(carrier=rate_provider)},
                meta=dict(carrier=rate_provider),
                info=dict(
                    source="api",
                    shipment_weight=str(pkg_weight),
                    shipment_package_count=str(len(parcels)),
                    customer_name=recipient.get("person_name"),
                    shipment_origin_country=shipper.get("country_code"),
                    shipment_origin_postal_code=shipper.get("postal_code"),
                    shipment_destination_country=recipient.get("country_code"),
                    shipment_destination_postal_code=recipient.get("postal_code"),
                    shipment_service=shipment.meta.get("service_name"),
                    shipping_date=shipping_date_str,
                    expected_delivery=estimated_delivery,
                    carrier_tracking_link=utils.get_carrier_tracking_link(
                        carrier, shipment.tracking_number
                    ),
                ),
            )
            tracker.save()
            link_org(tracker, context)
            logger.info(
                "Successfully added a tracker to the shipment", shipment_id=shipment.id
            )
        except Exception as e:
            logger.exception(
                "Failed to create new label tracker",
                error=str(e),
                shipment_id=shipment.id,
            )

        # Update shipment tracking url if different from the current one
        try:
            url = reverse(
                "karrio.server.manager:shipment-tracker",
                kwargs=dict(
                    tracking_number=shipment.tracking_number,
                    carrier_name=(
                        rate_provider
                        if carrier.gateway.is_hub
                        else carrier.carrier_name
                    ),
                ),
            )
            tracking_url = utils.app_tracking_query_params(url, carrier)

            if tracking_url != shipment.tracking_url:
                shipment.tracking_url = tracking_url
                shipment.save(update_fields=["tracking_url"])
        except Exception as e:
            logger.exception(
                "Failed to update shipment tracking url",
                error=str(e),
                shipment_id=shipment.id,
                tracking_number=shipment.tracking_number,
            )


def generate_custom_invoice(template: str, shipment: models.Shipment, **kwargs):
    """This function generates a custom invoice using Karrio's
    document generation service. And dispatch a document upload if
    paperless trade is supported.
    """
    # Skip document generation if not template is provided
    if any(template or "") is False:
        return

    # Check if carrier and shipment support ETD and document url is provided
    if conf.settings.DOCUMENTS_MANAGEMENT is False:
        logger.info("Document generation not supported", documents_management=False)
        return

    # generate invoice document
    import karrio.server.documents.generator as generator

    document = generator.Documents.generate_shipment_document(
        template, shipment, **kwargs
    )

    if getattr(shipment, "tracking_number", None) is not None:
        shipment.invoice = document["doc_file"]
        shipment.save(update_fields=["invoice"])

    logger.info(
        "Custom document successfully generated",
        shipment_id=shipment.id,
        template=template,
    )

    return document


def upload_customs_forms(shipment: models.Shipment, document: dict, context=None):
    return (
        DocumentUploadSerializer.map(
            getattr(shipment, "shipment_upload_record", None),
            data=dict(
                document_files=[document],
                shipment_id=shipment.id,
                reference=shipment.id,
            ),
            context=context,
        )
        .save(shipment=shipment)
        .instance
    )


def resolve_alternative_service_carrier(
    service: str,
    carrier_ids: list,
    carriers: list,
    options: dict,
    context: Context,
) -> typing.Tuple[bool, typing.Optional[str], typing.List[dict]]:
    """
    Resolve carrier and create synthetic rate for has_alternative_services flow.

    When has_alternative_services=True and a service is specified, this function:
    1. Determines if rate fetching should be skipped
    2. Resolves the carrier from the service name
    3. Creates a synthetic rate for direct label purchase

    Returns:
        Tuple of (skip_rate_fetching, resolved_carrier_name, synthetic_rates)
    """
    has_alternative_services = options.get("has_alternative_services", False)
    skip_rate_fetching = service is not None and has_alternative_services

    if not skip_rate_fetching:
        return False, None, []

    # Resolve carrier from service when no explicit carrier_ids provided
    resolved_carrier_name = None
    if not any(carrier_ids):
        resolved_carrier_name = utils._get_carrier_for_service(service, context=context)
        if resolved_carrier_name is None:
            raise exceptions.APIException(
                f"Could not resolve carrier for service '{service}'",
                code="validation_error",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    if len(carriers) == 0:
        return skip_rate_fetching, resolved_carrier_name, []

    # Find carrier connection matching the service's carrier
    carrier_name = resolved_carrier_name or utils._get_carrier_for_service(
        service, context=context
    )
    carrier = lib.identity(
        next(
            (c for c in carriers if c.carrier_name == carrier_name),
            carriers[0] if carrier_name is None else None,
        )
    )

    if carrier is None:
        raise exceptions.APIException(
            f"No carrier connection found for service '{service}'",
            code="validation_error",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # Create synthetic rate for direct label purchase
    synthetic_rates = [
        {
            "id": f"rat_{uuid.uuid4().hex}",
            "carrier_id": carrier.carrier_id,
            "carrier_name": carrier.carrier_name,
            "service": service,
            "currency": options.get("currency") or "USD",
            "total_charge": 0,
            "meta": {
                "carrier_connection_id": carrier.pk,
                "has_alternative_services": True,
                "rate_provider": carrier.carrier_name,
                "service_name": service.upper().replace("_", " "),
            },
            "test_mode": context.test_mode,
        }
    ]

    return skip_rate_fetching, resolved_carrier_name, synthetic_rates


def resolve_shipping_method(
    validated_data: dict,
    context: Context,
) -> typing.Tuple[bool, dict]:
    """
    Resolve and apply shipping method configuration if specified.

    When options.shipping_method is provided, this function:
    1. Validates the SHIPPING_METHODS feature is enabled
    2. Loads and applies the shipping method configuration

    Returns:
        Tuple of (apply_shipping_method_flag, modified_validated_data)
    """
    if not getattr(conf.settings, "SHIPPING_METHODS", False):
        options = validated_data.get("options") or {}
        shipping_method_id = options.get("shipping_method")

        if shipping_method_id is not None:
            raise exceptions.APIException(
                "Shipping methods feature is not enabled.",
                code="feature_disabled",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return False, validated_data

    options = validated_data.get("options") or {}
    shipping_method_id = options.get("shipping_method")

    if shipping_method_id is None:
        return False, validated_data

    modified_data = utils.load_and_apply_shipping_method(
        validated_data, shipping_method_id, context
    )

    return True, modified_data
