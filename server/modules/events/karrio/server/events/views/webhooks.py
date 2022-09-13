import logging

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, serializers
from drf_yasg.utils import swagger_auto_schema
from django.urls import path

from karrio.server.core.views.api import GenericAPIView, APIView
from karrio.server.serializers import SerializerDecorator, PaginatedResult, PlainDictField
from karrio.server.core.serializers import Operation, ErrorResponse
from karrio.server.events.serializers import WebhookData, Webhook, WebhookSerializer
from karrio.server.events.task_definitions.base.webhook import notify_subscribers
from karrio.server.events.router import router
from karrio.server.events import models


logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$$$$$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
Webhooks = PaginatedResult("WebhookList", Webhook)


class WebhookTestRequest(serializers.Serializer):
    payload = PlainDictField(required=True)


class WebhookList(GenericAPIView):
    pagination_class = LimitOffsetPagination
    default_limit = 20
    serializer_class = Webhooks

    @swagger_auto_schema(
        tags=["Webhooks"],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all webhooks",
        responses={
            200: Webhooks(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def get(self, request: Request):
        """
        Retrieve all webhooks.
        """
        webhooks = models.Webhook.access_by(request)
        response = self.paginate_queryset(Webhook(webhooks, many=True).data)
        return self.get_paginated_response(response)

    @swagger_auto_schema(
        tags=["Webhooks"],
        operation_id=f"{ENDPOINT_ID}create",
        operation_summary="Create a webhook",
        request_body=WebhookData(),
        responses={
            201: Webhook(),
            400: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def post(self, request: Request):
        """Create a new webhook."""
        webhook = (
            SerializerDecorator[WebhookSerializer](data=request.data, context=request)
            .save()
            .instance
        )

        return Response(Webhook(webhook).data, status=status.HTTP_201_CREATED)


class WebhookDetails(APIView):
    @swagger_auto_schema(
        tags=["Webhooks"],
        operation_id=f"{ENDPOINT_ID}retrieve",
        operation_summary="Retrieve a webhook",
        responses={
            201: Webhook(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def get(self, request: Request, pk: str):
        """
        Retrieve a webhook.
        """
        webhook = models.Webhook.access_by(request).get(pk=pk)
        return Response(Webhook(webhook).data)

    @swagger_auto_schema(
        tags=["Webhooks"],
        operation_id=f"{ENDPOINT_ID}update",
        operation_summary="Update a webhook",
        request_body=WebhookData(),
        responses={
            200: Webhook(),
            404: ErrorResponse(),
            400: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def patch(self, request: Request, pk: str):
        """
        update a webhook.
        """
        webhook = models.Webhook.access_by(request).get(pk=pk)

        SerializerDecorator[WebhookSerializer](webhook, data=request.data).save()
        return Response(Webhook(webhook).data)

    @swagger_auto_schema(
        tags=["Webhooks"],
        operation_id=f"{ENDPOINT_ID}remove",
        operation_summary="Remove a webhook",
        responses={
            200: Operation(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def delete(self, request: Request, pk: str):
        """
        Remove a webhook.
        """
        webhook = models.Webhook.access_by(request).get(pk=pk)

        webhook.delete(keep_parents=True)

        return Response(Webhook(webhook).data)


class WebhookTest(APIView):
    @swagger_auto_schema(
        tags=["Webhooks"],
        operation_id=f"{ENDPOINT_ID}test",
        operation_summary="Test a webhook",
        request_body=WebhookTestRequest(),
        responses={
            200: Operation(),
            400: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def post(self, request: Request, pk: str):
        """
        test a webhook.
        """
        webhook = models.Webhook.access_by(request).get(pk=pk)

        notification, *_ = notify_subscribers([webhook], request.data)
        _, response = notification
        serializer = Operation(dict(operation="Test Webhook", success=response.ok))
        return Response(serializer.data)


router.urls.append(path("webhooks", WebhookList.as_view(), name="webhook-list"))
router.urls.append(
    path("webhooks/<str:pk>", WebhookDetails.as_view(), name="webhook-details")
)
router.urls.append(
    path("webhooks/<str:pk>/test", WebhookTest.as_view(), name="webhook-test")
)
