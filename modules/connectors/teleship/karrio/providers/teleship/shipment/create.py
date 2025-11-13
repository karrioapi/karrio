"""Karrio Teleship shipment API implementation."""

import karrio.schemas.teleship.shipment_request as teleship_req
import karrio.schemas.teleship.shipment_response as teleship_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.teleship.error as error
import karrio.providers.teleship.utils as provider_utils
import karrio.providers.teleship.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Extract shipment details if present (work with raw dict)
    shipment = lib.identity(
        _extract_details(response, settings)
        if response.get("shipment")
        else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    """Extract shipment details from carrier response data"""
    # Convert to typed object for safe attribute access
    shipment_data = data.get("shipment") or {}
    shipment = lib.to_object(teleship_res.ShipmentType, shipment_data)

    # Extract charges using functional pattern (work with raw dicts)
    charges = [
        lib.to_object(teleship_res.ChargeType, charge)
        for charge in (shipment_data.get("charges") or [])
    ]

    # Calculate selected rate if charges are present
    selected_rate = lib.identity(
        models.RateDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            service=shipment.serviceCode or "",
            total_charge=lib.to_money(shipment.totalCharge.amount if shipment.totalCharge else 0),
            currency=shipment.totalCharge.currency if shipment.totalCharge else "USD",
            extra_charges=[
                models.ChargeDetails(
                    name=charge.name or "",
                    amount=lib.to_money(charge.amount),
                    currency=charge.currency or (shipment.totalCharge.currency if shipment.totalCharge else "USD"),
                )
                for charge in charges
            ] if any(charges) else [],
            meta=dict(
                service_name=shipment.serviceName or "",
            ),
        )
        if shipment.totalCharge and shipment.totalCharge.amount
        else None
    )

    # Extract label document from documents array
    label_doc = lib.identity(
        next(
            (doc for doc in (shipment.documents or []) if doc.type == "LABEL"),
            None
        )
    )

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.trackingNumber or "",
        shipment_identifier=shipment.shipmentId or "",
        label_type=label_doc.format if label_doc else "PDF",
        docs=models.Documents(label=label_doc.base64String if label_doc else ""),
        selected_rate=selected_rate,
        meta=dict(
            service_code=shipment.serviceCode,
            service_name=shipment.serviceName,
            customer_reference=shipment.customerReference,
            ship_date=shipment.shipDate,
            estimated_delivery=shipment.estimatedDelivery,
            package_type=shipment.packageType,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a shipment request for the carrier API"""
    # Convert karrio models using functional lib utilities
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
    )

    # Use functional pattern to select first package
    package = packages[0] if any(packages) else None

    # Build request using typed schema classes
    request = teleship_req.ShipmentRequestType(
        serviceCode=options.teleship_service_code.state or service,
        customerReference=payload.reference or options.teleship_customer_reference.state,
        description=options.teleship_shipment_description.state,
        shipDate=options.shipment_date.state,
        orderTrackingReference=options.teleship_order_tracking_reference.state,
        commercialInvoiceReference=lib.failsafe(lambda: customs.options.commercial_invoice_reference.state) if payload.customs else None,
        packageType=lib.identity(
            provider_units.PackagingType.map(
                package.packaging_type or "your_packaging"
            ).value if package else "parcel"
        ),
        shipTo=teleship_req.BillToType(
            name=recipient.person_name or recipient.company_name,
            company=recipient.company_name,
            email=recipient.email,
            phone=recipient.phone_number,
            address=teleship_req.AddressType(
                line1=recipient.address_line1,
                line2=recipient.address_line2,
                city=recipient.city,
                state=recipient.state_code,
                postcode=recipient.postal_code,
                country=recipient.country_code,
            ),
        ),
        shipFrom=teleship_req.BillToType(
            name=shipper.person_name or shipper.company_name,
            company=shipper.company_name,
            email=shipper.email,
            phone=shipper.phone_number,
            address=teleship_req.AddressType(
                line1=shipper.address_line1,
                line2=shipper.address_line2,
                city=shipper.city,
                state=shipper.state_code,
                postcode=shipper.postal_code,
                country=shipper.country_code,
            ),
        ),
        returnTo=lib.identity(
            teleship_req.BillToType(
                name=shipper.person_name or shipper.company_name,
                company=shipper.company_name,
                email=shipper.email,
                phone=shipper.phone_number,
                address=teleship_req.AddressType(
                    line1=shipper.address_line1,
                    line2=shipper.address_line2,
                    city=shipper.city,
                    state=shipper.state_code,
                    postcode=shipper.postal_code,
                    country=shipper.country_code,
                ),
            ) if options.teleship_return_address.state else None
        ),
        billTo=lib.identity(
            teleship_req.BillToType(
                name=lib.failsafe(lambda: payload.payment.account_number) or shipper.person_name or shipper.company_name,
                company=shipper.company_name,
                email=shipper.email,
                phone=shipper.phone_number,
                address=teleship_req.AddressType(
                    line1=shipper.address_line1,
                    line2=shipper.address_line2,
                    city=shipper.city,
                    state=shipper.state_code,
                    postcode=shipper.postal_code,
                    country=shipper.country_code,
                ),
                taxId=lib.identity(
                    teleship_req.TaxIDType(
                        type=lib.failsafe(lambda: customs.options.tax_id_type.state) or "VAT",
                        value=lib.failsafe(lambda: customs.options.tax_id.state),
                    ) if lib.failsafe(lambda: customs.options.tax_id.state) else None
                ),
            ) if payload.payment or lib.failsafe(lambda: customs.options.tax_id.state) else None
        ),
        weight=lib.identity(
            teleship_req.WeightType(
                value=package.weight.value,
                unit=package.weight.unit.lower(),
            ) if package else None
        ),
        dimensions=lib.identity(
            teleship_req.DimensionsType(
                unit=package.dimension_unit.lower(),
                length=package.length.value if package.length else None,
                width=package.width.value if package.width else None,
                height=package.height.value if package.height else None,
            ) if package and all([package.length, package.width, package.height]) else None
        ),
        additionalServices=lib.identity(
            teleship_req.AdditionalServicesType(
                signatureRequired=options.teleship_signature_required.state,
                deliveryWarranty=options.teleship_delivery_warranty.state,
                deliveryPUDO=options.teleship_delivery_pudo.state,
                lowCarbon=options.teleship_low_carbon.state,
                dutyTaxCalculation=options.teleship_duty_tax_calculation.state,
            ) if any([
                options.teleship_signature_required.state,
                options.teleship_delivery_warranty.state,
                options.teleship_delivery_pudo.state,
                options.teleship_low_carbon.state,
                options.teleship_duty_tax_calculation.state,
            ]) else None
        ),
        commodities=[
            teleship_req.CommodityType(
                sku=commodity.sku,
                EAN=commodity.metadata.get("ean") if commodity.metadata else None,
                TARIC=int(commodity.metadata.get("taric")) if commodity.metadata and commodity.metadata.get("taric") else None,
                HSTariffNumber=int(commodity.hs_code) if commodity.hs_code and commodity.hs_code.isdigit() else None,
                title=commodity.title or commodity.description,
                description=commodity.description,
                category=commodity.metadata.get("category") if commodity.metadata else None,
                value=teleship_req.ValueType(
                    amount=int(commodity.value_amount or 0),
                    currency=commodity.value_currency or "USD",
                ),
                quantity=commodity.quantity or 1,
                unitWeight=teleship_req.WeightType(
                    value=commodity.weight,
                    unit=(commodity.weight_unit or "KG").lower(),
                ),
                netWeight=lib.identity(
                    teleship_req.WeightType(
                        value=float(commodity.metadata.get("net_weight")) if commodity.metadata and commodity.metadata.get("net_weight") else commodity.weight,
                        unit=(commodity.weight_unit or "KG").lower(),
                    ) if commodity.metadata and commodity.metadata.get("net_weight") else None
                ),
                countryOfOrigin=commodity.origin_country,
                imageUrl=commodity.metadata.get("image_url") if commodity.metadata else None,
                productUrl=commodity.metadata.get("product_url") if commodity.metadata else None,
                compliance=lib.identity(
                    teleship_req.ComplianceType(
                        requiresLicensing=commodity.metadata.get("requires_licensing") if commodity.metadata else None,
                        isHazardous=commodity.metadata.get("is_hazardous") if commodity.metadata else None,
                        isRestricted=commodity.metadata.get("is_restricted") if commodity.metadata else None,
                        regulatoryInfo=commodity.metadata.get("regulatory_info") if commodity.metadata else None,
                    ) if commodity.metadata and any([
                        commodity.metadata.get("requires_licensing"),
                        commodity.metadata.get("is_hazardous"),
                        commodity.metadata.get("is_restricted"),
                        commodity.metadata.get("regulatory_info"),
                    ]) else None
                ),
                dutiesAndTaxes=lib.identity(
                    teleship_req.DutiesAndTaxesType(
                        dutyAmount=float(commodity.metadata.get("duty_amount")) if commodity.metadata and commodity.metadata.get("duty_amount") else None,
                        dutyRate=float(commodity.metadata.get("duty_rate")) if commodity.metadata and commodity.metadata.get("duty_rate") else None,
                        taxAmount=float(commodity.metadata.get("tax_amount")) if commodity.metadata and commodity.metadata.get("tax_amount") else None,
                        taxRate=float(commodity.metadata.get("tax_rate")) if commodity.metadata and commodity.metadata.get("tax_rate") else None,
                        currency=commodity.value_currency or "USD",
                    ) if commodity.metadata and any([
                        commodity.metadata.get("duty_amount"),
                        commodity.metadata.get("duty_rate"),
                        commodity.metadata.get("tax_amount"),
                        commodity.metadata.get("tax_rate"),
                    ]) else None
                ),
            )
            for commodity in (customs.commodities or [])
        ] if payload.customs and any(customs.commodities or []) else [],
        customs=lib.identity(
            teleship_req.CustomsType(
                EORI=lib.failsafe(lambda: customs.options.eori_number.state),
                IOSS=lib.failsafe(lambda: customs.options.ioss.state),
                VAT=lib.failsafe(lambda: customs.options.vat.state),
                EIN=lib.failsafe(lambda: customs.options.ein.state),
                VOECNUMBER=lib.failsafe(lambda: customs.options.voec_number.state),
                importerGST=lib.failsafe(lambda: customs.options.importer_gst.state),
                exporterGST=lib.failsafe(lambda: customs.options.exporter_gst.state),
                consigneeGST=lib.failsafe(lambda: customs.options.consignee_gst.state),
                contentType=provider_units.CustomsContentType.map(customs.content_type or "other").value,
                invoiceDate=customs.invoice_date,
                invoiceNumber=customs.invoice,
                GPSRContactInfo=lib.identity(
                    teleship_req.GPSRContactInfoType(
                        name=lib.failsafe(lambda: customs.options.gpsr_contact_name.state),
                        email=lib.failsafe(lambda: customs.options.gpsr_contact_email.state),
                        phone=lib.failsafe(lambda: customs.options.gpsr_contact_phone.state),
                        address=lib.identity(
                            teleship_req.AddressType(
                                line1=lib.failsafe(lambda: customs.options.gpsr_contact_address_line1.state),
                                city=lib.failsafe(lambda: customs.options.gpsr_contact_city.state),
                                state=lib.failsafe(lambda: customs.options.gpsr_contact_state.state),
                                country=lib.failsafe(lambda: customs.options.gpsr_contact_country.state),
                                postcode=lib.failsafe(lambda: customs.options.gpsr_contact_postcode.state),
                            ) if lib.failsafe(lambda: customs.options.gpsr_contact_address_line1.state) else None
                        ),
                    ) if lib.failsafe(lambda: customs.options.gpsr_contact_name.state) else None
                ),
                importerOfRecord=lib.identity(
                    teleship_req.BillToType(
                        name=lib.failsafe(lambda: customs.options.importer_name.state),
                        company=lib.failsafe(lambda: customs.options.importer_company.state),
                        email=lib.failsafe(lambda: customs.options.importer_email.state),
                        phone=lib.failsafe(lambda: customs.options.importer_phone.state),
                        address=lib.identity(
                            teleship_req.AddressType(
                                line1=lib.failsafe(lambda: customs.options.importer_address_line1.state),
                                line2=lib.failsafe(lambda: customs.options.importer_address_line2.state),
                                city=lib.failsafe(lambda: customs.options.importer_city.state),
                                state=lib.failsafe(lambda: customs.options.importer_state.state),
                                country=lib.failsafe(lambda: customs.options.importer_country.state),
                                postcode=lib.failsafe(lambda: customs.options.importer_postcode.state),
                            ) if lib.failsafe(lambda: customs.options.importer_address_line1.state) else None
                        ),
                        taxId=lib.identity(
                            teleship_req.TaxIDType(
                                type=lib.failsafe(lambda: customs.options.importer_tax_id_type.state),
                                value=lib.failsafe(lambda: customs.options.importer_tax_id.state),
                            ) if lib.failsafe(lambda: customs.options.importer_tax_id.state) else None
                        ),
                    ) if lib.failsafe(lambda: customs.options.importer_name.state) else None
                ),
            ) if payload.customs else None
        ),
        metadata=lib.identity(
            teleship_req.MetadataType(
                fulfillmentOrderId=options.teleship_order_tracking_reference.state,
            ) if options.teleship_order_tracking_reference.state else None
        ),
    )

    return lib.Serializable(request, lib.to_dict)
