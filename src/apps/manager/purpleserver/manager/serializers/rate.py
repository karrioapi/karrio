from purpleserver.core.gateway import Rates
from purpleserver.core.serializers import RateRequest, RateResponse


class RateSerializer(RateRequest):

    def create(self, validated_data: dict) -> RateResponse:
        user = validated_data['user']
        return Rates.fetch(RateRequest(validated_data).data, user=user)
