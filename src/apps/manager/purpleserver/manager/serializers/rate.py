from purpleserver.core.gateway import Rates
from purpleserver.core.serializers import RateRequest, RateResponse


class RateSerializer(RateRequest):

    def create(self, validated_data: dict) -> RateResponse:
        return Rates.fetch(validated_data)
