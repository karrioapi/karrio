import logging

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, serializers

from drf_yasg import openapi
from django.urls import path
from drf_yasg.utils import swagger_auto_schema

from purplship.core.utils import DP
from purpleserver.core.views.api import GenericAPIView, APIView
from purpleserver.core.exceptions import PurplShipApiException
from purpleserver.serializers import SerializerDecorator, PaginatedResult
from purpleserver.core.serializers import (
    CARRIERS,
    FlagField,
    ShipmentStatus,
    ErrorResponse,
    Shipment,
    ShipmentData,
    RateResponse,
    Message,
    Rate,
    OperationResponse,
    CustomsData,
    ParcelData,
)
from purpleserver.manager.router import router
from purpleserver.manager.serializers import (
    reset_related_shipment_rates,
    create_shipment_tracker,
    ShipmentSerializer,
    ShipmentPurchaseData,
    ShipmentValidationData,
    ShipmentCancelSerializer,
    RateSerializer,
    ParcelSerializer,
)
import purpleserver.manager.models as models

logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$$$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
Shipments = PaginatedResult('ShipmentList', Shipment)


class ShipmentFilters(serializers.Serializer):
    test_mode = FlagField(
        required=False, allow_null=True, default=None,
        help_text="This flag filter out shipment created in test or prod mode")


class ShipmentMode(serializers.Serializer):
    test = FlagField(
        required=False, allow_null=True, default=None,
        help_text="Create shipment in test or prod mode")


class ShipmentList(GenericAPIView):
    serializer_class = Shipment
    queryset = models.Shipment.objects
    pagination_class = type('CustomPagination', (LimitOffsetPagination,), dict(default_limit=20))

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all shipments",
        responses={200: Shipments(), 400: ErrorResponse()},
        query_serializer=ShipmentFilters
    )
    def get(self, request: Request):
        """
        Retrieve all shipments.
        """
        query = (
            SerializerDecorator[ShipmentFilters](data=request.query_params).data
            if any(request.query_params) else {}
        )
        shipments = models.Shipment.access_by(request).filter(**query)

        response = self.paginate_queryset(Shipment(shipments, many=True).data)
        return self.get_paginated_response(response)

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id=f"{ENDPOINT_ID}create",
        operation_summary="Create a shipment",
        responses={200: Shipment(), 400: ErrorResponse()},
        request_body=ShipmentData(),
        query_serializer=ShipmentMode,
    )
    def post(self, request: Request):
        """
        Create a new shipment instance.
        """
        query = SerializerDecorator[ShipmentMode](data=request.query_params).data
        shipment = SerializerDecorator[ShipmentSerializer](data=request.data, context=request).save(**query).instance

        return Response(Shipment(shipment).data, status=status.HTTP_201_CREATED)


class ShipmentDetail(APIView):

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id=f"{ENDPOINT_ID}retrieve",
        operation_summary="Retrieve a shipment",
        responses={200: Shipment(), 400: ErrorResponse()}
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve a shipment.
        """
        shipment = models.Shipment.access_by(request).get(pk=pk)

        return Response(Shipment(shipment).data)

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id=f"{ENDPOINT_ID}cancel",
        operation_summary="Cancel a shipment",
        responses={200: OperationResponse(), 400: ErrorResponse()}
    )
    def delete(self, request: Request, pk: str):
        """
        Void a shipment with the associated label.
        """
        shipment = models.Shipment.access_by(request).get(pk=pk)

        if shipment.status not in [ShipmentStatus.purchased.value, ShipmentStatus.created.value]:
            raise PurplShipApiException(
                f"The shipment is '{shipment.status}' and can therefore not be cancelled anymore...",
                code='state_error', status_code=status.HTTP_409_CONFLICT
            )

        if shipment.pickup_shipments.exists():
            raise PurplShipApiException(
                (
                    f"This shipment is scheduled for pickup '{shipment.pickup_shipments.first().pk}' "
                    "Please cancel this shipment from the pickup before."
                ),
                code='state_error', status_code=status.HTTP_409_CONFLICT
            )

        confirmation = SerializerDecorator[ShipmentCancelSerializer](shipment, data={}).save()
        return Response(OperationResponse(confirmation.instance).data)


class ShipmentRates(APIView):
    logging_methods = ['GET']

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id=f"{ENDPOINT_ID}rates",
        operation_summary="Fetch new shipment rates",
        responses={200: Shipment(), 400: ErrorResponse()}
    )
    def get(self, request: Request, pk: str):
        """
        Refresh the list of the shipment rates
        """
        shipment = models.Shipment.access_by(request).get(pk=pk)

        rate_response: RateResponse = SerializerDecorator[RateSerializer](
            data=ShipmentData(shipment).data, context=request).save(test=shipment.test_mode).instance

        payload: dict = dict(
            rates=Rate(rate_response.rates, many=True).data,
            messages=Message(rate_response.messages, many=True).data,
        )

        SerializerDecorator[ShipmentSerializer](shipment, data=payload).save()

        return Response(Shipment(shipment).data)


class ShipmentOptions(APIView):

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id=f"{ENDPOINT_ID}set_options",
        operation_summary="Add shipment options",
        responses={200: Shipment(), 400: ErrorResponse()},
        request_body=openapi.Schema(
            title='options',
            type=openapi.TYPE_OBJECT,
            additional_properties=True,
        )
    )
    def post(self, request: Request, pk: str):
        """
        Add one or many options to your shipment.<br/>
        **eg:**<br/>
        - add shipment **insurance**
        - specify the preferred transaction **currency**
        - setup a **cash collected on delivery** option

        ```json
        {
            "insurance": 120,
            "currency": "USD"
        }
        ```

        And many more, check additional options available in the [reference](#operation/all_references).
        """
        shipment = models.Shipment.access_by(request).get(pk=pk)

        if shipment.status == ShipmentStatus.purchased.value:
            raise PurplShipApiException(
                "Shipment already 'purchased'", code='state_error', status_code=status.HTTP_409_CONFLICT
            )

        payload: dict = dict(
            options=DP.to_dict(request.data),
            shipment_rates=[],
            messages=[]
        )

        SerializerDecorator[ShipmentSerializer](shipment, data=payload).save()

        return Response(Shipment(shipment).data)


class ShipmentCustoms(APIView):

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id=f"{ENDPOINT_ID}add_customs",
        operation_summary="Add a customs declaration",
        responses={200: Shipment(), 400: ErrorResponse()},
        request_body=CustomsData()
    )
    def post(self, request: Request, pk: str):
        """
        Add the customs declaration for the shipment if non existent.
        """
        shipment = models.Shipment.access_by(request).get(pk=pk)

        if shipment.status == ShipmentStatus.purchased.value:
            raise PurplShipApiException(
                "Shipment already 'purchased'", code='state_error', status_code=status.HTTP_409_CONFLICT
            )

        if shipment.customs is not None:
            raise PurplShipApiException(
                "Shipment customs declaration already defined", code='state_error', status_code=status.HTTP_409_CONFLICT
            )

        payload: dict = dict(
            customs=DP.to_dict(request.data),
            shipment_rates=[],
            messages=[]
        )

        SerializerDecorator[ShipmentSerializer](shipment, data=payload, context=request).save()
        return Response(Shipment(shipment).data)


class ShipmentParcels(APIView):

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id=f"{ENDPOINT_ID}add_parcel",
        operation_summary="Add a shipment parcel",
        responses={200: Shipment(), 400: ErrorResponse()},
        request_body=ParcelData()
    )
    def post(self, request: Request, pk: str):
        """
        Add a parcel to an existing shipment for a multi-parcel shipment.
        """
        shipment = models.Shipment.access_by(request).get(pk=pk)

        if shipment.status == ShipmentStatus.purchased.value:
            raise PurplShipApiException(
                "Shipment already 'purchased'", code='state_error', status_code=status.HTTP_409_CONFLICT
            )

        parcel = SerializerDecorator[ParcelSerializer](data=request.data, context=request).save().instance
        shipment.shipment_parcels.add(parcel)
        reset_related_shipment_rates(shipment)
        return Response(Shipment(shipment).data)


class ShipmentPurchase(APIView):

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id=f"{ENDPOINT_ID}purchase",
        operation_summary="Buy a shipment label",
        responses={200: Shipment(), 400: ErrorResponse()},
        request_body=ShipmentPurchaseData()
    )
    def post(self, request: Request, pk: str):
        """
        Select your preferred rates to buy a shipment label.
        """
        shipment = models.Shipment.access_by(request).get(pk=pk)

        if shipment.status == ShipmentStatus.purchased.value:
            raise PurplShipApiException(
                f"The shipment is '{shipment.status}' and therefore already {ShipmentStatus.purchased.value}",
                code='state_error', status_code=status.HTTP_409_CONFLICT
            )

        payload = {
            **Shipment(shipment).data,
            **SerializerDecorator[ShipmentPurchaseData](data=request.data).data
        }

        # Submit shipment to carriers
        response: Shipment = SerializerDecorator[ShipmentValidationData](
            data=payload, context=request).save().instance

        # Update shipment state
        SerializerDecorator[ShipmentSerializer](shipment, data=DP.to_dict(response), context=request).save()
        create_shipment_tracker(shipment)

        return Response(Shipment(shipment).data)


router.urls.append(path('shipments', ShipmentList.as_view(), name="shipment-list"))
router.urls.append(path('shipments/<str:pk>', ShipmentDetail.as_view(), name="shipment-details"))
router.urls.append(path('shipments/<str:pk>/rates', ShipmentRates.as_view(), name="shipment-rates"))
router.urls.append(path('shipments/<str:pk>/options', ShipmentOptions.as_view(), name="shipment-options"))
router.urls.append(path('shipments/<str:pk>/customs', ShipmentCustoms.as_view(), name="shipment-customs"))
router.urls.append(path('shipments/<str:pk>/parcels', ShipmentParcels.as_view(), name="shipment-parcels"))
router.urls.append(path('shipments/<str:pk>/purchase', ShipmentPurchase.as_view(), name="shipment-purchase"))
