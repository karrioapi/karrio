import rest_framework.status as status

import karrio.lib as lib
import karrio.server.serializers as serialiazers
import karrio.server.core.exceptions as exceptions
import karrio.server.core.serializers as core
import karrio.server.core.gateway as gateway
import karrio.server.manager.models as models


@serialiazers.owned_model_serializer
class DocumentUploadSerializer(core.DocumentUploadData):
    def create(
        self,
        validated_data: dict,
        context: serialiazers.Context,
        **kwargs,
    ) -> models.DocumentUploadRecord:
        shipment = validated_data.get("shipment")
        carrier = validated_data.get("carrier") or getattr(
            shipment, "selected_rate_carrier", None
        )
        tracking_number = getattr(shipment, "tracking_number", None)
        reference = validated_data.get("reference") or tracking_number
        
        payload = core.DocumentUploadData(validated_data).data
        options = ({
            "origin_country_code": shipment.shipper.country_code,
            "origin_postal_code": shipment.shipper.postal_code,
            "destination_country_code": shipment.recipient.country_code,
            "destination_postal_code": shipment.recipient.postal_code,
            **(payload.get("options") or {})
        } if shipment else payload.get("options"))

        response = gateway.Documents.upload(
            {
                **payload,
                "options": options,
                "reference": reference,
                "tracking_number": tracking_number,
            },
            carrier=carrier,
            context=context,
        )

        upload_record = models.DocumentUploadRecord.objects.create(
            documents=lib.to_dict(response.documents),
            messages=lib.to_dict(response.messages),
            options=response.options,
            meta=response.meta,
            shipment=shipment,
            upload_carrier=carrier,
            created_by=context.user,
        )

        return upload_record

    def update(
        self,
        instance: models.DocumentUploadRecord,
        validated_data: dict,
        context: serialiazers.Context,
        **kwargs,
    ) -> models.DocumentUploadRecord:
        changes = []

        response = gateway.Documents.upload(
            {
                "reference": getattr(instance.shipment, "tracking_number", None),
                **core.DocumentUploadData(validated_data).data,
            },
            carrier=instance.upload_carrier,
            context=context,
        )

        if any(response.documents):
            changes.append("documents")
            instance.documents = [*instance.documents, lib.to_dict(response.documents)]

        if any(response.messages):
            changes.append("messages")
            instance.messages = lib.to_dict(response.messages)

        instance.save(update_fields=changes)

        return instance


def can_upload_shipment_document(shipment: models.Shipment):
    carrier = getattr(shipment, "selected_rate_carrier", None)
    capabilities = getattr(carrier, "capabilities", [])

    if shipment is None:
        raise exceptions.APIException(
            detail=f"No purchased shipment found for trade document upload.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if shipment.status not in [
        core.ShipmentStatus.shipped.value,
        core.ShipmentStatus.purchased.value,
        core.ShipmentStatus.in_transit.value,
    ]:
        raise exceptions.APIException(
            detail=f"The trade document upload is not enabled for shipment status: '{shipment.status}'.",
            status_code=status.HTTP_409_CONFLICT,
        )

    if "paperless" not in capabilities:
        raise exceptions.APIException(
            detail=f"trade document upload is not supported by carrier: '{carrier.carrier_id}'",
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
