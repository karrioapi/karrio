from purpleserver.core.gateway import Rates
from purpleserver.core.serializers import RateRequest, RateResponse
from purpleserver.serializers import owned_model_serializer


@owned_model_serializer
class RateSerializer(RateRequest):

    def create(self, validated_data: dict, **kwargs) -> RateResponse:
        test = validated_data.pop('test') if 'test' in validated_data else None
        return Rates.fetch(RateRequest(validated_data).data, user=validated_data['created_by'], test=test)
