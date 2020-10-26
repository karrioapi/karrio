import logging

from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import NullBooleanField, ChoiceField, Serializer

from purpleserver.core.views.api import GenericAPIView
from purpleserver.core.gateway import Carriers
from purpleserver.core.serializers import CarrierSettings, ErrorResponse, CARRIERS
from purpleserver.providers.router import router

logger = logging.getLogger(__name__)
ENDPOINT_ID = "&"  # This endpoint id is used to make operation ids unique make sure not to duplicate


class CarrierFilters(Serializer):
    carrier_name = ChoiceField(choices=CARRIERS, required=False, help_text="Indicates a carrier (type)")
    test = NullBooleanField(required=False, help_text="The test flag filter carrier configured in test mode")


class CarrierList(GenericAPIView):

    @swagger_auto_schema(
        tags=['Carriers'],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all carriers",
        responses={200: CarrierSettings(many=True), 400: ErrorResponse()},
        query_serializer=CarrierFilters
    )
    def get(self, request: Request):
        """
        Returns the list of configured carriers
        """
        query = CarrierFilters(data=request.query_params)
        query.is_valid(raise_exception=True)

        carriers = [carrier.data for carrier in Carriers.list(**query.validated_data)]
        response = self.paginate_queryset(CarrierSettings(carriers, many=True).data)
        return Response(response)


router.urls.append(path('carriers', CarrierList.as_view()))
