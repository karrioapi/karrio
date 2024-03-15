import karrio.schemas.tge.label_request as tge
import karrio.schemas.tge.label_response as shipping
import uuid
import typing
import datetime
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.tge.error as error
import karrio.providers.tge.utils as provider_utils
import karrio.providers.tge.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    shipment = (
        _extract_details(response["TollMessage"], settings, ctx=_response.ctx)
        if "ResponseMessages" in response.get("TollMessage", {})
        and any(response["TollMessage"]["ResponseMessages"]["ResponseMessage"])
        else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict = {},
) -> models.ShipmentDetails:
    shipment = lib.to_object(shipping.TollMessageType, data)

    SSCCs = ctx["SSCCs"]
    sscc_count = ctx["sscc_count"]
    label_type = ctx["label_type"]
    tracking_number = ctx["ShipmentID"]
    shipment_count = ctx["shipment_count"]
    label = lib.bundle_base64(
        [_.ResponseMessage for _ in shipment.ResponseMessages.ResponseMessage],
        format=label_type,
    )

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=tracking_number,
        label_type=label_type,
        docs=models.Documents(label=label),
        meta=dict(
            SSCCs=SSCCs,
            sscc_count=sscc_count,
            ShipmentID=tracking_number,
            shipment_count=shipment_count,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    MessageIdentifier = str(uuid.uuid4())
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    is_pdf = "PDF" in (payload.label_type or "PDF")
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_count=len(payload.parcels),
        sssc_count=(
            settings.sssc_count
            if settings.sssc_count is not None
            else lib.to_int(settings.connection_config.SSCC_range_start.state) or 0
        ),
        shipment_count=(
            settings.shipment_count
            if settings.shipment_count is not None
            else lib.to_int(settings.connection_config.SHIP_range_start.state) or 0
        ),
        SSCC_GS1=settings.connection_config.SSCC_GS1.state or "",
        SHIP_GS1=settings.connection_config.SHIP_GS1.state or "",
        initializer=provider_units.shipping_options_initializer,
    )
    packages = lib.to_packages(
        payload.parcels,
        options=options,
        package_option_type=provider_units.ShippingOption,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )
    payment = payload.payment or models.Payment()
    create_date = datetime.datetime.now()
    shipping_date = lib.to_date(packages.options.shipment_date.state or create_date)
    SSCCs = (options.tge_ssc_ids.state or "").split(",")

    request = tge.LabelRequestType(
        TollMessage=tge.TollMessageType(
            Header=tge.HeaderType(
                MessageVersion="2.5",
                DocumentType="Label",
                MessageIdentifier=MessageIdentifier,
                CreateTimestamp=lib.fdatetime(
                    create_date,
                    output_format="%Y-%m-%dT%H:%M:%S.%fZ",
                ),
                Environment=("PRD" if not settings.test_mode else "TST"),
                SourceSystemCode=(settings.connection_config.channel.state or "YF73"),
                MessageSender=(
                    settings.connection_config.message_sender.state or "GOSHIPR"
                ),
            ),
            Print=tge.PrintType(
                BusinessID=(settings.connection_config.business_id.state or "IPEC"),
                PrintSettings=tge.PrintSettingsType(
                    IsLabelThermal=not is_pdf,
                    IsZPLRawResponseRequired=not is_pdf,
                    PDF=(
                        tge.PDFType(
                            IsPDFA4=True,
                            PDFSettings=tge.PDFSettingsType(StartQuadrant=1),
                        )
                        if is_pdf
                        else None
                    ),
                ),
                PrintDocumentType="Label",
                ConsignorParty=tge.ConsignPartyType(
                    Contact=tge.ContactType(
                        Name=shipper.company_name or shipper.person_name,
                    ),
                    PartyName=shipper.contact,
                    PhysicalAddress=tge.PhysicalAddressType(
                        AddressType=(
                            "Residential" if recipient.shipper else "Business"
                        ),
                        AddressLine1=shipper.address_line1,
                        AddressLine2=shipper.address_line2,
                        CountryCode=shipper.country_code,
                        PostalCode=shipper.postal_code,
                        StateCode=shipper.state_code,
                        Suburb=shipper.city,
                    ),
                ),
                CreateDateTime=lib.fdatetime(
                    create_date, output_format="%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                ShipmentCollection=tge.ShipmentCollectionType(
                    Shipment=[
                        tge.ShipmentType(
                            BillToParty=tge.BillToPartyType(
                                AccountCode=(
                                    payment.account_number or settings.account_code
                                ),
                                Payer=("S" if payment.paid_by == "sender" else "R"),
                            ),
                            ConsigneeParty=tge.ConsignPartyType(
                                Contact=tge.ContactType(
                                    Name=(
                                        recipient.company_name or recipient.person_name
                                    ),
                                ),
                                PartyName=recipient.contact,
                                PhysicalAddress=tge.PhysicalAddressType(
                                    AddressType=(
                                        "Residential"
                                        if recipient.residential
                                        else "Business"
                                    ),
                                    AddressLine1=recipient.address_line1,
                                    AddressLine2=recipient.address_line2,
                                    CountryCode=recipient.country_code,
                                    PostalCode=recipient.postal_code,
                                    StateCode=recipient.state_code,
                                    Suburb=recipient.city,
                                ),
                            ),
                            CreateDateTime=lib.fdatetime(
                                shipping_date,
                                output_format="%Y-%m-%dT%H:%M:%S.%fZ",
                            ),
                            DatePeriodCollection=tge.DatePeriodCollectionType(
                                DatePeriod=[
                                    tge.DatePeriodType(
                                        DateTime=(
                                            options.tge_despatch_date.state
                                            or f"{lib.fdate(shipping_date)}T90:00:00.000Z"
                                        ),
                                        DateType="DespatchDate",
                                    ),
                                    *(
                                        [
                                            tge.DatePeriodType(
                                                DateTime=options.tge_required_delivery_date.state,
                                                DateType="RequiredDeliveryDate",
                                            )
                                        ]
                                        if options.tge_required_delivery_date.state
                                        else []
                                    ),
                                ]
                            ),
                            FreightMode=(
                                lib.text(options.tge_freight_mode.state)
                                or lib.text(
                                    settings.connection_config.freight_mode.state
                                )
                                or "Road"
                            ),
                            References=(
                                tge.ReferencesType(
                                    Reference=[
                                        tge.ReferenceType(
                                            ReferenceType="ShipmentReference1",
                                            ReferenceValue=payload.reference,
                                        ),
                                    ]
                                )
                            ),
                            ShipmentID=options.tge_shipment_id.state,
                            ShipmentItemCollection=tge.ShipmentItemCollectionType(
                                ShipmentItem=[
                                    tge.ShipmentItemType(
                                        Commodity=tge.CommodityType(
                                            CommodityCode=(
                                                provider_units.PackagingType.map(
                                                    package.packaging_type
                                                ).value
                                                or "BG"
                                            ),
                                            CommodityDescription=(
                                                provider_units.PackagingType.map(
                                                    package.packaging_type
                                                ).name
                                                or "BAG"
                                            ),
                                        ),
                                        Description=package.description,
                                        Dimensions=tge.DimensionsType(
                                            Height=package.height.map(
                                                provider_units.MeasurementOptions
                                            ).CM,
                                            HeightUOM="cm",
                                            Length=package.length.map(
                                                provider_units.MeasurementOptions
                                            ).CM,
                                            LengthUOM="cm",
                                            Volume=package.volume.map(
                                                provider_units.MeasurementOptions
                                            ).cm3,
                                            VolumeUOM="cm3",
                                            Weight=package.weight.map(
                                                provider_units.MeasurementOptions
                                            ).KG,
                                            WeightUOM="kg",
                                            Width=package.width.map(
                                                provider_units.MeasurementOptions
                                            ).CM,
                                            WidthUOM="cm",
                                        ),
                                        IDs=tge.IDsType(
                                            ID=[
                                                tge.IDType(
                                                    SchemeName="SSCC",
                                                    Value=SSCCs[index],
                                                ),
                                            ]
                                        ),
                                        ShipmentItemTotals=tge.ShipmentItemTotalsType(
                                            ShipmentItemCount=len(packages),
                                        ),
                                        ShipmentService=tge.ShipmentServiceType(
                                            ServiceCode=service,
                                            ShipmentProductCode="",
                                        ),
                                    )
                                    for index, package in enumerate(packages)
                                ],
                            ),
                            SpecialInstruction=options.tge_special_instruction.state,
                        )
                    ]
                ),
            ),
        )
    )

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(
            SSCCs=SSCCs,
            label_type=("PDF" if is_pdf else "ZPL"),
            ShipmentID=options.tge_shipment_id.state,
            SourceSystemCode=(settings.connection_config.channel or "YF73"),
            MessageSender=(
                settings.connection_config.message_sender.state or "GOSHIPR"
            ),
            shipment_count=settings.shipment_count + 1,
            sscc_count=settings.sssc_count + len(packages),
        ),
    )
