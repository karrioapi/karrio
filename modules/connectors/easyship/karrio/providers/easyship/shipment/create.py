"""Karrio Easyship shipment API implementation."""

import karrio.schemas.easyship.shipment_request as easyship
import karrio.schemas.easyship.shipment_response as shipping

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.easyship.error as error
import karrio.providers.easyship.utils as provider_utils
import karrio.providers.easyship.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    shipment = lib.identity(
        _extract_details(response, settings, ctx=_response.ctx)
        if response.get("shipment")
        and any(response["shipment"].get("shipping_documents") or [])
        else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict,
) -> models.ShipmentDetails:
    details = lib.to_object(shipping.ShipmentType, data["shipment"])
    label_document = next(
        (_ for _ in details.shipping_documents if _.category == "label"), None
    )
    label_type = (label_document.format or ctx.get("label_type") or "PDF").upper()
    label = lib.bundle_base64(label_document.base64_encoded_strings, label_type)
    tracking_numbers = [tracking.tracking_number for tracking in details.trackings]
    tracking_number, *__ = tracking_numbers

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=details.easyship_shipment_id,
        label_type=label_type,
        docs=models.Documents(label=label),
        meta=dict(
            shipment_ids=[details.easyship_shipment_id],
            tracking_numbers=tracking_numbers,
            carrier=ctx["rate_provider"],
            rate_provider=ctx["rate_provider"],
            easyship_courier_id=ctx["courier_id"],
            easyship_shipment_id=details.easyship_shipment_id,
            easyship_courier_account_id=details.courier.id,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    return_address = lib.to_address(payload.return_address or payload.shipper)
    packages = lib.to_packages(payload.parcels, options=payload.options)
    weight_unit, dimension_unit = packages.compatible_units
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    service = lib.identity(
        options.easyship_courier_id.state
        or provider_units.ShippingServiceID.map(payload.service).name_or_key
    )
    courier = provider_units.ShippingCourierID.find(service)
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=weight_unit.name,
    )
    incoterms = lib.identity(
        options.easyship_incoterms.state or customs.options.incoterm.state or "DDU"
    )
    label_type = provider_units.LabelFormat.map(payload.label_type)

    # map data to convert karrio model to easyship specific type
    request = easyship.ShipmentRequestType(
        buyer_regulatory_identifiers=lib.identity(
            easyship.BuyerRegulatoryIdentifiersType(
                ein=customs.duty_billing_address.tax_id,
                vat_number=customs.options.vat_registration_number.state,
            )
            if any(
                [
                    customs.options.vat_registration_number.state,
                    customs.duty_billing_address.tax_id,
                ]
            )
            else None
        ),
        courier_selection=easyship.CourierSelectionType(
            allow_courier_fallback=lib.identity(
                options.easyship_allow_courier_fallback.state
                if options.easyship_allow_courier_fallback.state is not None
                else settings.connection_config.allow_courier_fallback.state
            ),
            apply_shipping_rules=lib.identity(
                options.easyship_apply_shipping_rules.state
                if options.easyship_apply_shipping_rules.state is not None
                else settings.connection_config.apply_shipping_rules.state
            ),
            list_unavailable_couriers=lib.identity(
                options.easyship_list_unavailable_couriers.state
                if options.easyship_list_unavailable_couriers.state is not None
                else False
            ),
            selected_courier_id=service,
        ),
        destination_address=easyship.AddressType(
            city=recipient.city,
            company_name=lib.text(recipient.company_name or "N/A", max=22),
            contact_email=lib.identity(
                recipient.email
                or options.email_notification_to.state
                or "user@mail.com"
            ),
            contact_name=lib.text(recipient.person_name, max=22),
            contact_phone=recipient.phone_number or "N/A",
            country_alpha2=recipient.country_code,
            line_1=recipient.address_line1,
            line_2=recipient.address_line2,
            postal_code=recipient.postal_code,
            state=recipient.state_code,
        ),
        consignee_tax_id=recipient.tax_id,
        eei_reference=options.easyship_eei_reference.state,
        incoterms=incoterms,
        metadata=payload.metadata,
        insurance=easyship.InsuranceType(
            is_insured=options.insurance.state is not None
        ),
        order_data=None,
        origin_address=easyship.AddressType(
            city=return_address.city,
            company_name=lib.text(return_address.company_name or "N/A", max=22),
            contact_email=lib.identity(
                return_address.email
                or options.email_notification_to.state
                or "user@mail.com"
            ),
            contact_name=lib.text(return_address.person_name, max=22),
            contact_phone=return_address.phone_number or "N/A",
            country_alpha2=return_address.country_code,
            line_1=return_address.address_line1,
            line_2=return_address.address_line2,
            postal_code=return_address.postal_code,
            state=return_address.state_code,
        ),
        regulatory_identifiers=lib.identity(
            easyship.RegulatoryIdentifiersType(
                eori=customs.options.eori.state,
                ioss=customs.options.ioss.state,
                vat_number=customs.options.vat_registration_number.state,
            )
            if any(
                [
                    customs.options.eori.state,
                    customs.options.vat_registration_number.state,
                    customs.duty_billing_address.tax_id,
                ]
            )
            else None
        ),
        shipment_request_return=options.is_return.state,
        return_address=easyship.AddressType(
            city=return_address.city,
            company_name=lib.text(return_address.company_name or "N/A", max=22),
            contact_email=lib.identity(
                return_address.email
                or options.email_notification_to.state
                or "user@mail.com"
            ),
            contact_name=lib.text(return_address.person_name, max=22),
            contact_phone=return_address.phone_number or "N/A",
            country_alpha2=return_address.country_code,
            line_1=return_address.address_line1,
            line_2=return_address.address_line2,
            postal_code=return_address.postal_code,
            state=return_address.state_code,
        ),
        return_address_id=options.easyship_return_address_id.state,
        sender_address=easyship.AddressType(
            city=shipper.city,
            company_name=lib.text(shipper.company_name or "N/A", max=22),
            contact_email=lib.identity(
                shipper.email or options.email_notification_to.state or "user@mail.com"
            ),
            contact_name=lib.text(shipper.person_name, max=22),
            contact_phone=shipper.phone_number or "N/A",
            country_alpha2=shipper.country_code,
            line_1=shipper.address_line1,
            line_2=shipper.address_line2,
            postal_code=shipper.postal_code,
            state=shipper.state_code,
        ),
        sender_address_id=options.easyship_sender_address_id.state,
        set_as_residential=recipient.residential,
        shipping_settings=easyship.ShippingSettingsType(
            additional_services=lib.identity(
                easyship.AdditionalServicesType(
                    delivery_confirmation=None,
                    qr_code=None,
                )
                if any(
                    [
                        options.easyship_delivery_confirmation.state,
                        options.easyship_qr_code.state,
                    ]
                )
                else None
            ),
            b13_a_filing=None,
            buy_label=True,
            buy_label_synchronous=True,
            printing_options=easyship.PrintingOptionsType(
                commercial_invoice="A4",
                format=label_type.value or "pdf",
                label="4x6",
                packing_slip=None,
                remarks=payload.reference,
            ),
            units=easyship.UnitsType(
                dimensions=provider_units.DimensionUnit.map(dimension_unit.name).value,
                weight=provider_units.WeightUnit.map(weight_unit.name).value,
            ),
        ),
        parcels=[
            easyship.ParcelType(
                box=easyship.BoxType(
                    height=package.height.value,
                    length=package.length.value,
                    width=package.width.value,
                    slug=package.parcel.options.get("easyship_box_slug"),
                ),
                items=[
                    easyship.ItemType(
                        dimensions=None,
                        declared_currency=lib.identity(
                            item.value_currency or options.currency.state or "USD"
                        ),
                        origin_country_alpha2=lib.identity(
                            item.origin_country or shipper.country_code
                        ),
                        quantity=item.quantity,
                        actual_weight=item.weight,
                        category=item.category or "bags_luggages",
                        declared_customs_value=item.value_amount,
                        description=item.description or item.title or "Item",
                        sku=item.sku or "N/A",
                        hs_code=item.hs_code or "N/A",
                        contains_liquids=item.metadata.get("contains_liquids"),
                        contains_battery_pi966=item.metadata.get(
                            "contains_battery_pi966"
                        ),
                        contains_battery_pi967=item.metadata.get(
                            "contains_battery_pi967"
                        ),
                    )
                    for item in lib.identity(
                        (package.items if any(package.items) else customs.commodities)
                        if any(package.items) or any(payload.customs or "")
                        else [
                            models.Commodity(
                                title=lib.text(package.description, max=35),
                                quantity=1,
                                value_amount=1.0,
                            )
                        ]
                    )
                ],
                total_actual_weight=package.weight.value,
            )
            for package in packages
        ],
    )

    return lib.Serializable(
        request,
        lambda _: lib.to_dict(
            lib.to_json(_).replace("shipment_request_return", "return")
        ),
        ctx=dict(
            courier_id=service,
            rate_provider=courier.name,
            label_type=label_type.name or "PDF",
        ),
    )
