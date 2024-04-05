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
    ShipmentIDs = ctx["ShipmentIDs"]
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
            ShipmentIDs=ShipmentIDs,
            ShipmentID=tracking_number,
            shipment_count=shipment_count,
            manifest_required=True,
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
        initializer=provider_units.shipping_options_initializer,
    )
    packages = lib.to_packages(
        payload.parcels,
        options=options,
        package_option_type=provider_units.ShippingOption,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )
    payment = payload.payment or models.Payment()

    ShipmentIDs, SSCCs, shipment_count, sscc_count = settings.next_shipment_identifiers(
        options, len(packages)
    )

    now = datetime.datetime.now()
    create_time = lib.fdatetime(now, output_format="%H:%M:%S")
    create_date = lib.fdatetime(now, output_format="%Y-%m-%dT")
    shipping_date = lib.to_date(options.shipment_date.state or now)
    pickup_date = lib.fdatetime(
        provider_utils.next_pickup_date(shipping_date), output_format="%Y-%m-%dT"
    )

    request = tge.LabelRequestType(
        TollMessage=tge.TollMessageType(
            Header=tge.HeaderType(
                MessageVersion="2.5",
                DocumentType="Label",
                MessageIdentifier=MessageIdentifier,
                CreateTimestamp=f"{create_date}{create_time}.000Z",
                Environment=("PRD" if not settings.test_mode else "TST"),
                SourceSystemCode=(settings.connection_config.channel.state or "YF73"),
                MessageSender=(
                    settings.connection_config.message_sender.state or "GOSHIPR"
                ),
            ),
            Print=tge.PrintType(
                BusinessID=(settings.connection_config.business_id.state or "IPEC"),
                PrintSettings=tge.PrintSettingsType(
                    IsLabelThermal="false" if is_pdf else "true",
                    IsZPLRawResponseRequired="false" if is_pdf else "true",
                    PDF=lib.identity(
                        tge.PDFType(
                            IsPDFA4="true",
                            PDFSettings=tge.PDFSettingsType(StartQuadrant="1"),
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
                CreateDateTime=f"{create_date}{create_time}.000Z",
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
                            CreateDateTime=f"{create_date}{create_time}.000Z",
                            DatePeriodCollection=tge.DatePeriodCollectionType(
                                DatePeriod=[
                                    tge.DatePeriodType(
                                        DateTime=(
                                            options.tge_despatch_date.state
                                            or f"{pickup_date}10:00:00.000Z"
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
                            FreightMode=lib.identity(
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
                                            ReferenceValue=(
                                                payload.reference
                                                or getattr(payload, "id", "N/A")
                                            ),
                                        ),
                                    ]
                                )
                            ),
                            ShipmentID=ShipmentIDs[index],
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
                                        Description=(package.description or "N/A"),
                                        Dimensions=tge.DimensionsType(
                                            Height=package.height.map(
                                                provider_units.MeasurementOptions
                                            ).CM,
                                            HeightUOM="m3",
                                            Length=package.length.map(
                                                provider_units.MeasurementOptions
                                            ).CM,
                                            LengthUOM="m3",
                                            Volume=package.volume.map(
                                                provider_units.MeasurementOptions
                                            ).m3,
                                            VolumeUOM="m3",
                                            Weight=package.weight.map(
                                                provider_units.MeasurementOptions
                                            ).KG,
                                            WeightUOM="kg",
                                            Width=package.width.map(
                                                provider_units.MeasurementOptions
                                            ).CM,
                                            WidthUOM="m3",
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
                                ],
                            ),
                            SpecialInstruction=options.tge_special_instruction.state,
                        )
                        for index, package in enumerate(packages)
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
            sscc_count=sscc_count,
            ShipmentIDs=ShipmentIDs,
            ShipmentID=ShipmentIDs[0],
            shipment_count=shipment_count,
            label_type=("PDF" if is_pdf else "ZPL"),
            SourceSystemCode=(settings.connection_config.channel or "YF73"),
            MessageSender=(
                settings.connection_config.message_sender.state or "GOSHIPR"
            ),
        ),
    )
