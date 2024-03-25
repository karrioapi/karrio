import karrio.schemas.fedex.rating_request as fedex
import karrio.schemas.fedex.rating_response as rating
import typing
import datetime
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.fedex.error as error
import karrio.providers.fedex.utils as provider_utils
import karrio.providers.fedex.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    rates = [
        _extract_details(rate, settings, ctx=_response.ctx)
        for rate in (response.get("output", {}).get("rateReplyDetails") or [])
    ]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict = {},
) -> models.RateDetails:
    # fmt: off
    rate = lib.to_object(rating.RateReplyDetailType, data)
    service = provider_units.ShippingService.map(rate.serviceType)
    details: rating.RatedShipmentDetailType = (
        next((_ for _ in rate.ratedShipmentDetails if _.rateType == "PREFERRED_CURRENCY"), None) or
        next((_ for _ in rate.ratedShipmentDetails if _.rateType == "ACCOUNT"), None) or
        rate.ratedShipmentDetails[0]
    )
    charges = [
        ("Base Charge", lib.to_money(details.totalBaseCharge)),
        ("Discounts", lib.to_money(details.totalDiscounts)),
        ("VAT Charge", lib.to_money(details.totalVatCharge)),
        ("Duties and Taxes", lib.to_money(details.totalDutiesAndTaxes)),
        *[(_.description, lib.to_money(_.amount)) for _ in details.shipmentRateDetail.surCharges or []],
    ]
    total_charge = lib.to_money(
        details.totalNetChargeWithDutiesAndTaxes 
        or details.totalNetCharge
    )
    estimated_delivery = lib.to_date(getattr(rate.operationalDetail, "commitDate", None), "%Y-%m-%dT%H:%M:%S")
    shipping_date = lib.to_date(ctx.get("shipment_date") or datetime.datetime.now())
    transit_day_list = (
        (shipping_date + datetime.timedelta(x + 1) for x in range((estimated_delivery.date() - shipping_date.date()).days))
        if estimated_delivery is not None 
        else None
    )
    transit_days = (
        sum(1 for day in transit_day_list if day.weekday() < 5)
        if transit_day_list is not None
        else None
    )
    # fmt: on

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        total_charge=total_charge,
        currency=details.currency,
        transit_days=transit_days,
        estimated_delivery=lib.fdate(estimated_delivery),
        extra_charges=[
            models.ChargeDetails(
                name=name,
                amount=amount,
                currency=details.currency,
            )
            for name, amount in charges
        ],
        meta=dict(
            service_name=service.name or rate.serviceName,
            transit_time=getattr(rate.operationalDetail, "transitTime", None),
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    service = lib.to_services(payload.services, provider_units.ShippingService).first
    packages = lib.to_packages(
        payload.parcels,
        required=["weight"],
        presets=provider_units.PackagePresets,
    )
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    request_types = ["LIST"] + ([] if "currency" not in options else ["PREFERRED"])
    shipment_date = lib.to_date(options.shipment_date.state or datetime.datetime.now())
    rate_options = lambda _options: [
        option
        for _, option in _options.items()
        if _options.state is not False and option.code in provider_units.RATING_OPTIONS
    ]
    shipment_options = lambda _options: [
        option
        for _, option in _options.items()
        if _options.state is not False
        and option.code in provider_units.SHIPMENT_OPTIONS
    ]
    hub_id = lib.text(options.fedex_smart_post_hub_id.state) or lib.text(
        settings.connection_config.smart_post_hub_id.state
    )

    request = fedex.RatingRequestType(
        accountNumber=fedex.RatingRequestAccountNumberType(
            value=settings.account_number,
        ),
        rateRequestControlParameters=fedex.RateRequestControlParametersType(
            returnTransitTimes=True,
            servicesNeededOnRateFailure=True,
            variableOptions=(
                [option.code for option in rate_options(options)]
                if any(rate_options(options))
                else []
            ),
            rateSortOrder="COMMITASCENDING",
        ),
        requestedShipment=fedex.RequestedShipmentType(
            shipper=fedex.ShipperClassType(
                address=fedex.ResponsiblePartyAddressType(
                    streetLines=shipper.address_lines,
                    city=shipper.city,
                    stateOrProvinceCode=shipper.state_code,
                    postalCode=shipper.postal_code,
                    countryCode=shipper.country_code,
                    residential=shipper.residential,
                )
            ),
            recipient=fedex.ShipperClassType(
                address=fedex.ResponsiblePartyAddressType(
                    streetLines=recipient.address_lines,
                    city=recipient.city,
                    stateOrProvinceCode=recipient.state_code,
                    postalCode=recipient.postal_code,
                    countryCode=recipient.country_code,
                    residential=recipient.residential,
                )
            ),
            serviceType=getattr(service, "value", None),
            emailNotificationDetail=None,
            preferredCurrency=options.currency.state,
            rateRequestType=request_types,
            shipDateStamp=lib.fdate(shipment_date, "%Y-%m-%d"),
            pickupType="DROPOFF_AT_FEDEX_LOCATION",
            requestedPackageLineItems=[
                fedex.RequestedPackageLineItemType(
                    subPackagingType=lib.identity(
                        provider_units.SubPackageType.map(package.packaging_type).value
                        or "OTHER"
                    ),
                    groupPackageCount=1,
                    contentRecord=[],
                    declaredValue=package.options.declared_value.state,
                    weight=fedex.WeightType(
                        units=package.weight.unit,
                        value=package.weight.value,
                    ),
                    dimensions=(
                        fedex.DimensionsType(
                            length=package.length.map(
                                provider_units.MeasurementOptions
                            ).value,
                            width=package.width.map(
                                provider_units.MeasurementOptions
                            ).value,
                            height=package.height.map(
                                provider_units.MeasurementOptions
                            ).value,
                            units=package.dimension_unit.value,
                        )
                        if (
                            # only set dimensions if the packaging type is set to your_packaging
                            package.has_dimensions
                            and provider_units.PackagingType.map(
                                package.packaging_type or "your_packaging"
                            ).value
                            == provider_units.PackagingType.your_packaging.value
                        )
                        else None
                    ),
                    variableHandlingChargeDetail=None,
                    packageSpecialServices=None,
                )
                for package in packages
            ],
            documentShipment=packages.is_document,
            variableHandlingChargeDetail=None,
            packagingType=provider_units.PackagingType.map(
                packages.package_type or "your_packaging"
            ).value,
            totalWeight=packages.weight.LB,
            shipmentSpecialServices=(
                fedex.ShipmentSpecialServicesType(
                    returnShipmentDetail=None,
                    deliveryOnInvoiceAcceptanceDetail=None,
                    internationalTrafficInArmsRegulationsDetail=None,
                    pendingShipmentDetail=None,
                    holdAtLocationDetail=None,
                    shipmentCODDetail=None,
                    shipmentDryIceDetail=None,
                    internationalControlledExportDetail=None,
                    homeDeliveryPremiumDetail=None,
                    specialServiceTypes=(
                        [option.code for option in shipment_options(packages.options)]
                        if any(shipment_options(packages.options))
                        else []
                    ),
                )
                if any(shipment_options(packages.options))
                else None
            ),
            customsClearanceDetail=None,
            groupShipment=None,
            serviceTypeDetail=None,
            smartPostInfoDetail=(
                fedex.SmartPostInfoDetailType(
                    ancillaryEndorsement=None,
                    hubId=hub_id,
                    indicia=(
                        lib.text(options.fedex_smart_post_allowed_indicia.state)
                        or "PARCEL_SELECT"
                    ),
                    specialServices=None,
                )
                if hub_id is not None
                else None
            ),
            expressFreightDetail=None,
            groundShipment=None,
        ),
        carrierCodes=None,
    )

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(shipment_date=shipment_date),
    )
