import logging
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.serializers import NullBooleanField, ChoiceField, Serializer

from django.urls import path
from django.db.models import Q

from drf_yasg.utils import swagger_auto_schema

from purpleserver.carriers.router import router
from purpleserver.core.gateway import Carriers
from purpleserver.core.serializers import CarrierSettings, ErrorResponse, CARRIERS

logger = logging.getLogger(__name__)


class CarrierFilters(Serializer):
    carrier_name = ChoiceField(choices=CARRIERS, required=False, help_text="Indicates a carrier (type)")
    test = NullBooleanField(required=False, help_text="The test flag filter carrier configured in test mode")


class CarrierAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


class CarrierList(CarrierAPIView):

    @swagger_auto_schema(
        tags=['Carriers'],
        operation_summary="List all Carriers",
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
        serializer = CarrierSettings(carriers, many=True)
        return Response(serializer.data)


class CarrierDetails(CarrierAPIView):

    @swagger_auto_schema(
        tags=['Carriers'],
        operation_id="carriers_retrieve",
        operation_summary="Retrieve a Carrier",
        responses={200: CarrierSettings(), 400: ErrorResponse()}
    )
    def get(self, _, carrier_id_or_pk: str):
        """
        Retrieve a configured carrier instance.
        """
        query = Q(id__startswith=carrier_id_or_pk) | Q(carrier_id__startswith=carrier_id_or_pk)

        carrier = Carriers.retrieve(query)
        return Response(CarrierSettings(carrier.data).data)


router.urls.append(path('carriers', CarrierList.as_view()))
router.urls.append(path('carriers/<str:carrier_id_or_pk>', CarrierDetails.as_view()))
