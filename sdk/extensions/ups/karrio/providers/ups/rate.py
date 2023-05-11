import ups_lib.rate_web_service_schema as ups
import time
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.ups.error as provider_error
import karrio.providers.ups.units as provider_units
import karrio.providers.ups.utils as provider_utils


def parse_rate_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = provider_error.parse_error_response(response, settings)
    rates = [
        _extract_details(node, settings, _response.ctx)
        for node in lib.find_element("RatedShipment", response)
    ]

    return rates, messages


def _extract_details(
    detail_node: lib.Element,
    settings: provider_utils.Settings,
    ctx: dict,
) -> typing.List[models.RateDetails]:
    rate = lib.to_object(ups.RatedShipmentType, detail_node)

    if rate.NegotiatedRateCharges is not None:
        total_charges = (
            rate.NegotiatedRateCharges.TotalChargesWithTaxes
            or rate.NegotiatedRateCharges.TotalCharge
        )
        taxes = rate.NegotiatedRateCharges.TaxCharges
        itemized_charges = rate.NegotiatedRateCharges.ItemizedCharges + taxes
    else:
        total_charges = rate.TotalChargesWithTaxes or rate.TotalCharges
        taxes = rate.TaxCharges
        itemized_charges = rate.ItemizedCharges + taxes

    charges = [
        ("Base charge", rate.TransportationCharges.MonetaryValue),
        *(
            []
            if any(itemized_charges)
            else [("Taxes", sum(lib.to_money(c.MonetaryValue) for c in taxes))]
        ),
        (rate.ServiceOptionsCharges.Code, rate.ServiceOptionsCharges.MonetaryValue),
        *(
            (getattr(c, "Code", None) or getattr(c, "Type", None), c.MonetaryValue)
            for c in itemized_charges
        ),
    ]
    estimated_arrival = (
        lib.find_element(
            "EstimatedArrival", detail_node, ups.EstimatedArrivalType, first=True
        )
        or ups.EstimatedArrivalType()
    )
    transit_days = (
        rate.GuaranteedDelivery.BusinessDaysInTransit
        if rate.GuaranteedDelivery is not None
        else estimated_arrival.BusinessDaysInTransit
    )
    currency = lib.find_element("CurrencyCode", detail_node, first=True).text
    service = provider_units.ServiceZone.find(rate.Service.Code, ctx["origin"])

    return models.RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency=currency,
        service=service.name_or_key,
        total_charge=lib.to_money(total_charges.MonetaryValue),
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
    indications = (["01"] if options.pickup_options.state else []) + (
        ["02"] if options.delivery_options.state else []
    )

    request = ups.RateRequest(
        Request=ups.RequestType(
            RequestOption=["Shoptimeintransit"],
            SubVersion=None,
            TransactionReference=ups.TransactionReferenceType(
                CustomerContext=payload.reference,
                TransactionIdentifier=getattr(payload, "id", None),
            ),
        ),
        PickupType=None,
        CustomerClassification=None,
        Shipment=ups.ShipmentType(
            OriginRecordTransactionTimestamp=None,
            Shipper=ups.ShipperType(
                Name=shipper.company_name,
                ShipperNumber=settings.account_number,
                Address=ups.ShipAddressType(
                    AddressLine=lib.join(
                        shipper.street,
                        shipper.address_line2,
                    ),
                    City=shipper.city,
                    StateProvinceCode=shipper.state_code,
                    PostalCode=shipper.postal_code,
                    CountryCode=shipper.country_code,
                ),
            ),
            ShipTo=ups.ShipToType(
                Name=recipient.company_name,
                Address=ups.ShipToAddressType(
                    AddressLine=lib.join(
                        recipient.street,
                        recipient.address_line2,
                    ),
                    City=recipient.city,
                    StateProvinceCode=recipient.state_code,
                    PostalCode=recipient.postal_code,
                    CountryCode=recipient.country_code,
                    ResidentialAddressIndicator=None,
                ),
            ),
            ShipFrom=None,
            AlternateDeliveryAddress=None,
            ShipmentIndicationType=(
                [ups.IndicationType(Code=code) for code in indications]
                if any(indications)
                else None
            ),
            PaymentDetails=None,
            FRSPaymentInformation=None,
            FreightShipmentInformation=None,
            GoodsNotInFreeCirculationIndicator=None,
            Service=(
                ups.UOMCodeDescriptionType(
                    Code=(
                        service.value
                        if service
                        else provider_units.ServiceCode.ups_standard.value
                    )
                )
            ),
            NumOfPieces=None,  # Only required for Freight
            ShipmentTotalWeight=ups.ShipmentWeightType(
                UnitOfMeasurement=ups.CodeDescriptionType1(
                    Code=provider_units.WeightUnit[packages.weight_unit].value
                ),
                Weight=packages.weight.value,
            ),  # Only required for "timeintransit" requests
            DocumentsOnlyIndicator=("" if is_document else None),
            Package=[
                ups.PackageType(
                    PackagingType=ups.UOMCodeDescriptionType(
                        Code=(
                            mps_packaging
                            or provider_units.PackagingType.map(
                                package.packaging_type
                            ).value
                            or provider_units.PackagingType.ups_customer_supplied_package.value
                        ),
                        Description=None,
                    ),
                    Dimensions=(
                        ups.DimensionsType(
                            UnitOfMeasurement=ups.UOMCodeDescriptionType(
                                Code=package.dimension_unit.value, Description=None
                            ),
                            Length=package.length.value,
                            Width=package.width.value,
                            Height=package.height.value,
                        )
                        if any(
                            [
                                package.length.value,
                                package.height.value,
                                package.width.value,
                            ]
                        )
                        else None
                    ),
                    DimWeight=None,
                    PackageWeight=ups.PackageWeightType(
                        UnitOfMeasurement=ups.UOMCodeDescriptionType(
                            Code=provider_units.WeightUnit[
                                package.weight_unit.name
                            ].value,
                            Description=None,
                        ),
                        Weight=package.weight.value,
                    )
                    if package.weight.value
                    else None,
                    Commodity=None,
                    PackageServiceOptions=None,
                    AdditionalHandlingIndicator=None,
                )
                for package in packages
            ],
            ShipmentServiceOptions=(
                ups.ShipmentServiceOptionsType(
                    SaturdayPickupIndicator=(
                        "" if options.ups_saturday_pickup_indicator.state else None
                    ),
                    SaturdayDeliveryIndicator=(
                        "" if options.ups_saturday_delivery_indicator.state else None
                    ),
                    AccessPointCOD=(
                        ups.ShipmentServiceOptionsAccessPointCODType(
                            CurrencyCode=currency,
                            MonetaryValue=lib.to_money(
                                options.ups_access_point_cod.state
                            ),
                        )
                        if options.ups_access_point_cod.state
                        else None
                    ),
                    DeliverToAddresseeOnlyIndicator=(
                        ""
                        if options.ups_deliver_to_addressee_only_indicator.state
                        else None
                    ),
                    DirectDeliveryOnlyIndicator=(
                        "" if options.ups_direct_delivery_only_indicator.state else None
                    ),
                    DeliveryConfirmation=(
                        ups.DeliveryConfirmationType(
                            DCISType=options.ups_delivery_confirmation.state or "01"
                        )
                        if options.ups_delivery_confirmation.state
                        else None
                    ),
                    ReturnOfDocumentIndicator=(
                        "" if options.ups_return_of_document_indicator.state else None
                    ),
                    UPScarbonneutralIndicator=(
                        "" if options.ups_carbonneutral_indicator.state else None
                    ),
                    CertificateOfOriginIndicator=(
                        ""
                        if options.ups_certificate_of_origin_indicator.state
                        else None
                    ),
                    PickupOptions=(
                        ups.PickupOptionsType(
                            HoldForPickupIndicator="",
                            LiftGateAtPickupIndicator=(
                                ""
                                if options.ups_lift_gate_at_pickup_indicator.state
                                else None
                            ),
                        )
                        if options.pickup_options.state
                        else None
                    ),
                    DeliveryOptions=(
                        ups.DeliveryOptionsType(
                            DropOffAtUPSFacilityIndicator="",
                            LiftGateAtDeliveryIndicator=(
                                ""
                                if options.ups_lift_gate_at_delivery_indicator.state
                                else None
                            ),
                        )
                        if options.delivery_options.state
                        else None
                    ),
                    RestrictedArticles=(
                        ups.RestrictedArticlesType(
                            AlcoholicBeveragesIndicator=None,
                            DiagnosticSpecimentsIndicator=None,
                            PerishablesIndicator=None,
                            PlantsIndicator=None,
                            SeedsIndicator=None,
                            SpecialExceptionsIndicator="",
                            TobaccoIndicator=None,
                        )
                        if options.dangerous_good.state
                        else None
                    ),
                    ShipperExportDeclarationIndicator=(
                        ""
                        if options.ups_shipper_export_declaration_indicator.state
                        else None
                    ),
                    CommercialInvoiceRemovalIndicator=(
                        ""
                        if options.ups_commercial_invoice_removal_indicator.state
                        else None
                    ),
                    ImportControl=None,
                    ReturnService=None,
                    SDLShipmentIndicator=(
                        "" if options.ups_sdl_shipment_indicator.state else None
                    ),
                    EPRAIndicator=("" if options.ups_epra_indicator.state else None),
                    InsideDelivery=None,
                    ItemDisposalIndicator=None,
                )
                if any(options.items())
                else None
            ),
            ShipmentRatingOptions=ups.ShipmentRatingOptionsType(
                NegotiatedRatesIndicator="",
                FRSShipmentIndicator=None,
                RateChartIndicator="",
                UserLevelDiscountIndicator=None,
            ),
            InvoiceLineTotal=ups.InvoiceLineTotalType(
                CurrencyCode=currency,
                MonetaryValue=options.declared_value.state or 1.0,
            ),
            RatingMethodRequestedIndicator="",
            TaxInformationIndicator="",
            PromotionalDiscountInformation=None,
            DeliveryTimeInformation=ups.TimeInTransitRequestType(
                PackageBillType="02" if is_document else "03",
                Pickup=ups.PickupType(
                    Date=lib.fdatetime(
                        options.shipment_date.state or time.strftime("%Y-%m-%d"),
                        current_format="%Y-%m-%d",
                        output_format="%Y%m%d",
                    ),
                ),
            ),
        ),
    )

    return lib.Serializable(
        lib.create_envelope(header_content=settings.Security, body_content=request),
        _request_serializer,
        ctx=dict(origin=shipper.country_code),
    )


def _request_serializer(envelope: lib.Envelope) -> str:
    namespace_ = (
        'xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/"'
        ' xmlns:xsd="http://www.w3.org/2001/XMLSchema"'
        ' xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0"'
        ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        ' xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0"'
        ' xmlns:rate="http://www.ups.com/XMLSchema/XOLTWS/Rate/v1.1"'
    )
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    envelope.Header.ns_prefix_ = envelope.ns_prefix_
    lib.apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "rate")
    lib.apply_namespaceprefix(envelope.Header.anytypeobjs_[0], "upss")
    lib.apply_namespaceprefix(envelope.Body.anytypeobjs_[0].Request, "common")

    return lib.to_xml(envelope, namespacedef_=namespace_)
