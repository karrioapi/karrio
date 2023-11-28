from karrio.server.core.gateway import Rates
from karrio.server.core.serializers import RateRequest, RateResponse
from karrio.server.serializers import owned_model_serializer, Context


@owned_model_serializer
class RateSerializer(RateRequest):

    def create(self, validated_data: dict, context: Context, **kwargs) -> RateResponse:
        carrier_filters = validated_data.get('carrier_filters') or {}
        carriers = validated_data.get('carriers')

        return Rates.fetch(RateRequest(validated_data).data, context=context, carriers=carriers, **carrier_filters)
