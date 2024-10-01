import karrio.schemas.eshipper.rate_request as eshipper
import karrio.schemas.eshipper.rate_response as rating
import typing
import datetime
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.eshipper.error as error
import karrio.providers.eshipper.utils as provider_utils
import karrio.providers.eshipper.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    rates = [_extract_details(rate, settings) for rate in response.get("quotes", [])]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate = lib.to_object(rating.QuoteType, data)
    service = provider_units.ShippingService.find(
        rate.serviceName,
        service_id=rate.serviceId,
        test_mode=settings.test_mode,
    )
    carrier_id = provider_units.ShippingService.carrier_id(
        rate.carrierName,
        test_mode=settings.test_mode,
        service_search=service.name_or_key,
        service_id=rate.serviceId,
    )
    rate_provider = provider_units.RateProvider.find(
        rate.carrierName,
        test_mode=settings.test_mode,
        service_search=service.name_or_key,
        service_id=rate.serviceId,
    )

    charges = [
        ("baseCharge", rate.baseCharge),
        ("fuelSurcharge", rate.fuelSurcharge),
        ("carbonNeutralFees", rate.carbonNeutralFees),
        ("processingFees", rate.processingFees),
        ("totalChargedAmount", rate.totalChargedAmount),
        *((_.name, _.amount) for _ in rate.surcharges),
        *((_.name, _.amount) for _ in rate.taxes),
    ]

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        total_charge=lib.to_money(rate.totalCharge),
        currency=rate.currency,
        transit_days=lib.to_int(rate.transitDays),
        extra_charges=[
            models.ChargeDetails(
                name=name,
                currency=rate.currency,
                amount=lib.to_money(amount),
            )
            for name, amount in charges
            if amount
        ],
        meta=dict(
            eshipper_carrier_id=carrier_id,
            eshipper_service_id=rate.serviceId,
            eshipper_carrier_name=rate.carrierName,
            eshipper_service_name=rate.serviceName,
            rate_provider=rate_provider.name_or_key,
            service_name=service.name or rate.serviceName,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
    )
    services = lib.to_services(payload.services, provider_units.ShippingService)
    print(services, "<<<")
    service_id = lib.identity(
        options.eshipper_service_id.state
        or provider_units.ShippingService.service_id(
            services.first,
            test_mode=settings.test_mode,
        )
    )

    request = eshipper.RateRequestType(
        scheduledShipDate=lib.fdatetime(
            lib.to_next_business_datetime(
                options.shipping_date.state or datetime.datetime.now(),
                current_format="%Y-%m-%dT%H:%M",
            ),
            output_format="%Y-%m-%d %H:%M",
        ),
        raterequestfrom=eshipper.FromType(
            attention=shipper.contact,
            company=shipper.company_name,
            address1=shipper.address_line1,
            address2=shipper.address_line2,
            city=shipper.city,
            province=shipper.state_code,
            country=shipper.country_code,
            zip=shipper.postal_code,
            email=shipper.email_address,
            phone=shipper.phone_number,
            instructions=None,
            residential=shipper.is_residential,
            tailgateRequired=None,
            confirmDelivery=None,
            notifyRecipient=None,
        ),
        to=eshipper.FromType(
            attention=recipient.contact,
            company=recipient.company_name,
            address1=recipient.address_line1,
            address2=recipient.address_line2,
            city=recipient.city,
            province=recipient.state_code,
            country=recipient.country_code,
            zip=recipient.postal_code,
            email=recipient.email_address,
            phone=recipient.phone_number,
            instructions=None,
            residential=recipient.is_residential,
            tailgateRequired=None,
            confirmDelivery=None,
            notifyRecipient=None,
        ),
        packagingUnit="Metric" if packages.weight_unit.lower() == "kg" else "Imperial",
        packages=eshipper.PackagesType(
            type="Package",
            packages=[
                eshipper.PackageType(
                    height=lib.to_int(package.height.value),
                    length=lib.to_int(package.length.value),
                    width=lib.to_int(package.width.value),
                    weight=lib.to_int(package.weight.value),
                    dimensionUnit=package.dimension_unit.value,
                    weightUnit=package.weight_unit.value,
                    type=provider_units.PackagingType.map(package.packaging_type).value,
                    freightClass=None,
                    nmfcCode=None,
                    insuranceAmount=None,
                    codAmount=None,
                    description=package.description,
                    harmonizedCode=None,
                    skuCode=None,
                )
                for package in packages
            ],
        ),
        reference1=payload.reference,
        reference2=None,
        reference3=None,
        transactionId=None,
        signatureRequired=options.eshipper_signature_required.state,
        insuranceType=None,
        dangerousGoodsType=None,
        pickup=None,
        customsInformation=None,
        customsInBondFreight=None,
        cod=None,
        isSaturdayService=options.eshipper_is_saturday_service.state,
        holdForPickupRequired=options.eshipper_hold_for_pickup_required.state,
        specialEquipment=options.eshipper_special_equipment.state,
        insideDelivery=options.eshipper_inside_delivery.state,
        deliveryAppointment=options.eshipper_delivery_appointment.state,
        insidePickup=options.eshipper_inside_pickup.state,
        saturdayPickupRequired=options.eshipper_saturday_pickup_required.state,
        stackable=options.eshipper_stackable.state,
        serviceId=service_id,
        thirdPartyBilling=None,
        commodityType=None,
    )

    return lib.Serializable(
        request,
        lambda _: lib.to_dict(lib.to_json(_).replace("raterequestfrom", "from")),
    )
