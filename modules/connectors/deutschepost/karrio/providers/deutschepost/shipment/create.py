import karrio.schemas.deutschepost.shipping_request as deutschepost
import karrio.schemas.deutschepost.shipping_response as shipping
import typing
import datetime
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.deutschepost.error as error
import karrio.providers.deutschepost.utils as provider_utils
import karrio.providers.deutschepost.units as provider_units


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
        if any(items)
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
            label_url=shipment.label.url,
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
        options=options,
        package_option_type=provider_units.ShippingOption,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )
    customs = lib.to_customs_info(
        payload.customs,
        weight_unit=units.WeightUnit.KG.name,
        option_type=provider_units.CustomsOption,
    )
    doc_format, print_format = provider_units.LabelType.map(
        payload.label_type or "PDF"
    ).value

    request = deutschepost.ShippingRequestType(
        profile=settings.profile,
        shipments=[
            deutschepost.ShipmentType(
                product=service,
                billingNumber=settings.customer_number,
                refNo=payload.reference,
                costCenter=settings.connection_config.cost_center.state,
                creationSoftware=settings.connection_config.creation_software.state,
                shipDate=lib.fdate(
                    package.options.shipment_date.state or datetime.datetime.now()
                ),
                shipper=deutschepost.ShipperType(
                    name1=shipper.company_name or shipper.person_name or "N/A",
                    name2=shipper.person_name,
                    name3=None,
                    addressStreet=shipper.street_name,
                    addressHouse=shipper.street_number,
                    postalCode=shipper.postal_code,
                    city=shipper.city,
                    country=units.CountryCode.map(shipper.country_code).value_or_key,
                    contactName=shipper.person_name,
                    email=shipper.email,
                ),
                consignee=deutschepost.ConsigneeType(
                    name1=recipient.company_name or recipient.person_name or "N/A",
                    name2=recipient.person_name,
                    name3=None,
                    dispatchingInformation=None,
                    addressStreet=recipient.street_name,
                    addressHouse=recipient.street_number,
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
                    lockerID=options.locker_id.state,
                    postNumber=options.post_number.state,
                    retailID=options.retail_id.state,
                    poBoxID=options.po_box_id.state,
                ),
                details=deutschepost.DetailsType(
                    dim=deutschepost.DimType(
                        uom=units.DimensionUnit.CM.name.lower(),
                        height=package.height.CM,
                        length=package.length.CM,
                        width=package.width.CM,
                    ),
                    weight=deutschepost.WeightType(
                        uom=units.WeightUnit.KG.name.lower(),
                        value=package.weight.KG,
                    ),
                ),
                services=(
                    deutschepost.ServicesType(
                        preferredNeighbour=package.options.deutschepost_preferred_neighbour.state,
                        preferredLocation=package.options.deutschepost_preferred_location.state,
                        visualCheckOfAge=package.options.deutschepost_visual_check_of_age.state,
                        namedPersonOnly=package.options.deutschepost_named_person_only.state,
                        identCheck=None,
                        signedForByRecipient=package.options.deutschepost_signed_for_by_recipient.state,
                        endorsement=package.options.deutschepost_endorsement.state,
                        preferredDay=package.options.deutschepost_preferred_day.state,
                        noNeighbourDelivery=package.options.deutschepost_no_neighbour_delivery.state,
                        additionalInsurance=(
                            deutschepost.PostalChargesType(
                                currency=package.options.currency.state,
                                value=package.options.deutschepost_additional_insurance.state,
                            )
                            if package.options.deutschepost_additional_insurance.state
                            is not None
                            else None
                        ),
                        bulkyGoods=package.options.deutschepost_bulky_goods.state,
                        cashOnDelivery=(
                            deutschepost.CashOnDeliveryType(
                                currency=package.options.currency.state,
                                value=package.options.deutschepost_cash_on_delivery.state,
                            )
                            if package.options.deutschepost_cash_on_delivery.state
                            is not None
                            else None
                        ),
                        individualSenderRequirement=package.options.deutschepost_individual_sender_requirement.state,
                        premium=package.options.deutschepost_premium.state,
                        closestDropPoint=package.options.deutschepost_closest_drop_point.state,
                        parcelOutletRouting=package.options.deutschepost_parcel_outlet_routing.state,
                        dhlRetoure=None,
                        postalDeliveryDutyPaid=package.options.deutschepost_postal_delivery_duty_paid.state,
                    )
                    if any(package.options.items())
                    else None
                ),
                customs=(
                    deutschepost.CustomsType(
                        invoiceNo=customs.invoice,
                        exportType=provider_units.CustomsContentType.map(
                            customs.content_type
                        ).value,
                        exportDescription=customs.content_description,
                        shippingConditions=(
                            provider_units.Incoterm.map(customs.incoterm).value or "DDP"
                        ),
                        permitNo=customs.options.permit_number.state,
                        attestationNo=customs.options.attestation_number.state,
                        hasElectronicExportNotification=customs.options.electronic_export_notification.state,
                        MRN=customs.options.mrn.state,
                        postalCharges=(
                            deutschepost.PostalChargesType(
                                currency=(
                                    package.options.currency.state
                                    or customs.duty.currency
                                ),
                                value=(
                                    customs.duty.declared_value
                                    or package.options.declared_value.state
                                ),
                            )
                            if any(
                                [
                                    customs.duty.declared_value,
                                    package.options.declared_value.state,
                                ]
                            )
                            else None
                        ),
                        officeOfOrigin=shipper.country_code,
                        shipperCustomsRef=customs.options.shipper_customs_ref.state,
                        consigneeCustomsRef=customs.options.consignee_customs_ref.state,
                        items=[
                            deutschepost.ItemType(
                                itemDescription=item.description,
                                countryOfOrigin=item.origin_country,
                                hsCode=item.hs_code,
                                packagedQuantity=item.quantity,
                                itemValue=(
                                    deutschepost.PostalChargesType(
                                        currency=(
                                            item.value_currency
                                            or package.options.currency.state
                                            or customs.duty.currency
                                        ),
                                        value=item.value_amount,
                                    )
                                    if item.value_amount is not None
                                    else None
                                ),
                                itemWeight=deutschepost.WeightType(
                                    uom=units.WeightUnit.KG.name.lower(),
                                    value=item.weight,
                                ),
                            )
                            for item in customs.commodities
                        ],
                    )
                    if payload.customs is not None
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
            validate="true",
            docFormat=doc_format,
            printFormat=print_format,
            combine="true",
        ),
    )
