from purpleserver.core.gateway import Rates
from purpleserver.core.serializers import RateRequest, RateResponse
from purpleserver.core.utils import owned_model_serializer


@owned_model_serializer
class RateSerializer(RateRequest):

    def create(self, validated_data: dict) -> RateResponse:
        return Rates.fetch(RateRequest(validated_data).data, user=self._context_user)
