"""Karrio MyDHL rate API implementation."""

import datetime
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.mydhl.error as error
import karrio.providers.mydhl.utils as provider_utils
import karrio.providers.mydhl.units as provider_units
import karrio.schemas.mydhl.rate_request as mydhl_req
import karrio.schemas.mydhl.rate_response as mydhl_res


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    rates = lib.identity(
        [
            _extract_details(product, settings)
            for product in lib.to_object(mydhl_res.RateResponseType, response).products or []
            if product.totalPrice and len(product.totalPrice) > 0
        ]
        if response.get("status") is None and response.get("products") is not None
        else []
    )

    return rates, messages


def _extract_details(
    product: mydhl_res.ProductType,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    """
    Extract rate details from MyDHL product data

    product: The MyDHL ProductType object from the rate response
    settings: The carrier connection settings

    Returns a RateDetails object with extracted rate information
    """
    # Get the primary price (usually BILLC - billing currency)
    total_price = next(
        (price for price in (product.totalPrice or []) if price.price),
        None
    )

    # Extract pricing information
    currency = total_price.priceCurrency if total_price else "USD"
    total_charge = float(total_price.price) if total_price and total_price.price else 0.0

    # Get transit days from deliveryCapabilities (more reliable than calculating from date)
    transit_days = (
        product.deliveryCapabilities.totalTransitDays
        if product.deliveryCapabilities
        else None
    )

    # Extract charges from price breakdown
    charges = [
        (charge.typeCode, lib.to_decimal(charge.price), breakdown.priceCurrency)
        for breakdown in (product.totalPriceBreakdown or [])
        for charge in (breakdown.priceBreakdown or [])
    ]

    # Map product code to service enum name
    service_code = provider_units.ShippingService.map(product.productCode).name_or_key

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service_code,
        total_charge=lib.to_money(total_charge),
        currency=currency,
        transit_days=transit_days,
        extra_charges=[
            models.ChargeDetails(
                name=name,
                amount=amount,
                currency=charge_currency or currency,
            )
            for name, amount, charge_currency in charges
            if name and amount
        ],
        meta=dict(
            service_name=product.productName or "",
            product_code=product.productCode,
            network_type_code=product.networkTypeCode,
            local_product_code=product.localProductCode,
            estimated_delivery=(
                product.deliveryCapabilities.estimatedDeliveryDateAndTime
                if product.deliveryCapabilities
                else None
            ),
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a rate request for the MyDHL API

    payload: The standardized RateRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    # Convert karrio models to carrier-specific format
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    services = lib.to_services(payload.services, provider_units.ShippingService)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Determine international shipment status
    is_international = shipper.country_code != recipient.country_code
    is_dutiable = is_international and not all([p.is_document for p in payload.parcels])

    # Determine unit of measurement (metric vs imperial)
    unit_of_measurement = (
        provider_units.MeasurementUnit.imperial.value
        if packages.weight_unit == units.WeightUnit.LB
        else provider_units.MeasurementUnit.metric.value
    )
    planned_date = lib.fdatetime(
        options.shipment_date.state or datetime.datetime.now(),
        output_format="%Y-%m-%dT%H:%M:%S GMT+00:00",
    )

    # Create the MyDHL rate request with complete address fields
    request = mydhl_req.RateRequestType(
        customerDetails=mydhl_req.CustomerDetailsType(
            shipperDetails=mydhl_req.ErDetailsType(
                postalCode=shipper.postal_code,
                cityName=shipper.city,
                countryCode=shipper.country_code,
                provinceCode=shipper.state_code,
                addressLine1=shipper.address_line1,
                addressLine2=shipper.address_line2,
                countyName=shipper.suburb,
            ),
            receiverDetails=mydhl_req.ErDetailsType(
                postalCode=recipient.postal_code,
                cityName=recipient.city,
                countryCode=recipient.country_code,
                provinceCode=recipient.state_code,
                addressLine1=recipient.address_line1,
                addressLine2=recipient.address_line2,
                countyName=recipient.suburb,
            ),
        ),
        accounts=[
            mydhl_req.AccountType(
                typeCode="shipper",
                number=settings.account_number,
            )
        ],
        productCode=getattr(services.first, "value", None),
        plannedShippingDateAndTime=planned_date,
        unitOfMeasurement=unit_of_measurement,
        isCustomsDeclarable=is_dutiable,
        packages=[
            mydhl_req.PackageType(
                typeCode=lib.identity(
                    provider_units.PackagingType.map(package.packaging_type).value
                    if package.packaging_type
                    else None
                ),
                weight=package.weight.value,
                dimensions=(
                    mydhl_req.DimensionsType(
                        length=int(package.length.value) if package.length else None,
                        width=int(package.width.value) if package.width else None,
                        height=int(package.height.value) if package.height else None,
                    )
                    if any([package.length, package.width, package.height])
                    else None
                ),
            )
            for package in packages
        ],
    )

    return lib.Serializable(request, lib.to_dict)
