"""GLS Customs Document Management — paperless trade upload.

The unified ``Document.upload`` flow on GLS does a three-step chain inside
``proxy.upload_document``:

1. POST ``/document-management/v1/documents/customs/prepare-upload`` per file
   → ``{documentId, uploadURL}``
2. PUT the binary PDF to ``uploadURL`` (no auth, 15-min validity)
3. POST ``/customs-management/.../v3/customs-consignments`` with
   ``parcelNumbers`` (the GLS TrackID from ``payload.tracking_number``)
   + ``linkedDocuments`` (the documentIds returned in step 1) — only when
   the upload request carries a customs payload in ``payload.options``.

The manager's ``upload_customs_forms`` populates ``payload.options`` with
the shipper / recipient / customs payload + the GLS TrackID so the
provider can shape the v3 envelope without DB access.
"""

import karrio.core.models as models
import karrio.core.units as core_units
import karrio.lib as lib
import karrio.providers.gls.error as error
import karrio.providers.gls.units as provider_units
import karrio.providers.gls.utils as provider_utils


def parse_document_upload_response(
    _response: lib.Deserializable,
    settings: provider_utils.Settings,
) -> tuple[models.DocumentUploadDetails | None, list[models.Message]]:
    """Collect documentIds from the prepare-upload responses (one per file)."""
    response = _response.deserialize()
    responses = response if isinstance(response, list) else [response]

    messages: list[models.Message] = []
    for body in responses:
        messages.extend(error.parse_error_response(body, settings))

    documents = [
        models.DocumentDetails(
            doc_id=body.get("documentId"),
            file_name=body.get("displayFileName") or body.get("documentId") or "",
        )
        for body in responses
        if isinstance(body, dict) and body.get("documentId")
    ]
    details = lib.identity(
        models.DocumentUploadDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            documents=documents,
            meta=dict(),
        )
        if documents
        else None
    )

    return details, messages


def document_upload_request(
    payload: models.DocumentUploadRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Build a Customs Document Management v1 upload batch.

    GLS uses a two-step upload: a JSON ``prepare-upload`` call per document
    returns a per-document ``uploadURL`` that we then PUT the binary to.
    The proxy carries out both legs; here we just emit one JSON envelope
    per ``DocumentFile`` and stash the binary on ``request.ctx`` so the
    proxy can stream it to the returned URL.
    """
    document_files = lib.to_document_files(payload.document_files)

    request = [
        dict(
            attributes=dict(
                documentType=(
                    provider_units.UploadDocumentType.map(document.doc_type).value
                    or provider_units.UploadDocumentType.commercial_invoice.value
                ),
                documentFormat=(document.doc_format or "pdf").lower(),
                displayFileName=document.doc_name,
            )
        )
        for document in document_files
    ]

    options = payload.options or {}
    customs_consignment = _build_customs_consignment_from_options(payload, settings, options)

    return lib.Serializable(
        request,
        lambda payloads: [lib.to_dict(payload) for payload in payloads],
        ctx=dict(
            files=[
                dict(
                    doc_file=document.doc_file,
                    doc_name=document.doc_name,
                    doc_format=(document.doc_format or "pdf").lower(),
                )
                for document in document_files
            ],
            tracking_number=payload.tracking_number,
            customs_consignment=customs_consignment,
        ),
    )


def _build_customs_consignment_from_options(payload, settings, options: dict):
    """If the manager passed shipper / recipient / customs through ``options``,
    shape them into a ``CustomsConsignmentRequestType`` so the proxy can fire
    the v3 leg after the prepare-upload + PUT chain. Returns ``None`` when no
    customs payload was provided (the proxy then skips the v3 leg)."""
    customs_dict = options.get("customs")
    if not customs_dict:
        return None

    shipper_model = lib.to_object(models.Address, options.get("shipper") or {})
    recipient_model = lib.to_object(models.Address, options.get("recipient") or {})
    shipper = lib.to_address(shipper_model)
    recipient = lib.to_address(recipient_model)
    customs = lib.to_customs_info(
        lib.to_object(models.Customs, customs_dict),
        shipper=shipper_model,
        recipient=recipient_model,
        weight_unit=provider_units.WeightUnit.KG.name,
    )

    is_international = provider_units.is_international(shipper.country_code, recipient.country_code)
    incoterm = (customs_dict.get("incoterm") if isinstance(customs_dict, dict) else None) or (
        "DDU" if is_international else None
    )
    incoterm_code = lib.identity(provider_units.Incoterm.map(incoterm).value if incoterm else None)
    default_currency = lib.identity(
        options.get("currency") or core_units.CountryCurrency.map(shipper.country_code).value or "EUR"
    )

    return provider_units.build_customs_consignment_request(
        # ``payload`` here is a DocumentUploadRequest; the builder only reads
        # ``.reference`` off it (the manager sets that to the shipment id /
        # tracking number). The customs options dict is passed explicitly
        # because DocumentUploadRequest has no ``.customs`` attribute.
        payload=payload,
        customs=customs,
        shipper=shipper,
        recipient=recipient,
        incoterm_code=incoterm_code,
        default_currency=default_currency,
        customs_opts=(customs_dict.get("options") or {}) if isinstance(customs_dict, dict) else {},
    )
