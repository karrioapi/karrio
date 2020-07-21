import logging
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status

from django.urls import path

from drf_yasg.utils import swagger_auto_schema

from purpleserver.core.utils import validate_and_save
from purpleserver.core.serializers import ErrorResponse, ParcelData, Parcel
from purpleserver.manager.serializers import ParcelSerializer
from purpleserver.manager.router import router

logger = logging.getLogger(__name__)


class ParcelAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


class ParcelList(ParcelAPIView):

    @swagger_auto_schema(
        tags=['Parcels'],
        operation_id="list_parcels",
        operation_summary="List all Parcels",
        responses={200: Parcel(many=True), 400: ErrorResponse()}
    )
    def get(self, request: Request):
        """
        Retrieve all stored parcels.
        """
        parcels = request.user.parcel_set.all()
        serializer = Parcel(parcels, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Parcels'],
        operation_id="create_parcel",
        operation_summary="Create a Parcel",
        request_body=ParcelData(),
        responses={200: Parcel(), 400: ErrorResponse()}
    )
    def post(self, request: Request):
        """
        Create a new parcel.
        """
        parcel = validate_and_save(ParcelSerializer, request.data, user=request.user)
        return Response(Parcel(parcel).data, status=status.HTTP_201_CREATED)


class ParcelDetail(ParcelAPIView):

    @swagger_auto_schema(
        tags=['Parcels'],
        operation_id="retrieve_parcel",
        operation_summary="Retrieve a Parcel",
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
        operation_id="update_parcel",
        operation_summary="Update a Parcel",
        request_body=ParcelData(),
        responses={200: Parcel(), 400: ErrorResponse()}
    )
    def patch(self, request: Request, pk: str):
        """
        modify an existing parcel's details.
        """
        parcel = request.user.parcel_set.get(pk=pk)
        validate_and_save(ParcelSerializer, request.data, instance=parcel)
        return Response(Parcel(parcel).data)


router.urls.append(path('parcels', ParcelList.as_view()))
router.urls.append(path('parcels/<str:pk>', ParcelDetail.as_view()))
