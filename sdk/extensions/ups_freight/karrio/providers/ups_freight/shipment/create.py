from ups_freight_lib.freight_ship_response import ShipmentResultsType
import ups_freight_lib.freight_ship_request as ups
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.ups_freight.error as error
import karrio.providers.ups_freight.utils as provider_utils
import karrio.providers.ups_freight.units as provider_units


def parse_shipment_response(
    response: dict,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    shipment_response = response.get("FreightShipResponse") or {}
    response_messages = [
        *response.get("response", {}).get("errors", []),
        *shipment_response.get("Response", {}).get("Alert", []),
    ]
    response_shipment = (
        shipment_response.get("ShipmentResults")
        if (
            shipment_response.get("ShipmentResults", {}).get("ShipmentNumber")
            is not None
        )
        else None
    )

    messages = error.parse_error_response(response_messages, settings)
    shipment = _extract_details(response_shipment, settings)

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    shipment = lib.to_object(ShipmentResultsType, data)
    service = provider_units.ShippingService.map(shipment.Service.Code)
    label = next(
        (img.GraphicImage for img in shipment.Documents.Image if img.Type.Code == "30"),
        None,
    )
    extra_charges = [
        models.ChargeDetails(
            name=charge.Type.Description,
            amount=lib.to_money(charge.Factor.Value),
            currency=charge.Factor.UnitOfMeasurement.Code,
        )
        for charge in shipment.Rate
    ]

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.ShipmentNumber,
        shipment_identifier=shipment.ShipmentNumber,
        label_type="PDF",
        docs=models.Documents(label=label),
        selected_rate=models.RateDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            service=service.name_or_key,
            currency=shipment.TotalShipmentCharge.CurrencyCode,
            total_charge=lib.to_money(shipment.TotalShipmentCharge.MonetaryValue),
            transit_days=lib.to_int(shipment.TimeInTransit.DaysInTransit),
            extra_charges=extra_charges,
            meta=dict(service_name=shipment.Service.Description or service.name_or_key),
        ),
        meta=dict(
            pickup_confirmation_number=shipment.PickupRequestConfirmationNumber,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels, options=payload.options)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    payment = payload.payment or models.Payment()
    payment_type = (
        provider_units.PaymentType.map(payment.paid_by)
        or provider_units.PaymentType.prepaid
    ).value
    billing_address = lib.to_address(
        {
            provider_units.PaymentType.prepaid.value: (
                payload.billing_address or payload.shipper
            ),
            provider_units.PaymentType.freight_collect.value: (
                payload.billing_address or payload.recipient
            ),
            provider_units.PaymentType.bill_to_third_party.value: payload.billing_address,
        }[payment_type]
    )

    request = ups.FreightShipRequestType(
        FreightShipRequest=ups.FreightShipRequestClassType(
            Shipment=ups.ShipmentType(
                ShipperNumber=settings.account_number,
                ShipFrom=ups.ShipFromType(
                    Name=(shipper.company_name or shipper.person_name or "N/A"),
                    Address=ups.AddressType(
                        AddressLine=shipper.address_line,
                        City=shipper.city,
                        StateProvinceCode=shipper.state_code,
                        PostalCode=shipper.postal_code,
                        CountryCode=shipper.country_code,
                    ),
                    AttentionName=shipper.person_name,
                    Phone=ups.PhoneType(Number=shipper.phone_number or "000 000 0000"),
                    EMailAddress=shipper.email,
                    TaxIdentificationNumber=(
                        shipper.federal_tax_id or shipper.state_tax_id
                    ),
                ),
                ShipTo=ups.ShipFromType(
                    Name=(recipient.company_name or recipient.person_name or "N/A"),
                    Address=ups.AddressType(
                        AddressLine=recipient.address_line,
                        City=recipient.city,
                        StateProvinceCode=recipient.state_code,
                        PostalCode=recipient.postal_code,
                        CountryCode=recipient.country_code,
                    ),
                    AttentionName=recipient.person_name,
                    Phone=ups.PhoneType(Number=recipient.phone_number or "0000"),
                    EMailAddress=recipient.email,
                    TaxIdentificationNumber=(
                        recipient.federal_tax_id or recipient.state_tax_id
                    ),
                ),
                PaymentInformation=ups.PaymentInformationType(
                    Payer=ups.ShipFromType(
                        Name=(
                            billing_address.company_name
                            or billing_address.person_name
                            or "N/A"
                        ),
                        Address=ups.AddressType(
                            AddressLine=billing_address.address_line,
                            City=billing_address.city,
                            StateProvinceCode=billing_address.state_code,
                            PostalCode=billing_address.postal_code,
                            CountryCode=billing_address.country_code,
                        ),
                        ShipperNumber=(
                            payment.account_number or settings.account_number
                        ),
                        AttentionName=billing_address.person_name,
                        Phone=(
                            ups.PhoneType(Number=billing_address.phone_number)
                            if billing_address.phone_number is not None
                            else None
                        ),
                    ),
                    ShipmentBillingOption=ups.ServiceType(Code=payment_type),
                ),
                Service=ups.ServiceType(Code=service),
                HandlingUnitOne=ups.HandlingUnitType(
                    Quantity=packages.items.quantity,
                    Type=ups.ServiceType(
                        Code=(
                            provider_units.PackagingType.map(
                                packages.package_type
                            ).value
                            or "PLT"
                        )
                    ),
                ),
                Commodity=[
                    ups.CommodityType(
                        CommodityID=None,
                        Weight=ups.WeightType(
                            UnitOfMeasurement=ups.ServiceType(
                                Code=provider_units.WeightUnit.map(
                                    package.weight_unit.value
                                ).value
                            ),
                            Value=package.weight.value,
                        ),
                        Dimensions=(
                            ups.CommodityDimensionsType(
                                UnitOfMeasurement=ups.ServiceType(
                                    Code=package.dimension_unit.value,
                                ),
                                Length=package.length.value,
                                Width=package.width.value,
                                Height=package.height.value,
                            )
                            if package.has_dimensions
                            else None
                        ),
                        NumberOfPieces=package.items.quantity,
                        PackagingType=ups.ServiceType(
                            Code=provider_units.PackagingType.map(
                                package.packaging_type or "your_packaging"
                            ).value
                        ),
                        FreightClass=(package.parcel.freight_class or "50"),
                    )
                    for package in packages
                ],
                PickupRequest=None,
                Documents=ups.DocumentsType(
                    Image=[
                        ups.ImageType(
                            Type=ups.ServiceType(Code="30"),
                            LabelsPerPage=1,
                            Format=ups.ServiceType(Code="01"),
                            PrintFormat=ups.ServiceType(Code="02"),
                            PrintSize=ups.PrintSizeType(
                                Length=4,
                                Width=64,
                            ),
                        )
                    ]
                ),
                TimeInTransitIndicator=(
                    None
                    if options.ups_freight_time_in_transit_indicator.state == False
                    else ""
                ),
                DensityEligibleIndicator=(
                    "" if options.ups_freight_density_eligible_indicator.state else None
                ),
            ),
            Miscellaneous=ups.MiscellaneousType(
                WSVersion="21.0.11",
                ReleaseID="07.12.2008",
            ),
        )
    )

    return lib.Serializable(request, lib.to_dict)
