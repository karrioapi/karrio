import easypost_lib.shipment_request as easypost
from easypost_lib.shipments_response import Shipment

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.easypost.error as provider_error
import karrio.providers.easypost.units as provider_units
import karrio.providers.easypost.utils as provider_utils


def parse_shipment_response(
    response: dict, settings: provider_utils.Settings
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    errors = (
        [provider_error.parse_error_response(response, settings)]
        if "error" in response
        else []
    )
    shipment = _extract_details(response, settings) if "error" not in response else None

    return shipment, errors


def _extract_details(
    response: dict, settings: provider_utils.Settings
) -> models.ShipmentDetails:
    shipment = lib.to_object(Shipment, response)
    label_type = shipment.postage_label.label_file_type.split("/")[-1]
    label = provider_utils.download_label(shipment.postage_label.label_url)

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        shipment_identifier=shipment.id,
        tracking_number=shipment.tracking_code,
        label_type=label_type.upper(),
        docs=models.Documents(label=label),
        meta=dict(
            rate_provider=shipment.selected_rate.carrier,
            service_name=shipment.selected_rate.service,
            label_url=shipment.postage_label.label_url,
        ),
    )


def shipment_request(payload: models.ShipmentRequest, _) -> lib.Serializable:
    service = provider_units.Service.map(payload.service).value_or_key
    package = lib.to_packages(
        payload.parcels,
        package_option_type=provider_units.ShippingOption,
    ).single

    payment = payload.payment or models.Payment()
    payor = payload.billing_address or (
        payload.shipper if payment.paid_by == "sender" else payload.recipient
    )
    options = lib.to_shipping_options(
        payload,
        payor=payor,
        package_options=package.options,
        initializer=provider_units.shipping_options_initializer,
    )
    is_intl = payload.shipper.country_code != payload.recipient.country_code
    customs = lib.to_customs_info(
        payload.customs,
        weight_unit=package.weight_unit,
        default_to=(
            models.Customs(
                commodities=(
                    package.parcel.items
                    if any(package.parcel.items)
                    else [
                        models.Commodity(
                            sku="0000",
                            quantity=1,
                            weight=package.weight.value,
                            weight_unit=package.weight_unit.value,
                            description=package.parcel.content,
                        )
                    ]
                )
            )
            if is_intl
            else None
        ),
    )

    requests = dict(
        service=service,
        insurance=options.insurance.state,
        data=easypost.ShipmentRequest(
            shipment=easypost.Shipment(
                reference=payload.reference,
                to_address=easypost.Address(
                    company=payload.recipient.company_name,
                    street1=payload.recipient.address_line1,
                    street2=payload.recipient.address_line2,
                    city=payload.recipient.city,
                    state=payload.recipient.state_code,
                    zip=payload.recipient.postal_code,
                    country=payload.recipient.country_code,
                    residential=payload.recipient.residential,
                    name=payload.recipient.person_name,
                    phone=payload.recipient.phone_number,
                    email=payload.recipient.email,
                    federal_tax_id=payload.recipient.federal_tax_id,
                    state_tax_id=payload.recipient.state_tax_id,
                ),
                from_address=easypost.Address(
                    company=payload.shipper.company_name,
                    street1=payload.shipper.address_line1,
                    street2=payload.shipper.address_line2,
                    city=payload.shipper.city,
                    state=payload.shipper.state_code,
                    zip=payload.shipper.postal_code,
                    country=payload.shipper.country_code,
                    residential=payload.shipper.residential,
                    name=payload.shipper.person_name,
                    phone=payload.shipper.phone_number,
                    email=payload.shipper.email,
                    federal_tax_id=payload.shipper.federal_tax_id,
                    state_tax_id=payload.shipper.state_tax_id,
                ),
                parcel=easypost.Parcel(
                    length=package.length.IN,
                    width=package.width.IN,
                    height=package.height.IN,
                    weight=package.weight.OZ,
                    predefined_package=provider_units.PackagingType.map(
                        package.packaging_type
                    ).value,
                ),
                options={option.code: option.state for _, option in options.items()},
                customs_info=(
                    easypost.CustomsInfo(
                        contents_explanation=customs.content_description,
                        contents_type=customs.content_type,
                        customs_certify=customs.certify,
                        customs_signer=(customs.signer or payload.shipper.person_name),
                        eel_pfc=customs.options.eel_pfc.state,
                        non_delivery_option=customs.options.non_delivery_option.state,
                        restriction_type=customs.options.restriction_type.state,
                        declaration=customs.options.declaration.state,
                        customs_items=[
                            easypost.CustomsItem(
                                description=item.description,
                                origin_country=item.origin_country,
                                quantity=item.quantity,
                                value=item.value_amount,
                                weight=units.Weight(item.weight, item.weight_unit).OZ,
                                code=item.sku,
                                manufacturer=None,
                                currency=item.value_currency,
                                eccn=(item.metadata or {}).get("eccn"),
                                printed_commodity_identifier=(item.sku or item.id),
                                hs_tariff_number=item.hs_code,
                            )
                            for item in customs.commodities
                        ],
                    )
                    if payload.customs
                    else None
                ),
            )
        ),
    )

    return lib.Serializable(requests, lib.to_dict)
