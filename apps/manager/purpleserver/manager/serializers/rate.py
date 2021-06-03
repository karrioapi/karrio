from purpleserver.core.gateway import Rates
from purpleserver.core.serializers import RateRequest, RateResponse
from purpleserver.serializers import owned_model_serializer, Context


@owned_model_serializer
class RateSerializer(RateRequest):

    def create(self, validated_data: dict, context: Context, **kwargs) -> RateResponse:
        test = validated_data.pop('test') if 'test' in validated_data else None
        return Rates.fetch(RateRequest(validated_data).data, context=context, test=test)
