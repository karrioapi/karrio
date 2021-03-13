import logging

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.urls import path

from purpleserver.core.views.api import GenericAPIView, APIView
from purpleserver.core.utils import SerializerDecorator, PaginatedResult
from purpleserver.core.serializers import ErrorResponse, Operation
from purpleserver.events.serializers import WebhookData, Webhook, WebhookSerializer
from purpleserver.events.router import router


logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$$$$$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
Webhooks = PaginatedResult('WebhookList', Webhook)


class WebhookList(GenericAPIView):
    pagination_class = LimitOffsetPagination
    default_limit = 20

    @swagger_auto_schema(
        tags=['Webhooks'],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all webhooks",
        responses={200: Webhooks(), 400: ErrorResponse()}
    )
    def get(self, request: Request):
        """
        Retrieve all webhooks.
        """
        webhooks = request.user.webhook_set.all()
        response = self.paginate_queryset(Webhook(webhooks, many=True).data)
        return self.get_paginated_response(response)

    @swagger_auto_schema(
        tags=['Webhooks'],
        operation_id=f"{ENDPOINT_ID}create",
        operation_summary="Create a webhook",
        request_body=WebhookData(),
        responses={200: Webhook(), 400: ErrorResponse()}
    )
    def post(self, request: Request):
        """
        Create a new webhook.
        """
        webhook = SerializerDecorator[WebhookSerializer](data=request.data).save(user=request.user).instance
        return Response(Webhook(webhook).data, status=status.HTTP_201_CREATED)


class WebhookDetail(APIView):

    @swagger_auto_schema(
        tags=['Webhooks'],
        operation_id=f"{ENDPOINT_ID}retrieve",
        operation_summary="Retrieve a webhook",
        responses={200: Webhook(), 400: ErrorResponse()}
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve a webhook.
        """
        webhook = request.user.webhook_set.get(pk=pk)
        return Response(Webhook(webhook).data)

    @swagger_auto_schema(
        tags=['Webhooks'],
        operation_id=f"{ENDPOINT_ID}update",
        operation_summary="Update a webhook",
        request_body=WebhookData(),
        responses={200: Webhook(), 400: ErrorResponse()}
    )
    def patch(self, request: Request, pk: str):
        """
        update a webhook.
        """
        webhook = request.user.webhook_set.get(pk=pk)

        SerializerDecorator[WebhookSerializer](webhook, data=request.data).save()
        return Response(Webhook(webhook).data)

    @swagger_auto_schema(
        tags=['Webhooks'],
        operation_id=f"{ENDPOINT_ID}remove",
        operation_summary="Remove a webhook",
        responses={200: Operation(), 400: ErrorResponse()}
    )
    def delete(self, request: Request, pk: str):
        """
        Remove a webhook.
        """
        webhook = request.user.customs_set.get(pk=pk)

        webhook.delete(keep_parents=True)
        serializer = Operation(dict(operation="Remove webhook", success=True))
        return Response(serializer.data)


router.urls.append(path('webhooks', WebhookList.as_view(), name="webhook-list"))
router.urls.append(path('webhooks/<str:pk>', WebhookDetail.as_view(), name="webhook-details"))
