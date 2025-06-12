import typing
import logging
import rest_framework.status as status
import django.db.transaction as transaction
from rest_framework.reverse import reverse

import karrio.lib as lib
import karrio.core.units as units
import karrio.server.conf as conf
import karrio.server.core.utils as utils
import karrio.server.core.gateway as gateway

import karrio.server.core.dataunits as dataunits
import karrio.server.core.datatypes as datatypes
import karrio.server.core.exceptions as exceptions
import karrio.server.providers.models as providers
import karrio.server.core.validators as validators
from karrio.server.serializers import (
    Serializer,
    CharField,
    ChoiceField,
    BooleanField,
    owned_model_serializer,
    save_one_to_one_data,
    save_many_to_many_data,
    link_org,
    Context,
    PlainDictField,
    StringListField,
)
from karrio.server.core.serializers import (
    SHIPMENT_STATUS,
    LABEL_TYPES,
    ShipmentCancelRequest,
    ShipmentDetails,
    ShipmentStatus,
    TrackerStatus,
    ShipmentData,
    Documents,
    Shipment,
    Payment,
    Message,
    Rate,
)
from karrio.server.manager.serializers.document import DocumentUploadSerializer
from karrio.server.manager.serializers.address import AddressSerializer
from karrio.server.manager.serializers.customs import CustomsSerializer
from karrio.server.manager.serializers.parcel import ParcelSerializer
from karrio.server.manager.serializers.rate import RateSerializer
import karrio.server.manager.models as models

logger = logging.getLogger(__name__)
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

    def __init__(self, instance: models.Shipment = None, **kwargs):
        data = kwargs.get("data") or {}
        context = getattr(self, "__context", None) or kwargs.get("context")
        is_update = instance is not None

        if is_update and ("parcels" in data):
            save_many_to_many_data(
                "parcels",
                ParcelSerializer,
                instance,
                payload=data,
                context=context,
                partial=True,
            )
        if is_update and ("customs" in data):
            instance.customs = save_one_to_one_data(
                "customs",
                CustomsSerializer,
                instance,
                payload=data,
                context=context,
                partial=instance.customs is not None,
            )

        super().__init__(instance, **kwargs)

    @transaction.atomic
    def create(
        self, validated_data: dict, context: Context, **kwargs
    ) -> models.Shipment:
        service = validated_data.get("service")
        carrier_ids = validated_data.get("carrier_ids") or []
        fetch_rates = validated_data.get("fetch_rates") is not False
        services = [service] if service is not None else validated_data.get("services")
        carriers = gateway.Carriers.list(
            context=context,
            carrier_ids=carrier_ids,
            **({"services": services} if any(services) else {}),
            **{"raise_not_found": True, **DEFAULT_CARRIER_FILTER},
        )
        payment = validated_data.get("payment") or lib.to_dict(
            datatypes.Payment(
                currency=(validated_data.get("options") or {}).get("currency")
            )
        )
        rating_data = {
            **validated_data,
            **({"services": services} if any(services) else {}),
        }
        rates = validated_data.get("rates") or []
        messages = validated_data.get("messages") or []
        apply_shipping_rules = lib.identity(
            getattr(conf.settings, "SHIPPING_RULES", False)
            and (validated_data.get("options") or {}).get("apply_shipping_rules", False)
        )

        # Get live rates.
        if fetch_rates or apply_shipping_rules:
            rate_response: datatypes.RateResponse = (
                RateSerializer.map(data=rating_data, context=context)
                .save(carriers=carriers)
                .instance
            )
            rates = lib.to_dict(rate_response.rates)
            messages = lib.to_dict(rate_response.messages)

        shipment = models.Shipment.objects.create(
            **{
                **{
                    key: value
                    for key, value in validated_data.items()
                    if key in models.Shipment.DIRECT_PROPS and value is not None
                },
                "customs": save_one_to_one_data(
                    "customs",
                    CustomsSerializer,
                    payload=validated_data,
                    context=context,
                ),
                "shipper": save_one_to_one_data(
                    "shipper",
                    AddressSerializer,
                    payload=validated_data,
                    context=context,
                ),
                "recipient": save_one_to_one_data(
                    "recipient",
                    AddressSerializer,
                    payload=validated_data,
                    context=context,
                ),
                "return_address": save_one_to_one_data(
                    "return_address",
                    AddressSerializer,
                    payload=validated_data,
                    context=context,
                ),
                "billing_address": save_one_to_one_data(
                    "billing_address",
                    AddressSerializer,
                    payload=validated_data,
                    context=context,
                ),
                "rates": rates,
                "payment": payment,
                "services": services,
                "messages": messages,
                "test_mode": context.test_mode,
            }
        )

        shipment.carriers.set(carriers if any(carrier_ids) else [])

        save_many_to_many_data(
            "parcels",
            ParcelSerializer,
            shipment,
            payload=validated_data,
            context=context,
        )

        # Buy label if preferred service is selected or shipping rules should applied.
        if (service and fetch_rates) or apply_shipping_rules:
            return buy_shipment_label(
                shipment,
                context=context,
                service=service,
            )

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

            if key in models.Shipment.RELATIONAL_PROPS and val is None:
                prop = getattr(instance, key)
                # Delete related data from database if payload set to null
                if hasattr(prop, "delete"):
                    prop.delete(keep_parents=True)
                    setattr(instance, key, None)
                    validated_data.pop(key)

        save_one_to_one_data(
            "shipper",
            AddressSerializer,
            instance,
            payload=validated_data,
            context=context,
        )
        save_one_to_one_data(
            "recipient",
            AddressSerializer,
            instance,
            payload=validated_data,
            context=context,
        )

        if "return_address" in validated_data:
            changes.append("return_address")
            instance.return_address = save_one_to_one_data(
                "return_address",
                AddressSerializer,
                instance,
                payload=validated_data,
                context=context,
            )

        if "billing_address" in validated_data:
            changes.append("billing_address")
            instance.billing_address = save_one_to_one_data(
                "billing_address",
                AddressSerializer,
                instance,
                payload=validated_data,
                context=context,
            )

        if "docs" in validated_data:
            changes.append("label")
            changes.append("invoice")
            instance.label = validated_data["docs"].get("label") or instance.label
            instance.invoice = validated_data["docs"].get("invoice") or instance.invoice

        if "selected_rate" in validated_data:
            selected_rate = validated_data.get("selected_rate", {})
            carrier = providers.Carrier.objects.filter(
                carrier_id=selected_rate.get("carrier_id")
            ).first()
            instance.test_mode = selected_rate.get("test_mode", instance.test_mode)

            instance.selected_rate = {
                **selected_rate,
                "meta": {
                    **selected_rate.get("meta", {}),
                    **(
                        {"carrier_connection_id": carrier.id}
                        if carrier is not None
                        else {}
                    ),
                },
            }
            instance.selected_rate_carrier = carrier
            changes += ["selected_rate", "selected_rate_carrier"]

        if any(changes):
            instance.save(update_fields=changes)

        if "carrier_ids" in validated_data:
            instance.carriers.set(carriers)

        return instance


class ShipmentPurchaseData(Serializer):
    selected_rate_id = CharField(required=True, help_text="The shipment selected rate.")
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
        self, instance: models.Shipment, validated_data: dict, **kwargs
    ) -> datatypes.ConfirmationResponse:
        if instance.status == ShipmentStatus.purchased.value:
            gateway.Shipments.cancel(
                payload={
                    **ShipmentCancelRequest(instance).data,
                    "options": {
                        **instance.options,
                        **instance.meta,
                        **(validated_data.get("options") or {}),
                    },
                },
                carrier=instance.selected_rate_carrier,
            )

        instance.status = ShipmentStatus.cancelled.value
        instance.save(update_fields=["status"])
        remove_shipment_tracker(instance)

        return instance


def fetch_shipment_rates(
    shipment: models.Shipment,
    context: typing.Any,
    data: dict = dict(),
) -> models.Shipment:
    carrier_ids = data["carrier_ids"] if "carrier_ids" in data else shipment.carrier_ids

    carriers = gateway.Carriers.list(
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
    carrier = gateway.Carriers.first(
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
        shipment.selected_rate = selected_rate
        shipment.selected_rate_carrier = carrier
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

    extra.update(
        parcels=[
            dict(id=parcel.id, reference_number=parcel.reference_number)
            for parcel in response.parcels
        ],
        docs={**lib.to_dict(response.docs), **invoice},
    )

    # Update shipment state
    purchased_shipment = lib.identity(
        ShipmentSerializer.map(
            shipment,
            context=context,
            data={
                **payload,
                **ShipmentDetails(response).data,
                **extra,
                # "meta": {**(response.meta or {}), "rule_activity": kwargs.get("rule_activity", None)},
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


def remove_shipment_tracker(shipment: models.Shipment):
    if hasattr(shipment, "shipment_tracker"):
        shipment.shipment_tracker.delete()


def create_shipment_tracker(shipment: typing.Optional[models.Shipment], context):
    rate_provider = (shipment.meta or {}).get("rate_provider") or shipment.carrier_name
    carrier = shipment.selected_rate_carrier

    # Get rate provider carrier if supported instead of carrier account
    if (
        rate_provider != shipment.carrier_name
    ) and rate_provider in dataunits.CARRIER_NAMES:
        carrier = (
            providers.Carrier.access_by(context)
            .filter(carrier_code=rate_provider)
            .first()
        )

    # Handle hub extension tracking
    if shipment.selected_rate_carrier.gateway.is_hub and carrier is None:
        carrier = shipment.selected_rate_carrier

    # Get dhl universal account if a dhl integration doesn't support tracking API
    if (
        carrier
        and "dhl" in carrier.carrier_name
        and "get_tracking" not in carrier.gateway.proxy_methods
    ):
        carrier = gateway.Carriers.first(
            carrier_name="dhl_universal",
            context=context,
        )

    if carrier is not None and "get_tracking" in carrier.gateway.proxy_methods:
        # Create shipment tracker
        try:
            pkg_weight = sum([p.weight or 0.0 for p in shipment.parcels.all()], 0.0)
            tracker = models.Tracking.objects.create(
                tracking_number=shipment.tracking_number,
                delivered=False,
                shipment=shipment,
                tracking_carrier=carrier,
                test_mode=carrier.test_mode,
                created_by=shipment.created_by,
                status=TrackerStatus.pending.value,
                events=utils.default_tracking_event(event_at=shipment.updated_at),
                options={shipment.tracking_number: dict(carrier=rate_provider)},
                meta=dict(carrier=rate_provider),
                info=dict(
                    source="api",
                    shipment_weight=str(pkg_weight),
                    shipment_package_count=str(shipment.parcels.count()),
                    customer_name=shipment.recipient.person_name,
                    shipment_origin_country=shipment.shipper.country_code,
                    shipment_origin_postal_code=shipment.shipper.postal_code,
                    shipment_destination_country=shipment.recipient.country_code,
                    shipment_destination_postal_code=shipment.recipient.postal_code,
                    shipment_service=shipment.meta.get("service_name"),
                    shipping_date=shipment.options.get("shipment_date"),
                    carrier_tracking_link=utils.get_carrier_tracking_link(
                        carrier, shipment.tracking_number
                    ),
                ),
            )
            tracker.save()
            link_org(tracker, context)
            logger.info(f"Successfully added a tracker to the shipment {shipment.id}")
        except Exception as e:
            logger.exception("Failed to create new label tracker", e)

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
            logger.exception("Failed to update shipment tracking url", e)


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
        logger.info("document generation not supported!")
        return

    # generate invoice document
    import karrio.server.documents.generator as generator

    document = generator.Documents.generate_shipment_document(
        template, shipment, **kwargs
    )

    if getattr(shipment, "tracking_number", None) is not None:
        shipment.invoice = document["doc_file"]
        shipment.save(update_fields=["invoice"])

    logger.info("> custom document successfully generated.")

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
