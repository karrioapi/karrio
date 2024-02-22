import karrio.schemas.fedex.paperless_request as fedex
import time
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.fedex.error as provider_error
import karrio.providers.fedex.units as provider_units
import karrio.providers.fedex.utils as provider_utils


def parse_document_upload_response(
    _response: lib.Deserializable[typing.List[dict]],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.DocumentUploadDetails, typing.List[models.Message]]:
    responses = _response.deserialize()

    metas = [_["output"]["meta"] for _ in responses if _.get("output", {}).get("meta")]
    details = _extract_details(metas, settings) if len(metas) > 0 else None
    errors = provider_error.parse_error_response([_ for _ in responses], settings)

    return details, errors


def _extract_details(
    metas: typing.List[dict],
    settings: provider_utils.Settings,
) -> models.DocumentUploadDetails:
    return models.DocumentUploadDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_id,
        documents=[
            models.DocumentDetails(
                doc_id=meta["docId"],
                file_name=meta["docId"],
            )
            for meta in metas
        ],
        meta=dict(),
    )


def document_upload_request(
    payload: models.DocumentUploadRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    document_files = lib.to_document_files(payload.document_files)
    options = lib.to_upload_options(
        payload.options,
        provider_units.DocumentUploadOption,
    )
    shipment_date = lib.fdatetime(
        payload.shipment_date or time.strftime("%Y-%m-%d"),
        current_format="%Y-%m-%d",
        output_format="%Y%m%dT%H%M%S",
    )

    request = [
        fedex.PaperlessRequestType(
            document=fedex.DocumentType(
                workflowName=(
                    "ETDPreshipment"
                    if options.pre_shipment.state
                    else "ETDPostshipment"
                ),
                carrierCode=options.fedex_carrier_code.state,
                name=document.doc_name,
                contentType=document.doc_format,
                meta=fedex.MetaType(
                    shipDocumentType=(
                        provider_units.UploadDocumentType.map(document.doc_type).value
                        or provider_units.UploadDocumentType.other.value
                    ),
                    formCode=None,
                    trackingNumber=payload.tracking_number,
                    shipmentDate=shipment_date,
                    originCountryCode=options.origin_country_code.state,
                    destinationCountryCode=options.destination_country_code.state,
                ),
            ),
            attachment=document.doc_file,
        )
        for document in document_files
    ]

    return lib.Serializable(
        request,
        lambda __: [lib.to_dict(_) for _ in __],
    )
