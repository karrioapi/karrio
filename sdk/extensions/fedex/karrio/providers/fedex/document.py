import fedex_lib.upload_document_service_v17 as fedex
import base64
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.fedex.error as provider_error
import karrio.providers.fedex.units as provider_units
import karrio.providers.fedex.utils as provider_utils


def parse_document_upload_response(
    response: lib.Element,
    settings: provider_utils.Settings,
) -> typing.Tuple[models.DocumentUploadDetails, typing.List[models.Message]]:
    errors = provider_error.parse_error_response(response, settings)
    document_statuses = lib.find_element(
        "DocumentStatuses", response, fedex.UploadDocumentStatusDetail
    )

    details = (
        _extract_details(document_statuses, settings)
        if len(document_statuses) > 0
        else None
    )

    return details, errors


def _extract_details(
    document_statuses: typing.List[fedex.UploadDocumentStatusDetail],
    settings: provider_utils.Settings,
) -> models.DocumentUploadDetails:
    return models.DocumentUploadDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_id,
        documents=[
            models.DocumentDetails(
                document_id=status.DocumentId,
                file_name=status.FileName,
            )
            for status in document_statuses
            if status.Status == "SUCCESS"
        ],
        meta=dict(),
    )


def document_upload_request(
    payload: models.DocumentUploadRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable[lib.Envelope]:
    document_files = lib.to_document_files(payload.document_files)
    options = lib.to_upload_options(
        payload.options,
        provider_units.DocumentUploadOption,
    )

    request = lib.create_envelope(
        body_content=fedex.UploadDocumentsRequest(
            WebAuthenticationDetail=settings.webAuthenticationDetail,
            ClientDetail=settings.clientDetail,
            UserDetail=None,
            TransactionDetail=fedex.TransactionDetail(
                CustomerTransactionId="Upload Documents",
            ),
            Version=fedex.VersionId(
                ServiceId="cdus", Major=19, Intermediate=0, Minor=0
            ),
            ApplicationId=None,
            ServiceLevel=None,
            ProcessingOptions=fedex.UploadDocumentsProcessingOptionsRequested(
                Options=None,
                PostShipmentUploadDetail=fedex.PostShipmentUploadDetail(
                    TrackingNumber=payload.tracking_number,
                ),
            ),
            OriginCountryCode=options.origin_country_code.state,
            OriginStateOrProvinceCode=None,
            OriginPostalCode=options.origin_postal_code.state,
            OriginLocationId=None,
            DestinationCountryCode=options.destination_country_code.state,
            DestinationStateOrProvinceCode=None,
            DestinationPostalCode=options.destination_postal_code.state,
            DestinationLocationId=None,
            FolderId=None,
            ShipTimestamp=None,
            CarrierCode=None,
            Usage=None,
            Documents=[
                fedex.UploadDocumentDetail(
                    LineNumber=index,
                    CustomerReference=payload.reference,
                    DocumentProducer=(
                        options.fedex_document_producer.state
                        or fedex.UploadDocumentProducerType.CUSTOMER
                    ),
                    DocumentType=(
                        provider_units.UploadDocumentType.map(document.doc_type).value
                        or fedex.UploadDocumentType.OTHER
                    ),
                    FileName=document.doc_name,
                    DocumentContent=base64.b64decode(document.doc_file),
                    ExpirationDate=options.fedex_expiration_date.state,
                )
                for index, document in enumerate(document_files, start=1)
            ],
        )
    )

    return lib.Serializable(
        request,
        lambda _: (
            provider_utils.default_request_serializer("v19", 'xmlns:v19="http://fedex.com/ws/uploaddocument/v19"')(_)
            .replace("<v19:DocumentContent>b'", "<v19:DocumentContent>")
            .replace("'</v19:DocumentContent>", "</v19:DocumentContent>")
        ),
    )
