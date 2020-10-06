import logging

from purpleserver.core.utils import SerializerDecorator
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import NullBooleanField, ChoiceField, Serializer
from rest_framework import generics, status

from django.urls import path
from django.forms.models import model_to_dict

from drf_yasg.utils import swagger_auto_schema

from purpleserver.core.gateway import Carriers
from purpleserver.core.serializers import CarrierSettings, ErrorResponse, CARRIERS
from purpleserver.providers.router import router
from purpleserver.providers.serializers import CarrierSerializer

logger = logging.getLogger(__name__)
ENDPOINT_ID = "&"  # This endpoint id is used to make operation ids unique make sure not to duplicate


class CarrierFilters(Serializer):
    carrier_name = ChoiceField(choices=CARRIERS, required=False, help_text="Indicates a carrier (type)")
    test = NullBooleanField(required=False, help_text="The test flag filter carrier configured in test mode")


class CarrierAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


class CarrierList(CarrierAPIView):

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


class ProviderList(CarrierAPIView):
    swagger_schema = None
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get(self, request: Request):
        """
        Returns the list of configured carriers
        """
        connections = request.user.carrier_set.all()
        response = self.paginate_queryset([connection.data.__dict__ for connection in connections])
        return Response(response)

    def post(self, request: Request):
        """
        Connect a carrier account.
        """
        connection = SerializerDecorator[CarrierSerializer](data=request.data).save(user=request.user).instance
        return Response(CarrierSettings(connection).data, status=status.HTTP_201_CREATED)


class ProviderDetails(CarrierAPIView):
    swagger_schema = None
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def patch(self, request: Request, pk: str):
        """
        Update a carrier connection details.
        """
        connection = request.user.carrier_set.get(pk=pk)

        SerializerDecorator[CarrierSerializer](connection, data=request.data).save()
        return Response(connection.data.__dict__)

    def delete(self, request: Request, pk: str):
        """
        Disconnect a carrier connection.
        """
        carrier = request.user.carrier_set.get(pk=pk)
        carrier.delete()
        return Response(dict(success=True, message="Carrier successfully disconnected."))


router.urls.append(path('carriers', CarrierList.as_view()))
router.urls.append(path('providers', ProviderList.as_view()))
router.urls.append(path('providers/<str:pk>', ProviderDetails.as_view()))
