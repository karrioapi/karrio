import typing

import karrio.server.core.gateway as gateway
import karrio.server.manager.models as models
import karrio.server.core.serializers as core
import karrio.server.serializers as serializers
import karrio.server.manager.serializers as manager

DEFAULT_CARRIER_FILTER: typing.Any = dict(active=True, capability="manifest")


@serializers.owned_model_serializer
class ManifestSerializer(core.ManifestRequest):
    def create(
        self, validated_data: dict, context: serializers.Context, **kwargs
    ) -> models.Manifest:
        request_data = core.ManifestRequest(validated_data).data
        carrier_filter = validated_data["carrier_filter"]
        carrier = gateway.Carriers.first(
            context=context,
            **{"raise_not_found": True, **DEFAULT_CARRIER_FILTER, **carrier_filter},
        )

        response = gateway.Manifests.create(payload=request_data, carrier=carrier)

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

        return models.Manifest.objects.create(
            **{
                **payload,
                "address": address,
                "created_by": context.user,
                "manifest_carrier": carrier,
                "test_mode": response.manifest.test_mode,
            }
        )
