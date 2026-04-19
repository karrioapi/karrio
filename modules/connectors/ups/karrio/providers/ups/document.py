import karrio.core.models as models
import karrio.core.units as units
import karrio.lib as lib
import karrio.providers.ups.error as error
import karrio.providers.ups.units as provider_units
import karrio.providers.ups.utils as provider_utils
import karrio.schemas.ups.document_upload_request as ups
from karrio.schemas.ups.document_upload_response import FormsHistoryDocumentIDType


def parse_document_upload_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> tuple[models.DocumentUploadDetails, list[models.Message]]:
    response = _response.deserialize()
    raw_documents = response.get("UploadResponse", {}).get("FormsHistoryDocumentID")
    details = _extract_details(raw_documents, settings) if raw_documents else None
    messages: list[models.Message] = error.parse_error_response(
        response,
        settings=settings,
    )

    return details, messages


def _extract_details(
    raw_documents: list[dict] | dict,
    settings: provider_utils.Settings,
) -> models.DocumentUploadDetails:
    documents: list[FormsHistoryDocumentIDType] = [
        lib.to_object(FormsHistoryDocumentIDType, doc)
        for doc in (raw_documents if isinstance(raw_documents, list) else [raw_documents])
    ]

    return models.DocumentUploadDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_id,
        documents=[
            models.DocumentDetails(
                doc_id=doc.DocumentID,
                file_name=doc.DocumentID,
            )
            for doc in documents
        ],
        meta=dict(),
    )


def document_upload_request(
    payload: models.DocumentUploadRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    document_files = lib.to_document_files(payload.document_files)
    options = lib.to_upload_options(payload.options)

    request = ups.DocumentUploadRequestType(
        UploadRequest=ups.UploadRequestType(
            Request=ups.RequestType(TransactionReference="document upload"),
            ShipperNumber=(options.ups_shipper_number.state or settings.account_number),
            UserCreatedForm=[
                ups.UserCreatedFormType(
                    UserCreatedFormFileName=document.doc_name,
                    UserCreatedFormFileFormat=document.doc_format,
                    UserCreatedFormDocumentType=provider_units.UploadDocumentType.map(
                        document.doc_type or units.UploadDocumentType.other.value
                    ).value,
                    UserCreatedFormFile=document.doc_file,
                )
                for document in document_files
            ],
        ),
    )

    return lib.Serializable(request, lib.to_dict)
