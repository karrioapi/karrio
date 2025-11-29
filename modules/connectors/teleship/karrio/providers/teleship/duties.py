"""Karrio Teleship duties calculation implementation."""

import typing
import karrio.schemas.teleship.duties_taxes_request as teleship
import karrio.schemas.teleship.duties_taxes_response as duties
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.teleship.error as error
import karrio.providers.teleship.utils as provider_utils


def parse_duties_calculation_response(
    _response: lib.Deserializable[str],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.DutiesCalculationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    details = lib.to_object(duties.DutiesTaxesResponseType, response)

    duties_details = lib.identity(
        models.DutiesCalculationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            total_charge=lib.to_money(details.price),
            currency=details.currency,
            charges=[
                models.ChargeDetails(
                    name=charge.name,
                    amount=lib.to_money(charge.amount),
                    currency=charge.currency,
                )
                for charge in (details.charges or [])
            ],
            meta=lib.to_dict(details),
        )
        if details and details.price
        else None
    )

    return duties_details, messages


def duties_calculation_request(
    payload: models.DutiesCalculationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    customs = lib.to_customs_info(payload.customs)
    commodities = lib.to_commodities(customs.commodities or [])

    request = teleship.DutiesTaxesRequestType(
        shipTo=teleship.ShipType(
            name=recipient.person_name,
            email=recipient.email,
            phone=recipient.phone_number,
            company=recipient.company_name,
            address=teleship.AddressType(
                line1=recipient.address_line1,
                line2=recipient.address_line2,
                city=recipient.city,
                state=recipient.state_code,
                postcode=recipient.postal_code,
                country=recipient.country_code,
            ),
        ),
        shipFrom=teleship.ShipType(
            name=shipper.person_name,
            email=shipper.email,
            phone=shipper.phone_number,
            company=shipper.company_name,
            address=teleship.AddressType(
                line1=shipper.address_line1,
                line2=shipper.address_line2,
                city=shipper.city,
                state=shipper.state_code,
                postcode=shipper.postal_code,
                country=shipper.country_code,
            ),
        ),
        commodities=[
            teleship.CommodityType(
                quantity=commodity.quantity,
                title=commodity.title or commodities.description,
                description=lib.identity(
                    commodity.description if commodity.title else None
                ),
                hsCode=commodity.hs_code,
                sku=commodity.sku,
                value=teleship.ConsigneeChargesType(
                    amount=commodity.value_amount,
                    currency=commodity.value_currency,
                ),
                unitWeight=teleship.UnitWeightType(
                    unit=commodity.weight_unit or "kg",
                    value=commodity.weight,
                ),
                countryOfOrigin=commodity.origin_country,
                category=commodity.category,
            )
            for commodity in commodities
        ],
        customs=teleship.CustomsType(
            contentType=customs.content_type or "CommercialGoods",
            incoterms=lib.failsafe(lambda: customs.options.incoterms.state),
            invoiceNumber=customs.invoice,
            invoiceDate=customs.invoice_date,
            EORI=lib.failsafe(lambda: customs.options.eori_number.state),
            VAT=lib.failsafe(lambda: customs.options.vat.state),
        ),
        currency=payload.options.get("currency") if payload.options else None,
        orderTrackingReference=payload.reference,
    )

    return lib.Serializable(request, lib.to_dict)
