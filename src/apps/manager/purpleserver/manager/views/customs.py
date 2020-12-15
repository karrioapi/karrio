import logging
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from django.urls import path

from drf_yasg.utils import swagger_auto_schema

from purpleserver.core.views.api import GenericAPIView, APIView
from purpleserver.core.utils import SerializerDecorator
from purpleserver.core.exceptions import PurplShipApiException
from purpleserver.core.serializers import ShipmentStatus, ErrorResponse, CustomsData, Customs, Operation
from purpleserver.manager.serializers import CustomsSerializer, reset_related_shipment_rates
from purpleserver.manager.router import router

logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate


class CustomsList(GenericAPIView):

    @swagger_auto_schema(
        tags=['Customs'],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all customs info",
        responses={200: Customs(many=True), 400: ErrorResponse()}
    )
    def get(self, request: Request):
        """
        Retrieve all stored customs declarations.
        """
        customs_info = request.user.customs_set.all()
        serializer = Customs(customs_info, many=True)
        response = self.paginate_queryset(serializer.data)
        return Response(response)

    @swagger_auto_schema(
        tags=['Customs'],
        operation_id=f"{ENDPOINT_ID}create",
        operation_summary="Create a customs info",
        request_body=CustomsData(),
        responses={200: Customs(), 400: ErrorResponse()}
    )
    def post(self, request: Request):
        """
        Create a new customs declaration.
        """
        customs = SerializerDecorator[CustomsSerializer](data=request.data).save(user=request.user).instance
        return Response(Customs(customs).data, status=status.HTTP_201_CREATED)


class CustomsDetail(APIView):

    @swagger_auto_schema(
        tags=['Customs'],
        operation_id=f"{ENDPOINT_ID}retrieve",
        operation_summary="Retrieve a customs info",
        responses={200: Customs(), 400: ErrorResponse()}
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve customs declaration.
        """
        address = request.user.customs_set.get(pk=pk)
        return Response(Customs(address).data)

    @swagger_auto_schema(
        tags=['Customs'],
        operation_id=f"{ENDPOINT_ID}update",
        operation_summary="Update a customs info",
        request_body=CustomsData(),
        responses={200: Customs(), 400: ErrorResponse()}
    )
    def patch(self, request: Request, pk: str):
        """
        modify an existing customs declaration.
        """
        customs = request.user.customs_set.get(pk=pk)
        shipment = customs.shipment_set.first()
        if shipment is not None and shipment.status == ShipmentStatus.purchased.value:
            raise PurplShipApiException(
                "The shipment related to this customs info has been 'purchased' and can no longer be modified",
                status_code=status.HTTP_409_CONFLICT,
                code='state_error'
            )

        SerializerDecorator[CustomsSerializer](customs, data=request.data).save()
        reset_related_shipment_rates(shipment)
        return Response(Customs(customs).data)

    @swagger_auto_schema(
        tags=['Customs'],
        operation_id=f"{ENDPOINT_ID}discard",
        operation_summary="Discard a customs info",
        responses={200: Operation(), 400: ErrorResponse()}
    )
    def delete(self, request: Request, pk: str):
        """
        Discard a customs declaration.
        """
        customs = request.user.customs_set.get(pk=pk)
        shipment = customs.shipment_set.first()
        if shipment is not None and shipment.status == ShipmentStatus.purchased.value:
            raise PurplShipApiException(
                "The shipment related to this customs info has been 'purchased' and cannot be discarded",
                status_code=status.HTTP_409_CONFLICT,
                code='state_error'
            )

        customs.delete(keep_parents=True)
        serializer = Operation(dict(operation="Discard customs info", success=True))
        reset_related_shipment_rates(shipment)
        return Response(serializer.data)


router.urls.append(path('customs_info', CustomsList.as_view(), name="customs-list"))
router.urls.append(path('customs_info/<str:pk>', CustomsDetail.as_view(), name="customs-details"))
