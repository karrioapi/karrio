import typing

import karrio.server.core.gateway as gateway
import karrio.server.manager.models as models
import karrio.server.core.serializers as core
import karrio.server.serializers as serializers
import karrio.server.manager.serializers as manager

DEFAULT_CARRIER_FILTER: typing.Any = dict(active=True, capability="manifest")


@serializers.owned_model_serializer
class ManifestSerializer(core.ManifestData):
    def create(
        self, validated_data: dict, context: serializers.Context, **kwargs
    ) -> models.Manifest:
        data = validated_data.copy()
        shipment_ids = list(set(data.pop("shipment_ids")))
        carrier_name = data["carrier_name"]
        carrier = gateway.Carriers.first(
            context=context,
            carrier_name=carrier_name,
            **{"raise_not_found": True, **DEFAULT_CARRIER_FILTER},
        )

        shipments = models.Shipment.access_by(context).filter(
            id__in=shipment_ids,
            manifest__isnull=True,
            selected_rate_carrier__carrier_code=carrier_name,
        )
        shipment_identifiers = [_.shipment_identifier for _ in shipments]

        if (
            len(shipment_identifiers) > len(shipment_ids)
            or len(shipment_identifiers) == 0
        ):
            raise serializers.ValidationError(
                {
                    "shipment_ids": (
                        "One or more shipment ids are invalid or not found. "
                        "Please make sure that the shipments referenced exist and have been purchased with the same carrier."
                    )
                }
            )

        response = gateway.Manifests.create(
            payload=core.ManifestRequest.map(
                data={
                    **data,
                    "shipment_identifiers": shipment_identifiers,
                    "options": {
                        **data.get("options", {}),
                        "shipments": core.Shipment(shipments, many=True).data,
                    },
                }
            ).data,
            carrier=carrier,
        )

        payload = {
            key: value
            for key, value in core.Manifest(response.manifest).data.items()
            if key in models.Manifest.DIRECT_PROPS
        }
        address = serializers.save_one_to_one_data(
            "address",
            manager.AddressSerializer,
            payload=validated_data,
            context=context,
        )

        manifest = models.Manifest.objects.create(
            **{
                **payload,
                "address": address,
                "created_by": context.user,
                "manifest_carrier": carrier,
                "options": data.get("options", {}),
                "test_mode": response.manifest.test_mode,
                "manifest": response.manifest.doc.manifest,
            }
        )
        manifest.shipments.set(shipments)

        return manifest
