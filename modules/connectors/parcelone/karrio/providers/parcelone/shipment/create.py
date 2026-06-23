"""Karrio ParcelOne shipment creation implementation."""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.parcelone.error as error
import karrio.providers.parcelone.units as provider_units
import karrio.providers.parcelone.utils as provider_utils
import karrio.schemas.parcelone.shipping_request as parcelone
import karrio.schemas.parcelone.shipping_response as shipping


def parse_shipment_response(
    _response: lib.Deserializable[list],
    settings: provider_utils.Settings,
) -> tuple[models.ShipmentDetails | None, list[models.Message]]:
    """Parse N per-parcel shipment responses and aggregate into one ShipmentDetails."""
    responses = _response.deserialize()

    messages = sum(
        [error.parse_error_response(r, settings) for r in responses],
        [],
    )

    items = [
        (f"{i}", details)
        for i, r in enumerate(responses, 1)
        if r.get("success") == 1
        and r.get("results")
        and (details := _extract_details(r, settings, ctx=_response.ctx)) is not None
    ]

    shipment = lib.to_multi_piece_shipment(items) if items else None

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict = None,
) -> models.ShipmentDetails | None:
    """Extract shipment details from a single ParcelOne API response."""
    result = lib.to_object(shipping.ResultsType, data.get("results") or {})

    action = result.ActionResult
    if action is None or action.Success != 1:
        return None

    packages = result.PackageResults or []
    package_tracking_ids = [p.TrackingID for p in packages if p.TrackingID]
    tracking_urls = [p.TrackingURL for p in packages if p.TrackingURL]
    labels = [p.Label for p in packages if p.Label]

    label_format = ctx.get("label_format") if ctx else "PDF"
    outbound_label = lib.bundle_base64(labels, label_format) if len(labels) > 1 else lib.failsafe(lambda: labels[0])

    return_documents = [
        models.ShippingDocument(
            category=d.DocType or "document",
            format=lib.failsafe(lambda d=d: d.Format.Type) or label_format,
            base64=d.Document,
        )
        for d in (result.DocumentsResults or [])
        if d.Document
    ]
    customs_documents = [
        models.ShippingDocument(
            category=d.DocType or "customs_document",
            format=lib.failsafe(lambda d=d: d.Format.Type) or label_format,
            base64=d.Document,
        )
        for d in (result.InternationalDocumentsResults or [])
        if d.Document
    ]

    label = outbound_label or lib.failsafe(lambda: return_documents[0].base64)

    total_charge = lib.failsafe(lambda: float(result.TotalCharges.Value)) if result.TotalCharges else None

    primary_tracking_id = lib.failsafe(lambda: package_tracking_ids[0]) or action.TrackingID

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=primary_tracking_id,
        shipment_identifier=action.ShipmentID or action.TrackingID,
        label_type=label_format,
        docs=models.Documents(
            label=label,
            extra_documents=[*return_documents, *customs_documents],
        ),
        meta=dict(
            parcelOneTrackingID=action.TrackingID,
            parcelOneShipmentID=action.ShipmentID,
            parcelOneShipmentRef=action.ShipmentRef,
            shipment_id=action.ShipmentID,
            shipment_ref=action.ShipmentRef,
            tracking_numbers=package_tracking_ids,
            tracking_urls=tracking_urls,
            label_url=result.LabelURL,
            carrier_tracking_link=settings.tracking_link.format(action.TrackingID or primary_tracking_id),
            total_charge=total_charge,
            currency=lib.failsafe(lambda: result.TotalCharges.Currency) or "EUR",
            return_document_ids=[d.DocumentID for d in (result.DocumentsResults or []) if d.DocumentID] or None,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Build one ShippingRequestType per parcel (Pattern B — per-parcel fan-out)."""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels, required=["weight"])
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    customs = payload.customs
    is_international = shipper.country_code != recipient.country_code

    service = provider_units.ShippingService.map(payload.service)
    service_code = service.value_or_key
    cep_id, product_id = provider_units.parse_service_code(service_code)
    cep_id = cep_id or settings.connection_config.cep_id.state
    product_id = product_id or settings.connection_config.product_id.state

    consigner_id = options.parcelone_consigner_id.state or settings.consigner_id
    mandator_id = options.parcelone_mandator_id.state or settings.mandator_id

    label_format = (
        provider_units.LabelFormat.map(payload.label_type or settings.connection_config.label_format.state).value
        or "PDF"
    )
    label_size = settings.connection_config.label_size.state or "A6"

    is_return = bool(options.is_return.state) or bool(options.parcelone_return_only.state)
    wants_return_label = bool(options.parcelone_return_label.state) and not is_return
    # ReturnShipmentIndicator is UPS-exclusive (Mark Friebus, 2026-06). Non-UPS
    # returns rely on the SRO service; UPS returns use the indicator instead.
    is_ups = cep_id == provider_units.CEP.UPS.value

    profile = lib.failsafe(lambda: settings.profile)
    available_services = set(provider_units.services_for_product(cep_id, product_id, profile=profile))
    force_carrier_label_state = settings.connection_config.force_carrier_label.state
    force_carrier_label = True if force_carrier_label_state is None else bool(force_carrier_label_state)
    auto_lbl = force_carrier_label and cep_id != provider_units.CEP.PA1.value and "LBL" in available_services

    package_services = [
        *(
            [
                parcelone.ServiceType(
                    ServiceID="COD",
                    Value=parcelone.MaxChargesType(
                        Value=str(options.parcelone_cod.state),
                        Currency=options.parcelone_cod_currency.state or "EUR",
                    ),
                )
            ]
            if options.parcelone_cod.state
            else []
        ),
        *(
            [
                parcelone.ServiceType(
                    ServiceID="EI",
                    Value=parcelone.MaxChargesType(
                        Value=str(options.parcelone_insurance.state),
                        Currency=options.parcelone_insurance_currency.state or "EUR",
                    ),
                )
            ]
            if options.parcelone_insurance.state
            else []
        ),
        *([parcelone.ServiceType(ServiceID="BSC")] if options.parcelone_bulky_goods.state else []),
        *([parcelone.ServiceType(ServiceID="SRL")] if wants_return_label else []),
        *([parcelone.ServiceType(ServiceID="SRO")] if (is_return and not is_ups) else []),
        *([parcelone.ServiceType(ServiceID="LBL")] if auto_lbl else []),
        *([parcelone.ServiceType(ServiceID="SIG")] if options.parcelone_signature.state else []),
        *([parcelone.ServiceType(ServiceID="SDO")] if options.parcelone_saturday_delivery.state else []),
        *(
            [
                parcelone.ServiceType(
                    ServiceID="MAIL",
                    Parameters=options.parcelone_notification_email.state,
                )
            ]
            if options.parcelone_notification_email.state
            else []
        ),
        *(
            [
                parcelone.ServiceType(
                    ServiceID="SMS",
                    Parameters=options.parcelone_notification_sms.state,
                )
            ]
            if options.parcelone_notification_sms.state
            else []
        ),
    ]

    multi_parcel = len(packages) > 1
    cn_form_size = lib.failsafe(lambda: (customs.options or {}).get("cn_form_size")) or "CN23"

    def _shipment_ref(index: int) -> str:
        return (
            f"{lib.text(payload.reference, max=17)}-{index}"
            if payload.reference and multi_parcel
            else lib.text(payload.reference, max=20)
        )

    requests = [
        parcelone.ShippingRequestType(
            ShippingData=parcelone.ShippingDataType(
                ShipmentRef=_shipment_ref(index),
                CEPID=cep_id,
                ProductID=product_id,
                MandatorID=mandator_id,
                ConsignerID=consigner_id,
                ShipToData=parcelone.ShipToDataType(
                    Reference=_shipment_ref(index),
                    BranchID=options.parcelone_branch_id.state,
                    Name1=recipient.company_name or recipient.person_name,
                    Name2=recipient.person_name if recipient.company_name else None,
                    ShipmentAddress=parcelone.ShipmentAddressType(
                        Street=recipient.street,
                        Streetno=recipient.street_number,
                        PostalCode=recipient.postal_code,
                        City=recipient.city,
                        State=recipient.state_code,
                        Country=recipient.country_code,
                    ),
                    ShipmentContact=parcelone.ShipmentContactType(
                        Email=recipient.email,
                        Phone=provider_units.compact_phone(recipient.phone_number),
                        AttentionName=recipient.person_name,
                    ),
                    PrivateAddressIndicator=1 if recipient.residential else 0,
                ),
                ShipFromData=parcelone.ShipFromDataType(
                    Name1=shipper.company_name or shipper.person_name,
                    Name2=shipper.person_name if shipper.company_name else None,
                    ShipmentAddress=parcelone.ShipmentAddressType(
                        Street=shipper.street,
                        Streetno=shipper.street_number,
                        PostalCode=shipper.postal_code,
                        City=shipper.city,
                        State=shipper.state_code,
                        Country=shipper.country_code,
                    ),
                    ShipmentContact=parcelone.ShipmentContactType(
                        Email=shipper.email,
                        Phone=provider_units.compact_phone(shipper.phone_number),
                    ),
                ),
                ReturnShipmentIndicator=(
                    (lib.to_int(options.parcelone_return_indicator.state) or 9) if (is_return and is_ups) else 0
                ),
                PrintLabel=1,
                LabelFormat=parcelone.FormatType(
                    Type=label_format,
                    Size=label_size,
                    Orientation=0,
                ),
                PrintDocuments=1 if is_international else 0,
                DocumentFormat=(parcelone.FormatType(Type=label_format, Orientation=0) if is_international else None),
                Software=settings.connection_app_identifier,
                Packages=[
                    parcelone.PackageType(
                        PackageRef=pkg.parcel.id or str(index),
                        PackageWeight=parcelone.PackageVolumeClassType(
                            Value=str(pkg.weight.KG),
                            Unit="kg",
                        ),
                        PackageDimensions=(
                            parcelone.PackageDimensionsType(
                                Length=str(pkg.length.CM),
                                Width=str(pkg.width.CM),
                                Height=str(pkg.height.CM),
                            )
                            if pkg.length.CM and pkg.width.CM and pkg.height.CM
                            else None
                        ),
                        IntDocData=(
                            parcelone.IntDocDataType(
                                Invoice=1 if customs.invoice else None,
                                InvoiceNo=customs.invoice,
                                ConsignerCustomsID=(
                                    lib.failsafe(lambda: customs.duty.account_number)
                                    or lib.failsafe(lambda: (customs.options or {}).get("consigner_customs_id"))
                                ),
                                PrintInternationalDocuments=1,
                                InternationalDocumentFormat=parcelone.FormatType(
                                    Type=label_format,
                                    Size=cn_form_size,
                                    Orientation=0,
                                ),
                                ShipToRef=_shipment_ref(index),
                                ItemCategory=lib.identity(
                                    4
                                    if is_return
                                    else provider_units.CustomsContentType.map(
                                        lib.failsafe(lambda: customs.content_type)
                                    ).value
                                    or provider_units.CustomsContentType.merchandise.value
                                ),
                                Postage=0.0,
                                TotalValue=lib.failsafe(
                                    lambda: round(
                                        sum(
                                            (c.value_amount or 0) * (c.quantity or 1)
                                            for c in (customs.commodities or [])
                                        ),
                                        2,
                                    )
                                ),
                                Currency=(
                                    lib.failsafe(lambda: customs.duty.currency) or options.currency.state or "EUR"
                                ),
                                TotalWeightkg=lib.failsafe(lambda p=pkg: float(p.weight.KG)),
                                CustomDetails=[
                                    parcelone.CustomDetailType(
                                        Contents=item.description or item.title,
                                        Quantity=item.quantity,
                                        ItemValuePerItem=item.value_amount,
                                        NetWeightPerItem=lib.units.Weight(item.weight, item.weight_unit or "KG").KG,
                                        Origin=item.origin_country,
                                        TariffNumber=item.hs_code,
                                        AdditionalInfo=[
                                            parcelone.CepSpecialType(Key=key, Value=value)
                                            for key, value in provider_units.additional_info_for_commodity(item)
                                        ],
                                    )
                                    for item in (customs.commodities or [])
                                ]
                                if customs.commodities
                                else None,
                            )
                            if is_international and customs
                            else None
                        ),
                        Services=package_services,
                        Remarks=(
                            (pkg.parcel.content or pkg.parcel.description or "Goods")
                            if (is_return and is_ups)
                            else None
                        ),
                    )
                ],
            ),
        )
        for index, pkg in enumerate(packages, 1)
    ]

    return lib.Serializable(
        requests,
        lib.to_dict,
        dict(label_format=label_format),
    )
