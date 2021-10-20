import logging

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.urls import path

from purplship.server.core.views.api import GenericAPIView, APIView
from purplship.server.serializers import SerializerDecorator, PaginatedResult
from purplship.server.core.exceptions import PurplShipApiException
from purplship.server.core.serializers import ShipmentStatus, ErrorResponse, ParcelData, Parcel, Operation
from purplship.server.manager.serializers import ParcelSerializer, reset_related_shipment_rates
from purplship.server.manager.router import router
import purplship.server.manager.models as models

logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
Parcels = PaginatedResult('ParcelList', Parcel)


class ParcelList(GenericAPIView):
    queryset = models.Parcel.objects
    pagination_class = type('CustomPagination', (LimitOffsetPagination,), dict(default_limit=20))

    @swagger_auto_schema(
        tags=['Parcels'],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all parcels",
        responses={200: Parcels(), 400: ErrorResponse()},
        code_examples=[
            {
                'lang': 'bash',
                'source': '''
                curl --request GET \\
                  --url '/v1/parcels' \\
                  --header 'Authorization: Token <API_KEY>'
                '''
            }
        ]
    )
    def get(self, request: Request):
        """
        Retrieve all stored parcels.
        """
        parcels = models.Parcel.access_by(request).filter(shipment_parcels=None)
        serializer = Parcel(parcels, many=True)
        response = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(response)

    @swagger_auto_schema(
        tags=['Parcels'],
        operation_id=f"{ENDPOINT_ID}create",
        operation_summary="Create a parcel",
        request_body=ParcelData(),
        responses={200: Parcel(), 400: ErrorResponse()},
        code_examples=[
            {
                'lang': 'bash',
                'source': '''
                curl --request POST \\
                    --url /v1/parcels \\
                    --header 'Authorization: Token <API_KEY>' \\
                    --header 'Content-Type: application/json' \\
                    --data '{
                      "weight": 1,
                      "weight_unit": "KG",
                      "package_preset": "canadapost_corrugated_small_box"
                    }'
                '''
            }
        ]
    )
    def post(self, request: Request):
        """
        Create a new parcel.
        """
        parcel = SerializerDecorator[ParcelSerializer](data=request.data, context=request).save().instance
        return Response(Parcel(parcel).data, status=status.HTTP_201_CREATED)


class ParcelDetail(APIView):

    @swagger_auto_schema(
        tags=['Parcels'],
        operation_id=f"{ENDPOINT_ID}retrieve",
        operation_summary="Retrieve a parcel",
        responses={200: Parcel(), 400: ErrorResponse()},
        code_examples=[
            {
                'lang': 'bash',
                'source': '''
                curl --request GET \\
                  --url /v1/parcels/<PARCEL_ID> \\
                  --header 'Authorization: Token <API_KEY>'
                '''
            }
        ]
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve a parcel.
        """
        address = models.Parcel.access_by(request).get(pk=pk)
        return Response(Parcel(address).data)

    @swagger_auto_schema(
        tags=['Parcels'],
        operation_id=f"{ENDPOINT_ID}update",
        operation_summary="Update a parcel",
        request_body=ParcelData(),
        responses={200: Parcel(), 400: ErrorResponse()},
        code_examples=[
            {
                'lang': 'bash',
                'source': '''
                curl --request PATCH \\
                    --url /v1/parcels/<PARCEL_ID> \\
                    --header 'Authorization: Token <API_KEY>' \\
                    --header 'Content-Type: application/json' \\
                    --data '{
                      "weight": 1.2,
                    }'
                '''
            }
        ]
    )
    def patch(self, request: Request, pk: str):
        """
        modify an existing parcel's details.
        """
        parcel = models.Parcel.access_by(request).get(pk=pk)
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
        responses={200: Operation(), 400: ErrorResponse()},
        code_examples=[
            {
                'lang': 'bash',
                'source': '''
                curl --request DELETE \\
                    --url /v1/parcels/<PARCEL_ID> \\
                    --header 'Authorization: Token <API_KEY>'
                '''
            }
        ]
    )
    def delete(self, request: Request, pk: str):
        """
        Remove a parcel.
        """
        parcel = models.Parcel.access_by(request).get(pk=pk)
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
