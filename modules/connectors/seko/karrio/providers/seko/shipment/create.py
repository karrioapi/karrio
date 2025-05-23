"""Karrio SEKO Logistics shipment API implementation."""

import karrio.schemas.seko.shipping_request as seko
import karrio.schemas.seko.shipping_response as shipping

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.seko.error as error
import karrio.providers.seko.utils as provider_utils
import karrio.providers.seko.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    print(_response.ctx)
    messages = error.parse_error_response(response, settings)
    shipment = lib.identity(
        _extract_details(response, settings, ctx=_response.ctx)
        if any(response.get("Consignments", []))
        else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict = None,
) -> models.ShipmentDetails:
    details = lib.to_object(shipping.ShippingResponseType, data)
    Connotes = [_.Connote for _ in details.Consignments]
    TrackingUrls = [_.TrackingUrl for _ in details.Consignments]
    ConsignmentIds = [_.ConsignmentId for _ in details.Consignments]
    label_type = ctx.get("label_type")
    label_format = ctx.get("label_format")

    label = lib.bundle_base64(
        sum([_["OutputFiles"][label_type] for _ in data["Consignments"]], []),
        label_format,
    )

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=Connotes[0],
        shipment_identifier=ConsignmentIds[0],
        label_type=label_format,
        docs=models.Documents(label=label),
        meta=dict(
            carrier_tracking_link=TrackingUrls[0],
            seko_site_id=details.SiteId,
            tracking_urls=TrackingUrls,
            consignment_id=ConsignmentIds[0],
            consignment_ids=ConsignmentIds,
            seko_carrier_id=details.CarrierId,
            seko_carrier_name=details.CarrierName,
            seko_carrier_type=details.CarrierType,
            rate_provider=details.CarrierName,
            seko_invoice_response=details.InvoiceResponse,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=units.WeightUnit.KG.name,
        option_type=provider_units.CustomsOption,
    )
    commodities: units.Products = lib.identity(
        customs.commodities if payload.customs else packages.items
    )
    [label_format, label_type] = lib.identity(
        provider_units.LabelType.map(payload.label_type).value
        or provider_units.LabelType.PDF.value
    )
    commercial_invoice = lib.identity(
        options.seko_invoice_data.state
        or next((
            _["doc_file"] for _ in options.doc_files.state or []
            if _["doc_type"] == "commercial_invoice"
            and _.get("doc_format", "PDF").lower() == "pdf"
        ), None)
    )

    # map data to convert karrio model to seko specific type
    request = seko.ShippingRequestType(
        DeliveryReference=payload.reference,
        Reference2=options.seko_reference_2.state,
        Reference3=options.seko_reference_3.state,
        Origin=seko.DestinationType(
            Id=options.seko_origin_id.state,
            Name=lib.identity(shipper.company_name or shipper.contact or "Shipper"),
            Address=seko.AddressType(
                BuildingName=None,
                StreetAddress=shipper.street,
                Suburb=shipper.city,
                City=shipper.state_code or shipper.city,
                PostCode=shipper.postal_code,
                CountryCode=shipper.country_code,
            ),
            ContactPerson=shipper.contact,
            PhoneNumber=shipper.phone_number or "000 000 0000",
            Email=shipper.email or " ",
            DeliveryInstructions=options.origin_instructions.state,
            RecipientTaxId=shipper.tax_id,
            SendTrackingEmail=None,
        ),
        Destination=seko.DestinationType(
            Id=options.seko_destination_id.state,
            Name=lib.identity(
                recipient.company_name or recipient.contact or "Recipient"
            ),
            Address=seko.AddressType(
                BuildingName=None,
                StreetAddress=recipient.street,
                Suburb=recipient.city,
                City=recipient.state_code or recipient.city,
                PostCode=recipient.postal_code,
                CountryCode=recipient.country_code,
            ),
            ContactPerson=recipient.contact,
            PhoneNumber=recipient.phone_number or "000 000 0000",
            Email=recipient.email or " ",
            DeliveryInstructions=options.destination_instructions.state,
            RecipientTaxId=recipient.tax_id,
            SendTrackingEmail=options.seko_send_tracking_email.state,
        ),
        DangerousGoods=None,
        Commodities=[
            seko.CommodityType(
                Description=lib.identity(
                    lib.text(commodity.description or commodity.title, max=35) or "item"
                ),
                HarmonizedCode=commodity.hs_code or "0000.00.00",
                Units=commodity.quantity,
                UnitValue=commodity.value_amount,
                UnitKg=commodity.weight,
                Currency=commodity.value_currency,
                Country=commodity.origin_country,
                IsDG=None,
                itemSKU=commodity.sku,
                DangerousGoodsItem=None,
            )
            for commodity in commodities
        ],
        Packages=[
            seko.PackageType(
                Height=package.height.CM,
                Length=package.length.CM,
                Width=package.width.CM,
                Kg=package.weight.KG,
                Name=lib.text(package.description, max=50),
                Type=lib.identity(
                    provider_units.PackagingType.map(package.packaging_type).value
                ),
                OverLabelBarcode=package.reference_number,
            )
            for package in packages
        ],
        issignaturerequired=options.seko_is_signature_required.state,
        DutiesAndTaxesByReceiver=lib.identity(
            customs.duty.paid_by == "recipient" if payload.customs else None
        ),
        ProductCategory=options.seko_product_category.state,
        ShipType=options.seko_ship_type.state,
        PrintToPrinter=lib.identity(
            options.seko_print_to_printer.state
            if options.seko_print_to_printer.state is not None
            else True
        ),
        IncludeLineDetails=True,
        Carrier=options.seko_carrier.state,
        Service=service,
        CostCentreName=settings.connection_config.cost_center.state,
        CostCentreId=settings.connection_config.cost_center_id.state,
        CodValue=options.cash_on_delivery.state,
        TaxCollected=lib.identity(
            options.seko_tax_collected.state
            if options.seko_tax_collected.state is not None
            else True
        ),
        AmountCollected=lib.to_money(options.seko_amount_collected.state),
        CIFValue=options.seko_cif_value.state,
        FreightValue=options.seko_freight_value.state,
        SendLabel="Y" if options.seko_send_label.state else None,
        LabelBranding=settings.connection_config.label_branding.state,
        InvoiceData=commercial_invoice,
        TaxIds=[
            seko.TaxIDType(
                IdType=option.code,
                IdNumber=option.state,
            )
            for key, option in customs.options.items()
            if key in provider_units.CustomsOption and option.state is not None
        ],
        Outputs=[label_type],
    )

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(label_type=label_type, label_format=label_format),
    )
