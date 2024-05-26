import logging

from django.urls import path
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from karrio.server.manager.router import router
from karrio.server.core.views.api import GenericAPIView, APIView
from karrio.server.manager.serializers import (
    PaginatedResult,
    ErrorResponse,
    ParcelData,
    Parcel,
    ParcelSerializer,
    can_mutate_parcel,
)
import karrio.server.manager.models as models
import karrio.server.openapi as openapi

logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
Parcels = PaginatedResult("ParcelList", Parcel)


class ParcelList(GenericAPIView):
    queryset = models.Parcel.objects
    pagination_class = type(
        "CustomPagination", (LimitOffsetPagination,), dict(default_limit=20)
    )
    serializer_class = Parcels

    @openapi.extend_schema(
        tags=["Parcels"],
        operation_id=f"{ENDPOINT_ID}list",
        extensions={"x-operationId": "listParcels"},
        summary="List all parcels",
        responses={
            200: Parcels(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def get(self, request: Request):
        """
        Retrieve all stored parcels.
        """
        parcels = models.Parcel.access_by(request).filter(
            **{
                f"{prop}__isnull": True
                for prop in models.Parcel.HIDDEN_PROPS
                if prop != "org"
            }
        )
        serializer = Parcel(parcels, many=True)
        response = self.paginate_queryset(serializer.data)

        return self.get_paginated_response(response)

    @openapi.extend_schema(
        tags=["Parcels"],
        operation_id=f"{ENDPOINT_ID}create",
        extensions={"x-operationId": "createParcel"},
        summary="Create a parcel",
        request=ParcelData(),
        responses={
            201: Parcel(),
            400: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def post(self, request: Request):
        """
        Create a new parcel.
        """
        parcel = (
            ParcelSerializer.map(data=request.data, context=request).save().instance
        )
        return Response(Parcel(parcel).data, status=status.HTTP_201_CREATED)


class ParcelDetail(APIView):

    @openapi.extend_schema(
        tags=["Parcels"],
        operation_id=f"{ENDPOINT_ID}retrieve",
        extensions={"x-operationId": "retrieveParcel"},
        summary="Retrieve a parcel",
        responses={
            200: Parcel(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve a parcel.
        """
        address = models.Parcel.access_by(request).get(pk=pk)
        return Response(Parcel(address).data)

    @openapi.extend_schema(
        tags=["Parcels"],
        operation_id=f"{ENDPOINT_ID}update",
        extensions={"x-operationId": "updateParcel"},
        summary="Update a parcel",
        request=ParcelData(),
        responses={
            200: Parcel(),
            400: ErrorResponse(),
            404: ErrorResponse(),
            409: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def patch(self, request: Request, pk: str):
        """
        modify an existing parcel's details.
        """
        parcel = models.Parcel.access_by(request).get(pk=pk)
        can_mutate_parcel(parcel, update=True)

        ParcelSerializer.map(parcel, data=request.data).save()

        return Response(Parcel(parcel).data)

    @openapi.extend_schema(
        tags=["Parcels"],
        operation_id=f"{ENDPOINT_ID}discard",
        extensions={"x-operationId": "discardParcel"},
        summary="Remove a parcel",
        responses={
            200: Parcel(),
            404: ErrorResponse(),
            409: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def delete(self, request: Request, pk: str):
        """
        Remove a parcel.
        """
        parcel = models.Parcel.access_by(request).get(pk=pk)
        can_mutate_parcel(parcel, update=True, delete=True)

        parcel.delete(keep_parents=True)

        return Response(Parcel(parcel).data)


router.urls.append(path("parcels", ParcelList.as_view(), name="parcel-list"))
router.urls.append(
    path("parcels/<str:pk>", ParcelDetail.as_view(), name="parcel-details")
)
