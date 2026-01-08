"""Karrio ParcelOne shipment creation implementation."""

import typing
import karrio.schemas.parcelone as parcelone
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.parcelone.error as error
import karrio.providers.parcelone.utils as provider_utils
import karrio.providers.parcelone.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.ShipmentDetails], typing.List[models.Message]]:
    """Parse shipment creation response from ParcelOne REST API."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    shipment = lib.identity(
        _extract_details(response, settings, ctx=_response.ctx)
        if response.get("success") == 1 and response.get("results")
        else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict = None,
) -> typing.Optional[models.ShipmentDetails]:
    """Extract shipment details from API response."""
    result = lib.to_object(parcelone.ShipmentResultType, data.get("results") or {})

    # Check action result for success
    action = result.ActionResult
    if action is None or action.Success != 1:
        return None

    # Get tracking IDs from package results
    packages = result.PackageResults or []
    tracking_ids = [p.TrackingID for p in packages if p.TrackingID]
    tracking_urls = [p.TrackingURL for p in packages if p.TrackingURL]

    # Get labels from package results - use list comprehension
    labels = [p.Label for p in packages if p.Label]

    # Bundle labels if multiple, otherwise use single label
    label_format = ctx.get("label_format") if ctx else "PDF"
    label = lib.bundle_base64(labels, label_format) if len(labels) > 1 else lib.failsafe(lambda: labels[0])

    # Calculate total charges if available
    total_charge = lib.failsafe(lambda: float(result.TotalCharges.Value)) if result.TotalCharges else None

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=action.TrackingID or lib.failsafe(lambda: tracking_ids[0]),
        shipment_identifier=action.ShipmentID or action.TrackingID,
        label_type=label_format,
        docs=models.Documents(label=label),
        meta=dict(
            shipment_id=action.ShipmentID,
            shipment_ref=action.ShipmentRef,
            tracking_numbers=tracking_ids,
            tracking_urls=tracking_urls,
            label_url=result.LabelURL,
            carrier_tracking_link=settings.tracking_link.format(
                action.TrackingID or lib.failsafe(lambda: tracking_ids[0])
            ),
            total_charge=total_charge,
            currency=lib.failsafe(lambda: result.TotalCharges.Currency) or "EUR",
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create ParcelOne shipment request."""
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

    # Parse service to get CEP and product
    service = provider_units.ShippingService.map(payload.service)
    service_code = service.value_or_key
    cep_id, product_id = provider_units.parse_service_code(service_code)
    cep_id = cep_id or settings.connection_config.cep_id.state
    product_id = product_id or settings.connection_config.product_id.state

    # Determine label format
    label_format = provider_units.LabelFormat.map(
        payload.label_type or settings.connection_config.label_format.state
    ).value or "PDF"
    label_size = settings.connection_config.label_size.state or "A6"

    request = parcelone.ShippingDataRequestType(
        ShippingData=parcelone.ShipmentType(
            ShipmentRef=payload.reference,
            CEPID=cep_id,
            ProductID=product_id,
            MandatorID=settings.mandator_id,
            ConsignerID=settings.consigner_id,
            ShipToData=parcelone.ShipToType(
                Name1=recipient.company_name or recipient.person_name,
                Name2=recipient.person_name if recipient.company_name else None,
                ShipmentAddress=parcelone.AddressType(
                    Street=recipient.street,
                    Streetno=recipient.street_number,
                    PostalCode=recipient.postal_code,
                    City=recipient.city,
                    State=recipient.state_code,
                    Country=recipient.country_code,
                ),
                ShipmentContact=parcelone.ContactType(
                    Email=recipient.email,
                    Phone=recipient.phone_number,
                ),
                PrivateAddressIndicator=1 if recipient.residential else 0,
            ),
            ShipFromData=parcelone.ShipFromType(
                Name1=shipper.company_name or shipper.person_name,
                Name2=shipper.person_name if shipper.company_name else None,
                ShipmentAddress=parcelone.AddressType(
                    Street=shipper.street,
                    Streetno=shipper.street_number,
                    PostalCode=shipper.postal_code,
                    City=shipper.city,
                    State=shipper.state_code,
                    Country=shipper.country_code,
                ),
                ShipmentContact=parcelone.ContactType(
                    Email=shipper.email,
                    Phone=shipper.phone_number,
                ),
            ),
            ReturnShipmentIndicator=1 if options.is_return.state else 0,
            PrintLabel=1,
            LabelFormat=parcelone.FormatType(
                Type=label_format,
                Size=label_size,
            ),
            PrintDocuments=1 if is_international else 0,
            Software="Karrio",
            Packages=[
                parcelone.ShipmentPackageType(
                    PackageRef=pkg.parcel.id or str(index),
                    PackageWeight=parcelone.MeasurementType(
                        Value=str(pkg.weight.KG),
                        Unit="kg",
                    ),
                    PackageDimensions=(
                        parcelone.DimensionsType(
                            Length=str(pkg.length.CM),
                            Width=str(pkg.width.CM),
                            Height=str(pkg.height.CM),
                        )
                        if pkg.length.CM and pkg.width.CM and pkg.height.CM
                        else None
                    ),
                    IntDocData=(
                        parcelone.IntDocDataType(
                            InvoiceNo=customs.invoice,
                            ItemCategory=1,
                            CustomDetails=[
                                parcelone.CustomDetailType(
                                    Contents=item.description or item.title,
                                    Quantity=item.quantity,
                                    ItemValue=item.value_amount,
                                    NetWeight=item.weight,
                                    Origin=item.origin_country,
                                    TariffNumber=item.hs_code,
                                )
                                for item in (customs.commodities or [])
                            ] if customs.commodities else None,
                        )
                        if is_international and customs
                        else None
                    ),
                )
                for index, pkg in enumerate(packages, 1)
            ],
            Services=[
                *(
                    [
                        parcelone.ShipmentServiceType(
                            ServiceID="COD",
                            Value=parcelone.AmountType(
                                Value=str(options.cash_on_delivery.state),
                                Currency=options.parcelone_cod_currency.state or "EUR",
                            ),
                        )
                    ]
                    if options.cash_on_delivery.state
                    else []
                ),
                *(
                    [
                        parcelone.ShipmentServiceType(
                            ServiceID="INS",
                            Value=parcelone.AmountType(
                                Value=str(options.insurance.state),
                                Currency=options.parcelone_insurance_currency.state or "EUR",
                            ),
                        )
                    ]
                    if options.insurance.state
                    else []
                ),
                *([parcelone.ShipmentServiceType(ServiceID="SIG")] if options.signature_required.state else []),
                *([parcelone.ShipmentServiceType(ServiceID="SDO")] if options.saturday_delivery.state else []),
                *(
                    [
                        parcelone.ShipmentServiceType(
                            ServiceID="MAIL",
                            Parameters=options.parcelone_notification_email.state,
                        )
                    ]
                    if options.parcelone_notification_email.state
                    else []
                ),
                *(
                    [
                        parcelone.ShipmentServiceType(
                            ServiceID="SMS",
                            Parameters=options.parcelone_notification_sms.state,
                        )
                    ]
                    if options.parcelone_notification_sms.state
                    else []
                ),
            ],
        ),
    )

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(label_format=label_format),
    )
