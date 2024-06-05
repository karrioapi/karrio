import karrio.schemas.easypost.shipment_request as easypost
from karrio.schemas.easypost.shipments_response import Shipment

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.easypost.error as provider_error
import karrio.providers.easypost.units as provider_units
import karrio.providers.easypost.utils as provider_utils


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.RateDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    errors = provider_error.parse_error_response(response, settings)
    rates = _extract_details(response, settings) if "error" not in response else []

    return rates, errors


def _extract_details(
    response: dict,
    settings: provider_utils.Settings,
) -> typing.List[models.RateDetails]:
    rates = lib.to_object(Shipment, response).rates

    return [
        (
            lambda rate_provider, service, service_name: models.RateDetails(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                service=service,
                currency=rate.currency,
                total_charge=lib.to_decimal(rate.rate),
                transit_days=rate.delivery_days,
                meta=dict(
                    service_name=service_name,
                    rate_provider=rate_provider,
                ),
            )
        )(*provider_units.Service.info(rate.service, rate.carrier))
        for rate in rates
    ]


def rate_request(payload: models.RateRequest, _) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    return_address = lib.to_address(payload.return_address)
    billing_address = lib.to_address(payload.billing_address)
    package = lib.to_packages(
        payload.parcels,
        package_option_type=provider_units.ShippingOption,
    ).single
    options = lib.to_shipping_options(
        payload,
        package_options=package.options,
        initializer=provider_units.shipping_options_initializer,
    )
    is_intl = shipper.country_code != recipient.country_code
    customs = (
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
                    )
                ]
            )
        )
        if is_intl
        else None
    )

    requests = easypost.ShipmentRequest(
        shipment=easypost.Shipment(
            reference=payload.reference,
            to_address=easypost.Address(
                company=recipient.company_name,
                street1=recipient.street,
                street2=recipient.address_line2,
                city=recipient.city,
                state=recipient.state_code,
                zip=recipient.postal_code,
                country=recipient.country_code,
                residential=recipient.residential,
                name=recipient.person_name,
                phone=recipient.phone_number,
                email=recipient.email,
                federal_tax_id=recipient.federal_tax_id,
                state_tax_id=recipient.state_tax_id,
            ),
            from_address=easypost.Address(
                company=shipper.company_name,
                street1=shipper.street,
                street2=shipper.address_line2,
                city=shipper.city,
                state=shipper.state_code,
                zip=shipper.postal_code,
                country=shipper.country_code,
                residential=shipper.residential,
                name=shipper.person_name,
                phone=shipper.phone_number,
                email=shipper.email,
                federal_tax_id=shipper.federal_tax_id,
                state_tax_id=shipper.state_tax_id,
            ),
            return_address=lib.identity(
                easypost.Address(
                    company=return_address.company_name,
                    street1=return_address.street,
                    street2=return_address.address_line2,
                    city=return_address.city,
                    state=return_address.state_code,
                    zip=return_address.postal_code,
                    country=return_address.country_code,
                    residential=return_address.residential,
                    name=return_address.person_name,
                    phone=return_address.phone_number,
                    email=return_address.email,
                    federal_tax_id=return_address.federal_tax_id,
                    state_tax_id=return_address.state_tax_id,
                )
                if payload.return_address
                else None
            ),
            buyer_address=lib.identity(
                easypost.Address(
                    company=billing_address.company_name,
                    street1=billing_address.street,
                    street2=billing_address.address_line2,
                    city=billing_address.city,
                    state=billing_address.state_code,
                    zip=billing_address.postal_code,
                    country=billing_address.country_code,
                    residential=billing_address.residential,
                    name=billing_address.person_name,
                    phone=billing_address.phone_number,
                    email=billing_address.email,
                    federal_tax_id=billing_address.federal_tax_id,
                    state_tax_id=billing_address.state_tax_id,
                )
                if payload.billing_address
                else None
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
                    contents_type="other",
                    customs_certify=True,
                    customs_signer=shipper.person_name,
                    customs_items=[
                        easypost.CustomsItem(
                            description=lib.text(
                                item.description or item.title or "N/A"
                            ),
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
                if customs
                else None
            ),
        )
    )

    return lib.Serializable(requests, lib.to_dict)
