import logging

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, serializers

from drf_yasg import openapi
from django.urls import path
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from django_filters import rest_framework as filters

from purplship.core.utils import DP
from purplship.server.core.gateway import Carriers
from purplship.server.core.views.api import GenericAPIView, APIView
from purplship.server.core.exceptions import PurplshipAPIException
from purplship.server.serializers import SerializerDecorator, PaginatedResult
from purplship.server.core.serializers import (
    MODELS,
    FlagField,
    ShipmentStatus,
    ErrorResponse,
    Shipment,
    ShipmentData,
    RateResponse,
    Rate,
    OperationResponse,
    CustomsData,
    ParcelData,
)
from purplship.server.manager.router import router
from purplship.server.manager.serializers import (
    reset_related_shipment_rates,
    create_shipment_tracker,
    ShipmentSerializer,
    ShipmentRateData,
    ShipmentPurchaseData,
    ShipmentPurchaseSerializer,
    ShipmentCancelSerializer,
    RateSerializer,
    ParcelSerializer,
)
import purplship.server.manager.models as models

logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$$$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
Shipments = PaginatedResult("ShipmentList", Shipment)


class ShipmentFilters(filters.FilterSet):
    created_after = filters.DateFilter(field_name="created_at", lookup_expr="gte")
    created_before = filters.DateFilter(field_name="created_at", lookup_expr="lte")
    carrier_id = filters.CharFilter(field_name="selected_rate_carrier__carrier_id")
    service = filters.CharFilter(field_name="selected_rate__service")
    reference = filters.CharFilter(field_name="reference", lookup_expr="iregex")

    parameters = [
        openapi.Parameter("test_mode", in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
        openapi.Parameter(
            "carrier_name",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            enum=list(MODELS.keys()),
        ),
        openapi.Parameter("carrier_id", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter(
            "status",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            enum=[c.value for c in list(ShipmentStatus)],
        ),
        openapi.Parameter("service", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter("reference", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter(
            "created_before",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATETIME,
            description="DateTime in format `YYYY-MM-DD H:M:S.fz`",
        ),
        openapi.Parameter(
            "created_after",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATETIME,
            description="DateTime in format `YYYY-MM-DD H:M:S.fz`",
        ),
    ]

    class Meta:
        model = models.Shipment
        fields = ["test_mode", "status"]


class ShipmentMode(serializers.Serializer):
    test = FlagField(
        required=False,
        allow_null=True,
        default=None,
        help_text="Create shipment in test or live mode",
    )


class ShipmentList(GenericAPIView):
    pagination_class = type(
        "CustomPagination", (LimitOffsetPagination,), dict(default_limit=20)
    )
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ShipmentFilters
    serializer_class = Shipments
    model = models.Shipment

    def get_queryset(self):
        queryset = super().get_queryset()
        _filters = tuple()
        query_params = getattr(self.request, "query_params", {})
        carrier_name = query_params.get("carrier_name")

        if carrier_name is not None:
            _filters += (
                Q(meta__rate_provider=carrier_name)
                | Q(
                    **{
                        f"selected_rate_carrier__{carrier_name.replace('_', '')}settings__isnull": False
                    }
                ),
            )

        return queryset.filter(*_filters)

    @swagger_auto_schema(
        tags=["Shipments"],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all shipments",
        responses={200: Shipments(), 400: ErrorResponse()},
        manual_parameters=ShipmentFilters.parameters,
    )
    def get(self, request: Request):
        """
        Retrieve all shipments.
        """
        shipments = self.filter_queryset(self.get_queryset())
        response = self.paginate_queryset(Shipment(shipments, many=True).data)
        return self.get_paginated_response(response)

    @swagger_auto_schema(
        tags=["Shipments"],
        operation_id=f"{ENDPOINT_ID}create",
        operation_summary="Create a shipment",
        responses={200: Shipment(), 400: ErrorResponse()},
        request_body=ShipmentData(),
        query_serializer=ShipmentMode(),
    )
    def post(self, request: Request):
        """
        Create a new shipment instance.
        """
        carrier_filter = {
            **SerializerDecorator[ShipmentMode](data=request.query_params).data
        }
        shipment = (
            SerializerDecorator[ShipmentSerializer](data=request.data, context=request)
            .save(carrier_filter=carrier_filter)
            .instance
        )

        return Response(Shipment(shipment).data, status=status.HTTP_201_CREATED)


class ShipmentDetail(APIView):
    @swagger_auto_schema(
        tags=["Shipments"],
        operation_id=f"{ENDPOINT_ID}retrieve",
        operation_summary="Retrieve a shipment",
        responses={200: Shipment(), 400: ErrorResponse()},
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve a shipment.
        """
        shipment = models.Shipment.access_by(request).get(pk=pk)

        return Response(Shipment(shipment).data)

    @swagger_auto_schema(
        tags=["Shipments"],
        operation_id=f"{ENDPOINT_ID}cancel",
        operation_summary="Cancel a shipment",
        responses={200: OperationResponse(), 400: ErrorResponse()},
    )
    def delete(self, request: Request, pk: str):
        """
        Void a shipment with the associated label.
        """
        shipment = models.Shipment.access_by(request).get(pk=pk)

        if shipment.status not in [
            ShipmentStatus.purchased.value,
            ShipmentStatus.created.value,
        ]:
            raise PurplshipAPIException(
                f"The shipment is '{shipment.status}' and can not be cancelled anymore...",
                code="state_error",
                status_code=status.HTTP_409_CONFLICT,
            )

        if shipment.pickup_shipments.exists():
            raise PurplshipAPIException(
                (
                    f"This shipment is scheduled for pickup '{shipment.pickup_shipments.first().pk}' "
                    "Please cancel this shipment pickup before."
                ),
                code="state_error",
                status_code=status.HTTP_409_CONFLICT,
            )

        confirmation = SerializerDecorator[ShipmentCancelSerializer](
            shipment, data={}, context=request
        ).save()
        return Response(OperationResponse(confirmation.instance).data)


class ShipmentRates(APIView):
    logging_methods = ["GET"]

    @swagger_auto_schema(
        tags=["Shipments"],
        operation_id=f"{ENDPOINT_ID}rates",
        operation_summary="Fetch new shipment rates",
        responses={200: Shipment(), 400: ErrorResponse()},
        request_body=ShipmentRateData(),
    )
    def post(self, request: Request, pk: str):
        """
        Refresh the list of the shipment rates
        """
        shipment = (
            models.Shipment.access_by(request)
            .exclude(status=ShipmentStatus.cancelled.value)
            .get(pk=pk)
        )

        rate_payload = SerializerDecorator[ShipmentRateData](data=request.data).data
        carrier_ids = (
            rate_payload["carrier_ids"]
            if "carrier_ids" in rate_payload
            else shipment.carrier_ids
        )

        carriers = Carriers.list(
            active=True,
            capability="shipping",
            context=request,
            test=shipment.test_mode,
            carrier_ids=carrier_ids,
        )

        rate_response: RateResponse = (
            SerializerDecorator[RateSerializer](
                context=request, data={**ShipmentData(shipment).data, **rate_payload}
            )
            .save(carriers=carriers)
            .instance
        )

        SerializerDecorator[ShipmentSerializer](
            shipment,
            context=request,
            data={
                "rates": Rate(rate_response.rates, many=True).data,
                "messages": DP.to_dict(rate_response.messages),
                **rate_payload,
            },
        ).save(carriers=carriers)

        return Response(Shipment(shipment).data)


class ShipmentOptions(APIView):
    @swagger_auto_schema(
        tags=["Shipments"],
        operation_id=f"{ENDPOINT_ID}set_options",
        operation_summary="Add shipment options",
        responses={200: Shipment(), 400: ErrorResponse()},
        request_body=openapi.Schema(
            title="options",
            type=openapi.TYPE_OBJECT,
            additional_properties=True,
        ),
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
        shipment = (
            models.Shipment.access_by(request)
            .exclude(status=ShipmentStatus.cancelled.value)
            .get(pk=pk)
        )

        if shipment.status == ShipmentStatus.purchased.value:
            raise PurplshipAPIException(
                "Shipment already 'purchased'",
                code="state_error",
                status_code=status.HTTP_409_CONFLICT,
            )

        payload: dict = dict(
            options=DP.to_dict(request.data), shipment_rates=[], messages=[]
        )

        SerializerDecorator[ShipmentSerializer](shipment, data=payload).save()

        return Response(Shipment(shipment).data)


class ShipmentCustoms(APIView):
    @swagger_auto_schema(
        tags=["Shipments"],
        operation_id=f"{ENDPOINT_ID}add_customs",
        operation_summary="Add a customs declaration",
        responses={200: Shipment(), 400: ErrorResponse()},
        request_body=CustomsData(),
    )
    def post(self, request: Request, pk: str):
        """
        Add the customs declaration for the shipment if non existent.
        """
        shipment = (
            models.Shipment.access_by(request)
            .exclude(status=ShipmentStatus.cancelled.value)
            .get(pk=pk)
        )

        if shipment.status == ShipmentStatus.purchased.value:
            raise PurplshipAPIException(
                "Shipment already 'purchased'",
                code="state_error",
                status_code=status.HTTP_409_CONFLICT,
            )

        if shipment.customs is not None:
            raise PurplshipAPIException(
                "Shipment customs declaration already defined",
                code="state_error",
                status_code=status.HTTP_409_CONFLICT,
            )

        payload: dict = dict(
            customs=DP.to_dict(request.data), shipment_rates=[], messages=[]
        )

        SerializerDecorator[ShipmentSerializer](
            shipment, data=payload, context=request
        ).save()
        return Response(Shipment(shipment).data)


class ShipmentParcels(APIView):
    @swagger_auto_schema(
        tags=["Shipments"],
        operation_id=f"{ENDPOINT_ID}add_parcel",
        operation_summary="Add a shipment parcel",
        responses={200: Shipment(), 400: ErrorResponse()},
        request_body=ParcelData(),
    )
    def post(self, request: Request, pk: str):
        """
        Add a parcel to an existing shipment for a multi-parcel shipment.
        """
        shipment = (
            models.Shipment.access_by(request)
            .exclude(status=ShipmentStatus.cancelled.value)
            .get(pk=pk)
        )

        if shipment.status == ShipmentStatus.purchased.value:
            raise PurplshipAPIException(
                "Shipment already 'purchased'",
                code="state_error",
                status_code=status.HTTP_409_CONFLICT,
            )

        parcel = (
            SerializerDecorator[ParcelSerializer](data=request.data, context=request)
            .save()
            .instance
        )
        shipment.shipment_parcels.add(parcel)
        reset_related_shipment_rates(shipment)
        return Response(Shipment(shipment).data)


class ShipmentPurchase(APIView):
    @swagger_auto_schema(
        tags=["Shipments"],
        operation_id=f"{ENDPOINT_ID}purchase",
        operation_summary="Buy a shipment label",
        responses={200: Shipment(), 400: ErrorResponse()},
        request_body=ShipmentPurchaseData(),
    )
    def post(self, request: Request, pk: str):
        """
        Select your preferred rates to buy a shipment label.
        """
        shipment = (
            models.Shipment.access_by(request)
            .exclude(status=ShipmentStatus.cancelled.value)
            .get(pk=pk)
        )

        if shipment.status == ShipmentStatus.purchased.value:
            raise PurplshipAPIException(
                f"The shipment is '{shipment.status}' and cannot be purchased again",
                code="state_error",
                status_code=status.HTTP_409_CONFLICT,
            )

        # Submit shipment to carriers
        response: Shipment = (
            SerializerDecorator[ShipmentPurchaseSerializer](
                context=request,
                data={
                    **Shipment(shipment).data,
                    **SerializerDecorator[ShipmentPurchaseData](data=request.data).data,
                },
            )
            .save()
            .instance
        )

        # Update shipment state
        SerializerDecorator[ShipmentSerializer](
            shipment, data=DP.to_dict(response), context=request
        ).save()
        create_shipment_tracker(shipment, context=request)

        return Response(Shipment(shipment).data)


router.urls.append(path("shipments", ShipmentList.as_view(), name="shipment-list"))
router.urls.append(
    path("shipments/<str:pk>", ShipmentDetail.as_view(), name="shipment-details")
)
router.urls.append(
    path("shipments/<str:pk>/rates", ShipmentRates.as_view(), name="shipment-rates")
)
router.urls.append(
    path(
        "shipments/<str:pk>/options", ShipmentOptions.as_view(), name="shipment-options"
    )
)
router.urls.append(
    path(
        "shipments/<str:pk>/customs", ShipmentCustoms.as_view(), name="shipment-customs"
    )
)
router.urls.append(
    path(
        "shipments/<str:pk>/parcels", ShipmentParcels.as_view(), name="shipment-parcels"
    )
)
router.urls.append(
    path(
        "shipments/<str:pk>/purchase",
        ShipmentPurchase.as_view(),
        name="shipment-purchase",
    )
)
