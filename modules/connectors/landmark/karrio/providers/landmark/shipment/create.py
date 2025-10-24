"""Karrio Landmark Global shipment creation implementation."""

import karrio.schemas.landmark.import_request as import_req
import karrio.schemas.landmark.import_response as import_res
import karrio.schemas.landmark.ship_request as ship_req
import karrio.schemas.landmark.ship_response as ship_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.landmark.error as error
import karrio.providers.landmark.utils as provider_utils
import karrio.providers.landmark.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    shipment = (
        _extract_details(response, settings, ctx=_response.ctx)
        if len(lib.find_element("TrackingNumber", response)) > 0
        else None
    )

    return shipment, messages


def _extract_details(
    data: lib.Element,
    settings: provider_utils.Settings,
    ctx: dict = dict(),
) -> models.ShipmentDetails:
    """Extract shipment details from ImportResponse or ShipResponse"""
    # fmt: off
    label_format = ctx.get("label_format", "PDF")
    packages = lib.find_element("Package", data, ship_res.PackageType)
    result = lib.find_element("Result", data, ship_res.ResultType, first=True)
    label_images = lib.find_element("LabelImages", data, ship_res.LabelImagesType)

    last_mile_carrier = getattr(result, "ShippingCarrier", None)
    tracking_numbers = [_.LandmarkTrackingNumber for _ in packages if _.LandmarkTrackingNumber is not None]
    last_mile_tracking_numbers = [_.TrackingNumber for _ in packages if _.TrackingNumber is not None]
    package_references = [_.PackageReference for _ in packages if _.PackageReference is not None]
    barcode_datas = [_.BarcodeData for _ in packages if _.BarcodeData is not None]
    landmark_ids = [_.PackageID for _ in packages if _.PackageID is not None]

    tracking_number = next(iter(tracking_numbers), None)
    shipment_identifier = next(iter(landmark_ids), tracking_number)
    last_mile_tracking_number = next(iter(last_mile_tracking_numbers), None) if last_mile_carrier else None
    last_mile_tracking_numbers = last_mile_tracking_numbers if last_mile_carrier else []
    shipment_identifiers = landmark_ids if len(landmark_ids) > 0 else tracking_numbers
    label = (
        lib.bundle_base64(
            [_.LabelImage[0] for _ in label_images if len(_.LabelImage) > 0],
            label_format,
        )
        if any(_.LabelImage for _ in label_images)
        else ""
    )
    # fmt: on

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=shipment_identifier,
        label_type=label_format,
        docs=models.Documents(label=label),
        meta=lib.to_dict(
            dict(
                last_mile_carrier=last_mile_carrier,
                last_mile_tracking_number=last_mile_tracking_number,
                last_mile_tracking_numbers=last_mile_tracking_numbers,
                shipment_identifiers=shipment_identifiers,
                package_references=package_references,
                tracking_numbers=tracking_numbers,
                barcode_datas=barcode_datas,
            )
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a shipment request for the carrier API"""
    # Convert karrio models to carrier-specific format
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    return_address = lib.to_address(payload.return_address)
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    weight_unit, dim_unit = packages.compatible_units

    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=weight_unit.value,
    )
    vendor = lib.to_address(
        dict(
            sender=payload.shipper,
            recipient=payload.recipient,
            third_party=customs.duty_billing_address,
        )[customs.duty.paid_by]
    )
    label_format = lib.identity(
        payload.label_type or settings.connection_config.label_type.state
    )
    label_encoding = "BASE64"
    is_import_request = lib.identity(
        options.landmark_import_request.state
        if options.landmark_import_request.state is not None
        else settings.connection_config.import_request_by_default.state
    )
    produce_label = lib.identity(
        options.landmark_produce_label.state
        if options.landmark_produce_label.state is not None
        else (
            settings.connection_config.impport_request_produce_label.state
            if settings.connection_config.impport_request_produce_label.state
            is not None
            else False
        )
    )
    items = lib.identity(customs.commodities if payload.customs else packages.items)

    request = lib.identity(
        import_req.ImportRequest(
            Login=import_req.LoginType(
                Username=settings.username,
                Password=settings.password,
            ),
            Test=settings.test_mode,
            ClientID=settings.client_id,
            AccountNumber=settings.account_number,
            Reference=payload.reference,
            ShipTo=import_req.ShipToType(
                Name=recipient.company_name or recipient.person_name or "",
                Attention=recipient.person_name,
                Address1=recipient.address_line1 or "",
                Address2=recipient.address_line2,
                Address3=None,
                City=recipient.city or "",
                State=lib.text(recipient.state_code, max=25) or "",
                PostalCode=recipient.postal_code or "",
                Country=recipient.country_code or "",
                Phone=recipient.phone_number,
                Email=recipient.email,
                ConsigneeTaxID=recipient.tax_id,
            ),
            ShippingLane=import_req.ShippingLaneType(
                Region=settings.region,
            ),
            ShipMethod=service,
            OrderTotal=lib.identity(
                customs.duty.declared_value or options.declared_value.state
            ),
            OrderInsuranceFreightTotal=options.landmark_order_insurance_freight_total.state,
            ShipmentInsuranceFreight=options.landmark_shipment_insurance_freight.state,
            ItemsCurrency=options.currency.state,
            IsCommercialShipment=("1" if customs.commercial_invoice else "0"),
            ProduceLabel=produce_label,
            LabelFormat=label_format,
            LabelEncoding=label_encoding,
            ShipOptions=None,
            VendorInformation=lib.identity(
                import_req.VendorInformationType(
                    VendorName=vendor.company_name or vendor.person_name or "",
                    VendorPhone=vendor.phone_number or "",
                    VendorEmail=vendor.email or "",
                    VendorAddress1=vendor.address_line1 or "",
                    VendorAddress2=vendor.address_line2,
                    VendorCity=vendor.city or "",
                    VendorState=lib.text(vendor.state_code, max=25) or "",
                    VendorPostalCode=vendor.postal_code or "",
                    VendorCountry=vendor.country_code or "",
                    VendorLowValueTaxID=customs.options.low_value_tax_id.state,
                    VendorCCN=customs.options.ccn.state,
                    VendorBusinessNumber=customs.options.business_number.state,
                    VendorRGRNumber=customs.options.rgr_number.state,
                    VendorIOSSNumber=customs.options.ioss.state,
                    VendorEORINumber=customs.options.eori_number.state,
                )
                if payload.customs
                else None
            ),
            FulfillmentAddress=import_req.FulfillmentAddressType(
                Name=shipper.company_name or shipper.person_name or "",
                Attention=shipper.person_name,
                Address1=shipper.address_line1 or "",
                Address2=shipper.address_line2,
                Address3=None,
                City=shipper.city or "",
                State=lib.text(shipper.state_code, max=25) or "",
                PostalCode=shipper.postal_code or "",
                Country=shipper.country_code or "",
            ),
            ReturnAddress=lib.identity(
                import_req.SendReturnToAddressType(
                    Code=options.landmark_return_address_code.state,
                    Name=return_address.company_name
                    or return_address.person_name
                    or "",
                    Attention=return_address.person_name,
                    Address1=return_address.address_line1 or "",
                    Address2=return_address.address_line2,
                    Address3=None,
                    City=return_address.city or "",
                    State=lib.text(return_address.state_code, max=25) or "",
                    PostalCode=return_address.postal_code or "",
                    Country=return_address.country_code or "",
                )
                if payload.return_address
                else None
            ),
            AdditionalFields=None,
            PickSlipAdditions=None,
            ValueAddedServices=None,
            Packages=lib.identity(
                import_req.PackagesType(
                    Package=[
                        import_req.PackageType(
                            WeightUnit=weight_unit.value,
                            Weight=pkg.weight[weight_unit.value],
                            DimensionsUnit=dim_unit.value,
                            Length=pkg.length[dim_unit.value],
                            Width=pkg.width[dim_unit.value],
                            Height=pkg.height[dim_unit.value],
                            PackageReference=pkg.reference_number,
                        )
                        for pkg in packages
                    ]
                )
                if options.fulfilled_by_landmark.state is not True
                else None
            ),
            Items=lib.identity(
                import_req.ItemsType(
                    Item=[
                        import_req.ItemType(
                            Sku=item.sku or "",
                            LineNumber=item.metadata.get("LineNumber"),
                            Quantity=lib.to_int(item.quantity),
                            UnitPrice=lib.to_money(item.value_amount),
                            Description=item.description or item.title or "",
                            HSCode=item.hs_code,
                            CountryOfOrigin=item.origin_country,
                            URL=item.product_url,
                            USMID=item.metadata.get("USMID"),
                            ContentCategory=import_req.ContentCategoryType(
                                ReturnCustomsInfo=lib.identity(
                                    import_req.ReturnCustomsInfoType(
                                        HSCode=item.hs_code,
                                        HSRegionCode=item.origin_country,
                                    )
                                    if item.hs_code or item.origin_country
                                    else None
                                ),
                                DangerousGoodsInformation=lib.identity(
                                    import_req.DangerousGoodsInformationType(
                                        UNCode=item.metadata.get("UNCode"),
                                        PackingGroup=item.metadata.get("PackingGroup"),
                                        PackingInstructions=item.metadata.get(
                                            "PackingInstructions"
                                        ),
                                        ItemWeight=item.weight,
                                        ItemWeightUnit=(
                                            item.weight_unit.lower()
                                            if item.weight_unit
                                            else None
                                        ),
                                        ItemVolume=item.metadata.get("ItemVolume"),
                                        ItemVolumeUnit=item.metadata.get(
                                            "ItemVolumeUnit"
                                        ),
                                    )
                                    if options.dangerous_goods.state
                                    else None
                                ),
                                ValueAddedServices=None,
                            ),
                        )
                        for item in items
                    ]
                )
                if len(items) > 0
                else None
            ),
            FreightDetails=lib.identity(
                import_req.FreightDetailsType(
                    ProNumber=options.landmark_freight_pro_number.state or "",
                    PieceUnit=options.landmark_freight_piece_unit.state or "",
                )
                if options.landmark_freight_pro_number.state
                and options.landmark_freight_piece_unit.state
                else None
            ),
        )
        if is_import_request
        else ship_req.ShipRequest(
            Login=ship_req.LoginType(
                Username=settings.username,
                Password=settings.password,
            ),
            Test=settings.test_mode,
            ClientID=settings.client_id,
            AccountNumber=settings.account_number,
            Reference=payload.reference,
            ShipTo=ship_req.ShipToType(
                Name=recipient.company_name or recipient.person_name or "",
                Attention=recipient.person_name,
                Address1=recipient.address_line1 or "",
                Address2=recipient.address_line2,
                Address3=None,
                City=recipient.city or "",
                State=lib.text(recipient.state_code, max=25) or "",
                PostalCode=recipient.postal_code or "",
                Country=recipient.country_code or "",
                Phone=recipient.phone_number,
                Email=recipient.email,
                ConsigneeTaxID=recipient.tax_id,
            ),
            ShippingLane=lib.identity(
                ship_req.ShippingLaneType(Region=settings.region)
                if settings.region
                else None
            ),
            ShipMethod=service,
            OrderTotal=lib.identity(
                customs.duty.declared_value
                if customs.duty and customs.duty.declared_value
                else options.declared_value.state
            ),
            OrderInsuranceFreightTotal=options.landmark_order_insurance_freight_total.state,
            ShipmentInsuranceFreight=options.landmark_shipment_insurance_freight.state,
            ItemsCurrency=options.currency.state,
            IsCommercialShipment="1" if customs.commercial_invoice else "0",
            LabelFormat=label_format,
            LabelDPI=("300" if label_format == "ZPL" else None),
            LabelEncoding=label_encoding,
            ShipOptions=None,
            VendorInformation=lib.identity(
                ship_req.VendorInformationType(
                    VendorName=vendor.company_name or vendor.person_name or "",
                    VendorPhone=vendor.phone_number or "",
                    VendorEmail=vendor.email or "",
                    VendorAddress1=vendor.address_line1 or "",
                    VendorAddress2=vendor.address_line2,
                    VendorCity=vendor.city or "",
                    VendorState=lib.text(vendor.state_code, max=25) or "",
                    VendorPostalCode=vendor.postal_code or "",
                    VendorCountry=vendor.country_code or "",
                    VendorLowValueTaxID=customs.options.low_value_tax_id.state,
                    VendorCCN=customs.options.ccn.state,
                    VendorBusinessNumber=customs.options.business_number.state,
                    VendorRGRNumber=customs.options.rgr_number.state,
                    VendorIOSSNumber=customs.options.ioss.state,
                    VendorEORINumber=customs.options.eori_number.state,
                )
                if payload.customs
                else None
            ),
            ReturnInformation=None,
            FulfillmentAddress=ship_req.FulfillmentAddressType(
                Name=shipper.company_name or shipper.person_name or "",
                Attention=shipper.person_name,
                Address1=shipper.address_line1 or "",
                Address2=shipper.address_line2,
                Address3=None,
                City=shipper.city or "",
                State=lib.text(shipper.state_code, max=25) or "",
                PostalCode=shipper.postal_code or "",
                Country=shipper.country_code or "",
            ),
            SendReturnToAddress=lib.identity(
                ship_req.SendReturnToAddressType(
                    Code=options.landmark_return_address_code.state,
                    Name=return_address.company_name
                    or return_address.person_name
                    or "",
                    Attention=return_address.person_name,
                    Address1=return_address.address_line1 or "",
                    Address2=return_address.address_line2,
                    Address3=None,
                    City=return_address.city or "",
                    State=lib.text(return_address.state_code, max=25) or "",
                    PostalCode=return_address.postal_code or "",
                    Country=return_address.country_code or "",
                )
                if payload.return_address
                else None
            ),
            AdditionalFields=None,
            Packages=lib.identity(
                ship_req.PackagesType(
                    Package=[
                        ship_req.PackageType(
                            WeightUnit=pkg.weight_unit.value,
                            Weight=pkg.weight[weight_unit.value],
                            DimensionsUnit=dim_unit.value,
                            Length=pkg.length[dim_unit.value],
                            Width=pkg.width[dim_unit.value],
                            Height=pkg.height[dim_unit.value],
                            PackageReference=pkg.parcel.reference_number,
                        )
                        for pkg in packages
                    ]
                )
                if options.fulfilled_by_landmark.state is not True
                else None
            ),
            Items=lib.identity(
                ship_req.ItemsType(
                    Item=[
                        ship_req.ItemType(
                            Sku=item.sku or "",
                            LineNumber=item.metadata.get("LineNumber"),
                            Quantity=item.quantity,
                            UnitPrice=item.value_amount,
                            Description=item.description or item.title or "",
                            HSCode=item.hs_code,
                            CountryOfOrigin=item.origin_country,
                            ContentCategory=item.category,
                            URL=item.product_url,
                            USMID=item.metadata.get("USMID"),
                            ReturnCustomsInfo=lib.identity(
                                ship_req.ReturnCustomsInfoType(
                                    HSCode=item.hs_code,
                                    HSRegionCode=item.origin_country,
                                )
                                if item.hs_code or item.origin_country
                                else None
                            ),
                            DangerousGoodsInformation=None,
                        )
                        for item in items
                    ]
                )
                if len(items) > 0
                else None
            ),
            FreightDetails=lib.identity(
                ship_req.FreightDetailsType(
                    ProNumber=options.landmark_freight_pro_number.state or "",
                    PieceUnit=options.landmark_freight_piece_unit.state or "",
                )
                if options.landmark_freight_pro_number.state
                and options.landmark_freight_piece_unit.state
                else None
            ),
        )
    )

    return lib.Serializable(
        request,
        lib.to_xml,
        ctx=dict(
            API=("Import" if is_import_request else "Ship"),
            label_format=label_format,
            label_encoding=label_encoding,
            is_import_request=is_import_request,
            produce_label=(produce_label if is_import_request else None),
        ),
    )
