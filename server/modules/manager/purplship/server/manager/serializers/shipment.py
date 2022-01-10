import logging
from typing import Optional, Any
from django.db import transaction
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.serializers import Serializer, CharField, ChoiceField, BooleanField

from purplship.core.utils import DP, DF
from purplship.server.core.gateway import Shipments, Carriers
from purplship.server.core.exceptions import PurplshipAPIException
from purplship.server.serializers import (
    SerializerDecorator,
    owned_model_serializer,
    save_one_to_one_data,
    save_many_to_many_data,
    link_org,
)
import purplship.server.core.datatypes as datatypes
from purplship.server.providers.models import Carrier, MODELS
from purplship.server.core.serializers import (
    SHIPMENT_STATUS,
    ShipmentStatus,
    ShipmentData,
    Shipment,
    Payment,
    Rate,
    ShippingRequest,
    ShipmentCancelRequest,
    LABEL_TYPES,
    LabelType,
    Message,
    PlainDictField,
    StringListField,
    TrackerStatus,
)
from purplship.server.manager.serializers.address import AddressSerializer
from purplship.server.manager.serializers.customs import CustomsSerializer
from purplship.server.manager.serializers.parcel import ParcelSerializer
from purplship.server.manager.serializers.rate import RateSerializer
import purplship.server.manager.models as models

logger = logging.getLogger(__name__)
DEFAULT_CARRIER_FILTER: Any = dict(active=True, capability="shipping")


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
    meta = PlainDictField(required=False, allow_null=True)
    messages = Message(many=True, required=False, default=[])

    @transaction.atomic
    def create(self, validated_data: dict, context: dict, **kwargs) -> models.Shipment:
        carrier_filter = validated_data.get("carrier_filter") or {}
        carrier_ids = validated_data.get("carrier_ids") or []
        carriers = Carriers.list(
            context=context,
            carrier_ids=carrier_ids,
            **{"raise_not_found": True, **DEFAULT_CARRIER_FILTER, **carrier_filter},
        )
        payment = validated_data.get("payment") or DP.to_dict(
            datatypes.Payment(
                currency=(validated_data.get("options") or {}).get("currency")
            )
        )

        # Get live rates
        rate_response: datatypes.RateResponse = (
            SerializerDecorator[RateSerializer](data=validated_data, context=context)
            .save(carriers=carriers)
            .instance
        )

        shipment_data = {
            **{
                key: value
                for key, value in validated_data.items()
                if key in models.Shipment.DIRECT_PROPS and value is not None
            },
            "customs": save_one_to_one_data(
                "customs", CustomsSerializer, payload=validated_data, context=context
            ),
            "shipper": save_one_to_one_data(
                "shipper", AddressSerializer, payload=validated_data, context=context
            ),
            "recipient": save_one_to_one_data(
                "recipient", AddressSerializer, payload=validated_data, context=context
            ),
        }

        shipment = models.Shipment.objects.create(
            **{
                **shipment_data,
                "payment": payment,
                "rates": DP.to_dict(rate_response.rates),
                "messages": DP.to_dict(rate_response.messages),
                "test_mode": all([r.test_mode for r in rate_response.rates]),
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

        return shipment

    @transaction.atomic
    def update(
        self, instance: models.Shipment, validated_data: dict, context: dict
    ) -> models.Shipment:
        changes = []
        data = validated_data.copy()
        carriers = validated_data.get("carriers") or []

        for key, val in data.items():
            if key in models.Shipment.DIRECT_PROPS:
                setattr(instance, key, val)
                changes.append(key)
                validated_data.pop(key)

            if key in models.Shipment.RELATIONAL_PROPS and val is None:
                prop = getattr(instance, key)
                changes.append(key)
                # Delete related data from database if payload set to null
                if hasattr(prop, "delete"):
                    prop.delete()
                    setattr(instance, key, None)
                    validated_data.pop(key)

        if validated_data.get("customs") is not None:
            changes.append("customs")
            save_one_to_one_data(
                "customs",
                CustomsSerializer,
                instance,
                payload=validated_data,
                context=context,
            )

        if "selected_rate" in validated_data:
            selected_rate = validated_data.get("selected_rate", {})
            carrier = Carrier.objects.filter(
                carrier_id=selected_rate.get("carrier_id")
            ).first()
            instance.test_mode = selected_rate.get("test_mode", instance.test_mode)

            instance.selected_rate = {
                **selected_rate,
                **({"carrier_ref": carrier.id} if carrier is not None else {}),
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
        default=LabelType.PDF.name,
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
        default=LabelType.PDF.name,
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
        "email_notification_to": shipper@mail.com,
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
        return Shipments.create(
            ShippingRequest(validated_data).data,
            resolve_tracking_url=(
                lambda tracking_number, carrier_name: reverse(
                    "purplship.server.manager:shipment-tracker",
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
            response = Shipments.cancel(
                payload=ShipmentCancelRequest(instance).data,
                carrier=instance.selected_rate_carrier,
            )
        else:
            response = datatypes.ConfirmationResponse(
                messages=[],
                confirmation=datatypes.Confirmation(
                    operation="Cancel Shipment",
                    carrier_name="None Selected",
                    carrier_id="None Selected",
                    success=True,
                ),
            )

        instance.status = ShipmentStatus.cancelled.value
        instance.save(update_fields=["status"])
        remove_shipment_tracker(instance)

        return response


def reset_related_shipment_rates(shipment: Optional[models.Shipment]):
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
        raise PurplshipAPIException(
            f"The shipment is '{shipment.status}' and cannot be purchased again",
            code="state_error",
            status_code=status.HTTP_409_CONFLICT,
        )

    if update and shipment.status != ShipmentStatus.created.value:
        raise PurplshipAPIException(
            f"Shipment is {shipment.status} and cannot be updated anymore...",
            code="state_error",
            status_code=status.HTTP_409_CONFLICT,
        )

    if delete and shipment.status not in [
        ShipmentStatus.purchased.value,
        ShipmentStatus.created.value,
    ]:
        raise PurplshipAPIException(
            f"The shipment is '{shipment.status}' and can not be cancelled anymore...",
            code="state_error",
            status_code=status.HTTP_409_CONFLICT,
        )

    if delete and shipment.pickup_shipments.exists():
        raise PurplshipAPIException(
            (
                f"This shipment is scheduled for pickup '{shipment.pickup_shipments.first().pk}' "
                "Please cancel this shipment pickup before."
            ),
            code="state_error",
            status_code=status.HTTP_409_CONFLICT,
        )


def remove_shipment_tracker(shipment: models.Shipment):
    if any(shipment.tracker.all()):
        shipment.tracker.all().delete()


def create_shipment_tracker(shipment: Optional[models.Shipment], context):
    rate_provider = (shipment.meta or {}).get("rate_provider") or shipment.carrier_name
    carrier = shipment.selected_rate_carrier

    if (rate_provider != shipment.carrier_name) and rate_provider in MODELS:
        carrier = (
            MODELS[rate_provider]
            .access_by(context)
            .filter(test=shipment.test_mode)
            .first()
        )

    if carrier is not None:
        try:
            tracker = models.Tracking.objects.create(
                tracking_number=shipment.tracking_number,
                events=[
                    DP.to_dict(
                        datatypes.TrackingEvent(
                            date=DF.fdate(shipment.updated_at),
                            description="Label created and ready for shipment",
                            location="",
                            code="CREATED",
                            time=DF.ftime(shipment.updated_at),
                        )
                    )
                ],
                delivered=False,
                status=TrackerStatus.pending.value,
                test_mode=carrier.test,
                tracking_carrier=carrier,
                created_by=shipment.created_by,
                shipment=shipment,
            )
            tracker.save()
            link_org(tracker, context)
            logger.info(f"Successfully added a tracker to the shipment {shipment.id}")
        except Exception as e:
            logger.exception("Failed to create new label tracker", e)
