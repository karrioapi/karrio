import io
import logging
import base64
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import Serializer, CharField
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import JSONOpenAPIRenderer

from django.urls import path

from drf_yasg.utils import swagger_auto_schema

from purpleserver.core.renderers import BinaryFileRenderer
from purpleserver.core.router import router
from purpleserver.core.serializers import ErrorResponse

logger = logging.getLogger(__name__)


class LabelPrintingRequest(Serializer):
    name = CharField(required=True, help_text="""
    PDF file name.
    
    eg: shipment-[trackingNumber]
    """)
    label = CharField(required=True, help_text="Shipment base64 label")


@swagger_auto_schema(
    methods=['post'],
    tags=['Utils'],
    request_body=LabelPrintingRequest(),
    responses={201: None, 400: ErrorResponse()},
    operation_description="Returns a label PDF file.",
    operation_id="Print Label",
)
@api_view(['POST'])
@renderer_classes([BinaryFileRenderer, JSONOpenAPIRenderer])
def print_label(request: Request):
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


router.urls.append(path('labels', print_label))
