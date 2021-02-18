import io
import logging
import base64
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import Serializer, CharField
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import JSONOpenAPIRenderer
from drf_yasg.utils import swagger_auto_schema
from django.urls import path

from purpleserver.core.views.api import APIView
from purpleserver.core.renderers import BinaryFileRenderer
from purpleserver.core.router import router
from purpleserver.core.serializers import ErrorResponse

logger = logging.getLogger(__name__)
ENDPOINT_ID = "&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate


class LabelPrintingRequest(Serializer):
    name = CharField(required=True, help_text="""
    PDF file name.
    
    eg: shipment-[trackingNumber]
    """)
    label = CharField(required=True, help_text="Shipment base64 label")


class Utils(APIView):
    logging_methods = []
    renderer_classes = [BinaryFileRenderer, JSONOpenAPIRenderer]

    @swagger_auto_schema(
        tags=['Utils'],
        operation_id=f"{ENDPOINT_ID}print_label",
        operation_summary="Print a Label",
        operation_description="Returns a label PDF file.",
        request_body=LabelPrintingRequest(),
        responses={201: None, 400: ErrorResponse()},
    )
    def post(self, request: Request):
        try:
            try:
                print_request = LabelPrintingRequest(data=request.data)
                print_request.is_valid(raise_exception=True)

                content = base64.b64decode(request.data["label"])
                buffer = io.BytesIO()
                buffer.write(content)

                return Response(
                    buffer.getvalue(),
                    headers={'Content-Disposition': f'attachment; filename="{request.data["name"]}.pdf"'},
                    content_type='application/pdf'
                )
            except ValidationError as ve:
                logger.exception(ve)
                return Response(ve.args, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


router.urls.append(path('labels', Utils.as_view(), name="print-label"))
