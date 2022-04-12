from typing import List, Tuple

import easypost_lib.shipment_request as easypost
from easypost_lib.shipments_response import Shipment
from karrio.core.utils.transformer import to_multi_piece_shipment
from karrio.core.utils import Serializable, DP
from karrio.core.models import (
    Documents,
    ShipmentRequest,
    ShipmentDetails,
    Message,
)
from karrio.core.units import Packages, Options, Weight
from karrio.providers.easypost.units import (
    Service,
    PackagingType,
    Option,
)
from karrio.providers.easypost.utils import Settings, download_label
from karrio.providers.easypost.error import parse_error_response


def parse_shipment_response(
    responses: List[Tuple[int, dict]], settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    errors = [
        parse_error_response(response, settings)
        for _, response in responses
        if "error" in response
    ]
    shipment = to_multi_piece_shipment(
        [
            (index, _extract_details(response, settings))
            for index, response in responses
            if "error" not in response
        ]
    )

    return shipment, errors


def _extract_details(response: dict, settings: Settings) -> ShipmentDetails:
    shipment = DP.to_object(Shipment, response)
    label_type = shipment.postage_label.label_file_type.split("/")[-1]
    label_url = getattr(
        shipment.postage_label,
        f"label_{label_type}_url",
        shipment.postage_label.label_url,
    )
    label = download_label(label_url, shipment.postage_label.label_type, settings)

    return ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        shipment_identifier=shipment.id,
        tracking_number=shipment.tracking_code,
        label_type=label_type.upper(),
        docs=Documents(label=label),
        meta=dict(
            rate_provider=shipment.selected_rate.carrier,
            service_name=shipment.selected_rate.service,
            label_url=shipment.postage_label.label_url,
        ),
    )


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable:
    packages = Packages(payload.packages)
    options = Options(payload.options, Option)
    constoms_options = getattr(payload.customs, "options", {})

    requests = [
        easypost.ShipmentRequest(
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
                length=package.length,
                width=package.width,
                height=package.height,
                weight=package.weight,
                predefined_package=PackagingType.map(package.packaging_type).value,
            ),
            options={
                getattr(option, "key", option): getattr(option, "value", None)
                for code, option in options
                if code in Option
            },
            customs_info=(
                easypost.CustomsInfo(
                    contents_explanation=payload.customs.content_description,
                    contents_type=payload.customs.content_type,
                    customs_certify=payload.customs.certify,
                    customs_signer=payload.customs.signer,
                    eel_pfc=constoms_options.get("eel_pfc"),
                    non_delivery_option=constoms_options.get("non_delivery_option"),
                    restriction_type=constoms_options.get("restriction_type"),
                    declaration=constoms_options.get("declaration"),
                    customs_items=[
                        easypost.CustomsItem(
                            description=item.description,
                            origin_country=item.origin_country,
                            quantity=item.quantity,
                            value=item.value_amount,
                            weight=Weight(item.weight, item.weight_unit).OZ,
                            code=item.sku,
                            manufacturer=None,
                            currency=item.value_currency,
                            eccn=(item.metadata or {}).get("eccn"),
                            printed_commodity_identifier=(item.sku or item.id),
                            hs_tariff_number=(item.metadata or {}).get(
                                "hs_tariff_number"
                            ),
                        )
                        for item in payload.customs.commodities
                    ],
                )
                if payload.customs is not None
                else None
            ),
        )
        for package in packages
    ]

    return Serializable(requests, DP.to_dict)
