import datetime
import uuid
import karrio.schemas.tge.label_request as tge
import karrio.schemas.tge.label_response as shipping
import typing
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
        _extract_details(response, settings, ctx=_response.ctx)
        if not response.is_error and "result" in (response.data or {})
        else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict = {},
) -> models.ShipmentDetails:
    shipment: shipping.LabelResponseType = lib.to_object(
        shipping.LabelResponseType, data.response
    )
    label = shipment.soapenvBody.ns1getLabelResponse.result

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.Tracking,
        shipment_identifier=shipment.Tracking,
        label_type="PDF",
        docs=models.Documents(label=label),
        meta=dict(
            postal_code=ctx.get("postal_code", ""),
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        option_type=provider_units.ShippingOption,
    )
    packages = lib.to_packages(
        payload.parcels,
        options=options,
        package_option_type=provider_units.ShippingOption,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )
    payment = payload.payment or models.Payment()

    request = tge.LabelRequestType(
        TollMessage=tge.TollMessageType(
            Header=tge.HeaderType(
                MessageVersion="1.0",
                MessageIdentifier=str(uuid.uuid4()),
                CreateTimestamp=(
                    datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z")
                ),
                DocumentType="RateEnquiry",
                Environment=("PRD" if not settings.test_mode else "TST"),
                SourceSystemCode=settings.channel or "XP41",
                MessageSender=settings.connection_config.app_name.state or "GOSHIPR",
            ),
            Print=tge.PrintType(
                BusinessID=options.tge_business_id.state,
                PrintSettings=tge.PrintSettingsType(
                    IsLabelThermal=False,
                    IsZPLRawResponseRequired=False,
                    PDF=tge.PDFType(
                        IsPDFA4=True,
                        PDFSettings=tge.PDFSettingsType(
                            StartQuadrant=1,
                        ),
                    ),
                ),
                PrintDocumentType="Label",
                ConsignorParty=tge.ConsignPartyType(
                    Contact=tge.ContactType(
                        Name=shipper.company_name or shipper.person_name,
                    ),
                    PartyName=shipper.contact,
                    PhysicalAddress=tge.PhysicalAddressType(
                        AddressLine1=shipper.address_line1,
                        AddressLine2=shipper.address_line2,
                        CountryCode=shipper.country_code,
                        PostalCode=shipper.postal_code,
                        StateCode=shipper.state_code,
                        Suburb=shipper.city,
                    ),
                ),
                CreateDateTime=datetime.datetime.now().strftime(
                    "%Y-%m-%dT%H:%M:%S.%f%z"
                ),
                ShipmentCollection=tge.ShipmentCollectionType(
                    Shipment=[
                        tge.ShipmentType(
                            BillToParty=tge.BillToPartyType(
                                AccountCode=(
                                    payment.account_number
                                    or settings.account_code.state
                                ),
                                Payer=("S" if payment.payer == "sender" else "R"),
                            ),
                            ConsigneeParty=tge.ConsignPartyType(
                                Contact=tge.ContactType(
                                    Name=(
                                        recipient.company_name or recipient.person_name
                                    ),
                                ),
                                PartyName=recipient.contact,
                                PhysicalAddress=tge.PhysicalAddressType(
                                    AddressLine1=recipient.address_line1,
                                    AddressLine2=recipient.address_line2,
                                    CountryCode=recipient.country_code,
                                    PostalCode=recipient.postal_code,
                                    StateCode=recipient.state_code,
                                    Suburb=recipient.city,
                                ),
                            ),
                            CreateDateTime=datetime.datetime.now().strftime(
                                "%Y-%m-%dT%H:%M:%S.%f%z"
                            ),
                            DatePeriodCollection=(
                                tge.DatePeriodCollectionType(
                                    DatePeriod=[
                                        *(
                                            [
                                                tge.DatePeriodType(
                                                    DateTime=lib.fdatetime(
                                                        options.tge_despatch_date.state
                                                    ),
                                                    Type="DespatchDate",
                                                )
                                            ]
                                            if options.tge_despatch_date.state
                                            else []
                                        ),
                                        *(
                                            [
                                                tge.DatePeriodType(
                                                    DateTime=lib.fdatetime(
                                                        options.tge_required_delivery_date.state
                                                    ),
                                                    Type="RequiredDeliveryDate",
                                                )
                                            ]
                                            if options.tge_required_delivery_date.state
                                            else []
                                        ),
                                    ]
                                )
                                if any(
                                    [
                                        options.tge_despatch_date.state,
                                        options.tge_required_delivery_date.state,
                                    ]
                                )
                                else None
                            ),
                            FreightMode=(
                                lib.text(options.tge_freight_mode.state)
                                or lib.text(
                                    settings.connection_config.freight_mode.state
                                )
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
                            ShipmentID=(
                                options.tge_shipment_id.state
                                or getattr(payload, "id", None)
                            ),
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
                                            Length=package.length.map(
                                                provider_units.MeasurementOptions
                                            ).CM,
                                            Volume=package.volume.map(
                                                provider_units.MeasurementOptions
                                            ).cm3,
                                            Weight=package.weight.map(
                                                provider_units.MeasurementOptions
                                            ).KG,
                                            Width=package.width.map(
                                                provider_units.MeasurementOptions
                                            ).CM,
                                        ),
                                        IDs=tge.IDsType(
                                            ID=[
                                                tge.IDType(
                                                    SchemeName="SSCC",
                                                    Value=(
                                                        package.parcel.reference_number
                                                        or getattr(package, "id", None)
                                                        or str(uuid.uuid4())
                                                    ),
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
                                    for package in packages
                                ],
                            ),
                            SpecialInstruction=options.tge_special_instruction.state,
                        )
                    ]
                ),
            ),
        )
    )

    return lib.Serializable(request, lib.to_dict)
