import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.mydhl.error as error
import karrio.providers.mydhl.utils as provider_utils
import karrio.providers.mydhl.units as provider_units


def parse_document_upload_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.DocumentUploadDetails, typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    details = _extract_details(response, settings)

    return details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.DocumentUploadDetails:
    documents: list = []  # documents ids and name extraction

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

    # map data to convert karrio model to mydhl specific type
    request = None

    return lib.Serializable(request, lib.to_dict)
