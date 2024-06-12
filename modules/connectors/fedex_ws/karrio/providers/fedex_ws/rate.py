import karrio.schemas.fedex_ws.rate_service_v28 as fedex
import typing
import datetime
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.fedex_ws.error as provider_error
import karrio.providers.fedex_ws.units as provider_units
import karrio.providers.fedex_ws.utils as provider_utils


def parse_rate_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    replys = lib.find_element("RateReplyDetails", response)
    rates: typing.List[models.RateDetails] = [
        _extract_details(detail_node, settings, _response.ctx) for detail_node in replys
    ]
    return rates, provider_error.parse_error_response(response, settings)


def _extract_details(
    detail_node: lib.Element,
    settings: provider_utils.Settings,
    ctx: dict,
) -> typing.Optional[models.RateDetails]:
    rate: fedex.RateReplyDetail = lib.to_object(fedex.RateReplyDetail, detail_node)
    service = provider_units.ServiceType.map(rate.ServiceType)
    rate_type = rate.ActualRateType
    applied_options = rate.AppliedOptions

    shipment_rate, shipment_discount = typing.cast(
        typing.Tuple[fedex.ShipmentRateDetail, fedex.Money],
        next(
            (
                (r.ShipmentRateDetail, r.EffectiveNetDiscount)
                for r in rate.RatedShipmentDetails
                if typing.cast(fedex.ShipmentRateDetail, r.ShipmentRateDetail).RateType
                == rate_type
            ),
            (None, None),
        ),
    )
    currency = typing.cast(fedex.Money, shipment_rate.TotalBaseCharge).Currency
    charges = [
        ("Base charge", shipment_rate.TotalBaseCharge.Amount),
        ("Discount", getattr(shipment_discount, "Amount", None)),
        *(
            (s.Description, s.Amount.Amount)
            for s in shipment_rate.Surcharges + shipment_rate.Taxes
        ),
    ]
    applied_options = (
        dict(applied_options=applied_options)
        if (applied_options is not None and len(applied_options) > 0)
        else {}
    )
    transit = None
    estimated_delivery = lib.to_date(rate.DeliveryTimestamp)
    shipping_date = lib.to_date(ctx.get("shipment_date") or datetime.datetime.now())
    if estimated_delivery is not None:
        days = (
            shipping_date + datetime.timedelta(x + 1)
            for x in range((estimated_delivery.date() - shipping_date.date()).days)
        )
        transit = sum(1 for day in days if day.weekday() < 5)

    return models.RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        service=service.name_or_key,
        currency=currency,
        total_charge=lib.to_decimal(
            shipment_rate.TotalNetChargeWithDutiesAndTaxes.Amount
        ),
        transit_days=transit,
        extra_charges=[
            models.ChargeDetails(
                name=name,
                amount=lib.to_decimal(amount),
                currency=currency,
            )
            for name, amount in charges
            if amount
        ],
        meta=dict(service_name=service.name_or_key, **applied_options),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    service = units.Services(payload.services, provider_units.ServiceType).first
    options = lib.to_shipping_options(
        payload.options,
        initializer=provider_units.shipping_options_initializer,
    )
    packages = lib.to_packages(
        payload.parcels,
        provider_units.PackagePresets,
        required=["weight"],
        options=options,
        package_option_type=provider_units.ShippingOption,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )
    request_types = ["LIST"] + ([] if "currency" not in options else ["PREFERRED"])
    shipment_date = lib.to_date(options.shipment_date.state or datetime.datetime.now())
    rate_options = lambda _options: [
        option
        for _, option in _options.items()
        if option.state is not False and option.code in provider_units.RATING_OPTIONS
    ]
    shipment_options = lambda _options: [
        option
        for _, option in _options.items()
        if option.state is not False and option.code in provider_units.SHIPMENT_OPTIONS
    ]
    hub_id = lib.text(options.fedex_smart_post_hub_id.state) or lib.text(
        settings.connection_config.smart_post_hub_id.state
    )

    request = fedex.RateRequest(
        WebAuthenticationDetail=settings.webAuthenticationDetail,
        ClientDetail=settings.clientDetail,
        TransactionDetail=fedex.TransactionDetail(CustomerTransactionId="FTC"),
        Version=fedex.VersionId(ServiceId="crs", Major=28, Intermediate=0, Minor=0),
        ReturnTransitAndCommit=True,
        CarrierCodes=None,
        VariableOptions=(
            [option.code for option in rate_options(packages.options)]
            if any(rate_options(packages.options))
            else []
        ),
        ConsolidationKey=None,
        RequestedShipment=fedex.RequestedShipment(
            ShipTimestamp=shipment_date,
            DropoffType="REGULAR_PICKUP",
            ServiceType=(service.value if service is not None else None),
            PackagingType=provider_units.PackagingType.map(
                packages.package_type or "your_packaging"
            ).value,
            VariationOptions=None,
            TotalWeight=fedex.Weight(
                Units=packages.weight.unit,
                Value=packages.weight.LB,
            ),
            TotalInsuredValue=None,
            PreferredCurrency=options.currency.state,
            ShipmentAuthorizationDetail=None,
            Shipper=fedex.Party(
                AccountNumber=settings.account_number,
                Tins=(
                    [fedex.TaxpayerIdentification(Number=tax) for tax in shipper.taxes]
                    if shipper.has_tax_info
                    else None
                ),
                Contact=(
                    fedex.Contact(
                        ContactId=None,
                        PersonName=shipper.person_name,
                        Title=None,
                        CompanyName=shipper.company_name,
                        PhoneNumber=shipper.phone_number,
                        PhoneExtension=None,
                        TollFreePhoneNumber=None,
                        PagerNumber=None,
                        FaxNumber=None,
                        EMailAddress=shipper.email,
                    )
                    if shipper.has_contact_info
                    else None
                ),
                Address=fedex.Address(
                    StreetLines=shipper.address_lines,
                    City=shipper.city,
                    StateOrProvinceCode=shipper.state_code,
                    PostalCode=shipper.postal_code,
                    UrbanizationCode=None,
                    CountryCode=shipper.country_code,
                    CountryName=shipper.country_name,
                    Residential=shipper.residential,
                    GeographicCoordinates=None,
                ),
            ),
            Recipient=fedex.Party(
                AccountNumber=None,
                Tins=(
                    [
                        fedex.TaxpayerIdentification(Number=tax)
                        for tax in recipient.taxes
                    ]
                    if recipient.has_tax_info
                    else None
                ),
                Contact=(
                    fedex.Contact(
                        ContactId=None,
                        PersonName=recipient.person_name,
                        Title=None,
                        CompanyName=recipient.company_name,
                        PhoneNumber=recipient.phone_number,
                        PhoneExtension=None,
                        TollFreePhoneNumber=None,
                        PagerNumber=None,
                        FaxNumber=None,
                        EMailAddress=recipient.email,
                    )
                    if recipient.has_contact_info
                    else None
                ),
                Address=fedex.Address(
                    StreetLines=recipient.address_lines,
                    City=recipient.city,
                    StateOrProvinceCode=recipient.state_code,
                    PostalCode=recipient.postal_code,
                    UrbanizationCode=None,
                    CountryCode=recipient.country_code,
                    CountryName=recipient.country_name,
                    Residential=recipient.residential,
                    GeographicCoordinates=None,
                ),
            ),
            RecipientLocationNumber=None,
            Origin=None,
            SoldTo=None,
            ShippingChargesPayment=None,
            SpecialServicesRequested=(
                fedex.ShipmentSpecialServicesRequested(
                    SpecialServiceTypes=(
                        [option.code for option in shipment_options(packages.options)]
                        if any(shipment_options(packages.options))
                        else []
                    ),
                    CodDetail=None,
                    DeliveryOnInvoiceAcceptanceDetail=None,
                    HoldAtLocationDetail=None,
                    EventNotificationDetail=None,
                    ReturnShipmentDetail=None,
                    PendingShipmentDetail=None,
                    InternationalControlledExportDetail=None,
                    InternationalTrafficInArmsRegulationsDetail=None,
                    ShipmentDryIceDetail=None,
                    HomeDeliveryPremiumDetail=None,
                    FlatbedTrailerDetail=None,
                    FreightGuaranteeDetail=None,
                )
                if any(shipment_options(packages.options))
                else None
            ),
            ExpressFreightDetail=None,
            FreightShipmentDetail=None,
            DeliveryInstructions=None,
            VariableHandlingChargeDetail=None,
            CustomsClearanceDetail=None,
            PickupDetail=None,
            SmartPostDetail=(
                fedex.SmartPostShipmentDetail(
                    ProcessingOptionsRequested=None,
                    Indicia=(
                        lib.text(options.fedex_smart_post_allowed_indicia.state)
                        or "PARCEL_SELECT"
                    ),
                    AncillaryEndorsement=None,
                    SpecialServices=None,
                    HubId=hub_id,
                    CustomerManifestId=None,
                )
                if hub_id
                else None
            ),
            BlockInsightVisibility=None,
            LabelSpecification=None,
            ShippingDocumentSpecification=None,
            RateRequestTypes=request_types,
            EdtRequestType=None,
            PackageCount=len(packages),
            ShipmentOnlyFields=None,
            ConfigurationData=None,
            RequestedPackageLineItems=[
                fedex.RequestedPackageLineItem(
                    SequenceNumber=index,
                    GroupNumber=None,
                    GroupPackageCount=1,
                    VariableHandlingChargeDetail=None,
                    InsuredValue=None,
                    Weight=(
                        fedex.Weight(
                            Units=package.weight.unit,
                            Value=package.weight.value,
                        )
                        if package.weight.value
                        else None
                    ),
                    Dimensions=(
                        fedex.Dimensions(
                            Length=package.length.map(
                                provider_units.MeasurementOptions
                            ).value,
                            Width=package.width.map(
                                provider_units.MeasurementOptions
                            ).value,
                            Height=package.height.map(
                                provider_units.MeasurementOptions
                            ).value,
                            Units=package.dimension_unit.value,
                        )
                        if (
                            # only set dimensions if the packaging type is set to your_packaging
                            package.has_dimensions
                            and provider_units.PackagingType.map(
                                package.packaging_type or "your_packaging"
                            ).value
                            == provider_units.PackagingType.your_packaging.value
                        )
                        else None
                    ),
                    PhysicalPackaging=None,
                    ItemDescription=package.parcel.description,
                    ItemDescriptionForClearance=None,
                    CustomerReferences=(
                        [
                            fedex.CustomerReference(
                                CustomerReferenceType=fedex.CustomerReferenceType.CUSTOMER_REFERENCE,
                                Value=payload.reference,
                            )
                        ]
                        if any(payload.reference or "")
                        else None
                    ),
                    SpecialServicesRequested=None,
                    ContentRecords=None,
                )
                for index, package in enumerate(packages, 1)
            ],
        ),
    )

    return lib.Serializable(
        request,
        _request_serializer,
        dict(shipment_date=shipment_date),
    )


def _request_serializer(request: fedex.RateRequest) -> str:
    namespacedef_ = (
        'xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/"'
        ' xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"'
        ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        ' xmlns:xsd="http://www.w3.org/2001/XMLSchema"'
        ' xmlns:v28="http://fedex.com/ws/rate/v28"'
    )

    envelope = lib.create_envelope(body_content=request)
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    lib.apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "v28")

    return lib.to_xml(envelope, namespacedef_=namespacedef_)
