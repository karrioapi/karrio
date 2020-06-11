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

from purpleserver.core.serializers import (
    ErrorResponse as ErrorResponseSerializer, Parcel as ParcelSerializer
)
from purpleserver.manager.router import router
from purpleserver.manager.models import Parcel

logger = logging.getLogger(__name__)


class ParcelAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


class ParcelList(ParcelAPIView):

    @swagger_auto_schema(
        tags=['Parcels'],
        operation_summary="List all Parcels",
        responses={200: ParcelSerializer(many=True), 400: ErrorResponseSerializer()}
    )
    def get(self, request: Request):
        """
        Retrieve all stored parcels.
        """
        parcels = request.user.parcel_set.all()
        serializer = ParcelSerializer(parcels, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Parcels'],
        operation_summary="Create a Parcel",
        responses={200: ParcelSerializer(), 400: ErrorResponseSerializer()}
    )
    def post(self, request: Request):
        """
        Create a new parcel.
        """
        serializer = ParcelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Parcel.objects.create(**serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ParcelDetail(ParcelAPIView):

    @swagger_auto_schema(
        tags=['Parcels'],
        operation_id="parcels_retrieve",
        operation_summary="Retrieve a Parcel",
        responses={200: ParcelSerializer(), 400: ErrorResponseSerializer()}
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve a parcel.
        """
        address = request.user.parcel_set.get(pk=pk)
        serializer = ParcelSerializer(address)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Parcels'],
        operation_summary="Update a Parcel",
        responses={200: ParcelSerializer(), 400: ErrorResponseSerializer()}
    )
    def put(self, request: Request, pk: str):
        """
        modify an existing parcel's details.
        """
        parcel = request.user.parcel_set.get(pk=pk)
        serializer = ParcelSerializer(parcel, data=request.data)
        serializer.is_valid(raise_exception=True)
        for key, val in serializer.validated_data:
            setattr(parcel, key, val)
        parcel.save()
        return Response(serializer.data)


router.urls.append(path('parcels', ParcelList.as_view()))
router.urls.append(path('parcels/<str:pk>', ParcelDetail.as_view()))
