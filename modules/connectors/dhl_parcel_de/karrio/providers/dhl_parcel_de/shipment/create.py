import karrio.schemas.dhl_parcel_de.shipping_request as dhl_parcel_de
import karrio.schemas.dhl_parcel_de.shipping_response as shipping
import typing
import datetime
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dhl_parcel_de.error as error
import karrio.providers.dhl_parcel_de.utils as provider_utils
import karrio.providers.dhl_parcel_de.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    items = response.get("items") or []

    messages = error.parse_error_response(response, settings)
    shipment = (
        lib.to_multi_piece_shipment(
            [
                (f"{_}", _extract_details(item, settings))
                for _, item in enumerate(items, start=1)
            ]
        )
        if any([lib.failsafe(lambda: _["sstatus"]["statusCode"]) == 200 for _ in items])
        else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    shipment = lib.to_object(shipping.ItemType, data)
    label_type = shipment.label.fileFormat or "PDF"
    label = shipment.label.b64 if label_type == "PDF" else shipment.label.zpl2
    invoice = getattr(shipment.customsDoc, "b64", None)
    tracking_number = str(shipment.shipmentNo)

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=tracking_number,
        label_type=label_type,
        docs=models.Documents(label=label, invoice=invoice),
        meta=dict(
            carrier_tracking_link=settings.tracking_url.format(tracking_number),
            shipmentNo=shipment.shipmentNo,
            shipmentRefNo=shipment.shipmentRefNo,
            tracking_numbers=[tracking_number],
            shipment_identifiers=[tracking_number],
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
        initializer=provider_units.shipping_options_initializer,
    )
    packages = lib.to_packages(
        payload.parcels,
        required=["weight"],
        options=payload.options,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )
    customs = lib.to_customs_info(
        payload.customs,
        weight_unit=units.WeightUnit.KG.name,
        option_type=provider_units.CustomsOption,
    )
    is_intl = shipper.country_code != recipient.country_code
    doc_format, print_format = provider_units.LabelType.map(
        settings.connection_config.label_type.state or payload.label_type or "PDF"
    ).value
    shipment_date = lib.to_date(
        options.shipping_date.state or datetime.datetime.now(),
        "%Y-%m-%dT%H:%M",
    )

    request = dhl_parcel_de.ShippingRequestType(
        profile=settings.profile,
        shipments=[
            dhl_parcel_de.ShipmentType(
                product=service,
                billingNumber=settings.billing_number,
                refNo=payload.reference,
                costCenter=settings.connection_config.cost_center.state,
                creationSoftware=settings.connection_config.creation_software.state,
                shipDate=lib.fdatetime(
                    shipment_date, output_format="%Y-%m-%dT%H:%M:%S"
                ),
                shipper=dhl_parcel_de.ShipperType(
                    name1=shipper.company_name or shipper.person_name,
                    name2=(shipper.person_name if shipper.company_name else None),
                    name3=None,
                    addressStreet=lib.identity(
                        shipper.street_name
                        if payload.shipper.street_number
                        else shipper.address_line1
                    ),
                    addressHouse=lib.identity(
                        payload.shipper.street_number
                        if payload.shipper.street_number
                        else shipper.address_line2
                    ),
                    postalCode=shipper.postal_code,
                    city=shipper.city,
                    country=units.CountryCode.map(shipper.country_code).value_or_key,
                    contactName=shipper.person_name,
                    email=shipper.email,
                ),
                consignee=dhl_parcel_de.ConsigneeType(
                    name1=recipient.company_name or recipient.person_name,
                    name2=(recipient.person_name if recipient.company_name else None),
                    name3=None,
                    dispatchingInformation=None,
                    addressStreet=lib.identity(
                        recipient.street_name
                        if payload.recipient.street_number
                        else recipient.address_line1
                    ),
                    addressHouse=lib.identity(
                        recipient.street_number
                        if payload.recipient.street_number
                        else recipient.address_line2
                    ),
                    additionalAddressInformation1=None,
                    additionalAddressInformation2=None,
                    postalCode=recipient.postal_code,
                    city=recipient.city,
                    state=recipient.state_code,
                    country=units.CountryCode.map(recipient.country_code).value_or_key,
                    contactName=recipient.person_name,
                    phone=recipient.phone_number,
                    email=recipient.email,
                    name=recipient.contact,
                    lockerID=package.options.dhl_parcel_de_locker_id.state,
                    postNumber=package.options.dhl_parcel_de_post_number.state,
                    retailID=package.options.dhl_parcel_de_retail_id.state,
                    poBoxID=package.options.dhl_parcel_de_po_box_id.state,
                ),
                details=dhl_parcel_de.DetailsType(
                    dim=dhl_parcel_de.DimType(
                        uom=units.DimensionUnit.CM.name.lower(),
                        height=package.height.CM,
                        length=package.length.CM,
                        width=package.width.CM,
                    ),
                    weight=dhl_parcel_de.WeightType(
                        uom=units.WeightUnit.KG.name.lower(),
                        value=package.weight.KG,
                    ),
                ),
                services=dhl_parcel_de.ServicesType(
                    preferredNeighbour=package.options.dhl_parcel_de_preferred_neighbour.state,
                    preferredLocation=package.options.dhl_parcel_de_preferred_location.state,
                    visualCheckOfAge=package.options.dhl_parcel_de_visual_check_of_age.state,
                    namedPersonOnly=package.options.dhl_parcel_de_named_person_only.state,
                    identCheck=None,
                    signedForByRecipient=package.options.dhl_parcel_de_signed_for_by_recipient.state,
                    endorsement=lib.identity(
                        package.options.dhl_parcel_de_endorsement.state or "RETURN"
                    ),
                    preferredDay=package.options.dhl_parcel_de_preferred_day.state,
                    noNeighbourDelivery=package.options.dhl_parcel_de_no_neighbour_delivery.state,
                    additionalInsurance=lib.identity(
                        dhl_parcel_de.PostalChargesType(
                            currency=package.options.currency.state,
                            value=package.options.dhl_parcel_de_additional_insurance.state,
                        )
                        if package.options.dhl_parcel_de_additional_insurance.state
                        is not None
                        else None
                    ),
                    bulkyGoods=package.options.dhl_parcel_de_bulky_goods.state,
                    cashOnDelivery=lib.identity(
                        dhl_parcel_de.CashOnDeliveryType(
                            currency=package.options.currency.state,
                            value=package.options.dhl_parcel_de_cash_on_delivery.state,
                        )
                        if package.options.dhl_parcel_de_cash_on_delivery.state
                        is not None
                        else None
                    ),
                    individualSenderRequirement=package.options.dhl_parcel_de_individual_sender_requirement.state,
                    premium=package.options.dhl_parcel_de_premium.state,
                    closestDropPoint=package.options.dhl_parcel_de_closest_drop_point.state,
                    parcelOutletRouting=package.options.dhl_parcel_de_parcel_outlet_routing.state,
                    dhlRetoure=package.options.dhl_parcel_de_dhl_retoure.state,
                    postalDeliveryDutyPaid=package.options.dhl_parcel_de_postal_delivery_duty_paid.state,
                ),
                customs=(
                    dhl_parcel_de.CustomsType(
                        invoiceNo=customs.invoice,
                        exportType=lib.identity(
                            provider_units.CustomsContentType.map(
                                customs.content_type
                            ).value
                            or "COMMERCIAL_GOODS"
                        ),
                        exportDescription=lib.identity(
                            customs.content_description
                            or package.parcel.description
                            or "Other"
                        ),
                        shippingConditions=(
                            provider_units.Incoterm.map(customs.incoterm).value or "DDP"
                        ),
                        permitNo=package.options.dhl_parcel_de_permit_no.state,
                        attestationNo=package.options.dhl_parcel_de_attestation_no.state,
                        hasElectronicExportNotification=package.options.dhl_parcel_de_has_electronic_export_notification.state,
                        MRN=package.options.dhl_parcel_de_MRN.state,
                        postalCharges=lib.identity(
                            dhl_parcel_de.PostalChargesType(
                                currency=(
                                    package.options.currency.state
                                    or customs.duty.currency
                                    or "EUR"
                                ),
                                value=package.options.dhl_parcel_de_postal_charges.state,
                            )
                            if package.options.dhl_parcel_de_postal_charges.state
                            is not None
                            else None
                        ),
                        officeOfOrigin=units.CountryCode.map(
                            shipper.country_code
                        ).value_or_key,
                        shipperCustomsRef=package.options.dhl_parcel_de_shipper_customs_ref.state,
                        consigneeCustomsRef=package.options.dhl_parcel_de_consignee_customs_ref.state,
                        items=[
                            dhl_parcel_de.ItemType(
                                itemDescription=item.description or item.title,
                                countryOfOrigin=units.CountryCode.map(
                                    item.origin_country
                                    or shipper.country_code
                                    or settings.account_country_code
                                    or "DE"
                                ).value_or_key,
                                hsCode=item.hs_code,
                                packagedQuantity=item.quantity,
                                itemValue=(
                                    dhl_parcel_de.PostalChargesType(
                                        currency=lib.identity(
                                            item.value_currency
                                            or package.options.currency.state
                                            or customs.duty.currency
                                            or "EUR"
                                        ),
                                        value=item.value_amount or 0.0,
                                    )
                                    if item.value_amount is not None
                                    else None
                                ),
                                itemWeight=dhl_parcel_de.WeightType(
                                    uom=units.WeightUnit.KG.name.lower(),
                                    value=item.weight,
                                ),
                            )
                            for item in customs.commodities
                        ],
                    )
                    if payload.customs is not None and is_intl
                    else None
                ),
            )
            for package in packages
        ],
    )

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(
            includeDocs="include" if is_intl else None,
            docFormat=doc_format,
            printFormat=print_format,
            combine="true",
            # validate="true",
        ),
    )
