import logging
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from django.urls import path

from drf_yasg.utils import swagger_auto_schema

from purpleserver.core.views.api import GenericAPIView
from purpleserver.core.utils import SerializerDecorator
from purpleserver.core.serializers import ErrorResponse, ParcelData, Parcel
from purpleserver.manager.serializers import ParcelSerializer
from purpleserver.manager.router import router

logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate


class ParcelList(GenericAPIView):

    @swagger_auto_schema(
        tags=['Parcels'],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all parcels",
        responses={200: Parcel(many=True), 400: ErrorResponse()}
    )
    def get(self, request: Request):
        """
        Retrieve all stored parcels.
        """
        parcels = request.user.parcel_set.all()
        serializer = Parcel(parcels, many=True)
        response = self.paginate_queryset(serializer.data)
        return Response(response)

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
        parcel = SerializerDecorator[ParcelSerializer](data=request.data).save(user=request.user).instance
        return Response(Parcel(parcel).data, status=status.HTTP_201_CREATED)


class ParcelDetail(GenericAPIView):

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
        address = request.user.parcel_set.get(pk=pk)
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
        parcel = request.user.parcel_set.get(pk=pk)
        SerializerDecorator[ParcelSerializer](parcel, data=request.data).save()
        return Response(Parcel(parcel).data)


router.urls.append(path('parcels', ParcelList.as_view(), name="parcel-list"))
router.urls.append(path('parcels/<str:pk>', ParcelDetail.as_view(), name="parcel-details"))
