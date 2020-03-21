from pypurolator.shipping_documents_service import (
    GetDocumentsRequest, RequestContext, DocumentCriteria, ArrayOfDocumentCriteria, PIN
)
from purplship.core.utils.soap import Envelope, create_envelope
from purplship.core.models import ShipmentRequest
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.helpers import export
from purplship.carriers.purolator.utils import Settings


def get_shipping_documents_request(pin: str, payload: ShipmentRequest, settings: Settings) -> Serializable[Envelope]:
    request = create_envelope(
        header_content=RequestContext(
            Version='1.3',
            Language=settings.language,
            GroupID=None,
            RequestReference=None,
            UserToken=settings.user_token
        ),
        body_content=GetDocumentsRequest(
            OutputType="PDF",
            Synchronous=True,
            DocumentCriterium=ArrayOfDocumentCriteria(
                DocumentCriteria=[
                    DocumentCriteria(
                        PIN=PIN(Value=pin),
                        DocumentTypes=None
                    )
                ]
            )
        )
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: Envelope) -> str:
    namespacedef_ = 'xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://purolator.com/pws/datatypes/v1"'
    request.ns_prefix_ = "SOAP-ENV"
    request.Body.ns_prefix_ = request.ns_prefix_
    request.Header.ns_prefix_ = request.ns_prefix_
    request.Body.anytypeobjs_[0].ns_prefix_ = "ns1"
    request.Header.anytypeobjs_[0].ns_prefix_ = "ns1"
    return export(request, namespacedef_=namespacedef_)
