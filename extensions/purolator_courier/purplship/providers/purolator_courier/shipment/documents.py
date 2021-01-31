from purolator_lib.shipping_documents_service_1_3_0 import (
    GetDocumentsRequest,
    RequestContext,
    DocumentCriteria,
    ArrayOfDocumentCriteria,
    PIN,
)
from purplship.core.utils.soap import Envelope, create_envelope, apply_namespaceprefix
from purplship.core.models import ShipmentRequest
from purplship.core.utils import Serializable, XP
from purplship.providers.purolator_courier.units import LabelType
from purplship.providers.purolator_courier.utils import Settings


def get_shipping_documents_request(
    pin: str, payload: ShipmentRequest, settings: Settings
) -> Serializable[Envelope]:
    label_format = LabelType[payload.label_type or 'PDF'].name

    request = create_envelope(
        header_content=RequestContext(
            Version="1.3",
            Language=settings.language,
            GroupID="",
            RequestReference="",
            UserToken=settings.user_token,
        ),
        body_content=GetDocumentsRequest(
            OutputType=label_format,
            Synchronous=True,
            DocumentCriterium=ArrayOfDocumentCriteria(
                DocumentCriteria=[
                    DocumentCriteria(PIN=PIN(Value=pin), DocumentTypes=None)
                ]
            ),
        ),
    )
    return Serializable(request, _request_serializer)


def _request_serializer(envelope: Envelope) -> str:
    namespacedef_ = 'xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v1="http://purolator.com/pws/datatypes/v1"'
    envelope.ns_prefix_ = "soap"
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    envelope.Header.ns_prefix_ = envelope.ns_prefix_
    apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "v1")
    apply_namespaceprefix(envelope.Header.anytypeobjs_[0], "v1")
    return XP.export(envelope, namespacedef_=namespacedef_)
