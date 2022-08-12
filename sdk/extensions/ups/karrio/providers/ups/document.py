from ups_lib.document_upload_response import FormsHistoryDocumentIDType
import ups_lib.document_upload_request as ups

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.ups.error as provider_error
import karrio.providers.ups.units as provider_units
import karrio.providers.ups.utils as provider_utils


def parse_document_upload_response(
    responses: typing.List[typing.Tuple[str, dict]],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.DocumentUploadDetails, typing.List[models.Message]]:
    raw_documents = [
        (name, result["UploadResponse"]["FormsHistoryDocumentID"])
        for name, result in responses
        if "UploadResponse" in result
        and result["UploadResponse"].get("FormsHistoryDocumentID") is not None
    ]
    messages: typing.List[models.Message] = sum(
        [
            provider_error.parse_rest_error_response(
                [
                    *(  # get errors from the response object returned by UPS
                        result["response"].get("errors", [])
                        if "response" in result
                        else []
                    ),
                    *(  # get warnings from the trackResponse object returned by UPS
                        result["UploadResponse"]["FormsHistoryDocumentID"].get(
                            "warnings", []
                        )
                        if "UploadResponse" in result
                        else []
                    ),
                ],
                settings,
                dict(file_name=file_name),
            )
            for file_name, result in responses
        ],
        [],
    )

    details = _extract_details(raw_documents, settings)

    return details, messages


def _extract_details(
    raw_documents: typing.List[typing.Tuple[str, dict]],
    settings: provider_utils.Settings,
) -> models.DocumentUploadDetails:
    documents: typing.List[typing.Tuple[str, FormsHistoryDocumentIDType]] = [
        (name, lib.to_object(FormsHistoryDocumentIDType, doc))
        for name, doc in raw_documents
    ]

    return models.DocumentUploadDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_id,
        documents=[
            models.DocumentDetails(
                document_id=doc.DocumentID,
                file_name=name,
            )
            for name, doc in documents
        ],
        meta=dict(),
    )


def document_upload_request(
    payload: models.DocumentUploadRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable[lib.Envelope]:
    document_files = lib.to_document_files(payload.document_files)
    options = lib.to_upload_options(payload.options)

    request = [
        ups.DocumentUploadRequestType(
            UPSSecurity=ups.UPSSecurityType(
                UsernameToken=ups.UsernameTokenType(
                    Username=settings.username,
                    Password=settings.password,
                ),
                ServiceAccessToken=ups.ServiceAccessTokenType(
                    AccessLicenseNumber=settings.access_license_number,
                ),
            ),
            UploadRequest=ups.UploadRequestType(
                ShipperNumber=(
                    options.ups_shipper_number.state or settings.account_number
                ),
                UserCreatedForm=ups.UserCreatedFormType(
                    UserCreatedFormFileName=document.doc_name,
                    UserCreatedFormFileFormat=document.doc_format,
                    UserCreatedFormDocumentType=provider_units.UploadDocumentType.map(
                        document.doc_type or units.UploadDocumentType.other.value
                    ).value,
                    UserCreatedFormFile=document.doc_file,
                ),
            ),
        )
        for document in document_files
    ]

    return lib.Serializable(request, lib.to_dict)
