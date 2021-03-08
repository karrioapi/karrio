from purpleserver.core.gateway import Rates
from purpleserver.core.serializers import RateRequest, RateResponse


class RateSerializer(RateRequest):

    def create(self, validated_data: dict) -> RateResponse:
        created_by = validated_data['created_by']
        return Rates.fetch(RateRequest(validated_data).data, created_by=created_by)
