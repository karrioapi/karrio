import karrio.schemas.tge.manifest_request as tge
import karrio.schemas.tge.manifest_response as manifest
import uuid
import typing
import datetime
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.tge.error as provider_error
import karrio.providers.tge.utils as provider_utils
import karrio.providers.tge.units as provider_units


def parse_manifest_response(
    _response: lib.Deserializable[typing.List[dict]],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ManifestDetails, typing.List[models.Message]]:
    responses = _response.deserialize()
    toll_messages = [
        _["TollMessage"]
        for _ in responses
        if "ResponseMessages" in _.get("TollMessage", {})
        and any(_["TollMessage"]["ResponseMessages"]["ResponseMessage"])
    ]

    shipment = _extract_details(toll_messages, settings) if any(toll_messages) else None
    messages: typing.List[models.Message] = sum(
        [
            provider_error.parse_error_response(response, settings)
            for response in responses
        ],
        start=[],
    )

    return shipment, messages


def _extract_details(
    data: typing.List[dict],
    settings: provider_utils.Settings,
) -> models.ManifestDetails:
    manifests = [lib.to_object(manifest.TollMessageType, _) for _ in data]
    manifest_file = lib.bundle_base64(
        sum(
            (
                [_.ResponseMessage for _ in _.ResponseMessages.ResponseMessage]
                for _ in manifests
            ),
            start=[],
        )
    )

    return models.ManifestDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_id,
        doc=models.ManifestDocument(manifest=manifest_file),
        meta=dict(),
    )


def manifest_request(
    payload: models.ManifestRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    manifest_options = lib.units.Options(
        payload.options,
        option_type=lib.units.create_enum(
            "ManifestOptions",
            {
                "manifest_id": lib.OptionEnum("manifest_id"),
                "shipments": lib.OptionEnum("shipments", lib.to_dict),
            },
        ),
    )
    requests = []

    for shipment_data in manifest_options.shipments.state or []:
        shipment_payload = lib.to_object(models.ShipmentRequest, shipment_data)
        meta = shipment_data.get("meta", {})
        ShipmentIDs = meta.get("ShipmentIDs")
        ShipmentID = meta.get("ShipmentID")
        SSCCs = meta.get("SSCCs")

        MessageIdentifier = str(uuid.uuid4())
        shipper = lib.to_address(shipment_payload.shipper)
        recipient = lib.to_address(shipment_payload.recipient)
        is_pdf = "PDF" in (shipment_payload.label_type or "PDF")
        options = lib.to_shipping_options(
            shipment_payload.options,
            initializer=provider_units.shipping_options_initializer,
        )
        packages = lib.to_packages(
            shipment_payload.parcels,
            options=options,
            package_option_type=provider_units.ShippingOption,
            shipping_options_initializer=provider_units.shipping_options_initializer,
        )
        service = provider_units.ShippingService.map(
            shipment_payload.service
        ).value_or_key
        payment = shipment_payload.payment or models.Payment()

        now = datetime.datetime.now()
        create_time = lib.fdatetime(now, output_format="%H:%M:%S")
        create_date = lib.fdatetime(now, output_format="%Y-%m-%dT")
        shipping_date = lib.to_date(options.shipment_date.state or now)
        pickup_date = lib.fdatetime(
            provider_utils.next_pickup_date(shipping_date), output_format="%Y-%m-%dT"
        )

        requests += [
            tge.ManifestRequestType(
                TollMessage=tge.TollMessageType(
                    Header=tge.HeaderType(
                        MessageVersion="2.5",
                        DocumentType="Manifest",
                        MessageIdentifier=MessageIdentifier,
                        CreateTimestamp=f"{create_date}{create_time}.000Z",
                        Environment=("PRD" if not settings.test_mode else "TST"),
                        SourceSystemCode=(
                            settings.connection_config.channel.state or "YF73"
                        ),
                        MessageSender=(
                            settings.connection_config.message_sender.state or "GOSHIPR"
                        ),
                    ),
                    Print=tge.PrintType(
                        BusinessID=(
                            settings.connection_config.business_id.state or "IPEC"
                        ),
                        PrintSettings=tge.PrintSettingsType(
                            IsLabelThermal="false" if is_pdf else "true",
                            IsZPLRawResponseRequired="false" if is_pdf else "true",
                            PDF=(
                                tge.PDFType(
                                    IsPDFA4="true",
                                    PDFSettings=tge.PDFSettingsType(StartQuadrant="1"),
                                )
                                if is_pdf
                                else None
                            ),
                        ),
                        PrintDocumentType="Manifest",
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
                        ManifestID=tge.ManifestIDType(
                            Value=(options.manifest_id.state or ShipmentID)
                        ),
                        CreateDateTime=f"{create_date}{create_time}.000Z",
                        DatePeriodCollection=tge.DatePeriodCollectionType(
                            DatePeriod=[
                                tge.DatePeriodType(
                                    DateTime=(
                                        options.tge_despatch_date.state
                                        or f"{pickup_date}{create_time}.000Z"
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
                        ShipmentCollection=tge.ShipmentCollectionType(
                            Shipment=[
                                tge.ShipmentType(
                                    BillToParty=tge.BillToPartyType(
                                        AccountCode=(
                                            payment.account_number
                                            or settings.account_code
                                        ),
                                        Payer=(
                                            "S" if payment.paid_by == "sender" else "R"
                                        ),
                                    ),
                                    ConsigneeParty=tge.ConsignPartyType(
                                        Contact=tge.ContactType(
                                            Name=(
                                                recipient.company_name
                                                or recipient.person_name
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
                                                    or f"{pickup_date}{create_time}.000Z"
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
                                                        shipment_payload.reference
                                                        or getattr(
                                                            shipment_payload,
                                                            "id",
                                                            "N/A",
                                                        )
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
                                                Description=(
                                                    package.description or "N/A"
                                                ),
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
                                                    ).cm3,
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
        ]

    return lib.Serializable(
        requests,
        lambda __: [lib.to_dict(_) for _ in __],
    )
