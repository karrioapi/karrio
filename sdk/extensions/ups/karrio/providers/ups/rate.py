import ups_lib.rating_request as ups
import ups_lib.rating_response as ups_response
import time
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.ups.error as provider_error
import karrio.providers.ups.units as provider_units
import karrio.providers.ups.utils as provider_utils


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = provider_error.parse_error_response(response, settings)
    raw_rates = response.get("RateResponse", {}).get("RatedShipment") or []
    rates = [_extract_details(rate, settings, _response.ctx) for rate in raw_rates]

    return rates, messages


def _extract_details(
    detail: dict,
    settings: provider_utils.Settings,
    ctx: dict,
) -> typing.List[models.RateDetails]:
    rate = lib.to_object(ups_response.RatedShipmentType, detail)

    if rate.NegotiatedRateCharges is not None:
        total_charge = (
            rate.NegotiatedRateCharges.TotalChargesWithTaxes
            or rate.NegotiatedRateCharges.TotalCharge
        )
        taxes = rate.NegotiatedRateCharges.TaxCharges or []
        itemized_charges = [*rate.NegotiatedRateCharges.ItemizedCharges, *taxes]
    else:
        total_charge = rate.TotalChargesWithTaxes or rate.TotalCharges
        taxes = rate.TaxCharges or []
        itemized_charges = [*rate.ItemizedCharges, *taxes]

    charges = [
        ("Base charge", rate.TransportationCharges.MonetaryValue),
        *(
            []
            if any(itemized_charges)
            else [("Taxes", sum(lib.to_money(c.MonetaryValue) for c in taxes))]
        ),
        (rate.Service.Code, rate.ServiceOptionsCharges.MonetaryValue),
        *(
            (getattr(c, "Code", None) or getattr(c, "Type", None), c.MonetaryValue)
            for c in itemized_charges
        ),
    ]

    transit_days = lib.failsafe(
        lambda: rate.TimeInTransit.ServiceSummary.EstimatedArrival.BusinessDaysInTransit,
    )
    currency = rate.TransportationCharges.CurrencyCode
    service = provider_units.ServiceZone.find(rate.Service.Code, ctx["origin"])

    return models.RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency=currency,
        service=service.name_or_key,
        total_charge=lib.to_money(total_charge.MonetaryValue),
        extra_charges=[
            models.ChargeDetails(
                name=name,
                amount=lib.to_money(amount),
                currency=currency,
            )
            for name, amount in charges
            if name is not None or not amount
        ],
        transit_days=lib.to_int(transit_days),
        meta=dict(service_name=service.name_or_key),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels, provider_units.PackagePresets)
    is_document = all([parcel.is_document for parcel in payload.parcels])
    service = lib.to_services(payload.services, provider_units.ServiceCode).first
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    currency = options.currency.state or settings.default_currency
    mps_packaging = (
        provider_units.PackagingType.ups_unknown.value if len(packages) > 1 else None
    )
    indications = [
        *(["01"] if options.pickup_options.state else []),
        *(["02"] if options.delivery_options.state else []),
    ]

    request = ups.RatingRequestType(
        RateRequest=ups.RateRequestType(
            Request=ups.RequestType(
                RequestOption="Shoptimeintransit",
                SubVersion="2205",
                TransactionReference=ups.TransactionReferenceType(
                    CustomerContext=payload.reference or "fetch rates",
                ),
            ),
            PickupType=None,
            CustomerClassification=None,
            Shipment=ups.ShipmentType(
                OriginRecordTransactionTimestamp=None,
                Shipper=ups.ShipType(
                    Name=shipper.name,
                    AttentionName=shipper.contact,
                    ShipperNumber=settings.account_number,
                    Address=ups.ShipFromAddressType(
                        AddressLine=shipper.address_line,
                        City=shipper.city,
                        StateProvinceCode=shipper.state_code,
                        PostalCode=shipper.postal_code,
                        CountryCode=shipper.country_code,
                    ),
                ),
                ShipTo=ups.ShipToType(
                    Name=recipient.name,
                    AttentionName=recipient.contact,
                    Address=ups.AlternateDeliveryAddressAddressType(
                        AddressLine=recipient.address_line,
                        City=recipient.city,
                        StateProvinceCode=recipient.state_code,
                        PostalCode=recipient.postal_code,
                        CountryCode=recipient.country_code,
                        ResidentialAddressIndicator=(
                            "Y" if recipient.residential else None
                        ),
                        POBoxIndicator=None,
                    ),
                ),
                ShipFrom=ups.ShipType(
                    Name=shipper.name,
                    AttentionName=shipper.contact,
                    Address=ups.ShipFromAddressType(
                        AddressLine=shipper.address_line,
                        City=shipper.city,
                        StateProvinceCode=shipper.state_code,
                        PostalCode=shipper.postal_code,
                        CountryCode=shipper.country_code,
                    ),
                ),
                AlternateDeliveryAddress=None,
                ShipmentIndicatorType=[
                    ups.CustomerClassificationType(Code=code, Description="Indicator")
                    for code in indications
                ],
                PaymentDetails=ups.PaymentDetailsType(
                    ShipmentCharge=ups.ShipmentChargeType(
                        Type="01",
                        BillShipper=ups.BillShipperType(
                            AccountNumber=settings.account_number,
                        ),
                        BillReceiver=None,
                        BillThirdParty=None,
                        ConsigneeBilledIndicator=None,
                    ),
                    SplitDutyVATIndicator=None,
                ),
                FRSPaymentInformation=None,
                FreightShipmentInformation=None,
                GoodsNotInFreeCirculationIndicator=None,
                Service=ups.CustomerClassificationType(
                    Code=(
                        service.value
                        if service
                        else provider_units.ServiceCode.ups_standard.value
                    ),
                    Description="Weight",
                ),
                NumOfPieces=None,  # Only required for Freight
                ShipmentTotalWeight=ups.WeightType(
                    UnitOfMeasurement=ups.CustomerClassificationType(
                        Code=provider_units.WeightUnit[packages.weight_unit].value,
                        Description="Dimension",
                    ),
                    Weight=str(packages.weight.value),
                ),  # Only required for "timeintransit" requests
                DocumentsOnlyIndicator=("Y" if is_document else None),
                Package=[
                    ups.PackageType(
                        PackagingType=ups.CustomerClassificationType(
                            Code=(
                                mps_packaging
                                or provider_units.PackagingType.map(
                                    package.packaging_type
                                ).value
                                or provider_units.PackagingType.ups_customer_supplied_package.value
                            ),
                            Description="Packaging Type",
                        ),
                        Dimensions=(
                            ups.DimensionsType(
                                UnitOfMeasurement=ups.CustomerClassificationType(
                                    Code=package.dimension_unit.value,
                                    Description="Dimension",
                                ),
                                Length=str(package.length.value),
                                Width=str(package.width.value),
                                Height=str(package.height.value),
                            )
                            if any([package.length, package.width, package.height])
                            else None
                        ),
                        DimWeight=None,
                        PackageWeight=ups.WeightType(
                            UnitOfMeasurement=ups.CustomerClassificationType(
                                Code=provider_units.WeightUnit[
                                    str(package.weight.unit)
                                ].value,
                                Description="Weight",
                            ),
                            Weight=str(package.weight.value),
                        ),
                        Commodity=None,
                        PackageServiceOptions=None,
                        UPSPremier=None,
                        OversizeIndicator=None,
                        MinimumBillableWeightIndicator=None,
                    )
                    for package in packages
                ],
                ShipmentServiceOptions=(
                    ups.ShipmentServiceOptionsType(
                        SaturdayDeliveryIndicator=(
                            "Y" if options.ups_saturday_delivery.state else None
                        ),
                        SaturdayPickupIndicator=(
                            "Y" if options.ups_saturday_pickup.state else None
                        ),
                        SundayDeliveryIndicator=(
                            "Y" if options.ups_sunday_delivery.state else None
                        ),
                        AvailableServicesOption=None,
                        AccessPointCOD=None,
                        DeliverToAddresseeOnlyIndicator=(
                            "Y" if options.ups_deliver_to_addressee_only.state else None
                        ),
                        DirectDeliveryOnlyIndicator=(
                            "Y" if options.ups_direct_delivery_only.state else None
                        ),
                        COD=None,
                        DeliveryConfirmation=None,
                        ReturnOfDocumentIndicator=(
                            "Y" if options.ups_return_of_document.state else None
                        ),
                        UPScarbonneutralIndicator=(
                            "Y" if options.ups_carbonneutral.state else None
                        ),
                        CertificateOfOriginIndicator=(
                            "Y" if options.ups_certificate_of_origin.state else None
                        ),
                        PickupOptions=(
                            ups.PickupOptionsType(
                                HoldForPickupIndicator="Y",
                                LiftGateForPickUpIndicator=(
                                    "Y"
                                    if options.ups_lift_gate_for_pickup.state
                                    else None
                                ),
                            )
                            if options.pickup_options.state
                            else None
                        ),
                        DeliveryOptions=(
                            ups.DeliveryOptionsType(
                                DropOffAtUPSFacilityIndicator="Y",
                                LiftGateForDeliveryIndicator=(
                                    "Y"
                                    if options.ups_lift_gate_for_delivery.state
                                    else None
                                ),
                            )
                            if options.delivery_options.state
                            else None
                        ),
                        RestrictedArticles=(
                            ups.RestrictedArticlesType(
                                AlcoholicBeveragesIndicator=None,
                                DiagnosticSpecimensIndicator=None,
                                PerishablesIndicator=None,
                                PlantsIndicator=None,
                                SeedsIndicator=None,
                                SpecialExceptionsIndicator="Y",
                                TobaccoIndicator=None,
                            )
                            if options.dangerous_goods.state
                            else None
                        ),
                        ShipperExportDeclarationIndicator=(
                            "Y"
                            if options.ups_shipper_export_declaration.state
                            else None
                        ),
                        CommercialInvoiceRemovalIndicator=(
                            "Y"
                            if options.ups_commercial_invoice_removal.state
                            else None
                        ),
                        ImportControl=None,
                        ReturnService=None,
                        SDLShipmentIndicator=(
                            "Y" if options.ups_sdl_shipment.state else None
                        ),
                        EPRAIndicator=(
                            "Y" if options.ups_epra_indicator.state else None
                        ),
                        InsideDelivery=None,
                        ItemDisposalIndicator=None,
                    )
                    if any(options.items())
                    else None
                ),
                ShipmentRatingOptions=ups.ShipmentRatingOptionsType(
                    NegotiatedRatesIndicator="Y",
                    FRSShipmentIndicator=None,
                    RateChartIndicator=None,
                    UserLevelDiscountIndicator=None,
                    TPFCNegotiatedRatesIndicator=None,
                ),
                InvoiceLineTotal=ups.InvoiceLineTotalType(
                    CurrencyCode=currency,
                    MonetaryValue=str(options.declared_value.state or 1.0),
                ),
                RatingMethodRequestedIndicator="Y",
                TaxInformationIndicator="Y",
                PromotionalDiscountInformation=None,
                DeliveryTimeInformation=ups.DeliveryTimeInformationType(
                    PackageBillType=("02" if is_document else "03"),
                    Pickup=ups.PickupType(
                        Date=lib.fdatetime(
                            options.shipment_date.state or time.strftime("%Y-%m-%d"),
                            current_format="%Y-%m-%d",
                            output_format="%Y%m%d",
                        )
                    ),
                ),
            ),
        )
    )

    return lib.Serializable(
        request,
        lib.to_dict,
        ctx=dict(origin=shipper.country_code),
    )
