"""Karrio MyDHL document upload API implementation."""

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.mydhl.error as error
import karrio.providers.mydhl.utils as provider_utils
import karrio.providers.mydhl.units as provider_units


# Document type mapping for MyDHL upload-image
DOCUMENT_TYPE_MAP = {
    "commercial_invoice": "CIN",
    "invoice": "INV",
    "proforma": "PNV",
    "certificate_of_origin": "COO",
    "nafta_certificate_of_origin": "NAF",
    "customs_declaration": "DCL",
    "air_waybill": "AWB",
}


def parse_document_upload_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.DocumentUploadDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    ctx = _response.ctx or {}

    # Check for success - MyDHL returns empty response or status on success
    details = lib.identity(
        _extract_details(response, settings, ctx)
        if response.get("status") is None
        else None
    )

    return details, messages


def _extract_details(
    response: dict,
    settings: provider_utils.Settings,
    ctx: dict = None,
) -> models.DocumentUploadDetails:
    ctx = ctx or {}
    return models.DocumentUploadDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        documents=[
            models.DocumentDetails(
                doc_id=ctx.get("tracking_number", "uploaded"),
                file_name=doc.get("doc_name", "document"),
            )
            for doc in ctx.get("documents", [{"doc_name": "document"}])
        ],
        meta=dict(
            tracking_number=ctx.get("tracking_number"),
        ),
    )


def document_upload_request(
    payload: models.DocumentUploadRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a document upload request for MyDHL API.

    MyDHL uses the upload-image endpoint for Paperless Trade (PLT) which accepts
    base64 encoded document images.
    """
    document_files = lib.to_document_files(payload.document_files)
    options = payload.options or {}

    # Get product code and ship date from options
    product_code = options.get("mydhl_product_code") or "P"
    planned_ship_date = lib.fdate(payload.shipment_date)

    # Build document images array
    document_images = [
        dict(
            typeCode=DOCUMENT_TYPE_MAP.get(doc.doc_type, "CIN"),
            imageFormat=(doc.doc_format or "PDF").upper(),
            content=doc.doc_file,
        )
        for doc in document_files
    ]

    # Build the request payload for upload-image endpoint
    request = dict(
        shipmentTrackingNumber=payload.tracking_number,
        originalPlannedShippingDate=planned_ship_date,
        accounts=[
            dict(typeCode="shipper", number=settings.account_number)
        ],
        productCode=product_code,
        documentImages=document_images,
    )

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(
            tracking_number=payload.tracking_number,
            documents=[
                dict(doc_name=doc.doc_name, doc_type=doc.doc_type)
                for doc in document_files
            ],
        ),
    )
