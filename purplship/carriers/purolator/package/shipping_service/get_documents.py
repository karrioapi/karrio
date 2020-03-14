from pypurolator.shipping_documents_service import (
    GetDocumentsRequestContainer, RequestContext, DocumentCriteria, ArrayOfDocumentCriteria, PIN
)
from purplship.core.utils.soap import Envelope, Body, Header
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.xml import Element
from purplship.core.utils.helpers import export
from purplship.carriers.purolator.utils import Settings


def get_shipping_documents_request(pin: str, settings: Settings) -> Serializable[Element]:
    request = Envelope(
        Header=Header(
            RequestContext(
                Version='1.3',
                Language=settings.language,
                GroupID=None,
                RequestReference=None,
                UserToken=settings.user_token
            )
        ),
        Body=Body(
            GetDocumentsRequestContainer(
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
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: Element) -> str:
    namespace_ = 'xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://purolator.com/pws/datatypes/v1"'
    return export(request, namespacedef_=namespace_)
