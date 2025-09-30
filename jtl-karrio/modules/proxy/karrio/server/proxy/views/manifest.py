import logging
import django.urls as urls
import rest_framework.status as status
import rest_framework.request as request
import rest_framework.response as response

import karrio.server.openapi as openapi
import karrio.server.core.views.api as api
import karrio.server.proxy.router as router
import karrio.server.core.gateway as gateway
import karrio.server.core.serializers as serializers

logger = logging.getLogger(__name__)
ENDPOINT_ID = "@@@$"  # This endpoint id is used to make operation ids unique make sure not to duplicate

DESCRIPTION = """
Some carriers require shipment manifests to be created for pickups and dropoff.
Creating a manifest for a shipment also kicks off billing as a commitment or confirmation of the shipment.
"""


class ManifestingAPI(api.APIView):
    throttle_scope = "carrier_request"

    @openapi.extend_schema(
        tags=["Proxy"],
        operation_id=f"{ENDPOINT_ID}generate_manifest",
        extensions={"x-operationId": "generateManifest"},
        summary="Create a manifest",
        description=DESCRIPTION,
        responses={
            200: serializers.ManifestResponse(),
            400: serializers.ErrorResponse(),
            424: serializers.ErrorMessages(),
            500: serializers.ErrorResponse(),
        },
        request=serializers.ManifestRequest(),
    )
    def post(self, request: request.Request):
        payload = serializers.ManifestRequest.map(data=request.data).data

        manifest = gateway.Manifests.create(payload, context=request)

        return response.Response(
            serializers.ManifestResponse(manifest).data, status=status.HTTP_200_OK
        )


router.router.urls.append(
    urls.path(
        "proxy/manifest",
        ManifestingAPI.as_view(),
        name="shipment-manifest",
    )
)
