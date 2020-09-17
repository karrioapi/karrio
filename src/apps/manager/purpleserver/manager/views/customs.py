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

from purpleserver.core.utils import SerializerDecorator
from purpleserver.core.serializers import ErrorResponse, CustomsData, Customs
from purpleserver.manager.serializers import CustomsSerializer
from purpleserver.manager.router import router

logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate


class CustomsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


class CustomsList(CustomsAPIView):

    @swagger_auto_schema(
        tags=['Customs'],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all Customs Info",
        responses={200: Customs(many=True), 400: ErrorResponse()}
    )
    def get(self, request: Request):
        """
        Retrieve all stored customs info.
        """
        customs_info = request.user.customs_set.all()
        serializer = Customs(customs_info, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Customs'],
        operation_id=f"{ENDPOINT_ID}create",
        operation_summary="Create a Customs Info",
        request_body=CustomsData(),
        responses={200: Customs(), 400: ErrorResponse()}
    )
    def post(self, request: Request):
        """
        Create a new customs info
        """
        customs = SerializerDecorator[CustomsSerializer](data=request.data).save(user=request.user).instance
        return Response(Customs(customs).data, status=status.HTTP_201_CREATED)


class CustomsDetail(CustomsAPIView):

    @swagger_auto_schema(
        tags=['Customs'],
        operation_id=f"{ENDPOINT_ID}retrieve",
        operation_summary="Retrieve a Customs Info",
        responses={200: Customs(), 400: ErrorResponse()}
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve a customs.
        """
        address = request.user.customs_set.get(pk=pk)
        return Response(Customs(address).data)

    @swagger_auto_schema(
        tags=['Customs'],
        operation_id=f"{ENDPOINT_ID}update",
        operation_summary="Update a Customs Info",
        request_body=CustomsData(),
        responses={200: Customs(), 400: ErrorResponse()}
    )
    def patch(self, request: Request, pk: str):
        """
        modify an existing customs's details.
        """
        customs = request.user.customs_set.get(pk=pk)
        SerializerDecorator[CustomsSerializer](customs, data=request.data).save()
        return Response(Customs(customs).data)


router.urls.append(path('customs_info', CustomsList.as_view(), name="customs-list"))
router.urls.append(path('customs_info/<str:pk>', CustomsDetail.as_view(), name="customs-details"))
