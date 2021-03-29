import logging

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.urls import path

from purpleserver.core.views.api import GenericAPIView, APIView
from purpleserver.core.utils import SerializerDecorator, PaginatedResult
from purpleserver.core.exceptions import PurplShipApiException
from purpleserver.core.serializers import ShipmentStatus, ErrorResponse, ParcelData, Parcel, Operation
from purpleserver.manager.serializers import ParcelSerializer, reset_related_shipment_rates
from purpleserver.manager.router import router
import purpleserver.manager.models as models

logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
Parcels = PaginatedResult('ParcelList', Parcel)


class ParcelList(GenericAPIView):
    pagination_class = LimitOffsetPagination
    default_limit = 20

    @swagger_auto_schema(
        tags=['Parcels'],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all parcels",
        responses={200: Parcels(), 400: ErrorResponse()}
    )
    def get(self, request: Request):
        """
        Retrieve all stored parcels.
        """
        parcels = models.Parcel.objects.access_with(request.user).all()
        serializer = Parcel(parcels, many=True)
        response = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(response)

    @swagger_auto_schema(
        tags=['Parcels'],
        operation_id=f"{ENDPOINT_ID}create",
        operation_summary="Create a parcel",
        request_body=ParcelData(),
        responses={200: Parcel(), 400: ErrorResponse()}
    )
    def post(self, request: Request):
        """
        Create a new parcel.
        """
        parcel = SerializerDecorator[ParcelSerializer](data=request.data).save(created_by=request.user).instance
        return Response(Parcel(parcel).data, status=status.HTTP_201_CREATED)


class ParcelDetail(APIView):

    @swagger_auto_schema(
        tags=['Parcels'],
        operation_id=f"{ENDPOINT_ID}retrieve",
        operation_summary="Retrieve a parcel",
        responses={200: Parcel(), 400: ErrorResponse()}
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve a parcel.
        """
        address = models.Parcel.objects.access_with(request.user).get(pk=pk)
        return Response(Parcel(address).data)

    @swagger_auto_schema(
        tags=['Parcels'],
        operation_id=f"{ENDPOINT_ID}update",
        operation_summary="Update a parcel",
        request_body=ParcelData(),
        responses={200: Parcel(), 400: ErrorResponse()}
    )
    def patch(self, request: Request, pk: str):
        """
        modify an existing parcel's details.
        """
        parcel = models.Parcel.objects.access_with(request.user).get(pk=pk)
        shipment = parcel.shipment_parcels.first()
        if shipment is not None and shipment.status == ShipmentStatus.purchased.value:
            raise PurplShipApiException(
                "The shipment related to this parcel has been 'purchased' and can no longer be modified",
                status_code=status.HTTP_409_CONFLICT,
                code='state_error'
            )

        SerializerDecorator[ParcelSerializer](parcel, data=request.data).save()
        reset_related_shipment_rates(shipment)
        return Response(Parcel(parcel).data)

    @swagger_auto_schema(
        tags=['Parcels'],
        operation_id=f"{ENDPOINT_ID}discard",
        operation_summary="Remove a parcel",
        responses={200: Operation(), 400: ErrorResponse()}
    )
    def delete(self, request: Request, pk: str):
        """
        Remove a parcel.
        """
        parcel = models.Parcel.objects.access_with(request.user).get(pk=pk)
        shipment = parcel.shipment_parcels.first()

        if shipment is not None and (
            shipment.status == ShipmentStatus.purchased.value or
            len(shipment.shipment_parcels.all()) == 1
        ):
            raise PurplShipApiException(
                "A shipment attached to this parcel is purchased or has only one parcel. The parcel cannot be removed!",
                status_code=status.HTTP_409_CONFLICT,
                code='state_error'
            )

        parcel.delete(keep_parents=True)
        shipment.shipment_parcels.set(shipment.shipment_parcels.exclude(id=parcel.id))
        serializer = Operation(dict(operation="Remove parcel", success=True))
        reset_related_shipment_rates(shipment)
        return Response(serializer.data)


router.urls.append(path('parcels', ParcelList.as_view(), name="parcel-list"))
router.urls.append(path('parcels/<str:pk>', ParcelDetail.as_view(), name="parcel-details"))
