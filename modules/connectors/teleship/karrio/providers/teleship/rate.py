"""Karrio Teleship rate API implementation."""

import karrio.schemas.teleship.rate_request as teleship_req
import karrio.schemas.teleship.rate_response as teleship_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.teleship.error as error
import karrio.providers.teleship.utils as provider_utils
import karrio.providers.teleship.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Extract rates array as raw dicts (don't convert to typed object first)
    rates = [
        _extract_details(rate, settings)
        for rate in (response.get("rates") or [])
    ]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    """Extract rate details from carrier response data"""
    # Convert to typed object for safe attribute access
    rate = lib.to_object(teleship_res.RateType, data)

    # Access service from raw dict to avoid nested typed object issues
    service_data = data.get("service") or {}
    service = lib.to_object(teleship_res.ServiceType, service_data)

    # Extract charges using functional pattern (access from raw dict)
    charges = [
        lib.to_object(teleship_res.ChargeType, charge)
        for charge in (data.get("charges") or [])
    ]

    # Calculate extra charges
    extra_charges = [
        models.ChargeDetails(
            name=charge.name or "",
            amount=lib.to_money(charge.amount),
            currency=charge.currency or rate.currency or "USD",
        )
        for charge in charges
    ] if any(charges) else []

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.code or "",
        total_charge=lib.to_money(rate.price),
        currency=rate.currency or "USD",
        transit_days=rate.transit if rate.transit else None,
        extra_charges=extra_charges,
        meta=dict(
            service_name=service.name or "",
            estimated_delivery=rate.estimatedDelivery,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a rate request for the carrier API"""
    # Convert karrio models using functional lib utilities
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
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
    request = teleship_req.RateRequestType(
        customerReference=payload.reference or options.teleship_customer_reference.state,
        packageType=lib.identity(
            provider_units.PackagingType.map(
                package.packaging_type or "your_packaging"
            ).value if package else "parcel"
        ),
        shipTo=teleship_req.ShipToType(
            name=recipient.person_name or recipient.company_name,
            email=recipient.email,
            phone=recipient.phone_number,
            address=teleship_req.AddressType(
                line1=recipient.address_line1,
                city=recipient.city,
                state=recipient.state_code,
                postcode=recipient.postal_code,
                country=recipient.country_code,
            ),
        ),
        shipFrom=teleship_req.ShipFromType(
            name=shipper.person_name or shipper.company_name,
            company=shipper.company_name,
            address=teleship_req.AddressType(
                line1=shipper.address_line1,
                city=shipper.city,
                state=shipper.state_code,
                postcode=shipper.postal_code,
                country=shipper.country_code,
            ),
        ),
        weight=lib.identity(
            teleship_req.WeightType(
                value=package.weight.value,
                unit=package.weight.unit.lower(),
            ) if package else None
        ),
        dimensions=lib.identity(
            teleship_req.DimensionsType(
                unit=(package.dimension_unit or "CM").lower(),
                length=int(package.length.value) if package.length else None,
                width=int(package.width.value) if package.width else None,
                height=int(package.height.value) if package.height else None,
            ) if package and all([package.length, package.width, package.height]) else None
        ),
        commodities=[
            teleship_req.CommodityType(
                sku=commodity.sku,
                title=commodity.title or commodity.description,
                value=teleship_req.ValueType(
                    amount=int(commodity.value_amount or 0),
                    currency=commodity.value_currency or "USD",
                ),
                quantity=commodity.quantity or 1,
                unitWeight=teleship_req.WeightType(
                    value=commodity.weight,
                    unit=(commodity.weight_unit or "KG").lower(),
                ),
                description=commodity.description,
                countryOfOrigin=commodity.origin_country,
            )
            for commodity in (customs.commodities or [])
        ] if payload.customs and any(customs.commodities or []) else [],
        customs=lib.identity(
            teleship_req.CustomsType(
                EORI=lib.failsafe(lambda: customs.options.eori_number.state),
                contentType=customs.content_type,
                invoiceDate=customs.invoice_date,
                invoiceNumber=customs.invoice,
            ) if payload.customs else None
        ),
        metadata=lib.identity(
            teleship_req.MetadataType(
                fulfillmentOrderId=options.teleship_order_tracking_reference.state,
            ) if options.teleship_order_tracking_reference.state else None
        ),
    )

    return lib.Serializable(request, lib.to_dict)
