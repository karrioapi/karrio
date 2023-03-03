import typing
import logging
import django.db.transaction as transaction
import rest_framework.status as status
from rest_framework.reverse import reverse
from rest_framework.serializers import Serializer, CharField, ChoiceField, BooleanField

import karrio.lib as lib
import karrio.core.units as units
import karrio.server.conf as conf
import karrio.server.core.utils as utils
import karrio.server.core.gateway as gateway
import karrio.server.core.datatypes as datatypes
import karrio.server.core.exceptions as exceptions
import karrio.server.providers.models as providers
from karrio.server.serializers import (
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
    Documents,
    ShipmentStatus,
    ShipmentData,
    Shipment,
    Payment,
    Rate,
    ShipmentCancelRequest,
    LABEL_TYPES,
    Message,
    TrackerStatus,
    ShipmentDetails,
)
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
        if is_update and data.get("customs") is not None:
            instance.customs = save_one_to_one_data(
                "customs",
                CustomsSerializer,
                instance,
                payload=data,
                context=context,
            )

        super().__init__(instance, **kwargs)

    @transaction.atomic
    def create(
        self, validated_data: dict, context: Context, **kwargs
    ) -> models.Shipment:
        fetch_rates = validated_data.get("fetch_rates") is not False
        carrier_ids = validated_data.get("carrier_ids") or []
        service = validated_data.get("service")
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

        # Get live rates.
        if fetch_rates:
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

        # Buy label if preferred service is already selected.
        if service and fetch_rates:
            return buy_shipment_label(
                shipment,
                context,
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
                    prop.delete()
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

        if "customs" in validated_data:
            changes.append("customs")
            instance.customs = save_one_to_one_data(
                "customs",
                CustomsSerializer,
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

        instance.save(update_fields=changes)

        if "carrier_ids" in validated_data:
            instance.carriers.set(carriers)

        return instance


@owned_model_serializer
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


class ShipmentUpdateData(Serializer):
    label_type = ChoiceField(
        required=False,
        choices=LABEL_TYPES,
        default=units.LabelType.PDF.name,
        help_text="The shipment label file type.",
    )
    payment = Payment(required=False, help_text="The payment details")
    options = PlainDictField(
        required=False,
        allow_null=True,
        help_text="""
    <details>
    <summary>The options available for the shipment.</summary>

    ```
    {
        "currency": "USD",
        "insurance": 100.00,
        "cash_on_delivery": 30.00,
        "shipment_date": "2020-01-01",
        "dangerous_good": true,
        "declared_value": 150.00,
        "email_notification": true,
        "email_notification_to": "shipper@mail.com",
        "signature_confirmation": true,
    }
    ```

    Please check the docs for carrier specific options.
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
class ShipmentRateData(Serializer):
    services = StringListField(
        required=False,
        allow_null=True,
        help_text="""
    The requested carrier service for the shipment.

    Please consult [the reference](#operation/references) for specific carriers services.<br/>
    Note that this is a list because on a Multi-carrier rate request you could specify a service per carrier.
    """,
    )
    carrier_ids = StringListField(
        required=False,
        allow_null=True,
        help_text="""
    The list of configured carriers you wish to get rates from.

    *Note that the request will be sent to all carriers in nothing is specified*
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
    reference = CharField(required=False, allow_blank=True, allow_null=True)

    def create(self, validated_data: dict, **kwargs) -> datatypes.Shipment:
        return gateway.Shipments.create(
            Shipment(validated_data).data,
            resolve_tracking_url=(
                lambda tracking_number, carrier_name: reverse(
                    "karrio.server.manager:shipment-tracker",
                    kwargs=dict(
                        tracking_number=tracking_number, carrier_name=carrier_name
                    ),
                )
            ),
        )


class ShipmentCancelSerializer(Shipment):
    def update(
        self, instance: models.Shipment, validated_data: dict, **kwargs
    ) -> datatypes.ConfirmationResponse:
        if instance.status == ShipmentStatus.purchased.value:
            gateway.Shipments.cancel(
                payload=ShipmentCancelRequest(instance).data,
                carrier=instance.selected_rate_carrier,
            )

        instance.status = ShipmentStatus.cancelled.value
        instance.save(update_fields=["status"])
        remove_shipment_tracker(instance)

        return instance


def buy_shipment_label(
    shipment: models.Shipment,
    context: typing.Any,
    data: dict = dict(),
    service: str = None,
) -> models.Shipment:
    extra: dict = {}
    invoice_template = shipment.options.get("invoice_template")
    rate = next(
        (
            rate
            for rate in shipment.rates
            if rate["service"] == service or rate["id"] == data.get("selected_rate_id")
        ),
        None,
    )
    payload = {**data, "selected_rate_id": rate["id"]}
    carrier = gateway.Carriers.first(
        carrier_id=rate["carrier_id"],
        test_mode=rate["test_mode"],
    )

    # Submit shipment to carriers
    response: Shipment = (
        ShipmentPurchaseSerializer.map(
            context=context,
            data={**Shipment(shipment).data, **payload},
        )
        .save(carrier=carrier)
        .instance
    )

    extra.update(
        parcels=[
            dict(id=parcel.id, reference_number=parcel.reference_number)
            for parcel in response.parcels
        ],
    )

    # Update shipment state
    purchased_shipment = (
        ShipmentSerializer.map(
            shipment,
            context=context,
            data={
                **payload,
                **ShipmentDetails(response).data,
                **extra,
            },
        )
        .save()
        .instance
    )

    create_shipment_tracker(purchased_shipment, context=context)
    generate_custom_invoice(invoice_template, purchased_shipment)

    return purchased_shipment


def reset_related_shipment_rates(shipment: typing.Optional[models.Shipment]):
    if shipment is not None:
        shipment.selected_rate = None
        shipment.rates = []
        shipment.messages = []
        shipment.save()


def can_mutate_shipment(
    shipment: models.Shipment,
    update: bool = False,
    delete: bool = False,
    purchase: bool = False,
):
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
    if (rate_provider != shipment.carrier_name) and rate_provider in providers.MODELS:
        carrier = providers.MODELS[rate_provider].access_by(context).first()

    # Handle hub extension tracking
    if shipment.selected_rate_carrier.gateway.is_hub and carrier is None:
        carrier = shipment.selected_rate_carrier

    # Get dhl universal account if a dhl integration doesn't support tracking API
    if (
        carrier
        and "dhl" in carrier.carrier_name
        and "get_tracking" not in carrier.gateway.capabilities
    ):
        carrier = gateway.Carriers.first(
            carrier_name="dhl_universal",
            context=context,
        )

    if carrier is not None and "get_tracking" in carrier.gateway.capabilities:
        # Create shipment tracker
        try:
            tracker = models.Tracking.objects.create(
                tracking_number=shipment.tracking_number,
                events=utils.default_tracking_event(event_at=shipment.updated_at),
                delivered=False,
                status=TrackerStatus.pending.value,
                test_mode=carrier.test_mode,
                tracking_carrier=carrier,
                created_by=shipment.created_by,
                shipment=shipment,
                meta=dict(carrier=rate_provider),
                options={
                    shipment.tracking_number: dict(carrier=rate_provider),
                },
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


def generate_custom_invoice(
    template: str,
    shipment: models.Shipment,
    **kwargs
):
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
    import karrio.server.documents.generator as documents

    document = documents.generate_document(template, shipment)
    shipment.invoice = document["doc_file"]
    shipment.save(update_fields=["invoice"])
    logger.info("> custom document successfully generated.")

    # dispatch paperless invoice upload if supported
    import karrio.server.events.tasks as tasks
    tasks.upload_paperless_document(
        document=document,
        shipment_id=shipment.id,
        schema=conf.settings.schema,
    )
