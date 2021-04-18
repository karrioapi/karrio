from purpleserver.core.gateway import Rates
from purpleserver.core.serializers import RateRequest, RateResponse


class RateSerializer(RateRequest):

    def create(self, validated_data: dict) -> RateResponse:
        return Rates.fetch(RateRequest(validated_data).data, user=validated_data['created_by'])
