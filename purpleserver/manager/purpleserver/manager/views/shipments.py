import logging
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from django.urls import path

from drf_yasg.utils import swagger_auto_schema

from purpleserver.core.serializers import (
    Serializer, CharField,

    ErrorResponse as ErrorResponseSerializer,
    ShipmentResponse,
    Shipment as ShipmentSerializer,
    ShipmentPayload,
    Options,
    Payment
)
from purpleserver.manager.router import router
from purpleserver.manager.models import Shipment

logger = logging.getLogger(__name__)


class ShipmentPurchaseRequest(Serializer):
    selected_rate_id = CharField(required=True, help_text="The shipment selected rate.")
    payment = Payment(required=True, help_text="The payment details")


class ShipmentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


class ShipmentList(ShipmentAPIView):

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_summary="List all Shipments",
        operation_description="""
        Retrieve all shipments.
        """,
        responses={200: ShipmentSerializer(many=True), 400: ErrorResponseSerializer()}
    )
    def get(self, request: Request):
        shipments = request.user.shipment_set.all()
        serializer = ShipmentSerializer(shipments, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_summary="Create a Shipment",
        operation_description="""
        Create a new shipment instance.
        """,
        responses={200: ShipmentResponse(), 400: ErrorResponseSerializer()},
        request_body=ShipmentPayload()
    )
    def post(self, request: Request):
        pass


class ShipmentDetail(ShipmentAPIView):

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id="shipments_retrieve",
        operation_summary="Retrieve a Shipment",
        operation_description="""
        Retrieve a shipment.
        """,
        responses={200: ShipmentSerializer(), 400: ErrorResponseSerializer()}
    )
    def get(self, request: Request, pk: str):
        address = request.user.shipment_set.get(pk=pk)
        serializer = ShipmentSerializer(address)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_summary="Update a Shipment",
        operation_description="""
        Refresh the list of the shipment rates
        """,
        responses={200: ShipmentSerializer(), 400: ErrorResponseSerializer()},
        request_body=ShipmentPayload()
    )
    def put(self, request: Request, pk: str):
        pass


class ShipmentRates(ShipmentAPIView):

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id="shipments_fetch_rates",
        operation_summary="Fetch new Shipment Rates",
        operation_description="""
        Refresh the list of the shipment rates
        """,
        responses={200: ShipmentSerializer(), 400: ErrorResponseSerializer()}
    )
    def get(self, request: Request, pk: str):
        pass


class ShipmentOptions(ShipmentAPIView):

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id="shipments_add_options",
        operation_summary="Add Shipment Options",
        operation_description="""
        Add one or many options to your shipment.<br/>
        **eg:**<br/>
        - add shipment **insurance**
        - specify the preferred transaction **currency**
        - setup a **cash collected on delivery** option
        
        
        And many more, check additional options available in the [reference](#operation/all_references).
        """,
        responses={200: ShipmentResponse(), 400: ErrorResponseSerializer()},
        request_body=Options()
    )
    def post(self, request: Request, pk: str):
        pass


class ShipmentPurchase(ShipmentAPIView):

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id="shipments_purchase",
        operation_summary="Buy a Shipment",
        operation_description="""
        Select your preferred rates to buy a shipment label.
        """,
        responses={200: ShipmentResponse(), 400: ErrorResponseSerializer()},
        request_body=ShipmentPurchaseRequest()
    )
    def post(self, request: Request, pk: str):
        pass


router.urls.append(path('shipments', ShipmentList.as_view()))
router.urls.append(path('shipments/<str:pk>', ShipmentDetail.as_view()))
router.urls.append(path('shipments/<str:pk>/rates', ShipmentRates.as_view()))
router.urls.append(path('shipments/<str:pk>/options', ShipmentOptions.as_view()))
router.urls.append(path('shipments/<str:pk>/purchase', ShipmentPurchase.as_view()))
