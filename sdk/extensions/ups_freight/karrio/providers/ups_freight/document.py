
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.ups_freight.error as error
import karrio.providers.ups_freight.utils as provider_utils
import karrio.providers.ups_freight.units as provider_units


def parse_document_upload_response(
    response: dict,
    settings: provider_utils.Settings,
) -> typing.Tuple[models.DocumentUploadDetails, typing.List[models.Message]]:
    response_messages = []  # extract carrier response errors and messages
    response_details = []  # extract carrier response details

    messages = error.parse_error_response(response_messages, settings)
    details = _extract_details(response_details, settings)

    return details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.DocumentUploadDetails:
    documents = []  # documents ids and name extraction

    return models.DocumentUploadDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_id,
        documents=[
            models.DocumentDetails(
                document_id="doc_id",
                file_name="file_name",
            )
            for doc in documents
        ],
        meta=dict(),
    )


def document_upload_request(
    payload: models.DocumentUploadRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:

    request = None  # map data to convert karrio model to ups_freight specific type

    return lib.Serializable(request)
