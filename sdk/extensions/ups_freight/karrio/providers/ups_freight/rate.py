from ups_freight_lib.freight_rate_response import FreightRateResponseClassType
import ups_freight_lib.freight_rate_request as ups
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.ups_freight.error as error
import karrio.providers.ups_freight.utils as provider_utils
import karrio.providers.ups_freight.units as provider_units


def parse_rate_response(
    response: dict,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    rate_response = response.get("FreightRateResponse") or {}
    response_messages = [
        *response.get("response", {}).get("errors", []),
        *rate_response.get("Response", {}).get("Alert", []),
    ]
    messages = error.parse_error_response(response_messages, settings)
    rates = [
        _extract_details(rate, settings)
        for rate in [rate_response]
        if rate_response.get("TotalShipmentCharge") is not None
    ]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    detail = lib.to_object(FreightRateResponseClassType, data)
    service = provider_units.ShippingService.map(detail.Service.Code)

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        currency=detail.TotalShipmentCharge.CurrencyCode,
        total_charge=lib.to_money(detail.TotalShipmentCharge.MonetaryValue),
        transit_days=lib.to_int(detail.TimeInTransit.DaysInTransit),
        meta=dict(service_name=(service.name or detail.Service.Code)),
        extra_charges=[
            models.ChargeDetails(
                name=provider_units.RateType.map(charge.Type.Code).name_or_key,
                amount=lib.to_money(charge.Factor.Value),
                currency=charge.Factor.UnitOfMeasurement.Code,
            )
            for charge in detail.Rate
        ],
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels, options=payload.options)
    services = lib.to_services(
        payload.services,
        provider_units.ShippingService,
    )
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    request = ups.FreightRateRequestType(
        FreightRateRequest=ups.FreightRateRequestClassType(
            ShipFrom=ups.ShipFromType(
                Name=shipper.company_name,
                Address=ups.AddressType(
                    AddressLine=shipper.address_line,
                    City=shipper.city,
                    StateProvinceCode=shipper.state_code,
                    Town=None,
                    PostalCode=shipper.postal_code,
                    CountryCode=shipper.country_code,
                    ResidentialAddressIndicator=(
                        "true" if shipper.residential else None
                    ),
                ),
            ),
            ShipTo=ups.ShipToType(
                Name=recipient.company_name,
                Address=ups.AddressType(
                    AddressLine=recipient.address_line,
                    City=recipient.city,
                    StateProvinceCode=recipient.state_code,
                    Town=None,
                    PostalCode=recipient.postal_code,
                    CountryCode=recipient.country_code,
                    ResidentialAddressIndicator=(
                        "true" if recipient.residential else None
                    ),
                ),
                AttentionName=recipient.person_name,
            ),
            PaymentInformation=ups.PaymentInformationType(
                Payer=ups.ShipToType(
                    Name=shipper.company_name,
                    Address=ups.AddressType(
                        AddressLine=shipper.address_line,
                        City=shipper.city,
                        StateProvinceCode=shipper.state_code,
                        PostalCode=shipper.postal_code,
                        CountryCode=shipper.country_code,
                        ResidentialAddressIndicator=(
                            "true" if shipper.residential else None
                        ),
                    ),
                    ShipperNumber=settings.account_number,
                    AttentionName=shipper.person_name,
                ),
                ShipmentBillingOption=ups.AccountTypeType(Code="10"),
            ),
            Service=ups.AccountTypeType(
                Code=(
                    services.first
                    or provider_units.ShippingService.ups_tforce_freight_ltl
                ).value
            ),
            Commodity=[
                ups.CommodityType(
                    Weight=ups.EightType(
                        UnitOfMeasurement=ups.AccountTypeType(
                            Code=(
                                provider_units.WeightUnit.map(package.weight_unit).value
                                or "LBS"
                            ),
                        ),
                        Value=package.weight.value,
                    ),
                    Dimensions=(
                        ups.CommodityDimensionsType(
                            UnitOfMeasurement=ups.AccountTypeType(
                                Code=(
                                    units.DimensionUnit.map(
                                        package.dimension_unit.value
                                    ).value
                                    or "IN"
                                ),
                            ),
                            Length=package.length.value,
                            Width=package.width.value,
                            Height=package.height.value,
                        )
                        if package.has_dimensions
                        else None
                    ),
                    NumberOfPieces=package.items.quantity,
                    PackagingType=ups.AccountTypeType(
                        Code=provider_units.PackagingType.map(
                            package.packaging_type or "your_packaging"
                        ).value
                    ),
                    FreightClass=(package.parcel.freight_class or "50"),
                )
                for package in packages
            ],
            ShipmentServiceOptions=(
                ups.ShipmentServiceOptionsType(
                    PickupOptions=None,
                    DeliveryOptions=(
                        ups.DeliveryOptionsType(
                            CallBeforeDeliveryIndicator=(
                                "true"
                                if options.ups_freight_call_before_delivery_indicator.state
                                is not None
                                else None
                            ),
                            HolidayDeliveryIndicator=(
                                "true"
                                if options.ups_freight_holiday_delivery_indicator.state
                                is not None
                                else None
                            ),
                            InsideDeliveryIndicator=(
                                "true"
                                if options.ups_freight_inside_delivery_indicator.state
                                is not None
                                else None
                            ),
                            ResidentialDeliveryIndicator=(
                                "true"
                                if options.ups_freight_residential_delivery_indicator.state
                                is not None
                                else None
                            ),
                            WeekendDeliveryIndicator=(
                                "true"
                                if options.ups_freight_weekend_delivery_indicator.state
                                is not None
                                else None
                            ),
                            LiftGateRequiredIndicator=(
                                "true"
                                if options.ups_freight_lift_gate_required_indicator.state
                                is not None
                                else None
                            ),
                            LimitedAccessDeliveryIndicator=(
                                "true"
                                if options.ups_freight_limited_access_delivery_indicator.state
                                is not None
                                else None
                            ),
                        )
                        if any(
                            [
                                options.ups_freight_call_before_delivery_indicator.state,
                                options.ups_freight_holiday_delivery_indicator.state,
                                options.ups_freight_inside_delivery_indicator.state,
                                options.ups_freight_residential_delivery_indicator.state,
                                options.ups_freight_weekend_delivery_indicator.state,
                                options.ups_freight_lift_gate_required_indicator.state,
                                options.ups_freight_limited_access_delivery_indicator.state,
                            ]
                        )
                        else None
                    ),
                    OverSeasLeg=None,
                    COD=(
                        ups.CodType(
                            CODValue=ups.DeclaredValueType(
                                CurrencyCode=options.currency.state or "USD",
                                MonetaryValue=lib.to_money(
                                    options.cash_on_delivery.state
                                ),
                            ),
                            CODPaymentMethod=ups.AccountTypeType(Code="R"),
                            CODBillingOption=ups.AccountTypeType(Code="02"),
                            RemitTo=ups.RemitToType(
                                Name=(
                                    recipient.company_name
                                    or recipient.person_name
                                    or "N/A"
                                ),
                                Address=ups.AddressType(
                                    AddressLine=recipient.address_line,
                                    City=recipient.city,
                                    StateProvinceCode=recipient.state_code,
                                    Town=None,
                                    PostalCode=recipient.postal_code,
                                    CountryCode=recipient.country_code,
                                    ResidentialAddressIndicator=(
                                        "true" if recipient.residential else None
                                    ),
                                ),
                                AttentionName=recipient.person_name or "N/A",
                            ),
                        )
                        if options.cash_on_delivery.state is not None
                        else None
                    ),
                    DangerousGoods=(
                        ups.DangerousGoodsType(
                            Name=shipper.company_name or shipper.person_name,
                            Phone=ups.PhoneType(Number=shipper.phone_number),
                            TransportationMode=ups.AccountTypeType(
                                Code=options.dangerous_good.state
                            ),
                        )
                        if options.dangerous_good.state is not None
                        else None
                    ),
                    SortingAndSegregating=None,
                    DeclaredValue=(
                        ups.DeclaredValueType(
                            CurrencyCode=options.currency.state or "USD",
                            MonetaryValue=options.declared_value.state,
                        )
                        if options.declared_value.state is not None
                        else None
                    ),
                    HandlingCharge=None,
                    FreezableProtectionIndicator=(
                        "true"
                        if options.ups_freight_freezable_protection_indicator.state
                        is not None
                        else None
                    ),
                    ExtremeLengthIndicator=(
                        "true"
                        if options.ups_freight_extreme_length_indicator.state
                        is not None
                        else None
                    ),
                    LinearFeet=(
                        "true"
                        if options.ups_freight_linear_feet.state is not None
                        else None
                    ),
                    AdjustedHeight=(
                        ups.EightType(
                            UnitOfMeasurement=ups.AccountTypeType(
                                Code=packages.compatible_units[1].value
                            ),
                            Value=options.ups_freight_ajusted_height.state,
                        )
                        if options.ups_freight_ajusted_height.state is not None
                        else None
                    ),
                )
                if options.has_content
                else None
            ),
            PickupRequest=None,
            AlternateRateOptions=ups.AccountTypeType(
                Code=(options.ups_freight_alternate_rate_option.state or "3")
            ),
            GFPOptions=(
                ups.GFPOptionsType(GPFAccesorialRateIndicator="true")
                if options.ups_freight_gpf_accesorial_rate_indicator.state
                else None
            ),
            TimeInTransitIndicator=(
                "true" if options.ups_freight_time_in_transit_indicator.state else None
            ),
        )
    )

    return lib.Serializable(request, lib.to_dict)
