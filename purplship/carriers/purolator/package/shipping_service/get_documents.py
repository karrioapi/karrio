from pypurolator.shipping_documents_service_1_3_0 import (
    GetDocumentsRequest,
    RequestContext,
    DocumentCriteria,
    ArrayOfDocumentCriteria,
    PIN,
)
from purplship.core.utils.soap import Envelope, create_envelope
from purplship.core.models import ShipmentRequest
from purplship.core.utils.serializable import Serializable
from purplship.carriers.purolator.utils import Settings, standard_request_serializer


def get_shipping_documents_request(
    pin: str, payload: ShipmentRequest, settings: Settings
) -> Serializable[Envelope]:
    request = create_envelope(
        header_content=RequestContext(
            Version="1.3",
            Language=settings.language,
            GroupID="",
            RequestReference="",
            UserToken=settings.user_token,
        ),
        body_content=GetDocumentsRequest(
            OutputType="PDF",
            Synchronous=True,
            DocumentCriterium=ArrayOfDocumentCriteria(
                DocumentCriteria=[
                    DocumentCriteria(PIN=PIN(Value=pin), DocumentTypes=None)
                ]
            ),
        ),
    )
    return Serializable(request, standard_request_serializer)
