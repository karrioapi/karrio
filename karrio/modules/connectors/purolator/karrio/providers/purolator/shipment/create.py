from karrio.schemas.purolator.shipping_documents_service_1_3_0 import DocumentDetail
from karrio.schemas.purolator.shipping_service_2_1_3 import (
    CreateShipmentRequest,
    PIN,
    Shipment,
    SenderInformation,
    ReceiverInformation,
    PackageInformation,
    TrackingReferenceInformation,
    Address,
    InternationalInformation,
    PickupInformation,
    PickupType,
    ArrayOfPiece,
    Piece,
    Weight as PurolatorWeight,
    WeightUnit as PurolatorWeightUnit,
    RequestContext,
    Dimension as PurolatorDimension,
    DimensionUnit as PurolatorDimensionUnit,
    TotalWeight,
    PhoneNumber,
    PaymentInformation,
    DutyInformation,
    NotificationInformation,
    ArrayOfOptionIDValuePair,
    OptionIDValuePair,
    BusinessRelationship,
    PrinterType,
    ContentDetail,
    ArrayOfContentDetail,
)

import typing
import functools
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.purolator.error as provider_error
import karrio.providers.purolator.units as provider_units
import karrio.providers.purolator.utils as provider_utils
import karrio.providers.purolator.shipment.documents as documents


def parse_shipment_response(
    _response: lib.Deserializable[lib.Element], settings: provider_utils.Settings
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    pin = lib.find_element("ShipmentPIN", response, PIN, first=True)
    shipment = (
        _extract_shipment(response, settings)
        if (getattr(pin, "Value", None) is not None)
        else None
    )

    return shipment, provider_error.parse_error_response(response, settings)


def _extract_shipment(
    response: lib.Element,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    pin: PIN = lib.find_element("ShipmentPIN", response, PIN, first=True)
    documents = lib.find_element("DocumentDetail", response, DocumentDetail)
    label = next(
        (doc for doc in documents if "BillOfLading" in doc.DocumentType),
        DocumentDetail(),
    )
    invoice = next((doc for doc in documents if "Invoice" in doc.DocumentType), None)

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=pin.Value,
        shipment_identifier=pin.Value,
        docs=models.Documents(
            label=getattr(label, "Data", ""),
            **(dict(invoice=invoice.Data) if invoice else {}),
        ),
        meta=dict(
            carrier_tracking_link=settings.tracking_url.format(pin.Value),
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    requests: lib.Pipeline = lib.Pipeline(
        create=lambda *_: functools.partial(
            _create_shipment, payload=payload, settings=settings
        )(),
        document=functools.partial(
            _get_shipment_label, payload=payload, settings=settings
        ),
    )
    return lib.Serializable(requests)


def _shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(
        payload.parcels,
        provider_units.PackagePresets,
        required=["weight"],
    )
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    payment = payload.payment or models.Payment()
    customs = lib.to_customs_info(payload.customs)
    printing = provider_units.PrintType.map(payload.label_type or "PDF").value
    service = provider_units.ShippingService.map(payload.service).value_or_key
    is_international = shipper.country_code != recipient.country_code
    shipper_phone_number = units.Phone(
        shipper.phone_number or "000 000 0000", shipper.country_code
    )
    recipient_phone_number = units.Phone(
        recipient.phone_number or "000 000 0000", recipient.country_code
    )

    request = lib.create_envelope(
        header_content=RequestContext(
            Version="2.1",
            Language=settings.language,
            GroupID="",
            RequestReference=(getattr(payload, "id", None) or ""),
            UserToken=settings.user_token,
        ),
        body_content=CreateShipmentRequest(
            Shipment=Shipment(
                SenderInformation=SenderInformation(
                    Address=Address(
                        Name=shipper.person_name,
                        Company=shipper.company_name,
                        Department=None,
                        StreetNumber=shipper.street_number or "",
                        StreetSuffix=None,
                        StreetName=lib.text(shipper.address_line1),
                        StreetType=None,
                        StreetDirection=None,
                        Suite=None,
                        Floor=None,
                        StreetAddress2=lib.text(shipper.address_line2),
                        StreetAddress3=None,
                        City=shipper.city or "",
                        Province=shipper.state_code or "",
                        Country=shipper.country_code or "",
                        PostalCode=shipper.postal_code or "",
                        PhoneNumber=PhoneNumber(
                            CountryCode=shipper_phone_number.country_code or "0",
                            AreaCode=shipper_phone_number.area_code or "0",
                            Phone=shipper_phone_number.phone or "0",
                            Extension=None,
                        ),
                        FaxNumber=None,
                    ),
                    TaxNumber=(shipper.federal_tax_id or shipper.state_tax_id),
                ),
                ReceiverInformation=ReceiverInformation(
                    Address=Address(
                        Name=recipient.person_name,
                        Company=recipient.company_name,
                        Department=None,
                        StreetNumber=recipient.street_number or "",
                        StreetSuffix=None,
                        StreetName=lib.text(recipient.address_line1),
                        StreetType=None,
                        StreetDirection=None,
                        Suite=None,
                        Floor=None,
                        StreetAddress2=lib.text(recipient.address_line2),
                        StreetAddress3=None,
                        City=recipient.city or "",
                        Province=recipient.state_code or "",
                        Country=recipient.country_code or "",
                        PostalCode=recipient.postal_code or "",
                        PhoneNumber=PhoneNumber(
                            CountryCode=recipient_phone_number.country_code or "0",
                            AreaCode=recipient_phone_number.area_code or "0",
                            Phone=recipient_phone_number.phone or "0",
                            Extension=None,
                        ),
                        FaxNumber=None,
                    ),
                    TaxNumber=(recipient.federal_tax_id or recipient.state_tax_id),
                ),
                FromOnLabelIndicator=None,
                FromOnLabelInformation=None,
                ShipmentDate=options.shipment_date.state,
                PackageInformation=PackageInformation(
                    ServiceID=service,
                    Description=(
                        packages.description[:25]
                        if any(packages.description or "")
                        else None
                    ),
                    TotalWeight=(
                        TotalWeight(
                            Value=packages.weight.map(
                                provider_units.MeasurementOptions
                            ).LB,
                            WeightUnit=PurolatorWeightUnit.LB.value,
                        )
                        if packages.weight.value
                        else None
                    ),
                    TotalPieces=1,
                    PiecesInformation=ArrayOfPiece(
                        Piece=[
                            Piece(
                                Weight=(
                                    PurolatorWeight(
                                        Value=package.weight.map(
                                            provider_units.MeasurementOptions
                                        ).value,
                                        WeightUnit=PurolatorWeightUnit[
                                            package.weight_unit.value
                                        ].value,
                                    )
                                    if package.weight.value
                                    else None
                                ),
                                Length=(
                                    PurolatorDimension(
                                        Value=package.length.map(
                                            provider_units.MeasurementOptions
                                        ).value,
                                        DimensionUnit=PurolatorDimensionUnit[
                                            package.dimension_unit.value
                                        ].value,
                                    )
                                    if package.length.value
                                    else None
                                ),
                                Width=(
                                    PurolatorDimension(
                                        Value=package.width.map(
                                            provider_units.MeasurementOptions
                                        ).value,
                                        DimensionUnit=PurolatorDimensionUnit[
                                            package.dimension_unit.value
                                        ].value,
                                    )
                                    if package.width.value
                                    else None
                                ),
                                Height=(
                                    PurolatorDimension(
                                        Value=package.height.map(
                                            provider_units.MeasurementOptions
                                        ).value,
                                        DimensionUnit=PurolatorDimensionUnit[
                                            package.dimension_unit.value
                                        ].value,
                                    )
                                    if package.height.value
                                    else None
                                ),
                                Options=None,
                            )
                            for package in packages
                        ]
                    ),
                    DangerousGoodsDeclarationDocumentIndicator=None,
                    OptionsInformation=(
                        ArrayOfOptionIDValuePair(
                            OptionIDValuePair=[
                                OptionIDValuePair(
                                    ID=option.code,
                                    Value=lib.to_money(option.state),
                                )
                                for _, option in options.items()
                            ]
                        )
                        if any(options.items())
                        else None
                    ),
                ),
                InternationalInformation=(
                    InternationalInformation(
                        DocumentsOnlyIndicator=packages.is_document,
                        ContentDetails=(
                            ArrayOfContentDetail(
                                ContentDetail=[
                                    ContentDetail(
                                        Description=lib.text(
                                            item.title or item.description or "", max=25
                                        ),
                                        HarmonizedCode=item.hs_code or "0000",
                                        CountryOfManufacture=(
                                            item.origin_country or shipper.country_code
                                        ),
                                        ProductCode=item.sku or "0000",
                                        UnitValue=item.value_amount,
                                        Quantity=item.quantity,
                                        NAFTADocumentIndicator=None,
                                        FDADocumentIndicator=None,
                                        FCCDocumentIndicator=None,
                                        SenderIsProducerIndicator=None,
                                        TextileIndicator=None,
                                        TextileManufacturer=None,
                                    )
                                    for item in customs.commodities
                                ]
                            )
                            if not packages.is_document
                            else None
                        ),
                        BuyerInformation=None,
                        PreferredCustomsBroker=None,
                        DutyInformation=DutyInformation(
                            BillDutiesToParty=provider_units.DutyPaymentType.map(
                                customs.duty.paid_by
                            ).value
                            or "Sender",
                            BusinessRelationship=BusinessRelationship.NOT_RELATED.value,
                            Currency=(customs.duty.currency or options.currence.state),
                        ),
                        ImportExportType="Permanent",
                        CustomsInvoiceDocumentIndicator=True,
                    )
                    if is_international
                    else None
                ),
                ReturnShipmentInformation=None,
                PaymentInformation=(
                    PaymentInformation(
                        PaymentType=provider_units.PaymentType[payment.paid_by].value,
                        RegisteredAccountNumber=(
                            payment.account_number or settings.account_number
                        ),
                        BillingAccountNumber=(
                            payment.account_number or settings.account_number
                        ),
                        CreditCardInformation=None,
                    )
                    if payload.payment is not None
                    else None
                ),
                PickupInformation=PickupInformation(
                    PickupType=PickupType.DROP_OFF.value
                ),
                NotificationInformation=(
                    NotificationInformation(
                        ConfirmationEmailAddress=(
                            options.email_notification_to.state or recipient.email
                        )
                    )
                    if options.email_notification.state
                    and any([options.email_notification_to.state, recipient.email])
                    else None
                ),
                TrackingReferenceInformation=(
                    TrackingReferenceInformation(Reference1=payload.reference)
                    if any(payload.reference or "")
                    else None
                ),
                OtherInformation=None,
                ProactiveNotification=None,
            ),
            PrinterType=PrinterType(printing).value,
        ),
    )
    return lib.Serializable(request, provider_utils.standard_request_serializer)


def _create_shipment(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Job:
    return lib.Job(
        id="create",
        data=_shipment_request(payload, settings),
    )


def _get_shipment_label(
    create_response: str,
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Job:
    response = lib.to_element(create_response)
    valid = len(provider_error.parse_error_response(response, settings)) == 0
    shipment_pin = (
        getattr(
            lib.find_element("ShipmentPIN", response, PIN, first=True), "Value", None
        )
        if valid
        else None
    )
    data = (
        documents.get_shipping_documents_request(shipment_pin, payload, settings)
        if valid
        else None
    )

    return lib.Job(id="document", data=data, fallback="")
