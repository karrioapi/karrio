"""Karrio SEKO Logistics rating API implementation."""

import karrio.schemas.seko.rating_request as seko
import karrio.schemas.seko.rating_response as rating

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.seko.error as error
import karrio.providers.seko.utils as provider_utils
import karrio.providers.seko.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    rates = [_extract_details(rate, settings) for rate in response.get("Available", [])]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    details = lib.to_object(rating.AvailableType, data)
    service = provider_units.ShippingService.map(details.DeliveryType)

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        total_charge=lib.to_money(details.Cost),
        currency=settings.connection_config.currency.state or "USD",
        meta=dict(
            service_name=service.value_or_key,
            seko_carrier=details.CarrierName,
            Route=details.Route,
            QuoteId=details.QuoteId,
            DeliveryType=details.DeliveryType,
            CarrierServiceType=details.CarrierServiceType,
            IsFreightForward=details.IsFreightForward,
            IsRuralDelivery=details.IsRuralDelivery,
            IsSaturdayDelivery=details.IsSaturdayDelivery,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    options = lib.to_shipping_options(
        payload.options,
        initializer=provider_units.shipping_options_initializer,
    )
    packages = lib.to_packages(
        payload.parcels,
        options=options,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit="KG",
    )
    commodities = lib.identity(customs.commodities if any(customs.commodities) else packages.items)

    # map data to convert karrio model to seko specific type
    request = seko.RatingRequestType(
        DeliveryReference=payload.reference,
        Reference2=options.seko_reference_2.state,
        Reference3=options.seko_reference_3.state,
        Origin=seko.DestinationType(
            Id=options.seko_origin_id.state,
            Name=payload.shipper.company_name,
            Address=seko.AddressType(
                BuildingName=shipper.company_name,
                StreetAddress=shipper.street,
                Suburb=shipper.city,
                City=shipper.state_code,
                PostCode=shipper.postal_code,
                CountryCode=shipper.country_code,
            ),
            ContactPerson=shipper.contact,
            PhoneNumber=shipper.phone_number,
            Email=shipper.email,
            DeliveryInstructions=options.origin_instructions.state,
            RecipientTaxId=shipper.tax_id,
            SendTrackingEmail=None,
        ),
        Destination=seko.DestinationType(
            Id=options.seko_destination_id.state,
            Name=recipient.company_name,
            Address=seko.AddressType(
                BuildingName="",
                StreetAddress=recipient.street,
                Suburb=recipient.city,
                City=recipient.state_code,
                PostCode=recipient.postal_code,
                CountryCode=recipient.country_code,
            ),
            ContactPerson=recipient.contact,
            PhoneNumber=recipient.phone_number,
            Email=recipient.email,
            DeliveryInstructions=options.destination_instructions.state,
            RecipientTaxId=recipient.tax_id,
            SendTrackingEmail=None,
        ),
        IsSaturdayDelivery=options.seko_is_saturday_delivery.state,
        IsSignatureRequired=options.seko_is_signature_required.state,
        DangerousGoods=None,
        Commodities=[
            seko.CommodityType(
                Description=commodity.description,
                HarmonizedCode=commodity.sku,
                Units=commodity.quantity,
                UnitValue=commodity.value_amount,
                UnitCostValue=commodity.value_amount,
                UnitKg=commodity.weight,
                Currency=commodity.value_currency,
                Country=commodity.country_code,
                IsDG=None,
                itemSKU=commodity.sku,
                ImageURL=commodity.metadata.get("image_url"),
                DangerousGoodsItem=None,
                Manufacturer=None,
            )
            for commodity in commodities
        ],
        Packages=[
            seko.PackageType(
                Height=package.height.CM,
                Length=package.length.CM,
                Id=package.options.seko_package_id.state,
                Width=package.width.CM,
                Kg=package.weight.KG,
                Name=lib.text(package.description, max=50),
                PackageCode=None,
                Type=provider_units.PackagingType.map(
                    package.packaging_type or "your_packaging"
                ).value,
            )
            for package in packages
        ],
        ShipType=options.seko_ship_type.state,
        CostCentreName=settings.connection_config.cost_centre_name.state,
        CostCentreId=settings.connection_config.cost_centre_id.state,
        CodValue=options.cash_on_delivery.state,
        TaxCollected=options.seko_tax_collected.state,
        AmountCollected=options.seko_amount_collected.state,
        CIFValue=options.seko_cif_value.state,
        FreightValue=options.seko_freight_value.state,
        DutiesAndTaxesByReceiver=lib.identity(
            customs.duty.paid_by == "recipient" if payload.customs else None
        ),
        TaxIds=[
            seko.TaxIDType(
                IdType=option.code,
                IdNumber=option.state,
            )
            for key, option in customs.options.items()
            if key in provider_units.CustomsOption and option.state is not None
        ],
    )

    return lib.Serializable(request, lib.to_dict)
