"""Karrio MyDHL rate API implementation."""

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

    # Convert response to typed object
    rate_response = lib.to_object(mydhl_res.RateResponseType, response)

    # Extract products from the response
    products = rate_response.products or []
    rates = [
        _extract_details(product, settings)
        for product in products
        if product.totalPrice and len(product.totalPrice) > 0
    ]

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

    # Calculate transit days from delivery date
    transit_days = None
    if product.deliveryCapabilities and product.deliveryCapabilities.estimatedDeliveryDateAndTime:
        try:
            delivery_date = lib.to_date(
                product.deliveryCapabilities.estimatedDeliveryDateAndTime,
                "%Y-%m-%dT%H:%M:%S"
            )
            if delivery_date:
                # Calculate days from now
                from datetime import datetime
                transit_days = (delivery_date.date() - datetime.now().date()).days
        except:
            pass

    # Extract extra charges from price breakdown
    extra_charges = []
    if product.totalPriceBreakdown:
        for breakdown in product.totalPriceBreakdown:
            if breakdown.priceBreakdown:
                for charge in breakdown.priceBreakdown:
                    if charge.typeCode and charge.price:
                        extra_charges.append(
                            models.ChargeDetails(
                                name=charge.typeCode,
                                amount=lib.to_decimal(charge.price),
                                currency=breakdown.priceCurrency or currency,
                            )
                        )

    # Map product code to service enum name for proper service identification
    # Follow guide pattern: use product code directly, with display name in meta
    service_map = {
        "Q": "mydhl_medical_express",
        "P": "mydhl_express_worldwide",
        "8": "mydhl_express_easy",
        "T": "mydhl_express_12_00",
        "N": "mydhl_express_domestic",
        "J": "mydhl_jetline",
        "R": "mydhl_sprintline",
        "Y": "mydhl_express_9_00",
        "W": "mydhl_economy_select",
        "X": "mydhl_express_10_30",
        "G": "mydhl_globalmail",
        "S": "mydhl_same_day",
    }

    service_code = service_map.get(product.productCode, f"mydhl_{product.productCode.lower()}")

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service_code,
        total_charge=lib.to_money(total_charge),
        currency=currency,
        transit_days=transit_days,
        extra_charges=extra_charges if extra_charges else None,
        meta=dict(
            service_name=product.productName or "",
            product_code=product.productCode,
            network_type_code=product.networkTypeCode,
            local_product_code=product.localProductCode,
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

    # Get planned shipping date and time
    import datetime
    planned_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SGMT%z")

    # Create the MyDHL rate request
    request = mydhl_req.RateRequestType(
        customerDetails=mydhl_req.CustomerDetailsType(
            shipperDetails=mydhl_req.ErDetailsType(
                postalCode=shipper.postal_code or "",
                cityName=shipper.city or "",
                countryCode=shipper.country_code,
            ),
            receiverDetails=mydhl_req.ErDetailsType(
                postalCode=recipient.postal_code or "",
                cityName=recipient.city or "",
                countryCode=recipient.country_code,
            ),
        ),
        accounts=(
            [
                mydhl_req.AccountType(
                    typeCode="shipper",
                    number=settings.account_number,
                )
            ]
            if settings.account_number
            else None
        ),
        productCode=services.first.value if services.first else None,
        plannedShippingDateAndTime=planned_date,
        unitOfMeasurement=unit_of_measurement,
        isCustomsDeclarable=is_dutiable,
        packages=[
            mydhl_req.PackageType(
                typeCode=(
                    provider_units.PackagingType[package.packaging_type or "your_packaging"].value
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
