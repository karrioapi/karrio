from karrio.schemas.purolator.estimate_service_2_1_2 import (
    GetFullEstimateRequest,
    Shipment,
    SenderInformation,
    Address,
    ReceiverInformation,
    PackageInformation,
    TrackingReferenceInformation,
    PickupInformation,
    ArrayOfPiece,
    Piece,
    Weight as PurolatorWeight,
    WeightUnit as PurolatorWeightUnit,
    RequestContext,
    Dimension as PurolatorDimension,
    DimensionUnit as PurolatorDimensionUnit,
    TotalWeight,
    ShipmentEstimate,
    PickupType,
    PhoneNumber,
    PaymentInformation,
    PaymentType,
    InternationalInformation,
    ArrayOfOptionIDValuePair,
    OptionIDValuePair,
)

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.purolator.error as provider_error
import karrio.providers.purolator.units as provider_units
import karrio.providers.purolator.utils as provider_utils


def parse_rate_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    estimates = lib.find_element("ShipmentEstimate", response)
    return (
        [_extract_rate(node, settings) for node in estimates],
        provider_error.parse_error_response(response, settings),
    )


def _extract_rate(
    estimate_node: lib.Element,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    estimate = lib.to_object(ShipmentEstimate, estimate_node)
    currency = units.Currency.CAD.name
    service = provider_units.ShippingService.map(estimate.ServiceID)
    charges = [
        ("Base charge", estimate.BasePrice),
        *(
            (s.Description, s.Amount)
            for s in (
                estimate.Taxes.Tax
                + estimate.Surcharges.Surcharge
                + estimate.OptionPrices.OptionPrice
            )
        ),
    ]

    return models.RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        service=service.name_or_key,
        currency=currency,
        transit_days=estimate.EstimatedTransitDays,
        total_charge=lib.to_decimal(estimate.TotalPrice),
        extra_charges=[
            models.ChargeDetails(
                name=name,
                amount=lib.to_decimal(amount),
                currency=currency,
            )
            for name, amount in charges
            if amount
        ],
        meta=dict(service_name=service.name_or_key),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(
        payload.parcels,
        provider_units.PackagePresets,
        required=["weight"],
    )
    service = units.Services(payload.services, provider_units.ShippingService).first
    is_international = shipper.country_code != recipient.country_code

    service = lib.to_services(
        payload.services,
        is_international=is_international,
        recipient_country=recipient.country_code,
        service_type=provider_units.ShippingService,
        initializer=provider_units.shipping_services_initializer,
    ).first
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        service_is_defined=(getattr(service, "value", None) in payload.services),
        initializer=provider_units.shipping_options_initializer,
    )
    shipper_phone = units.Phone(shipper.phone_number, shipper.country_code or "CA")
    recipient_phone = units.Phone(recipient.phone_number, recipient.country_code)

    request = lib.create_envelope(
        header_content=RequestContext(
            Version="2.1",
            Language=settings.language,
            GroupID="",
            RequestReference=getattr(payload, "id", ""),
            UserToken=settings.user_token,
        ),
        body_content=GetFullEstimateRequest(
            Shipment=Shipment(
                SenderInformation=SenderInformation(
                    Address=Address(
                        Name=shipper.person_name or "",
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
                            CountryCode=shipper_phone.country_code or "0",
                            AreaCode=shipper_phone.area_code or "0",
                            Phone=shipper_phone.phone or "0",
                            Extension=None,
                        ),
                        FaxNumber=None,
                    ),
                    TaxNumber=(shipper.federal_tax_id or shipper.state_tax_id),
                ),
                ReceiverInformation=ReceiverInformation(
                    Address=Address(
                        Name=recipient.person_name or "",
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
                            CountryCode=recipient_phone.country_code or "0",
                            AreaCode=recipient_phone.area_code or "0",
                            Phone=recipient_phone.phone or "0",
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
                    ServiceID=service.value,
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
                        if packages.weight.value is not None
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
                                        Value=package.length.value,
                                        DimensionUnit=PurolatorDimensionUnit[
                                            package.dimension_unit.value
                                        ].value,
                                    )
                                    if package.length.value
                                    else None
                                ),
                                Width=(
                                    PurolatorDimension(
                                        Value=package.width.value,
                                        DimensionUnit=PurolatorDimensionUnit[
                                            package.dimension_unit.value
                                        ].value,
                                    )
                                    if package.width.value
                                    else None
                                ),
                                Height=(
                                    PurolatorDimension(
                                        Value=package.height.value,
                                        DimensionUnit=PurolatorDimensionUnit[
                                            package.dimension_unit.value
                                        ].value,
                                    )
                                    if package.height.value
                                    else None
                                ),
                                Options=ArrayOfOptionIDValuePair(
                                    OptionIDValuePair=[
                                        OptionIDValuePair(
                                            ID=option.code,
                                            Value=lib.to_money(option.state),
                                        )
                                        for _, option in options.items()
                                    ]
                                )
                                if any(options.items())
                                else None,
                            )
                            for package in packages
                        ]
                    ),
                    DangerousGoodsDeclarationDocumentIndicator=None,
                    OptionsInformation=None,
                ),
                InternationalInformation=(
                    InternationalInformation(
                        DocumentsOnlyIndicator=packages.is_document,
                        ContentDetails=None,
                        BuyerInformation=None,
                        PreferredCustomsBroker=None,
                        DutyInformation=None,
                        ImportExportType=None,
                        CustomsInvoiceDocumentIndicator=None,
                    )
                    if is_international
                    else None
                ),
                ReturnShipmentInformation=None,
                PaymentInformation=PaymentInformation(
                    PaymentType=PaymentType.SENDER.value,
                    RegisteredAccountNumber=settings.account_number,
                ),
                PickupInformation=PickupInformation(
                    PickupType=PickupType.DROP_OFF.value
                ),
                NotificationInformation=None,
                TrackingReferenceInformation=(
                    TrackingReferenceInformation(Reference1=payload.reference)
                    if payload.reference != ""
                    else None
                ),
                OtherInformation=None,
                ProactiveNotification=None,
            ),
            ShowAlternativeServicesIndicator=options.purolator_show_alternative_services.state,
        ),
    )

    return lib.Serializable(request, provider_utils.standard_request_serializer)
