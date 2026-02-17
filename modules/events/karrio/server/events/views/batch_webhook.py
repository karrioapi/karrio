import logging

from django.urls import path
from django.utils import timezone
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, serializers

import karrio.server.openapi as openapi
from karrio.server.core.views.api import APIView
from karrio.server.core.serializers import ErrorResponse
from karrio.server.core import utils
from karrio.server.conf import settings
from karrio.server.events.router import router
import karrio.server.core.serializers as core_serializers
import karrio.server.manager.models as manager_models
import karrio.server.events.tasks as tasks
import karrio.server.events.models as event_models
import karrio.server.events.serializers.event as event_serializers
from karrio.server.events.task_definitions.base.webhook import notify_subscribers


logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$$$$$$$"  # Unique endpoint id for operation ids


OBJECT_TYPE_MAP = {
    "tracker": {
        "model": lambda: manager_models.Tracking,
        "serializer": lambda instance: core_serializers.TrackingStatus(instance).data,
        "event_type": "tracker_updated",
    },
    "shipment": {
        "model": lambda: manager_models.Shipment,
        "serializer": lambda instance: core_serializers.Shipment(instance).data,
        "event_type": "shipment_purchased",
    },
}


class BatchWebhookResendRequest(serializers.Serializer):
    entity_ids = serializers.ListField(
        child=serializers.CharField(), required=True
    )
    object_type = serializers.ChoiceField(
        choices=["tracker", "shipment"],
        default="tracker",
        required=False,
    )
    webhook_id = serializers.CharField(required=False)


class BatchWebhookResource(serializers.Serializer):
    id = serializers.CharField()
    status = serializers.ChoiceField(choices=["queued", "failed"])
    error = serializers.CharField(required=False, allow_null=True)


class BatchWebhookResendResponse(serializers.Serializer):
    object_type = serializers.CharField()
    resources = BatchWebhookResource(many=True)
    count = serializers.IntegerField()
    test_mode = serializers.BooleanField()
    created_at = serializers.DateTimeField()


class BatchWebhookResend(APIView):

    @openapi.extend_schema(
        tags=["Batches"],
        operation_id=f"{ENDPOINT_ID}resend_webhooks",
        extensions={"x-operationId": "resendWebhooks"},
        summary="Resend webhooks",
        request=BatchWebhookResendRequest(),
        responses={
            200: BatchWebhookResendResponse(),
            400: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def post(self, request: Request):
        """
        Resend webhook notifications for a batch of entities.
        """
        serializer = BatchWebhookResendRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        entity_ids = serializer.validated_data["entity_ids"]
        object_type = serializer.validated_data.get("object_type", "tracker")
        webhook_id = serializer.validated_data.get("webhook_id")

        type_config = OBJECT_TYPE_MAP.get(object_type)
        if type_config is None:
            return Response(
                ErrorResponse(
                    dict(errors=[dict(message=f"Unsupported object type: {object_type}")])
                ).data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        model = type_config["model"]()
        entities = model.access_by(request).filter(pk__in=entity_ids)
        resources = []

        # Pre-fetch targeted webhook once if specified
        webhook = None
        if webhook_id:
            webhook = event_models.Webhook.access_by(request).get(pk=webhook_id)

        for instance in entities:
            try:
                data = type_config["serializer"](instance)
                event = type_config["event_type"]
                event_at = instance.updated_at
                context = dict(
                    user_id=utils.failsafe(lambda: instance.created_by.id),
                    test_mode=instance.test_mode,
                    org_id=utils.failsafe(
                        lambda: instance.org.first().id
                        if hasattr(instance, "org")
                        else None
                    ),
                )

                if webhook:
                    event_serializers.EventSerializer.map(
                        data=dict(
                            type=event,
                            data=data,
                            test_mode=context.get("test_mode", False),
                            pending_webhooks=1,
                        ),
                        context=request,
                    ).save()
                    payload = dict(event=event, data=data)
                    notify_subscribers([webhook], payload)
                else:
                    tasks.notify_webhooks(
                        event, data, event_at, context, schema=settings.schema
                    )

                resources.append(dict(id=instance.pk, status="queued", error=None))
            except (serializers.ValidationError, ValueError, KeyError) as e:
                logger.warning(
                    "Failed to resend webhook for entity",
                    entity_id=str(instance.pk),
                    error=str(e),
                )
                resources.append(dict(id=instance.pk, status="failed", error=str(e)))

        # Mark any entity_ids not found in the queryset
        found_ids = {str(r["id"]) for r in resources}
        resources.extend([
            dict(id=eid, status="failed", error="Not found")
            for eid in entity_ids
            if eid not in found_ids
        ])

        response_data = dict(
            object_type=object_type,
            resources=resources,
            count=len([r for r in resources if r["status"] == "queued"]),
            test_mode=getattr(request, "test_mode", False),
            created_at=timezone.now(),
        )

        return Response(
            BatchWebhookResendResponse(response_data).data,
            status=status.HTTP_200_OK,
        )


router.urls.append(
    path(
        "batches/webhooks",
        BatchWebhookResend.as_view(),
        name="batch-webhook-resend",
    )
)
