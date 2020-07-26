import logging
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status

from django.urls import path
from drf_yasg.utils import swagger_auto_schema

from purplship.core.utils.helpers import to_dict

from purpleserver.core.exceptions import PurplShipApiException
from purpleserver.core.utils import SerializerDecorator
from purpleserver.core.serializers import (
    ShipmentStatus,
    ErrorResponse,
    Shipment,
    ShipmentData,
    ShipmentResponse,
    RateResponse,
    Message,
    Rate
)
from purpleserver.manager.router import router
from purpleserver.manager.serializers import (
    ShipmentSerializer,
    ShipmentPurchaseData,
    ShipmentValidationData,
    RateSerializer,
)

logger = logging.getLogger(__name__)


class ShipmentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]


class ShipmentList(ShipmentAPIView):

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id="list_shipments",
        operation_summary="List all Shipments",
        operation_description="""
        Retrieve all shipments.
        """,
        responses={200: Shipment(many=True), 400: ErrorResponse()}
    )
    def get(self, request: Request):
        shipments = request.user.shipment_set.all()

        return Response(Shipment(shipments, many=True).data)

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id="create_shipment",
        operation_summary="Create a Shipment",
        operation_description="""
        Create a new shipment instance.
        """,
        responses={200: Shipment(), 400: ErrorResponse()},
        request_body=ShipmentData()
    )
    def post(self, request: Request):
        shipment = SerializerDecorator[ShipmentSerializer](
            data=request.data).save(user=request.user).instance

        return Response(Shipment(shipment).data, status=status.HTTP_201_CREATED)


class ShipmentDetail(ShipmentAPIView):

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id="retrieve_shipment",
        operation_summary="Retrieve a Shipment",
        operation_description="""
        Retrieve a shipment.
        """,
        responses={200: Shipment(), 400: ErrorResponse()}
    )
    def get(self, request: Request, pk: str):
        shipment = request.user.shipment_set.get(pk=pk)

        return Response(Shipment(shipment).data)

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id="update_shipment",
        operation_summary="Update a Shipment",
        operation_description="""
        Refresh the list of the shipment rates
        """,
        responses={200: Shipment(), 400: ErrorResponse()},
        request_body=ShipmentData(),
    )
    def patch(self, request: Request, pk: str):
        shipment = request.user.shipment_set.get(pk=pk)

        if shipment.status == ShipmentStatus.purchased.value:
            raise PurplShipApiException(
                "Shipment already 'purchased'", code='state_error', status_code=status.HTTP_409_CONFLICT
            )

        SerializerDecorator[ShipmentSerializer](shipment, data=request.data).save()
        return Response(Shipment(shipment).data)


class ShipmentRates(ShipmentAPIView):

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id="fetch_shipments_rates",
        operation_summary="Fetch new Shipment Rates",
        operation_description="""
        Refresh the list of the shipment rates
        """,
        responses={200: ShipmentResponse(), 400: ErrorResponse()}
    )
    def get(self, request: Request, pk: str):
        shipment = request.user.shipment_set.get(pk=pk)

        rate_response: RateResponse = SerializerDecorator[RateSerializer](
            data=ShipmentData(shipment).data).save().instance
        payload: dict = to_dict(dict(rates=Rate(rate_response.rates, many=True).data))

        SerializerDecorator[ShipmentSerializer](shipment, data=payload).save()

        response = dict(
            shipment=Shipment(shipment).data,
            messages=Message(rate_response.messages, many=True).data
        )
        return Response(ShipmentResponse(response).data)


class ShipmentOptions(ShipmentAPIView):

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id="add_shipment_options",
        operation_summary="Add Shipment Options",
        operation_description="""
        Add one or many options to your shipment.<br/>
        **eg:**<br/>
        - add shipment **insurance**
        - specify the preferred transaction **currency**
        - setup a **cash collected on delivery** option
        
        ```json
        {
            "insurane": {
                "amount": 120,
            },
            "currency": "USD"
        }
        ```
        
        And many more, check additional options available in the [reference](#operation/all_references).
        """,
        responses={200: Shipment(), 400: ErrorResponse()},
    )
    def post(self, request: Request, pk: str):
        shipment = request.user.shipment_set.get(pk=pk)

        if shipment.status == ShipmentStatus.purchased.value:
            raise PurplShipApiException(
                "Shipment already 'purchased'", code='state_error', status_code=status.HTTP_409_CONFLICT
            )

        payload: dict = to_dict(dict(options={
            **ShipmentData(shipment).data.get('options'),
            **request.data
        }))

        SerializerDecorator[ShipmentSerializer](shipment, data=payload).save()
        return Response(Shipment(shipment).data)


class ShipmentPurchase(ShipmentAPIView):

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id="purchase_shipment",
        operation_summary="Buy a Shipment",
        operation_description="""
        Select your preferred rates to buy a shipment label.
        """,
        responses={200: ShipmentResponse(), 400: ErrorResponse()},
        request_body=ShipmentPurchaseData()
    )
    def post(self, request: Request, pk: str):
        shipment = request.user.shipment_set.get(pk=pk)

        if shipment.status == ShipmentStatus.purchased.value:
            raise PurplShipApiException(
                "Shipment already 'purchased'", code='state_error', status_code=status.HTTP_409_CONFLICT
            )

        payload = {
            **Shipment(shipment).data,
            **ShipmentPurchaseData(request.data).data
        }

        # Submit shipment to carriers
        shipment_response: ShipmentResponse = SerializerDecorator[ShipmentValidationData](
            data=payload).save(request=request).instance
        # Update shipment state
        SerializerDecorator[ShipmentSerializer](
            shipment, data=to_dict(shipment_response.shipment)).save()

        response = dict(
            shipment=Shipment(shipment).data,
            messages=Message(shipment_response.messages, many=True).data
        )
        return Response(ShipmentResponse(response).data)


router.urls.append(path('shipments', ShipmentList.as_view(), name="shipment-list"))
router.urls.append(path('shipments/<str:pk>', ShipmentDetail.as_view(), name="shipment-details"))
router.urls.append(path('shipments/<str:pk>/rates', ShipmentRates.as_view(), name="shipment-rates"))
router.urls.append(path('shipments/<str:pk>/options', ShipmentOptions.as_view(), name="shipment-options"))
router.urls.append(path('shipments/<str:pk>/purchase', ShipmentPurchase.as_view(), name="shipment-purchase"))
