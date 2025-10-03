import logging
import django.urls as urls
import rest_framework.status as status
import rest_framework.request as request
import rest_framework.response as response

import karrio.server.openapi as openapi
import karrio.server.core.views.api as api
import karrio.server.core.serializers as core
import karrio.server.serializers as serializers
import karrio.server.automation.router as router
import karrio.server.automation.models as models
import karrio.server.automation.serializers.models as model_serializers


logger = logging.getLogger(__name__)


class WorkflowTrigger(api.APIView):
    @openapi.extend_schema(
        exclude=True,
        tags=["Workflow"],
        operation_id=f"trigger",
        extensions={"x-operationId": "triggerWorkflow"},
        summary="Trigger a workflow",
        request=serializers.PlainDictField(),
        responses={
            200: core.Operation(),
            400: core.ErrorResponse(),
            500: core.ErrorResponse(),
        },
    )
    def post(self, request: request.Request, pk: str):
        """Trigger a workflow."""
        workflow = models.Workflow.access_by(request).get(pk=pk)
        (
            model_serializers.WorkflowEventModelSerializer.map(
                data=dict(
                    workflow=workflow,
                    parameters=request.data,
                    test_mode=getattr(request, "test_mode", False),
                    event_type=getattr(workflow.trigger, "event_type", "webhook"),
                ),
                context=request,
            ).save()
        )

        serializer = core.Operation(dict(operation="Workflow triggered", success=True))
        return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)


router.router.urls.append(
    urls.path(
        "workflows/<str:pk>/trigger", WorkflowTrigger.as_view(), name="workflow-trigger"
    )
)
